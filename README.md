# Wealth Inequality Emergence Simulation

Interactive real-time simulation showing how wealth inequality emerges from simple rules.

## The Story

**Everyone starts equal** → Simple trading rules + slight rich advantage → **Massive inequality + wealth concentration**

## Model

### Starting Conditions

- All agents start with **equal wealth** (default: $100)
- No initial class differences
- Only difference: **trading styles** (Greedy, Neutral, Contrarian)

### Trading Mechanism (Yard-Sale Model)

Each round:

1. Two random agents are paired
2. Each stakes a % of their wealth based on style:
   - **Greedy**: 30% (high risk)
   - **Neutral**: 20% (medium risk)
   - **Contrarian**: 10% (low risk)
3. Actual stake = minimum of both
4. **Rich-Get-Richer**: Richer agent has slight advantage (default 5%)
5. Winner takes stake, loser loses it
6. Bankruptcy: Agents with near-zero wealth exit

### Emergent Phenomena

- **Gini Coefficient**: Rises from 0 (perfect equality) to high values
- **Wealth Concentration**: Top 10% and top 1% own increasing shares
- **Bankruptcies**: Many agents go broke
- **Few Winners**: Small fraction becomes extremely wealthy

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the simulation
python app_wealth_inequality.py
```

Open browser at `http://localhost:8050`

## Usage

1. **Configure parameters**:

   - Number of agents, initial wealth
   - Style ratios (Greedy/Neutral/Contrarian)
   - Rich bias (structural advantage)
   - Simulation speed (1x to 1000x)

2. **Click Start**: Watch inequality emerge in real-time

3. **Observe**:
   - Gini coefficient climbing from 0
   - Wealth histogram spreading out
   - Top 1% and 10% shares increasing
   - Bankruptcies accumulating

## Key Parameters

| Parameter        | Description                 | Impact                        |
| ---------------- | --------------------------- | ----------------------------- |
| Rich Bias        | Advantage for richer agent  | Higher = faster concentration |
| Greedy Ratio     | % of high-risk agents       | More greedy = more volatility |
| Simulation Speed | Rounds per update (1-1000x) | Higher = faster simulation    |

## Experiments

1. **Zero Bias**: Set rich_bias=0 → Should see random walk, less concentration
2. **High Bias**: Set rich_bias=15% → Extreme concentration, rapid bankruptcies
3. **All Greedy**: greedy_ratio=1.0 → High stakes, extreme outcomes
4. **All Contrarian**: contrarian_ratio=1.0 → Low stakes, slower inequality

## What This Demonstrates

This model shows how **structural advantages compound over time**:

- Even a tiny 5% advantage for richer agents
- Over thousands of interactions
- Produces massive inequality

Real-world parallels:

- Better access to information
- Lower transaction costs
- Better credit terms
- Network effects
- Compounding returns

## Files

```
market_simulation/
├── app_wealth_inequality.py       # Dash interface
├── wealth_inequality_sim.py       # Core simulation
├── requirements.txt                # Dependencies
└── README.md                      # This file
```

## License

MIT
