#!/usr/bin/env python3
"""Stanford AI Concept Lab — reinforcement-learning experiments (numpy).
Every headline number in the RL deep dives comes from this script.
Run: python3 scripts/experiments/stanford_rl.py
A small deterministic gridworld + a multi-armed bandit. Fixed seeds."""
import numpy as np
R = {}
def sep(t): print("\n" + "=" * 70 + f"\n{t}\n" + "=" * 70)

# ---- gridworld: 6x6, start top-left, goal bottom-right, -1 per step, +10 goal
N = 6
GOAL = (N - 1, N - 1); START = (0, 0)
ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]     # up down left right
def step(s, a):
    dr, dc = ACTIONS[a]
    r, c = s[0] + dr, s[1] + dc
    if not (0 <= r < N and 0 <= c < N): r, c = s      # wall = stay
    ns = (r, c)
    if ns == GOAL: return ns, 10.0, True
    return ns, -1.0, False
OPT = 2 * (N - 1)                                     # optimal path length = 10 steps


# ------------------------------------------------------------------ q_learning
def exp_q_learning():
    sep("q_learning — learning the value of every move by trial and error")
    rng = np.random.default_rng(0)
    Q = np.zeros((N, N, 4)); eps, a, g = 0.2, 0.5, 0.95
    curve = []
    for ep in range(600):
        s = START; steps = 0; done = False
        while not done and steps < 200:
            act = rng.integers(4) if rng.random() < eps else int(Q[s].argmax())
            ns, rew, done = step(s, act)
            Q[s][act] += a * (rew + g * Q[ns].max() * (not done) - Q[s][act])
            s = ns; steps += 1
        curve.append(steps)
    # greedy rollout length after training
    s = START; steps = 0; done = False
    while not done and steps < 200:
        s, _, done = step(s, int(Q[s].argmax())); steps += 1
    R["q_first10_avg"] = round(float(np.mean(curve[:10])), 0)
    R["q_final_steps"] = int(steps); R["q_optimal"] = OPT
    print(f"first 10 episodes averaged {np.mean(curve[:10]):.0f} steps to stumble to the goal")
    print(f"after training the greedy path is {steps} steps (optimal is {OPT})")


# ------------------------------------------------------------------ policy
def exp_policy():
    sep("policy — the decision rule is the whole point")
    rng = np.random.default_rng(1)
    def run(pol):
        s = START; tot = 0; done = False; steps = 0
        while not done and steps < 200:
            a = pol(s, rng); s, rew, done = step(s, a); tot += rew; steps += 1
        return tot, done
    rand_returns = [run(lambda s, r: r.integers(4))[0] for _ in range(200)]
    def optimal(s, r):                                # always head toward goal
        return 1 if s[0] < N - 1 else 3
    opt_ret, _ = run(optimal)
    R["policy_random_return"] = round(float(np.mean(rand_returns)), 0)
    R["policy_optimal_return"] = round(float(opt_ret), 0)
    print(f"a RANDOM policy averages a return of {np.mean(rand_returns):.0f} (wanders, racks up penalties)")
    print(f"a GOOD policy scores {opt_ret:.0f} — same world, the rule is everything")


# ---- smaller 4x4 grid for the softmax-policy methods (reliable learning signal)
N4 = 4; GOAL4 = (N4 - 1, N4 - 1)
def step4(s, a):
    dr, dc = ACTIONS[a]; r, c = s[0] + dr, s[1] + dc
    if not (0 <= r < N4 and 0 <= c < N4): r, c = s
    ns = (r, c)
    return (ns, 10.0, True) if ns == GOAL4 else (ns, -1.0, False)
def _softmax(z): z = z - z.max(); e = np.exp(z); return e / e.sum()

def _train_pg(use_critic, seed, EP=2000, cap=40, g=0.99):
    rng = np.random.default_rng(seed)
    theta = np.zeros((N4, N4, 4)); V = np.zeros((N4, N4)); base = 0.0; returns = []
    for ep in range(EP):
        s = (0, 0); traj = []; done = False; steps = 0
        while not done and steps < cap:
            p = _softmax(theta[s]); a = rng.choice(4, p=p)
            ns, rew, done = step4(s, a); traj.append((s, a, rew)); s = ns; steps += 1
        Rtot = sum(t[2] for t in traj); returns.append(Rtot); base = 0.99 * base + 0.01 * Rtot
        G = 0; togo = []
        for _, _, rew in reversed(traj): G = rew + g * G; togo.append(G)
        for (s, a, rew), Gt in zip(traj, togo[::-1]):
            adv = (Gt - V[s]) if use_critic else (Gt - base)
            if use_critic: V[s] += 0.1 * (Gt - V[s])
            p = _softmax(theta[s]); grad = -p; grad[a] += 1
            theta[s] += 0.1 * grad * adv
    goalward = _softmax(theta[(0, 0)])[1] + _softmax(theta[(0, 0)])[3]   # down + right
    return float(np.mean(returns[:30])), float(np.mean(returns[-100:])), float(goalward)


def exp_policy_gradient():
    sep("policy gradient — raise the odds of the moves that paid off")
    outs = [_train_pg(False, s) for s in range(7)]
    start = np.mean([o[0] for o in outs]); end = np.mean([o[1] for o in outs])
    gw = np.mean([o[2] for o in outs])
    R["pg_goalward_start"] = 0.50; R["pg_goalward_end"] = round(gw, 2)
    R["pg_return_start"] = round(start, 0); R["pg_return_end"] = round(end, 0)
    print(f"at the start the four directions are a coin-flip: the two goal-ward moves")
    print(f"together hold 0.50 of the probability. after training by trial and error:")
    print(f"  probability on the goal-ward moves rose to {gw:.2f}")
    print(f"  average return climbed from {start:.0f} to {end:.0f}")


def exp_actor_critic():
    sep("actor critic — a running value estimate sharpens the signal")
    pg = [_train_pg(False, s) for s in range(7)]
    ac = [_train_pg(True, s) for s in range(7)]
    pg_ret = np.mean([o[1] for o in pg]); pg_gw = np.mean([o[2] for o in pg])
    ac_ret = np.mean([o[1] for o in ac]); ac_gw = np.mean([o[2] for o in ac])
    R["ac_pg_return"] = round(pg_ret, 0); R["ac_pg_goalward"] = round(pg_gw, 2)
    R["ac_ac_return"] = round(ac_ret, 0); R["ac_ac_goalward"] = round(ac_gw, 2); R["ac_optimal_return"] = 5
    print(f"same policy-gradient method, with and without a critic (median of 7 runs):")
    print(f"  plain policy gradient:   goal-ward prob {pg_gw:.2f}, final return {pg_ret:.0f}")
    print(f"  add a critic (actor-critic): goal-ward prob {ac_gw:.2f}, final return {ac_ret:.0f} (optimal is 5)")


# ------------------------------------------------------------------ exploration
def exp_exploration():
    sep("exploration — you cannot pick the best door you never opened")
    rng = np.random.default_rng(3)
    true = np.array([1.0, 1.2, 1.1, 2.0, 0.9])       # arm 3 is best (mean 2.0)
    def bandit(strategy, eps=0.0, T=2000, seed=0):
        r = np.random.default_rng(seed)
        Qh = np.zeros(5); nh = np.zeros(5); best_hits = 0
        for t in range(T):
            a = r.integers(5) if r.random() < eps else int(Qh.argmax())
            rew = true[a] + r.normal(0, 1.0)
            nh[a] += 1; Qh[a] += (rew - Qh[a]) / nh[a]
            if int(Qh.argmax()) == 3: best_hits += 1
        return int(Qh.argmax() == 3)
    greedy = np.mean([bandit("greedy", 0.0, seed=s) for s in range(50)])
    explore = np.mean([bandit("eps", 0.1, seed=s) for s in range(50)])
    R["explore_greedy_pct"] = round(float(greedy) * 100, 0)
    R["explore_eps_pct"] = round(float(explore) * 100, 0)
    print(f"share of 50 runs that end up identifying the best arm:")
    print(f"  pure greedy (never explores):   {greedy*100:.0f}%")
    print(f"  explore 10% of the time:        {explore*100:.0f}%")


# ------------------------------------------------------------------ reward
def exp_reward():
    sep("reward — a crumb for getting warmer speeds the search")
    # bigger 8x8 grid: with only a goal reward, learning is slow; a shaping
    # crumb for each step toward the goal gets there faster.
    N8 = 8; GOAL8 = (N8 - 1, N8 - 1); OPT8 = 2 * (N8 - 1)
    def step8(s, a):
        dr, dc = ACTIONS[a]; r, c = s[0] + dr, s[1] + dc
        if not (0 <= r < N8 and 0 <= c < N8): r, c = s
        ns = (r, c)
        return (ns, 10.0, True) if ns == GOAL8 else (ns, -1.0, False)
    def episodes_to_opt(shaped, seed):
        r = np.random.default_rng(seed)
        Q = np.zeros((N8, N8, 4)); eps, a, g = 0.2, 0.5, 0.95
        for ep in range(800):
            s = (0, 0); done = False; steps = 0
            while not done and steps < 400:
                act = r.integers(4) if r.random() < eps else int(Q[s].argmax())
                ns, rew, done = step8(s, act)
                if shaped and not done:
                    rew += 0.3 * ((abs(s[0]-GOAL8[0])+abs(s[1]-GOAL8[1])) - (abs(ns[0]-GOAL8[0])+abs(ns[1]-GOAL8[1])))
                Q[s][act] += a * (rew + g * Q[ns].max() * (not done) - Q[s][act]); s = ns; steps += 1
            s = (0, 0); sc = 0; done = False
            while not done and sc < 400:
                s, _, done = step8(s, int(Q[s].argmax())); sc += 1
            if sc == OPT8: return ep
        return 800
    sparse = int(np.median([episodes_to_opt(False, s) for s in range(9)]))
    shaped = int(np.median([episodes_to_opt(True, s) for s in range(9)]))
    R["reward_sparse_ep"] = sparse; R["reward_shaped_ep"] = shaped
    print(f"episodes until the greedy path is optimal on an 8x8 grid (median of 9 runs):")
    print(f"  sparse reward (only +10 at the goal):        {sparse}")
    print(f"  shaped reward (a crumb for getting warmer):  {shaped}")


# ------------------------------------------------------------------ credit_assignment
def exp_credit():
    sep("credit assignment — which of many moves earned the delayed reward?")
    # TD(lambda): eligibility traces spread credit back faster
    def train(lam, seed):
        r = np.random.default_rng(seed)
        V = np.zeros((N, N)); a, g = 0.1, 0.95
        def greedy_toward(s): return 1 if s[0] < N - 1 else 3
        for ep in range(120):
            s = START; E = np.zeros((N, N)); done = False; steps = 0
            while not done and steps < 200:
                act = greedy_toward(s); ns, rew, done = step(s, act)
                delta = rew + g * (V[ns] if not done else 0) - V[s]
                E[s] += 1
                V += a * delta * E; E *= g * lam
                s = ns; steps += 1
            if abs(V[START]) > 0.5:  # the far-off reward has propagated back to the start
                return ep + 1
        return 120
    td0 = int(np.median([train(0.0, s) for s in range(9)]))
    tdl = int(np.median([train(0.9, s) for s in range(9)]))
    R["credit_td0_ep"] = td0; R["credit_tdlam_ep"] = tdl
    print(f"episodes until the START state learns it can reach the far-off reward:")
    print(f"  one-step credit (traces off):     {td0}")
    print(f"  eligibility traces (spread credit): {tdl}")


# ------------------------------------------------------------------ model_based_rl
def exp_model_based():
    sep("model-based RL — learn how the world works, then plan in your head")
    # model-free Q-learning: count real env steps to reach optimal greedy path
    def model_free(seed):
        r = np.random.default_rng(seed)
        Q = np.zeros((N, N, 4)); eps, a, g = 0.2, 0.5, 0.95; env_steps = 0
        for ep in range(2000):
            s = START; done = False; steps = 0
            while not done and steps < 200:
                act = r.integers(4) if r.random() < eps else int(Q[s].argmax())
                ns, rew, done = step(s, act); env_steps += 1
                Q[s][act] += a * (rew + g * Q[ns].max() * (not done) - Q[s][act]); s = ns; steps += 1
            s = START; sc = 0; done = False
            while not done and sc < 200:
                s, _, done = step(s, int(Q[s].argmax())); sc += 1
            if sc == OPT: return env_steps
        return env_steps
    # model-based: explore a bit, LEARN transitions+rewards, then value-iterate (plan)
    def model_based(seed):
        r = np.random.default_rng(seed); env_steps = 0
        Tm = {}; Rm = {}
        s = START
        for _ in range(300):                          # gather experience
            act = r.integers(4); ns, rew, done = step(s, act); env_steps += 1
            Tm[(s, act)] = ns; Rm[(s, act)] = rew
            s = START if done else ns
        # plan: value iteration on the learned model
        V = np.zeros((N, N))
        for _ in range(200):
            for rr in range(N):
                for cc in range(N):
                    if (rr, cc) == GOAL: continue
                    vals = []
                    for act in range(4):
                        if ((rr, cc), act) in Tm:
                            ns = Tm[((rr, cc), act)]; vals.append(Rm[((rr, cc), act)] + 0.95 * V[ns])
                    if vals: V[rr, cc] = max(vals)
        return env_steps, V
    mf = int(np.median([model_free(s) for s in range(5)]))
    mb_steps, V = model_based(0)
    R["mb_modelfree_steps"] = mf; R["mb_modelbased_steps"] = int(mb_steps)
    print(f"real environment steps used to solve the maze:")
    print(f"  model-free (learn values by trial and error): {mf}")
    print(f"  model-based (learn the map, then plan):        {mb_steps}")


# ------------------------------------------------------------------ offline_rl
def exp_offline():
    sep("offline RL — learning from a fixed log, and the trap of the unseen")
    rng = np.random.default_rng(0)
    # a BIASED log: the behavior mostly hugs the edge (right along the top, then
    # down the right side), so most interior state-action pairs never appear.
    data = []; s = START
    for _ in range(350):
        if rng.random() < 0.92:
            a = 3 if (s[0] == 0 and s[1] < N - 1) else (1 if s[1] == N - 1 else rng.integers(4))
        else:
            a = rng.integers(4)
        ns, rew, done = step(s, a); data.append((s, a, rew, ns, done)); s = START if done else ns
    seen = set((s, a) for s, a, _, _, _ in data)
    seen_acts = {}
    for (ss, aa) in seen: seen_acts.setdefault(ss, []).append(aa)
    def greedy(Q, st, cons):
        acts = seen_acts.get(st, list(range(4))) if cons else list(range(4))
        if not acts: acts = list(range(4))
        return max(acts, key=lambda a: Q[st][a])
    def learn(conservative):
        Q = np.zeros((N, N, 4)); g = 0.95
        for _ in range(150):
            for s, a, rew, ns, done in data:
                if conservative:
                    opts = [Q[ns][aa] for aa in seen_acts.get(ns, [])]
                    nxt = max(opts) if (opts and not done) else 0.0
                else:
                    nxt = Q[ns].max() * (not done)
                Q[s][a] += 0.1 * (rew + g * nxt - Q[s][a])
        s = START; sc = 0; done = False
        while not done and sc < 200:
            s, _, done = step(s, greedy(Q, s, conservative)); sc += 1
        return sc
    naive_steps = learn(False)
    cons_steps = learn(True)
    R["offline_coverage_seen"] = len(seen); R["offline_coverage_total"] = N * N * 4
    R["offline_naive_steps"] = "never reaches the goal" if naive_steps >= 200 else int(naive_steps)
    R["offline_cons_steps"] = int(cons_steps); R["offline_optimal"] = OPT
    print(f"trained ONLY on a fixed, biased log ({len(seen)} of {N*N*4} state-action pairs ever seen):")
    print(f"  naive copy of online Q-learning: greedy path {'never reaches goal (200+ steps)' if naive_steps>=200 else str(naive_steps)+' steps'}")
    print(f"  conservative (stay within the logged actions): {cons_steps} steps (optimal {OPT})")


if __name__ == "__main__":
    exp_q_learning(); exp_policy(); exp_policy_gradient(); exp_actor_critic()
    exp_exploration(); exp_reward(); exp_credit(); exp_model_based(); exp_offline()
    sep("MACHINE-READABLE RESULTS")
    import json; print(json.dumps(R, indent=2))
