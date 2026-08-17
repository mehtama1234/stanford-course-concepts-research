#!/usr/bin/env python3
"""Stanford AI Concept Lab — REAL GPT-2 (124M) experiments for the transformer
family. Every headline number in those deep dives comes from this script.
Run: .venv-torch/bin/python scripts/experiments/stanford_gpt2.py
torch + transformers, CPU, the actual pretrained gpt2 weights."""
import math, json
import numpy as np
import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

torch.manual_seed(0); np.random.seed(0)
tok = GPT2TokenizerFast.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2", output_hidden_states=True, output_attentions=True)
model.eval()
R = {}
def sep(t): print("\n" + "=" * 70 + f"\n{t}\n" + "=" * 70)
def ids(s): return tok(s, return_tensors="pt")


# ------------------------------------------------------------------ attention
def exp_attention():
    sep("attention — the model concentrates, it does not average")
    s = "The trophy did not fit in the suitcase because it was too big"
    enc = ids(s)
    with torch.no_grad():
        out = model(**enc)
    att = torch.stack(out.attentions)          # [layers, 1, heads, T, T]
    T = att.shape[-1]
    # top-1 attention mass, averaged over every query/head/layer
    top1 = att.max(dim=-1).values.mean().item()
    uniform_top1 = 1.0 / T
    # entropy vs uniform (nats)
    ent = -(att * (att + 1e-12).log()).sum(-1).mean().item()
    R["attn_tokens"] = int(T); R["attn_top1"] = round(top1, 2)
    R["attn_uniform_top1"] = round(uniform_top1, 3)
    R["attn_entropy"] = round(ent, 2); R["attn_uniform_entropy"] = round(math.log(T), 2)
    print(f"sentence has {T} tokens; if attention were a flat average, each token")
    print(f"would get {uniform_top1:.3f} of the weight and entropy would be {math.log(T):.2f}")
    print(f"measured: the single most-attended token gets {top1:.2f} of the weight,")
    print(f"mean attention entropy {ent:.2f} (far below the flat {math.log(T):.2f}) -> it concentrates")


# ------------------------------------------------------------------ embeddings
def exp_embeddings():
    sep("embeddings — meaning becomes geometry")
    W = model.transformer.wte.weight.detach()   # [vocab, 768]
    def vec(word):
        i = tok(" " + word)["input_ids"]
        return W[i[0]] if len(i) == 1 else W[i].mean(0)
    def cos(a, b): return torch.nn.functional.cosine_similarity(vec(a), vec(b), dim=0).item()
    pairs = [("king", "queen"), ("king", "man"), ("dog", "cat"), ("king", "bicycle"), ("Monday", "Tuesday")]
    R["emb_dim"] = W.shape[1]
    res = {f"{a}/{b}": round(cos(a, b), 2) for a, b in pairs}
    R["emb_cos"] = res
    print(f"each of {W.shape[0]} tokens is a point in {W.shape[1]}-dimensional space")
    for k, v in res.items(): print(f"  cosine similarity {k:16s} = {v:+.2f}")
    print("related words sit close; unrelated words sit far — with no rule ever written")


# ------------------------------------------------------------------ positional
def exp_positional():
    sep("positional encoding — without order, language collapses")
    s = "the cat sat on the mat and then went to sleep"
    def loss_of(text_ids):
        with torch.no_grad():
            o = model(text_ids, labels=text_ids)
        return o.loss.item()
    base = ids(s)["input_ids"]
    L_ord = loss_of(base)
    torch.manual_seed(1)
    perm = base[:, torch.randperm(base.shape[1])]
    L_shuf = loss_of(perm)
    # position-embedding geometry: nearby positions more alike than far
    P = model.transformer.wpe.weight.detach()
    c_near = torch.nn.functional.cosine_similarity(P[5], P[6], dim=0).item()
    c_far = torch.nn.functional.cosine_similarity(P[5], P[200], dim=0).item()
    R["pos_loss_ordered"] = round(L_ord, 2); R["pos_loss_shuffled"] = round(L_shuf, 2)
    R["pos_near_cos"] = round(c_near, 2); R["pos_far_cos"] = round(c_far, 2)
    print(f"same words, correct order  -> loss {L_ord:.2f}")
    print(f"same words, shuffled order -> loss {L_shuf:.2f}  (much worse)")
    print(f"position vectors: neighbours cos {c_near:.2f}, distant cos {c_far:.2f}")


# ------------------------------------------------------------------ tokenization
def exp_tokenization():
    sep("tokenization — words are built from reusable pieces")
    words = ["cat", "running", "unbelievable", "antidisestablishmentarianism", "tokenization"]
    counts = {}
    for w in words:
        pieces = tok.tokenize(" " + w)
        counts[w] = (len(pieces), [p.replace("Ġ", "").strip() for p in pieces])
    R["tok_vocab"] = tok.vocab_size
    R["tok_counts"] = {w: c[0] for w, c in counts.items()}
    R["tok_split_example"] = counts["antidisestablishmentarianism"][1]
    print(f"vocabulary: {tok.vocab_size} pieces")
    for w, (n, ps) in counts.items():
        print(f"  {w:32s} -> {n} piece(s): {ps}")


# ------------------------------------------------------------------ transformer block / logit lens
def exp_block():
    sep("transformer block — the guess sharpens layer by layer (logit lens)")
    s = "Mr and Mrs Dursley of number four, Privet Drive. Mr Dursley"
    enc = ids(s)
    with torch.no_grad():
        out = model(**enc)
    hs = out.hidden_states                      # tuple: [layer0..layer12], each [1,T,768]
    lnf = model.transformer.ln_f
    head = model.lm_head
    # track WHERE the finally-chosen token sits in the 50,257-word ranking, layer by
    # layer (the "logit lens"). Absolute probs are tiny in gpt2-small; rank tells the story.
    target = int(head(lnf(hs[-1][:, -1, :])).argmax(-1).item())
    ranks = []
    for h in hs:
        lg = head(lnf(h[:, -1, :]))[0]
        ranks.append(int((lg > lg[target]).sum().item()) + 1)
    R["block_layers"] = len(hs) - 1
    R["block_vocab"] = tok.vocab_size
    R["block_rank_start"] = ranks[0]
    R["block_rank_mid"] = ranks[len(ranks) // 2]
    R["block_rank_end"] = ranks[-1]
    print(f"the token the model will finally pick, tracked through the {len(hs)-1} layers,")
    print(f"by its rank among all {tok.vocab_size} words (1 = the top choice):")
    print(f"  after layer 0:  rank {ranks[0]}")
    print(f"  after layer 6:  rank {ranks[len(ranks)//2]}")
    print(f"  after layer 12: rank {ranks[-1]}   (it climbs from buried to the very top)")


# ------------------------------------------------------------------ pretraining
def exp_pretraining():
    sep("pretraining — one goal, predict the next piece, on held-out text")
    text = (" Machine learning models are trained on large amounts of text to predict "
            "what comes next in a sequence of words.")
    enc = ids(text); X = enc["input_ids"]
    with torch.no_grad():
        out = model(X, labels=X)
    loss = out.loss.item(); ppl = math.exp(loss)
    # top-1 next-token accuracy
    logits = out.logits[0, :-1]; gold = X[0, 1:]
    acc = (logits.argmax(-1) == gold).float().mean().item()
    R["pre_loss"] = round(loss, 2); R["pre_ppl"] = round(ppl, 1); R["pre_acc"] = round(acc * 100, 0)
    print(f"on a sentence it was never explicitly taught:")
    print(f"  average surprise (loss) {loss:.2f}, perplexity {ppl:.1f}")
    print(f"  it names the exact next word {acc*100:.0f}% of the time")


# ------------------------------------------------------------------ scaling laws
def exp_scaling():
    sep("scaling laws — bigger models are predictably less surprised")
    text = (" The scientist carefully recorded the results of the experiment in her notebook "
            "before presenting them to the committee the following morning.")
    sizes = [("distilgpt2", 82), ("gpt2", 124), ("gpt2-medium", 355)]
    rows = []
    for name, mparams in sizes:
        try:
            m = GPT2LMHeadModel.from_pretrained(name); m.eval()
            enc = tok(text, return_tensors="pt")
            with torch.no_grad():
                l = m(**enc, labels=enc["input_ids"]).loss.item()
            rows.append((name, mparams, round(math.exp(l), 1)))
            print(f"  {name:14s} {mparams:>4d}M params -> perplexity {math.exp(l):.1f}")
        except Exception as e:
            print(f"  {name:14s} skipped ({repr(e)[:50]})")
    R["scaling"] = rows


# ------------------------------------------------------------------ generalization
def exp_generalization():
    sep("generalization — structure it never memorized, noise it can't fake")
    novel = " A purple giraffe quietly negotiated the quarterly budget with three enthusiastic penguins."
    rng = np.random.default_rng(0)
    rand_ids = torch.tensor([[int(x) for x in rng.integers(0, tok.vocab_size, size=16)]])
    def loss_ids(x):
        with torch.no_grad(): return model(x, labels=x).loss.item()
    L_novel = loss_ids(ids(novel)["input_ids"])
    L_rand = loss_ids(rand_ids)
    R["gen_novel"] = round(L_novel, 2); R["gen_random"] = round(L_rand, 2)
    print(f"a brand-new but grammatical sentence -> loss {L_novel:.2f}  (comfortable)")
    print(f"a string of random tokens            -> loss {L_rand:.2f}  (lost)")
    print("it generalized the RULES of language, it did not memorize strings")


# ------------------------------------------------------------------ latent space / contextual
def exp_latent():
    sep("latent space — the same word, two meanings, two vectors")
    s1 = "I sat on the river bank and watched the water"
    s2 = "I deposited the cheque at the bank downtown"
    # GPT-2 hidden states are anisotropic (all vectors squashed into a narrow cone,
    # so raw cosine ~ 0.99 everywhere). Center by the layer's mean over ALL tokens
    # of both sentences first — the standard fix — then compare the two 'bank's.
    def all_states(sentence, layer):
        enc = ids(sentence)
        with torch.no_grad():
            out = model(**enc)
        toks = tok.convert_ids_to_tokens(enc["input_ids"][0])
        bidx = [i for i, t in enumerate(toks) if "bank" in t.lower()][0]
        return out.hidden_states[layer][0], bidx
    def centered_cos(layer):
        h1, i1 = all_states(s1, layer); h2, i2 = all_states(s2, layer)
        mean = torch.cat([h1, h2], 0).mean(0)
        v1, v2 = h1[i1] - mean, h2[i2] - mean
        return torch.nn.functional.cosine_similarity(v1, v2, dim=0).item()
    c0 = centered_cos(0); cL = centered_cos(12)
    R["lat_cos_input"] = round(c0, 2); R["lat_cos_deep"] = round(cL, 2)
    print(f"'bank' at the input layer (same token):   centered cosine {c0:.2f}  (nearly identical start)")
    print(f"'bank' after 12 layers of context:        centered cosine {cL:.2f}  (pulled apart)")
    print("context reshapes the vector — river-bank and money-bank separate")


# ------------------------------------------------------------------ vision transformers (mechanism demo)
def exp_vit():
    sep("vision transformers — an image becomes a sentence of patches")
    # synthetic 32x32 grayscale image: bright square object in the top-left region
    img = np.zeros((32, 32), dtype=np.float32)
    img[4:12, 4:12] = 1.0                        # the "object"
    P = 8; grid = 32 // P                         # 4x4 = 16 patches
    patches = []
    obj_patches = []
    for r in range(grid):
        for c in range(grid):
            patch = img[r*P:(r+1)*P, c*P:(c+1)*P].flatten()
            patches.append(patch)
            if patch.mean() > 0.2: obj_patches.append(len(patches) - 1)
    X = np.array(patches)                         # 16 x 64  (patch "tokens")
    # one untrained self-attention pass: attention = softmax(X X^T / sqrt(d))
    d = X.shape[1]
    scores = X @ X.T / math.sqrt(d)
    scores -= scores.max(1, keepdims=True)
    A = np.exp(scores); A /= A.sum(1, keepdims=True)
    # for an object patch, how much attention lands on other object patches?
    q = obj_patches[0]
    on_obj = A[q, obj_patches].sum()
    R["vit_patches"] = len(patches); R["vit_obj_patches"] = len(obj_patches)
    R["vit_attn_on_object"] = round(float(on_obj), 2)
    R["vit_attn_chance"] = round(len(obj_patches) / len(patches), 2)
    print(f"image cut into {len(patches)} patches, {len(obj_patches)} contain the object")
    print(f"an object patch sends {on_obj:.2f} of its attention to the other object patches")
    print(f"(chance if it attended blindly would be {len(obj_patches)/len(patches):.2f}) -> like-attends-to-like")


if __name__ == "__main__":
    exp_attention(); exp_embeddings(); exp_positional(); exp_tokenization()
    exp_block(); exp_pretraining(); exp_scaling(); exp_generalization()
    exp_latent(); exp_vit()
    sep("MACHINE-READABLE RESULTS")
    print(json.dumps(R, indent=2))
