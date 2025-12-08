# Wealth Inequality Emergence Simulation

**An interactive agent-based model demonstrating how extreme wealth inequality emerges naturally from simple, symmetric trading rules—even when everyone starts with equal wealth.**

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🎯 What This Simulates

This simulation implements the **"yard-sale model"** of wealth exchange, showing a profound economic insight:

> **Equal starting conditions + Fair exchange rules + Tiny structural advantage = Massive inequality**

- Everyone starts with **$100** (perfectly equal)
- Simple pairwise trading with symmetric rules
- Richer agent gets a **5%** edge (e.g., better information, lower costs)
- After thousands of rounds: **Top 1% owns 30-50%, most agents bankrupt**

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

```bash
# Clone or download this repository
cd market_simulation

# Install dependencies
pip install -r requirements.txt
```

### Run the Simulation

```bash
python app_wealth_inequality.py
```

Then open your browser at:

```
http://localhost:8050
```

---

## 📊 How It Works

### 1. Initial Setup

- **Population**: 50-500 agents (default: 100)
- **Starting wealth**: Everyone gets **$100** (perfectly equal, no advantages)
- **Agent types** differ only in risk appetite:
  - **Greedy** (33%): Stakes 30% of wealth per trade (high risk/reward)
  - **Neutral** (33%): Stakes 20% of wealth per trade (medium risk)
  - **Contrarian** (33%): Stakes 10% of wealth per trade (low risk)

### 2. Trading Mechanism (Each Round)

1. **Random pairing**: Two active agents selected randomly
2. **Stake determination**:
   - Each agent proposes a stake based on their type
   - Actual stake = `min(agent_a_stake, agent_b_stake)` (both risk the same)
3. **Biased coin flip**:
   - Richer agent wins with probability: **50% + bias** (default: **55%**)
   - Poorer agent wins with probability: **50% - bias** (default: **45%**)
4. **Wealth transfer**: Winner takes the stake, loser loses it
5. **Bankruptcy**: Agent with wealth < $0.10 goes bankrupt (wealth = 0, exits market)

### 3. The "Rich-Get-Richer" Dynamic

The **5% advantage** seems tiny but compounds exponentially:

- After 1 trade: Rich agent has 55% vs 45% odds (slight edge)
- After 100 trades: Rich agent has likely won ~10 more times
- After 10,000 trades: Wealth concentrates at the top, most agents broke

This mirrors real-world advantages:

- Better access to information
- Lower transaction costs
- Superior credit terms
- Network effects
- Compounding returns on capital

---

## 🎛️ Controls & Parameters

### Basic Configuration

| Parameter            | Range     | Default | Effect                   |
| -------------------- | --------- | ------- | ------------------------ |
| **Number of Agents** | 50-500    | 100     | Population size          |
| **Initial Wealth**   | $10-$1000 | $100    | Everyone starts equal    |
| **Rich Bias**        | 0-15%     | 5%      | Richer agent's advantage |
| **Simulation Speed** | 1-1000x   | 10x     | Rounds per update        |

### Agent Style Ratios

Control the risk appetite distribution:

- **Greedy Ratio**: % of high-risk traders (30% stake)
- **Neutral Ratio**: % of medium-risk traders (20% stake)
- **Contrarian Ratio**: Auto-calculated (1 - greedy - neutral)

### Redistribution Policies (Optional)

Test interventions to combat natural inequality:

#### 💰 Wealth Tax

- **Tax Top %**: Which percentile to tax (1-50%, default 10%)
- **Tax Rate**: % of wealth collected per round (0.1-10%, default 2%)

#### 🏦 Universal Basic Income (UBI)

- **UBI Amount**: Fixed payment to all active agents per round ($0.1-$10, default $1)

#### 🛡️ Safety Net

- **Minimum Wealth Floor**: Guaranteed minimum wealth ($1-$50, default $10)
- Prevents complete bankruptcy by topping up agents below the floor

---

## 🧪 Suggested Experiments

### Experiment 1: Pure Free Market (Baseline)

**Goal**: Observe natural inequality emergence

**Settings**:

- Agents: 100
- Initial wealth: $100
- Rich bias: 5%
- All policies: **OFF**

**Expected outcome**:

- Gini rises from 0.0 → 0.85-0.95
- Top 10% own 70-90% of wealth
- 70-90% of agents go bankrupt
- Time: ~5,000-20,000 rounds

---

### Experiment 2: Zero Bias (Null Hypothesis)

**Goal**: What happens without structural advantage?

**Settings**:

- Rich bias: **0%**
- Everything else: default
- All policies: OFF

**Expected outcome**:

- Gini stays around 0.3-0.5 (moderate inequality)
- Much slower wealth concentration
- Fewer bankruptcies
- Tests whether bias is the key driver (it is)

---

### Experiment 3: Extreme Bias

**Goal**: Accelerate inequality to see endgame fast

**Settings**:

- Rich bias: **15%**
- Everything else: default

**Expected outcome**:

- Rapid concentration (<5,000 rounds)
- Very high bankruptcy rate
- Top 1% dominates quickly

---

### Experiment 4: All Greedy Traders

**Goal**: High-stakes environment

**Settings**:

- Greedy ratio: **100%**
- Neutral/Contrarian: 0%
- Rich bias: 5%

**Expected outcome**:

- Extreme volatility
- Faster inequality (bigger stakes = bigger wins/losses)
- High early bankruptcy rate

---

### Experiment 5: All Contrarian Traders

**Goal**: Risk-averse population

**Settings**:

- Contrarian ratio: **100%**
- Others: 0%
- Rich bias: 5%

**Expected outcome**:

- Slower inequality growth (lower stakes)
- More agents survive longer
- Same endgame but takes more rounds

---

### Experiment 6: Wealth Tax Only

**Goal**: Can taxation reduce inequality?

**Settings**:

- Rich bias: 5%
- **Wealth tax: ON** (top 10%, 2% rate)
- UBI: OFF
- Safety net: OFF

**Expected outcome**:

- Gini may peak lower (~0.7-0.8 vs 0.9)
- Slows concentration but doesn't prevent it
- Test higher rates (5-10%) for stronger effect

---

### Experiment 7: UBI Only

**Goal**: Can basic income prevent poverty?

**Settings**:

- Rich bias: 5%
- Wealth tax: OFF
- **UBI: ON** ($1 per round)
- Safety net: OFF

**Expected outcome**:

- Fewer bankruptcies (UBI provides income floor)
- Inequality may still grow at top
- Test if $1 is sufficient vs bankruptcy rate

---

### Experiment 8: Safety Net Only

**Goal**: Guaranteed minimum wealth

**Settings**:

- Rich bias: 5%
- Wealth tax: OFF
- UBI: OFF
- **Safety net: ON** ($10 minimum)

**Expected outcome**:

- Zero bankruptcies (by definition)
- But inequality persists (rich still get richer)
- Agents cluster at floor vs soaring top

---

### Experiment 9: Full Intervention

**Goal**: Maximum redistribution

**Settings**:

- Rich bias: 5%
- **Wealth tax: ON** (top 10%, 5% rate)
- **UBI: ON** ($2 per round)
- **Safety net: ON** ($20 minimum)

**Expected outcome**:

- Can you maintain Gini < 0.5?
- Trade-off: May reduce total wealth accumulation
- Test sustainability of policies vs market forces

---

## 📈 Metrics Explained

### Gini Coefficient

Measures inequality on a 0-1 scale:

- **0.0** = Perfect equality (everyone has the same)
- **0.3-0.4** = Moderate inequality (typical welfare states)
- **0.5-0.6** = High inequality (USA ~0.48)
- **0.8-0.9** = Extreme inequality (common in simulation)
- **1.0** = Perfect inequality (one person has everything)

### Wealth Concentration

- **Top 10% share**: % of total wealth owned by richest 10%
- **Top 1% share**: % of total wealth owned by richest 1%

### Active Agents

Number of agents still trading (not bankrupt)

### Bankruptcies

Count of agents with wealth fallen below $0.10

### Redistribution Totals (if policies enabled)

- **Taxes collected**: Cumulative wealth tax revenue
- **UBI distributed**: Cumulative basic income paid out
- **Safety net interventions**: Times agents were topped up to floor

---

## 📁 Project Structure

```
market_simulation/
├── app_wealth_inequality.py       # Dash web interface (UI + callbacks)
├── wealth_inequality_sim.py       # Core simulation engine (model logic)
├── requirements.txt               # Python dependencies
├── README.md                      # This file (quick start)
└── SIMULATION_SUMMARY.md          # Detailed model explanation
```

---

## 🔬 Technical Details

- **Framework**: Dash + Plotly (Python web framework)
- **Model**: Agent-based simulation
- **Update frequency**: 50ms (20 UI updates/second)
- **Simulation speed**: 1-1000 rounds per update (adjustable)
- **Performance optimization**:
  - Sparse history recording (every 5th round)
  - Limited serialization (last 1000 data points)
  - Efficient Gini calculation with sorted arrays

---

## 📚 Further Reading

For detailed mathematical explanations, policy analysis, and deeper insights, see:

- **[SIMULATION_SUMMARY.md](SIMULATION_SUMMARY.md)** - Complete model documentation

### Relevant Research

- Yard-sale model: Chakraborti & Chakrabarti (2000)
- Wealth inequality dynamics: Yakovenko & Rosser (2009)
- Agent-based wealth models: Angle (1986)

---

## 💡 Key Takeaways

1. **Equality is unstable**: Even with equal start, inequality emerges naturally
2. **Small advantages compound**: 5% bias → 90% wealth concentration
3. **Randomness ≠ fairness**: "Fair" coin flips can produce unfair outcomes
4. **Bankruptcy is absorbing**: No way back once you're out
5. **Intervention required**: Without redistribution, concentration is inevitable

This is a simplified model, but it captures a real dynamic: **structural advantages compound over time, producing extreme inequality without any individual "bad actors."**

---

## 🛠️ Reproducibility Notes

### Randomness

- Uses `numpy.random` for all random operations
- **No seed set by default** (different results each run)
- To reproduce exact runs, add at top of `wealth_inequality_sim.py`:
  ```python
  np.random.seed(42)  # Or any integer
  ```

### Parameter Ranges

All sliders and inputs have validation:

- Ratios must sum to ~1.0
- Minimum values enforced
- Simulation stops at <2 active agents

### Performance

- **Small runs** (100 agents, 10x speed): Real-time visualization smooth
- **Large runs** (500 agents, 1000x speed): May lag on older hardware
- Tested on: Python 3.8-3.12, macOS/Linux/Windows

---

## 📄 License

MIT License - Feel free to use, modify, and distribute.

---

## 🤝 Contributing

Found a bug or have suggestions? Open an issue or submit a pull request!

---

**Made to demonstrate how structural inequality emerges from simple rules. Play with it, break it, learn from it.**
