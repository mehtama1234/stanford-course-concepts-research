#!/usr/bin/env python3
"""Stanford AI Concept Lab — generative-modeling experiments (torch, 2D toy).
Every headline number in the diffusion-family deep dives comes from this script.
Run: .venv-torch/bin/python scripts/experiments/stanford_diffusion.py
A ring of 8 Gaussians (for diffusion/score/flow) + two class-blobs (for guidance)."""
import math, json
import numpy as np
import torch
import torch.nn as nn

torch.manual_seed(0); np.random.seed(0)
R = {}
def sep(t): print("\n" + "=" * 70 + f"\n{t}\n" + "=" * 70)

# ---- target: 8 Gaussians evenly spaced on a circle of radius 4
K = 8
MODES = torch.tensor([[4 * math.cos(2 * math.pi * k / K), 4 * math.sin(2 * math.pi * k / K)]
                      for k in range(K)], dtype=torch.float32)
def sample_data(n):
    idx = torch.randint(0, K, (n,))
    return MODES[idx] + 0.15 * torch.randn(n, 2)
def frac_on_manifold(pts, r=0.6):
    d = torch.cdist(pts, MODES).min(dim=1).values
    return (d < r).float().mean().item()

def mlp(inp, hidden=128, out=2):
    return nn.Sequential(nn.Linear(inp, hidden), nn.SiLU(),
                         nn.Linear(hidden, hidden), nn.SiLU(),
                         nn.Linear(hidden, out))


# ------------------------------------------------------------------ diffusion (DDPM)
def exp_diffusion():
    sep("diffusion — destroy structure with noise, then learn to undo it")
    T = 50
    betas = torch.linspace(1e-4, 0.05, T)
    alphas = torch.cumprod(1 - betas, 0)                 # alpha-bar
    net = mlp(3); opt = torch.optim.Adam(net.parameters(), 1e-3)
    for it in range(4000):
        x0 = sample_data(512); t = torch.randint(0, T, (512,))
        ab = alphas[t].unsqueeze(1)
        noise = torch.randn_like(x0)
        xt = ab.sqrt() * x0 + (1 - ab).sqrt() * noise
        inp = torch.cat([xt, t.float().unsqueeze(1) / T], 1)
        loss = ((net(inp) - noise) ** 2).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    # reverse sampling
    x = torch.randn(2000, 2)
    with torch.no_grad():
        for t in reversed(range(T)):
            ab = alphas[t]; b = betas[t]
            inp = torch.cat([x, torch.full((x.shape[0], 1), t / T)], 1)
            eps = net(inp)
            mean = (x - b / (1 - ab).sqrt() * eps) / (1 - b).sqrt()
            x = mean + (b.sqrt() * torch.randn_like(x) if t > 0 else 0)
    on = frac_on_manifold(x); base = frac_on_manifold(torch.randn(2000, 2))
    R["diff_steps"] = T; R["diff_on_manifold"] = round(on * 100, 0)
    R["diff_noise_baseline"] = round(base * 100, 0)
    print(f"pure noise lands on the target shape {base*100:.0f}% of the time")
    print(f"after learning to denoise over {T} steps, samples land on it {on*100:.0f}% of the time")


# ------------------------------------------------------------------ score matching
def exp_score():
    sep("score matching — learn which way is uphill toward the data")
    sigma = 0.4
    net = mlp(2); opt = torch.optim.Adam(net.parameters(), 1e-3)
    for it in range(4000):                               # denoising score matching
        x0 = sample_data(512); noise = torch.randn_like(x0)
        xt = x0 + sigma * noise
        target = -noise / sigma                          # score of the noised density
        loss = ((net(xt) - target) ** 2).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    # Langevin sampling: walk uphill along the learned score
    x = 4 * torch.randn(2000, 2); step = 0.02
    with torch.no_grad():
        for _ in range(400):
            x = x + step * net(x) + math.sqrt(2 * step) * torch.randn_like(x)
    on = frac_on_manifold(x, r=0.8)
    R["score_on_manifold"] = round(on * 100, 0)
    print(f"following the learned 'uphill' arrows by random walk (Langevin),")
    print(f"samples settle onto the target shape {on*100:.0f}% of the time")


# ------------------------------------------------------------------ flow matching
def exp_flow():
    sep("flow matching — learn a straight current from noise to data")
    net = mlp(3); opt = torch.optim.Adam(net.parameters(), 1e-3)
    for it in range(4000):                               # conditional flow matching, straight paths
        x1 = sample_data(512); x0 = torch.randn(512, 2)
        t = torch.rand(512, 1)
        xt = (1 - t) * x0 + t * x1
        target = x1 - x0                                 # constant velocity along the straight path
        inp = torch.cat([xt, t], 1)
        loss = ((net(inp) - target) ** 2).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    def integrate(steps):
        x = torch.randn(2000, 2); dt = 1.0 / steps
        with torch.no_grad():
            for i in range(steps):
                t = torch.full((x.shape[0], 1), i * dt)
                x = x + dt * net(torch.cat([x, t], 1))
        return frac_on_manifold(x)
    on10 = integrate(10); on4 = integrate(4)
    R["flow_on_manifold_10"] = round(on10 * 100, 0); R["flow_on_manifold_4"] = round(on4 * 100, 0)
    print(f"integrating the learned current in just 10 steps: {on10*100:.0f}% on the target")
    print(f"even in only 4 steps: {on4*100:.0f}% — straight paths need few steps")


# ------------------------------------------------------------------ guidance
def exp_guidance():
    sep("guidance — steer the sampler toward the class you asked for")
    # two overlapping classes: left blob (-2,0) and right blob (+2,0)
    C = torch.tensor([[-2.0, 0.0], [2.0, 0.0]])
    def sample_class(n, c):
        return C[c] + 0.6 * torch.randn(n, 2)
    net = mlp(4)                                         # input: x(2), t(1), label(1)
    opt = torch.optim.Adam(net.parameters(), 1e-3)
    for it in range(4000):
        c = torch.randint(0, 2, (512,))
        x1 = sample_class(512, c); x0 = torch.randn(512, 2); t = torch.rand(512, 1)
        xt = (1 - t) * x0 + t * x1; target = x1 - x0
        lab = c.float().unsqueeze(1)
        drop = (torch.rand(512, 1) < 0.2).float()        # randomly drop the label (train unconditional too)
        lab_in = torch.where(drop.bool(), torch.full_like(lab, -1.0), lab)
        loss = ((net(torch.cat([xt, t, lab_in], 1)) - target) ** 2).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    def generate(w, target_c=1, steps=20):
        x = torch.randn(2000, 2); dt = 1.0 / steps
        lab = torch.full((2000, 1), float(target_c)); un = torch.full((2000, 1), -1.0)
        with torch.no_grad():
            for i in range(steps):
                t = torch.full((2000, 1), i * dt)
                vc = net(torch.cat([x, t, lab], 1)); vu = net(torch.cat([x, t, un], 1))
                v = vu + w * (vc - vu)                    # classifier-free guidance
                x = x + dt * v
        purity = (x[:, 0] > 0).float().mean().item()      # fraction on the requested (right) class
        conc = (x - C[1]).norm(dim=1).mean().item()       # mean distance to the requested center
        return purity, conc
    p0, c0 = generate(0.0)          # unconditional: ignore the label
    p1, c1 = generate(1.0)          # add the guidance direction (conditional)
    R["guid_purity_unguided"] = round(p0 * 100, 0); R["guid_purity_guided"] = round(p1 * 100, 0)
    R["guid_dist_unguided"] = round(c0, 2); R["guid_dist_guided"] = round(c1, 2)
    print(f"asking for the right-hand class:")
    print(f"  no guidance (ignore the label):  {p0*100:.0f}% land on it, mean distance {c0:.2f}")
    print(f"  add the guidance direction:      {p1*100:.0f}% land on it, mean distance {c1:.2f}")


if __name__ == "__main__":
    exp_diffusion(); exp_score(); exp_flow(); exp_guidance()
    sep("MACHINE-READABLE RESULTS")
    print(json.dumps(R, indent=2))
