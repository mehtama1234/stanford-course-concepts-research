#!/usr/bin/env python3
"""Build the LLM/reasoning machine bridge page: Build -> Reason -> Align.

  stanford-course (build the LLM: tokenization -> attention -> transformer -> pretraining)
    -> cs329a (make it reason: traces, test-time compute, verifiers, process rewards)
    -> align (RL for LLMs, verifier robustness) -> better traces -> more training signal -> loop.

Hosted in the stanford-course site. Build links are relative; cs329a uses CS_BASE.
Companion visual labs (build-an-llm-lab, build-a-reasoning-lab) are named in prose.
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "machine.html"
CS_BASE = "https://mehtama1234.github.io/stanford-cs329a-self-improving-ai-agents-concepts-research/concepts/"   # swap to public Pages URL at deploy

def e(s): return html.escape(str(s), quote=True)
def sc(cid, label): return f'<a href="concepts/{cid}-deep.html">{e(label)}</a>'   # underscore ids
def cs(cid, label): return f'<a href="{CS_BASE}{cid}-deep.html">{e(label)}</a>'     # dash ids

HOPS = [
 {"t": "Hop 1 · Build → Reason", "s": "the trained model's internals become external reasoning",
  "rows": [
   {"f": [("sc","attention","attention"), ("sc","transformer_block","the transformer block")], "o": "focus, turned into written steps",
    "to": [("cs","reasoning-traces","reasoning traces"), ("cs","test-time-compute","test-time compute")],
    "h": "Attention learns which tokens matter inside one pass, and the block fixes the model's depth at training time. Reasoning traces externalise that focus as written steps, and test-time compute adds flexible depth at inference by sampling and checking."},
   {"f": [("sc","tokenization","tokenization")], "o": "the grain of thought",
    "to": [("cs","reasoning-traces","reasoning traces")],
    "h": "Tokenization decides how text is chopped into pieces; a reasoning trace is written in exactly those pieces, so the grain set here is the grain the model thinks in."},
  ]},
 {"t": "Hop 2 · Reason → Align", "s": "reasoning is made reliable by rewarding good steps and refusing to be gamed",
  "rows": [
   {"f": [("cs","process-reward-models","process reward models"), ("cs","verifier-robustness","verifier robustness")], "o": "a signal the model cannot trick",
    "to": [("sc","reward","reward"), ("sc","rl_for_llms","RL for LLMs")],
    "h": "A single final reward is easy to game, and naive RL collapses by finding the loophole. Scoring each step (process rewards) and using a grader that is hard to fool (verifier robustness) is what turns raw RL into reliable alignment."},
   {"f": [("cs","train-time-scaling-rl","train-time RL scaling")], "o": "reasoning baked into the weights",
    "to": [("sc","policy_gradient","policy gradient")],
    "h": "The policy-gradient update is the machinery; scaling it under a KL leash is how reasoning moves from a test-time trick into the model's own weights."},
  ]},
 {"t": "Hop 3 · The loop closes", "s": "an aligned model makes better traces, which become training data",
  "rows": [
   {"f": [("cs","self-improvement-loop","the self-improvement loop"), ("cs","rationale-bootstrapping","rationale bootstrapping")], "o": "the model's own good traces",
    "to": [("sc","fine_tuning","fine-tuning"), ("sc","pretraining","pretraining")],
    "h": "Once the model reasons well, its own correct traces become training data: distil them back in by fine-tuning, and the next round starts stronger. Build feeds reason feeds align feeds build."},
  ]},
]

CSS = """
.bh .kick{color:var(--accent-2,#8b3f18)}
.mac{max-width:760px;margin:20px auto 6px;display:block}
.leg{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:10px 0 24px}
.leg .s{border:1px solid var(--line);border-radius:10px;background:var(--paper,#fff);padding:13px 15px;border-top:3px solid #5b45c7}
.leg .s h3{margin:0 0 4px;font-size:15px;color:#5b45c7}.leg .s p{margin:0;font-size:13px;color:var(--muted,#5d6875)}
.hop{margin:24px 0 6px}.hop .hh{border-bottom:1px solid var(--line);padding-bottom:6px;margin-bottom:12px}
.hop h2{margin:0;font-size:20px}.hop .hs{font-size:14px;color:var(--muted,#5d6875)}
.cn{border:1px solid var(--line);border-radius:12px;background:var(--paper,#fff);margin:12px 0;overflow:hidden}
.cn .top{display:grid;grid-template-columns:1fr auto 1fr;align-items:stretch}.cn .c{padding:13px 15px}
.cn .fr{background:#f3f0fb;border-right:1px solid var(--line)}.cn .to{background:#eef5f4;border-left:1px solid var(--line)}
.cn .md{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:10px 14px;min-width:150px;text-align:center}
.cn .md .o{font-size:13px;font-weight:600;line-height:1.35}.cn .md .a{font-family:ui-monospace,monospace;color:#5b45c7;font-size:17px}
.cn .lab{font-family:ui-monospace,monospace;font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);display:block;margin-bottom:6px}
.cn .chips a{display:inline-block;margin:0 5px 5px 0;padding:3px 9px;border-radius:999px;border:1px solid var(--line);background:#fff;font-size:13px;text-decoration:none}
.cn .h{padding:11px 15px;border-top:1px solid var(--line);font-size:14.5px;color:#24323a;background:#fff}.cn .h b{color:#8b3f18}
@media(max-width:720px){.cn .top{grid-template-columns:1fr}.leg{grid-template-columns:1fr}}
"""

def chips(items): return "".join((sc if k=="sc" else cs)(i, l) for k, i, l in items)
def row(r): return (f'<div class="cn"><div class="top">'
    f'<div class="c fr"><span class="lab">upstream</span><div class="chips">{chips(r["f"])}</div></div>'
    f'<div class="c md"><div class="a">&rarr;</div><div class="o">{e(r["o"])}</div><div class="a">&rarr;</div></div>'
    f'<div class="c to"><span class="lab">downstream</span><div class="chips">{chips(r["to"])}</div></div>'
    f'</div><div class="h"><b>How it hands off.</b> {e(r["h"])}</div></div>')
def hop(h): return f'<div class="hop"><div class="hh"><h2>{e(h["t"])}</h2><div class="hs">{e(h["s"])}</div></div>' + "".join(row(r) for r in h["rows"])

def machine_svg():
    return """<svg class="mac" viewBox="0 0 760 150" role="img" aria-label="build to reason to align loop">
 <defs><marker id="a" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#5b45c7"/></marker></defs>
 <rect x="20" y="46" width="180" height="58" rx="10" fill="#f3f0fb" stroke="#5b45c7"/><text x="110" y="70" text-anchor="middle" font-size="13" font-weight="700" fill="#5b45c7">Build the LLM</text><text x="110" y="88" text-anchor="middle" font-size="10.5" fill="#5d6875">tokens → attention → pretrain</text>
 <rect x="290" y="46" width="180" height="58" rx="10" fill="#f3f0fb" stroke="#5b45c7"/><text x="380" y="70" text-anchor="middle" font-size="13" font-weight="700" fill="#5b45c7">Make it reason</text><text x="380" y="88" text-anchor="middle" font-size="10.5" fill="#5d6875">traces · test-time compute</text>
 <rect x="560" y="46" width="180" height="58" rx="10" fill="#eef5f4" stroke="#0b6b64"/><text x="650" y="70" text-anchor="middle" font-size="13" font-weight="700" fill="#0b6b64">Align with RL</text><text x="650" y="88" text-anchor="middle" font-size="10.5" fill="#5d6875">verifiers · process rewards</text>
 <path d="M200,75 L288,75" fill="none" stroke="#5b45c7" stroke-width="2" marker-end="url(#a)"/>
 <path d="M470,75 L558,75" fill="none" stroke="#5b45c7" stroke-width="2" marker-end="url(#a)"/>
 <path d="M650,104 C650,138 110,138 110,104" fill="none" stroke="#5d6875" stroke-width="2" stroke-dasharray="4 3" marker-end="url(#a)"/>
 <text x="352" y="132" font-size="10.5" fill="#5d6875">better traces become training data</text></svg>"""

def page():
    hops = "".join(hop(h) for h in HOPS)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Build → Reason → Align: One Machine</title><link rel="stylesheet" href="assets/styles.css">
<style>{CSS}</style></head><body>
<main style="max-width:1120px;margin:0 auto;padding:0 26px">
<div class="hero bh" style="padding:34px 0 20px"><div class="kick" style="font-family:ui-monospace,monospace;font-size:11px;text-transform:uppercase;letter-spacing:.16em">connecting the dots · two courses, one pipeline</div>
<h1 style="font-size:clamp(30px,5vw,52px);margin:8px 0">Build &rarr; Reason &rarr; Align: One Machine</h1>
<p class="lede" style="font-size:18px;max-width:80ch;color:#33414a">Two Stanford courses are two stages of one machine. The <b>build</b> course grows a language model from tokens through attention to pretraining. <b>CS329A</b> makes that model reason &mdash; writing traces, spending test-time compute, checking itself with verifiers &mdash; and aligns it with reinforcement learning. The aligned model produces better traces, which become the next round's training data, and the loop closes. (The <b>build-an-llm</b> and <b>build-a-reasoning</b> visual labs show each stage running on real models.)</p></div>
{machine_svg()}
<div class="leg">
<div class="s"><h3>Build the LLM</h3><p>Tokenization, embeddings, attention, the transformer block, pretraining — grow the model that everything else steers.</p></div>
<div class="s"><h3>Make it reason</h3><p>Reasoning traces, test-time compute, repeated sampling, process rewards, verifiers — spend inference to think.</p></div>
<div class="s"><h3>Align with RL</h3><p>RL for LLMs, policy gradient, train-time RL scaling, verifier robustness — reward good steps, refuse to be gamed.</p></div>
</div>
<div style="font-family:ui-monospace,monospace;font-size:11px;text-transform:uppercase;letter-spacing:.16em;color:#8b3f18;margin:28px 0 6px">The connections</div>
<h2 style="margin:0 0 4px">Where the dots connect</h2>
<p class="muted" style="max-width:80ch;color:#5d6875">Each row is one wire: an upstream concept produces the object in the middle, a downstream concept consumes it. Click any concept to open its deep dive.</p>
{hops}
<p class="muted" style="font-size:12px;margin-top:34px;border-top:1px solid var(--line);padding-top:18px;color:#5d6875">Build&rarr;Reason&rarr;Align bridge · scripts/build_llm_bridge.py · build links local; cs329a via CS_BASE (set public at deploy).</p>
</main></body></html>"""

def main():
    OUT.write_text(page(), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} | {sum(len(h['rows']) for h in HOPS)} rows")

if __name__ == "__main__":
    main()
