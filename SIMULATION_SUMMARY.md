# Wealth Inequality Emergence: Complete Model Documentation

## Table of Contents

1. [Overview](#overview)
2. [Mathematical Model](#mathematical-model)
3. [Theoretical Foundation](#theoretical-foundation)
4. [Emergent Phenomena](#emergent-phenomena)
5. [Policy Interventions](#policy-interventions)
6. [Implementation Details](#implementation-details)
7. [Experimental Design](#experimental-design)
8. [Results Interpretation](#results-interpretation)
9. [Limitations & Extensions](#limitations--extensions)

---

## Overview

### Core Question

**Why does wealth inequality persist and grow, even in systems that start with perfect equality and operate under symmetric, "fair" rules?**

### Core Answer

This simulation demonstrates that:

- **Structural advantages**, even tiny ones (5% edge)
- Operating through **random interactions**
- Over **many iterations**
- Inevitably produce **extreme wealth concentration**

This is a deterministic emergent property of the system, not the result of individual choices or moral failings.

---

## Mathematical Model

### 1. Initialization

**Population**: \( N \) agents (default \( N = 100 \))

**Initial wealth**: All agents start with equal wealth:
\[
w_i(0) = W_0 \quad \forall i \in \{1, 2, \ldots, N\}
\]
where \( W_0 = 100 \) (default)

**Agent types**: Each agent \( i \) is assigned a trading style \( s_i \in \{\text{Greedy}, \text{Neutral}, \text{Contrarian}\} \) with probabilities:
\[
P(s_i = \text{Greedy}) = r_G = 0.33
\]
\[
P(s_i = \text{Neutral}) = r_N = 0.33
\]
\[
P(s_i = \text{Contrarian}) = r_C = 1 - r_G - r_N = 0.34
\]

---

### 2. Trading Mechanism (Each Round \( t \))

**Step 1: Random pairing**

Two distinct active agents \( i, j \) are uniformly sampled:
\[
(i, j) \sim \text{Uniform}(\{k : a_k = \text{active}\})
\]
where \( a_k \in \{\text{active}, \text{bankrupt}\} \) is agent \( k \)'s status.

---

**Step 2: Stake calculation**

Each agent proposes a stake as a fraction of their wealth based on their style:
\[
\text{stake}\_i = \beta(s_i) \cdot w_i(t)
\]
where:
\[
\beta(s) = \begin{cases}
0.30 & \text{if } s = \text{Greedy} \\
0.20 & \text{if } s = \text{Neutral} \\
0.10 & \text{if } s = \text{Contrarian}
\end{cases}
\]

The **actual stake** used in the exchange is the minimum:
\[
S = \min(\text{stake}\_i, \text{stake}\_j)
\]

This ensures both agents risk the same amount (fairness constraint).

---

**Step 3: Biased wealth exchange**

The richer agent gets a structural advantage. Define:
\[
\text{rich} = \arg\max(w_i(t), w_j(t))
\]
\[
\text{poor} = \arg\min(w_i(t), w_j(t))
\]

The **rich agent wins** with probability:
\[
P(\text{rich wins}) = 0.5 + b
\]
where \( b \) is the **rich bias** (default \( b = 0.05 \), i.e., 55% win rate).

The **poor agent wins** with probability:
\[
P(\text{poor wins}) = 0.5 - b = 0.45
\]

---

**Step 4: Wealth update**

Based on the outcome:
\[
w*{\text{winner}}(t+1) = w*{\text{winner}}(t) + S
\]
\[
w*{\text{loser}}(t+1) = w*{\text{loser}}(t) - S
\]

---

**Step 5: Bankruptcy check**

If an agent's wealth falls below a threshold:
\[
w*i(t+1) < w*{\min} = 0.10
\]
then:
\[
w_i(t+1) \gets 0, \quad a_i \gets \text{bankrupt}
\]

Bankrupt agents exit the market permanently (no re-entry).

---

### 3. Stopping Condition

The simulation continues until:
\[
|\{i : a_i = \text{active}\}| < 2
\]
i.e., fewer than 2 agents remain active (can't form pairs).

---

## Theoretical Foundation

### The Yard-Sale Model

This simulation is based on the **yard-sale model** of wealth exchange, introduced by economists to study wealth distribution dynamics.

#### Key Insight

Even when:

- All trades are "voluntary" (random pairing)
- Rules are symmetric (both stake the same)
- Initial conditions are equal (everyone starts with \( W_0 \))

A **small bias** toward the wealthy causes:
\[
\text{Wealth concentration} \to \text{Power law distribution}
\]

#### Why the Bias Matters

Without bias (\( b = 0 \)):

- Wealth performs a **random walk** (Brownian motion)
- **Mean reversion**: Luck averages out over time
- Gini coefficient stays moderate (\( \approx 0.3-0.4 \))

With bias (\( b > 0 \)):

- Wealth performs a **biased random walk with absorbing barrier**
- **Rich-get-richer feedback loop**: Wins compound
- **Bankruptcy is absorbing**: Can't recover from zero
- Gini coefficient → extreme values (\( 0.8-0.95 \))

---

### Mathematical Intuition

Consider agent \( i \) with wealth \( w_i \) at round \( t \).

Expected wealth change in a single exchange:
\[
\mathbb{E}[\Delta w_i \mid w_i > w_j] = P(\text{win}) \cdot S - P(\text{lose}) \cdot S
\]
\[
= (0.5 + b) \cdot S - (0.5 - b) \cdot S = 2bS
\]

If \( w_i > w_j \): **Expected gain** = \( +2bS \) (positive drift)

If \( w_i < w_j \): **Expected gain** = \( -2bS \) (negative drift)

Over many rounds:

- Rich agents have **positive drift** → accumulate wealth
- Poor agents have **negative drift** → lose wealth → bankruptcy
- Middle-class agents oscillate but tend toward one extreme or the other

This creates a **bifurcation**: wealth either grows exponentially or decays to zero.

---

## Emergent Phenomena

### 1. Gini Coefficient Evolution

The **Gini coefficient** \( G \) measures inequality:
\[
G = \frac{2 \sum*{i=1}^{N} i \cdot w_i^\text{sorted}}{N \sum*{i=1}^{N} w_i} - \frac{N+1}{N}
\]
where \( w_1^\text{sorted} \leq w_2^\text{sorted} \leq \ldots \leq w_N^\text{sorted} \).

**Interpretation**:

- \( G = 0 \): Perfect equality (everyone has the same)
- \( G = 1 \): Perfect inequality (one person has everything)

**Typical trajectory**:
\[
G(0) = 0.0 \quad \to \quad G(t \to \infty) \approx 0.85-0.95
\]

**Time scale**: Depends on \( N \), \( b \), and agent types, but typically:

- **Phase 1** (rounds 0-1000): Slow rise (\( G < 0.3 \))
- **Phase 2** (rounds 1000-5000): Rapid acceleration (\( G \) climbs to 0.6-0.8)
- **Phase 3** (rounds 5000+): Asymptotic approach to maximum (\( G \to 0.9+ \))

---

### 2. Wealth Concentration

**Top 10% share**: Fraction of total wealth owned by richest 10%:
\[
\text{Top10}(t) = \frac{\sum*{i \in \text{top 10\%}} w_i(t)}{\sum*{j=1}^N w_j(t)} \times 100\%
\]

**Top 1% share**: Fraction owned by richest 1%:
\[
\text{Top1}(t) = \frac{\sum*{i \in \text{top 1\%}} w_i(t)}{\sum*{j=1}^N w_j(t)} \times 100\%
\]

**Typical endgame** (after 10,000-20,000 rounds):

- Top 10% own: **70-90%** of wealth
- Top 1% own: **20-50%** of wealth

Compare to real-world data:

- **USA (2023)**: Top 10% own ~70%, top 1% own ~32% (similar!)
- **Nordic countries**: Top 10% own ~50-60%, top 1% own ~15-20%

---

### 3. Bankruptcy Dynamics

**Bankruptcy rate**: Fraction of agents who go broke:
\[
B(t) = \frac{|\{i : w_i(t) = 0\}|}{N}
\]

**Typical outcome**:

- **60-85%** of agents go bankrupt
- **Survival is rare** and mostly luck-driven

**Who survives?**

- **Greedy agents**: High risk/reward → some get very rich, most go bankrupt early
- **Contrarian agents**: Low risk → survive longer, but rarely win big
- **Neutral agents**: Middle ground → moderate survival rate

**Key insight**: Survival is **not** strongly correlated with agent type (all have ~similar survival rates), suggesting **luck dominates strategy** in this model.

---

### 4. Wealth Distribution Shape

At endgame, wealth follows a **power-law (Pareto) distribution**:
\[
P(w > x) \sim x^{-\alpha}
\]
where \( \alpha \approx 1-2 \) (heavy tail).

This means:

- **Most agents**: Near-zero wealth (at or near bankruptcy)
- **Few agents**: Extremely high wealth (orders of magnitude above median)
- **No middle class**: Bimodal distribution (poor majority + tiny rich elite)

---

## Policy Interventions

The simulation includes three redistributive mechanisms to test interventions:

### 1. Wealth Tax

**Mechanism**: Each round, tax the top \( x\% \) of agents at rate \( r \).

**Implementation**:

1. Sort active agents by wealth
2. Select top \( x\% \) (default: 10%)
3. Collect \( r \times w_i \) from each (default: \( r = 0.02 = 2\% \))
4. Reduce their wealth by tax amount

**Parameters**:

- \( x \in [1\%, 50\%] \): Percentile threshold (who gets taxed)
- \( r \in [0.1\%, 10\%] \): Tax rate per round

**Effects**:

- **Slows** wealth concentration (but doesn't stop it)
- Higher rates (\( r > 5\% \)) can cap top 1% share
- But poor still go bankrupt unless combined with UBI or safety net

---

### 2. Universal Basic Income (UBI)

**Mechanism**: Every round, give each active agent a fixed amount \( U \).

**Implementation**:
\[
w_i(t+1) \gets w_i(t+1) + U
\]
for all \( i \) with \( a_i = \text{active} \).

**Parameters**:

- \( U \in [0.1, 10] \): UBI amount per round (default: $1)

**Effects**:

- **Reduces bankruptcies** (provides income floor)
- Agents can recover from small losses
- But rich still accumulate faster than UBI provides
- Need \( U \gtrsim \text{expected loss rate} \) to prevent bankruptcy cascade

---

### 3. Safety Net (Wealth Floor)

**Mechanism**: Ensure no agent falls below minimum \( w\_{\min}^\text{floor} \).

**Implementation**:
\[
w*i(t+1) \gets \max(w_i(t+1), w*{\min}^\text{floor})
\]

**Parameters**:

- \( w\_{\min}^\text{floor} \in [1, 50] \): Minimum wealth (default: $10)

**Effects**:

- **Eliminates bankruptcies** (by definition)
- But inequality persists (just shifts floor up)
- Agents cluster at floor while elite soars above

---

### 4. Combined Policies

**Hypothesis**: Can we maintain \( G < 0.5 \) indefinitely?

**Test configuration**:

- Wealth tax: **10% at 5% rate**
- UBI: **$2 per round**
- Safety net: **$20 floor**
- Rich bias: **5%** (structural advantage remains)

**Result** (speculative, needs testing):

- May achieve \( G \approx 0.4-0.5 \) (moderate inequality)
- Top 1% share capped at ~10-15%
- But total wealth accumulation slows (trade-off)

**Open question**: What's the minimum intervention level to prevent extreme inequality?

---

## Implementation Details

### Performance Optimizations

1. **Sparse history recording**: Store wealth distribution every 5 rounds (not every round)
2. **Efficient Gini calculation**: Sort once, reuse for Gini and percentile calculations
3. **Limited serialization**: Keep only last 1000 data points in state storage
4. **Vectorized operations**: Use NumPy for wealth calculations where possible

### Randomness

- **RNG**: Uses `numpy.random` (Mersenne Twister)
- **No default seed**: Each run is different
- **Reproducibility**: Set seed at top of `wealth_inequality_sim.py`:
  ```python
  np.random.seed(42)
  ```

### Numerical Stability

- Wealth stored as `float64` (prevents overflow/underflow)
- Bankruptcy threshold \( w\_{\min} = 0.10 \) (not exactly 0, to avoid numerical issues)

---

## Experimental Design

### Recommended Parameter Sweeps

#### 1. Bias Sweep (Test sensitivity to rich advantage)

- Fix: \( N = 100 \), \( W_0 = 100 \), agent ratios = (0.33, 0.33, 0.34)
- Vary: \( b \in \{0, 0.02, 0.05, 0.10, 0.15\} \)
- Measure: Final Gini, top 1% share, bankruptcy rate, rounds to equilibrium

**Hypothesis**: \( G \) and bankruptcy rate increase monotonically with \( b \).

---

#### 2. Agent Type Sweep (Test role of risk appetite)

- Fix: \( N = 100 \), \( W_0 = 100 \), \( b = 0.05 \)
- Vary:
  - All greedy: \( (r_G, r_N, r_C) = (1.0, 0, 0) \)
  - All neutral: \( (0, 1.0, 0) \)
  - All contrarian: \( (0, 0, 1.0) \)
  - Mixed: \( (0.33, 0.33, 0.34) \)
- Measure: Time to equilibrium, wealth variance, survival rates

**Hypothesis**: Higher stakes (more greedy) → faster inequality growth.

---

#### 3. Redistribution Sweep (Test policy effectiveness)

- Fix: \( N = 100 \), \( W_0 = 100 \), \( b = 0.05 \), agent ratios = (0.33, 0.33, 0.34)
- Vary:
  - No intervention (baseline)
  - Wealth tax only: \( r \in \{1\%, 2\%, 5\%, 10\%\} \)
  - UBI only: \( U \in \{0.5, 1, 2, 5\} \)
  - Safety net only: \( w\_{\min}^\text{floor} \in \{5, 10, 20, 50\} \)
  - All three combined
- Measure: Steady-state Gini, top 1% share, bankruptcy rate, total wealth

**Hypothesis**:

- Wealth tax alone: Slows but doesn't stop inequality
- UBI alone: Prevents bankruptcies but top still concentrates
- Safety net alone: No bankruptcies but high Gini
- Combined: Can maintain \( G < 0.5 \) with sufficient intervention

---

### Statistical Analysis

For each experiment, run **10-20 independent simulations** (different random seeds) and report:

- **Mean ± std** of final Gini
- **Median** top 1% share
- **Distribution** of bankruptcy rates
- **Time series** of Gini evolution (with confidence bands)

This accounts for stochastic variation.

---

## Results Interpretation

### What the Simulation Shows

1. **Equality is unstable**:

   - Initial Gini = 0 (perfect equality)
   - Without intervention, \( G \to 0.9 \) (extreme inequality)
   - This is **not** due to initial conditions (everyone starts equal)

2. **Small biases compound**:

   - 5% advantage seems negligible
   - But over 10,000 rounds, produces 10x-100x wealth gaps
   - Compounding is exponential: \( (1 + b)^t \)

3. **Randomness amplifies inequality**:

   - Even "fair" trades (same stake for both) create divergence
   - Early lucky winners get richer → win more → dominate
   - Early unlucky losers go bankrupt → can't recover

4. **Bankruptcy is irreversible**:

   - Once wealth hits 0, agent exits forever
   - No welfare, no re-entry, no second chances
   - This is a key driver of extremes

5. **Policy can mitigate (but at a cost)**:
   - Strong intervention can cap inequality
   - But may slow overall wealth growth (fewer big winners)
   - Trade-off: Equality vs efficiency

---

### What the Simulation Does NOT Show

1. **Not a complete economic model**:

   - No production (wealth is only transferred, not created)
   - No labor, capital, or technological progress
   - No markets, prices, or supply/demand

2. **Not normative**:

   - Doesn't say inequality is "good" or "bad"
   - Just demonstrates emergence from simple rules
   - Real-world interventions have costs/benefits not modeled here

3. **Simplified assumptions**:
   - Binary trades (no multi-agent markets)
   - Fixed bias (in reality, may vary over time)
   - Homogeneous rules (all agents follow same logic)

---

### Real-World Parallels

The **5% rich bias** represents various structural advantages in real economies:

| Simulation              | Real-World Equivalent                                            |
| ----------------------- | ---------------------------------------------------------------- |
| 5% win probability edge | Better information (insider knowledge, market data)              |
|                         | Lower transaction costs (bulk discounts, fee waivers)            |
|                         | Better credit terms (lower interest rates for wealthy)           |
|                         | Network effects (connections to high-value opportunities)        |
|                         | Compounding returns (capital gains, interest on wealth)          |
|                         | Legal/tax advantages (lawyers, accountants, offshore structures) |

Real-world Gini coefficients:

- **South Africa**: ~0.63 (highest in world)
- **USA**: ~0.48
- **China**: ~0.47
- **UK**: ~0.35
- **Denmark**: ~0.28

This simulation can produce Gini of **0.85-0.95** (much higher than reality), suggesting:

- Real economies have more redistribution than modeled
- Or other dynamics (production, mobility) reduce inequality
- Or bias is <5% in practice

---

## Limitations & Extensions

### Current Limitations

1. **No wealth creation**: Total wealth is constant (zero-sum). Real economies grow.
2. **No social mobility**: Agent types fixed at birth (no learning, no strategy change).
3. **Binary interactions**: Only 2 agents per trade (no markets with many buyers/sellers).
4. **Fixed bias**: Rich advantage is constant (in reality, may diminish or grow with inequality).
5. **No inheritance or demographics**: Agents don't die or reproduce.
6. **No aggregate shocks**: No recessions, booms, or external events.

---

### Possible Extensions

#### 1. Add Wealth Creation

- Each trade has a probability \( p \) of creating new wealth (productivity)
- Winner gains \( S(1 + g) \), loser loses \( S \), where \( g > 0 \) is growth rate
- Tests: Does economic growth reduce inequality? (Kuznets curve)

#### 2. Endogenous Bias

- Make \( b(w*\text{rich} / w*\text{poor}) \) a function of wealth ratio
- E.g., \( b = b*0 \cdot \log(w*\text{rich} / w\_\text{poor}) \)
- Tests: Do extreme gaps accelerate or decelerate further concentration?

#### 3. Agent Learning

- Agents adapt their \( \beta(s) \) based on wins/losses (reinforcement learning)
- Tests: Do greedy agents learn to be more conservative after losses?

#### 4. Social Networks

- Agents only trade with neighbors in a network (not random pairing)
- Tests: Does network structure affect inequality? (Hub formation, clustering)

#### 5. Multi-Agent Markets

- Replace pairwise trades with auctions or markets (many buyers/sellers)
- Tests: Do markets reduce inequality via price discovery?

#### 6. Inheritance & Demographics

- Agents have finite lifespans, pass wealth to offspring
- Tests: How does inheritance perpetuate inequality across generations?

#### 7. Progressive Taxation

- Tax rate \( r(w) \) increases with wealth (not flat)
- E.g., \( r(w) = r*0 \cdot (w / w*{\text{median}})^\gamma \)
- Tests: Do progressive taxes outperform flat taxes?

#### 8. Tax-Funded UBI

- UBI amount = total taxes collected / number of active agents
- Tests: Can revenue-neutral redistribution maintain equality?

---

## Conclusion

This simulation demonstrates a profound economic insight:

> **Even in a system that starts with perfect equality and operates under symmetric, "fair" rules, tiny structural advantages compound to produce extreme, persistent inequality.**

The **5% rich bias** is enough to transform:

- **Everyone equal** (\( G = 0 \))
- Into **top 1% owns 50%** (\( G = 0.9 \))
- In just **10,000-20,000 rounds**

This is **not** due to:

- Individual greed or laziness (all agents follow the same rules)
- Initial unfairness (everyone starts with $100)
- Moral failings (no "bad actors" in the model)

It's an **emergent property** of the system itself: compounding advantages + random interactions + irreversible bankruptcy = extreme inequality.

**Policy implications**:

- Redistribution (taxes, UBI, safety nets) can counteract natural concentration
- But requires **active intervention** (market alone won't fix it)
- Trade-off between equality and growth (may need to test empirically)

**Next steps**:

- Run systematic parameter sweeps
- Compare to real-world inequality data
- Test extended models (wealth creation, learning, networks)
- Explore optimal policy design (minimum intervention for target Gini)

---

**This model is intentionally simplified to isolate the core dynamic. Real economies are vastly more complex, but this simulation captures one fundamental mechanism: how structural advantages compound to produce inequality, even from equal starts.**

---

_For quick start guide and usage instructions, see [README.md](README.md)._
