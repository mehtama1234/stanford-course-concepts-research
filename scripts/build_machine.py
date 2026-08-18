#!/usr/bin/env python3
"""Build the synthesis layer for the Stanford AI Concept Lab, matching the
CVPR site's connective tissue: hub.html ("the one machine"), math.html (the
mathematics capstone that cross-links recurring primitives to the concepts),
and idea-graph.html (force-directed graph, edges = shared primitives).
Then inject the three into the site nav. Run: python3 scripts/build_machine.py"""
import html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
def esc(s): return html.escape(str(s), quote=False)

NAME = {
 "attention":"Attention","embeddings":"Embeddings","positional_encoding":"Positional Encoding",
 "tokenization":"Tokenization","transformer_block":"The Transformer Block","pretraining":"Pretraining",
 "scaling_laws":"Scaling Laws","generalization":"Generalization","latent_space":"Latent Space",
 "vision_transformers":"Vision Transformers","diffusion":"Diffusion","score_matching":"Score Matching",
 "flow_matching":"Flow Matching","guidance":"Guidance","q_learning":"Q-Learning","policy":"Policy",
 "policy_gradient":"Policy Gradient","actor_critic":"Actor-Critic","exploration":"Exploration",
 "reward":"Reward","credit_assignment":"Credit Assignment","model_based_rl":"Model-Based RL",
 "offline_rl":"Offline RL","reasoning_traces":"Reasoning Traces","evaluation":"Evaluation",
 "fine_tuning":"Fine-tuning","rl_for_llms":"RL for Language Models","agents_and_tools":"Agents & Tools",
}
def href(cid): return f'concepts/{cid}-deep.html'

# ---- the one machine: seven stages that turn raw data into an agent that acts
STAGES = [
 ("01","Encode","turn raw input into vectors the machine can work with",
   ["tokenization","embeddings","positional_encoding"]),
 ("02","Process","mix and refine those vectors, deciding what to attend to",
   ["attention","transformer_block","vision_transformers","latent_space"]),
 ("03","Learn at scale","one simple objective over oceans of data, and what emerges",
   ["pretraining","scaling_laws","generalization"]),
 ("04","Generate","create brand-new data by reversing noise into structure",
   ["diffusion","score_matching","flow_matching","guidance"]),
 ("05","Value & decide","judge how good a situation is and choose an action",
   ["policy","q_learning","policy_gradient","actor_critic"]),
 ("06","Learn to act","the machinery that turns trial and error into skill",
   ["exploration","reward","credit_assignment","model_based_rl","offline_rl"]),
 ("07","Reason & align","make a language model think in steps and behave",
   ["reasoning_traces","fine_tuning","rl_for_llms","evaluation","agents_and_tools"]),
]
STAGE_OF = {cid:i for i,(_,_,_,ids) in enumerate(STAGES) for cid in ids}
STAGE_COLORS = ["#0f766e","#0e7490","#4f46e5","#7c3aed","#b45309","#be185d","#15803d"]

ENGINES = [
 ("Soft choice","turn scores into a weighted pick that gradients can flow through",
   ["attention","policy","guidance","exploration"]),
 ("Gradient descent","nudge millions of dials downhill on an error signal",
   ["pretraining","policy_gradient","diffusion","fine_tuning","transformer_block"]),
 ("Sampling from a distribution","draw plausible outcomes you can't write down directly",
   ["diffusion","score_matching","flow_matching","reasoning_traces","exploration"]),
 ("Value of a situation","estimate long-run reward and let it ripple backward",
   ["q_learning","actor_critic","credit_assignment","model_based_rl"]),
 ("Objective design","the signal you optimize IS the behavior you get",
   ["reward","rl_for_llms","evaluation","guidance"]),
 ("Meaning as geometry","related things sit close in a space of numbers",
   ["embeddings","latent_space","vision_transformers","attention"]),
 ("Scale into emergence","more data and parameters buy predictably more skill",
   ["scaling_laws","generalization","pretraining"]),
 ("Stay close to what you trust","a leash that stops training from degenerating",
   ["rl_for_llms","fine_tuning","offline_rl","guidance"]),
]

# ---- the mathematics capstone: recurring primitives -> the concepts that use them
PRIMITIVES = [
 ("Softmax — differentiable choice","Turn a list of scores into positive weights that sum to one, so 'pick the best' becomes smooth and trainable.",
   "weight_i = exp(score_i) / sum_j exp(score_j)",
   ["attention","policy","guidance"]),
 ("Gradient descent","Everything learns the same way: measure the error, compute which direction lowers it, take a small step, repeat.",
   "params <- params - step * gradient(loss)",
   ["pretraining","policy_gradient","diffusion","fine_tuning","transformer_block"]),
 ("Cross-entropy / next-token likelihood","Reward the model for putting probability on the true next piece; minimizing surprise IS learning language.",
   "loss = - sum  log P(true next token)",
   ["pretraining","tokenization","generalization"]),
 ("Dot-product similarity","Meaning becomes geometry: how aligned two vectors are measures how related two things are.",
   "similarity(a,b) = a . b   (large when aligned)",
   ["attention","embeddings","latent_space"]),
 ("The score — gradient of log-density","Instead of the probability itself (impossible to normalize), learn which way is 'uphill' toward the data everywhere.",
   "score(x) = gradient of log p(x)",
   ["score_matching","diffusion","flow_matching"]),
 ("Probability transport","Carry a simple noise distribution to the complex data distribution, one small step at a time.",
   "noise  ->  ...  ->  data   (denoise or flow)",
   ["diffusion","flow_matching","score_matching"]),
 ("Expected value & the Bellman recursion","The worth of a situation is the reward now plus the (discounted) worth of where you land next.",
   "V(s) = reward + discount * V(next state)",
   ["q_learning","actor_critic","credit_assignment","model_based_rl"]),
 ("Policy-gradient / REINFORCE estimator","Raise the probability of the moves that led to good outcomes, weighted by how good.",
   "nudge = grad(log P(action)) * (return)",
   ["policy_gradient","actor_critic","rl_for_llms"]),
 ("Advantage & baselines","Subtract what you 'expected' so the learning signal is only the surprise — far less noisy.",
   "advantage = return - baseline(state)",
   ["actor_critic","credit_assignment","policy_gradient"]),
 ("KL divergence — a leash","Penalize drifting too far from a trusted reference distribution; the guardrail against collapse.",
   "penalty = KL( new || reference )",
   ["rl_for_llms","guidance","fine_tuning","offline_rl"]),
 ("Discounting — credit over time","A reward far in the future counts a little less each step, which is what makes long-horizon credit tractable.",
   "return = r0 + g r1 + g^2 r2 + ...",
   ["credit_assignment","q_learning","reward"]),
 ("Power-law scaling","Loss falls as a straight line on a log-log plot against size — capability you can forecast and budget for.",
   "loss  ~  (size) ^ (-a)",
   ["scaling_laws","pretraining","generalization"]),
 ("Explore vs exploit","Spend some tries on the unknown, not just the current best — and sample many paths, not one.",
   "act = best-known  (usually)  /  random  (sometimes)",
   ["exploration","offline_rl","reasoning_traces"]),
 ("Distribution shift — the unseen","A model is only trustworthy where it had data; the gap between train and test governs everything.",
   "danger where  test distribution != train distribution",
   ["offline_rl","generalization","evaluation"]),
]

HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Stanford AI Concept Lab</title>
<link rel="stylesheet" href="assets/styles.css">
<style>
:root{{--a:#0f766e}}
main{{max-width:1080px}}
.lead{{font-size:19px;line-height:1.55;color:#2c2c2c;max-width:820px;margin:6px 0 26px}}
.kick{{font-size:12px;color:var(--a);font-weight:800;text-transform:uppercase;letter-spacing:.07em;margin:8px 0 2px}}
.stage{{border:1px solid #d9d7cf;border-radius:12px;background:#fff;padding:14px 18px;margin:12px 0}}
.stage h3{{margin:0 0 3px;font-size:17px}}.stage .sub{{color:#5a5a5a;font-size:14px;margin:0 0 10px}}
.stnum{{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:#fff;padding:2px 8px;border-radius:20px;margin-right:8px}}
.chips{{display:flex;flex-wrap:wrap;gap:7px}}
.chip{{font-size:13.5px;text-decoration:none;border:1px solid #d9d7cf;border-radius:20px;padding:4px 12px;background:#f7f7f4;color:#1a1a1a;transition:.12s}}
.chip:hover{{border-color:var(--a);color:var(--a)}}
.prim{{border-left:4px solid var(--a);background:#f2f7f6;border-radius:0 10px 10px 0;padding:14px 18px;margin:16px 0}}
.prim h3{{margin:0 0 6px;font-size:17px}}.prim p{{margin:0 0 8px;font-size:15px;color:#2c2c2c;max-width:78ch}}
.eqn{{font-family:ui-monospace,Menlo,monospace;font-size:13px;background:#0f2320;color:#a7f3d0;border-radius:6px;padding:8px 12px;margin:8px 0;overflow-x:auto}}
.thesis{{border-top:1px solid #d9d7cf;margin-top:26px;padding-top:18px;font-size:16px;color:#2c2c2c;max-width:80ch}}
.eng{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}}
.eng .stage{{margin:0}}
canvas{{width:100%;height:620px;border:1px solid #d9d7cf;border-radius:12px;background:#fbfbf9;display:block}}
.legend{{display:flex;flex-wrap:wrap;gap:12px;margin:12px 0;font-size:13px}}
.legend span{{display:inline-flex;align-items:center;gap:6px}}
.dot{{width:11px;height:11px;border-radius:50%;display:inline-block}}
</style></head><body>
<header class="topbar"><a class="brand" href="index.html">Stanford AI Concept Lab</a>
<nav><a href="index.html">Overview</a><a href="concepts.html">Concepts</a><a href="deep-track.html">Deep Track</a><a class="{h}" href="hub.html">The Machine</a><a class="{m}" href="math.html">Mathematics</a><a class="{g}" href="idea-graph.html">Idea Graph</a></nav></header>
<main>
"""
FOOT = '</main></body></html>\n'

def chips(ids):
    return '<div class="chips">' + "".join(
        f'<a class="chip" href="{href(c)}">{esc(NAME[c])}</a>' for c in ids) + '</div>'

def build_hub():
    out = [HEAD.format(title="The Machine", h="active", m="", g="")]
    out.append('<div class="kick">the one machine</div>')
    out.append('<h1>All 28 ideas are one pipeline</h1>')
    out.append('<p class="lead">Large language models, reinforcement learning, and diffusion look like three separate fields. They are not. Read left to right, they are one machine that turns raw data into an agent that can perceive, imagine, decide, and act — each of the 28 concepts is one stage or one recurring part of it. Every tile opens its computed deep dive.</p>')
    for i,(num,name,sub,ids) in enumerate(STAGES):
        c = STAGE_COLORS[i]
        out.append(f'<div class="stage"><h3><span class="stnum" style="background:{c}">{num}</span>{esc(name)}</h3>'
                   f'<p class="sub">{esc(sub)}</p>{chips(ids)}</div>')
    out.append('<div class="kick" style="margin-top:26px">the recurring engines</div>')
    out.append('<h2>Eight parts show up again and again</h2>')
    out.append('<p class="lead">Cut across the stages and the same handful of mechanisms reappear everywhere — the real vocabulary of the field. Each links the concepts that share it.</p>')
    out.append('<div class="eng">')
    for name,sub,ids in ENGINES:
        out.append(f'<div class="stage"><h3>{esc(name)}</h3><p class="sub">{esc(sub)}</p>{chips(ids)}</div>')
    out.append('</div>')
    out.append('<p class="thesis"><strong>The through-line:</strong> almost every idea here is the same meta-move — when you cannot do something directly (choose the best token, sample a realistic image, know the value of a move, get a model to reason), replace it with something a gradient can improve, then refuse the shortcut that would let it cheat. Learn the machine once and the three fields collapse into one.</p>')
    out.append(FOOT)
    (SITE/"hub.html").write_text("\n".join(out))

def build_math():
    out = [HEAD.format(title="Mathematics", h="", m="active", g="")]
    out.append('<div class="kick">the mathematics capstone</div>')
    out.append('<h1>Fourteen pieces of math run all 28 ideas</h1>')
    out.append('<p class="lead">Strip away the names and the same small set of mathematical objects appears across large language models, reinforcement learning, and diffusion. Here is each one in plain words, its shape, and the concepts that are really just one of these in disguise. Every chip opens the computed deep dive.</p>')
    for name,gloss,eqn,ids in PRIMITIVES:
        out.append(f'<div class="prim"><h3>{esc(name)}</h3><p>{esc(gloss)}</p>'
                   f'<div class="eqn">{esc(eqn)}</div>{chips(ids)}</div>')
    out.append('<p class="thesis"><strong>One meta-move underneath:</strong> take a thing you cannot compute directly — the best choice, a sample from an impossible distribution, the value of a state, the gradient of a log-probability — and replace it with a differentiable surrogate you CAN push downhill. Softmax makes choice differentiable; the score makes sampling differentiable; the Bellman recursion makes long-horizon value computable; the policy gradient makes reward differentiable. The other half of the craft is the leash — KL penalties, baselines, staying inside the data — that stops the surrogate from being gamed. That is the whole subject.</p>')
    out.append(FOOT)
    (SITE/"math.html").write_text("\n".join(out))

def build_graph():
    # edges: two concepts linked if they share a primitive (weight = # shared)
    from collections import defaultdict
    pairw = defaultdict(int)
    for _,_,_,ids in PRIMITIVES:
        for a in range(len(ids)):
            for b in range(a+1,len(ids)):
                key = tuple(sorted((ids[a],ids[b])))
                pairw[key]+=1
    nodes = [{"id":c,"name":NAME[c],"stage":STAGE_OF[c]} for c in NAME]
    edges = [{"s":a,"t":b,"w":w} for (a,b),w in pairw.items()]
    import json
    out = [HEAD.format(title="Idea Graph", h="", m="", g="active")]
    out.append('<div class="kick">the idea graph</div>')
    out.append('<h1>The 28 ideas, wired by shared mathematics</h1>')
    out.append('<p class="lead">Every concept is a dot, colored by where it sits in the machine. A line joins two concepts that share a mathematical primitive (from the <a href="math.html">capstone</a>) — the more they share, the heavier the line. The clusters and bridges are not imposed; they fall out of the shared math. Drag a dot; click it to open its deep dive.</p>')
    out.append('<div class="legend">' + "".join(
        f'<span><i class="dot" style="background:{STAGE_COLORS[i]}"></i>{esc(STAGES[i][1])}</span>' for i in range(len(STAGES))) + '</div>')
    out.append('<canvas id="g"></canvas>')
    out.append(f'<script>const NODES={json.dumps(nodes)};const EDGES={json.dumps(edges)};'
               f'const COLORS={json.dumps(STAGE_COLORS)};const HREF=id=>"concepts/"+id+"-deep.html";</script>')
    out.append(GRAPH_JS)
    out.append(FOOT)
    (SITE/"idea-graph.html").write_text("\n".join(out))

GRAPH_JS = r"""<script>
const cv=document.getElementById('g'),ctx=cv.getContext('2d');
let W,H;function size(){const r=cv.getBoundingClientRect();W=cv.width=r.width*devicePixelRatio;H=cv.height=r.height*devicePixelRatio;ctx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);}
size();window.addEventListener('resize',size);
const w=()=>cv.getBoundingClientRect().width,h=()=>cv.getBoundingClientRect().height;
const idx={};NODES.forEach((n,i)=>{idx[n.id]=i;n.x=w()/2+Math.cos(i)*180+Math.random()*40;n.y=h()/2+Math.sin(i*1.7)*180+Math.random()*40;n.vx=0;n.vy=0;});
const E=EDGES.map(e=>({s:idx[e.s],t:idx[e.t],w:e.w}));
let drag=null,hover=null;
function tick(){
  for(let i=0;i<NODES.length;i++){const a=NODES[i];for(let j=i+1;j<NODES.length;j++){const b=NODES[j];
    let dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1;const rep=1400/(d*d);a.vx-=dx/d*rep;a.vy-=dy/d*rep;b.vx+=dx/d*rep;b.vy+=dy/d*rep;}}
  for(const e of E){const a=NODES[e.s],b=NODES[e.t];let dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1;const f=(d-90)*0.008*e.w;a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;}
  const cx=w()/2,cy=h()/2;
  for(const n of NODES){n.vx+=(cx-n.x)*0.002;n.vy+=(cy-n.y)*0.002;n.vx*=0.85;n.vy*=0.85;if(n!==drag){n.x+=n.vx;n.y+=n.vy;}n.x=Math.max(40,Math.min(w()-40,n.x));n.y=Math.max(30,Math.min(h()-30,n.y));}
}
function draw(){ctx.clearRect(0,0,w(),h());
  for(const e of E){const a=NODES[e.s],b=NODES[e.t];ctx.strokeStyle='rgba(15,118,110,'+(0.10+0.10*e.w)+')';ctx.lineWidth=e.w;ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();}
  for(const n of NODES){const r=n===hover?9:6.5;ctx.beginPath();ctx.arc(n.x,n.y,r,0,7);ctx.fillStyle=COLORS[n.stage];ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=1.5;ctx.stroke();
    ctx.fillStyle=n===hover?'#0f2320':'#3a3a3a';ctx.font=(n===hover?'700 ':'')+'12px system-ui';ctx.fillText(n.name,n.x+9,n.y+4);}
}
function loop(){tick();draw();requestAnimationFrame(loop);}loop();
function at(x,y){for(const n of NODES){if(Math.hypot(n.x-x,n.y-y)<11)return n;}return null;}
cv.addEventListener('mousemove',e=>{const r=cv.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top;if(drag){drag.x=x;drag.y=y;}else{hover=at(x,y);cv.style.cursor=hover?'pointer':'default';}});
cv.addEventListener('mousedown',e=>{const r=cv.getBoundingClientRect();drag=at(e.clientX-r.left,e.clientY-r.top);});
window.addEventListener('mouseup',()=>{drag=null;});
cv.addEventListener('click',e=>{const r=cv.getBoundingClientRect();const n=at(e.clientX-r.left,e.clientY-r.top);if(n)location.href=HREF(n.id);});
</script>"""

def wire_nav():
    # add the three synthesis links after "Deep Track" on every top-level page
    n=0
    add='<a href="deep-track.html">Deep Track</a>'
    ins=add+'<a href="hub.html">The Machine</a><a href="math.html">Mathematics</a><a href="idea-graph.html">Idea Graph</a>'
    for p in SITE.glob("*.html"):
        if p.name in ("hub.html","math.html","idea-graph.html"): continue
        t=p.read_text()
        if 'hub.html' in t: continue
        if add in t:
            t=t.replace(add,ins,1); p.write_text(t); n+=1
    print("wired synthesis nav into",n,"pages")

def main():
    build_hub(); build_math(); build_graph()
    print("built hub.html, math.html, idea-graph.html")
    wire_nav()

if __name__=="__main__":
    main()
