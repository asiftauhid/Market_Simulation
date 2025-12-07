# Wealth Inequality Emergence Simulation

## Overview

This is an agent-based model demonstrating how **massive wealth inequality naturally emerges** from simple, fair-seeming rules - even when everyone starts with exactly equal wealth.

---

## Core Concept: The Yard-Sale Model

The simulation is based on the "yard-sale" economic model, which shows that:

- **Equal starting point** → Everyone begins with the same wealth
- **Simple repeated exchanges** → Random pairwise wealth transfers
- **Slight bias** → Richer agents have a tiny advantage
- **Inevitable outcome** → Extreme wealth concentration

---

## Initial Conditions

### Everyone Starts Equal

- All agents begin with **identical wealth** (default: $100)
- No inherent advantages, skills, or resources
- Population size: 50-500 agents (default: 100)

### Agent Types (Risk Appetite)

Agents differ only in how much they're willing to risk per exchange:

- **Greedy** (33%): Stakes 30% of their wealth
- **Neutral** (33%): Stakes 20% of their wealth
- **Contrarian** (33%): Stakes 10% of their wealth

These ratios are adjustable but always sum to 100%.

---

## The Rules

### Each Round:

1. **Random Selection**: Two active agents are randomly chosen
2. **Stake Calculation**: Each proposes to stake a % of their wealth based on their style
3. **Actual Stake**: The smaller of the two proposed stakes is used (both risk the same amount)
4. **The Exchange** (Biased Coin Flip):
   - If **Agent A is richer** than Agent B:
     - Agent A wins with probability: **50% + bias** (default: 55%)
     - Agent B wins with probability: **50% - bias** (default: 45%)
   - Winner gains the stake, loser loses it
5. **Bankruptcy Check**: If wealth drops below $0.10, agent goes bankrupt (wealth = 0, marked inactive)

### Stopping Condition:

Simulation continues until fewer than 2 active agents remain.

---

## The "Rich-Get-Richer" Mechanism

The **critical insight**: The bias is small (typically 5%) but compounding:

- A richer agent has a 55% win probability vs a poorer agent's 45%
- This tiny advantage compounds over thousands of exchanges
- Wealth snowballs: winners keep winning, losers keep losing
- The rich accumulate more, the poor get bankrupted

---

## What Emerges

### Wealth Concentration

- **Top 10%** typically end up with 60-90% of all wealth
- **Top 1%** can control 20-40% of total wealth
- Most agents go bankrupt

### Gini Coefficient

- Starts at **0.0** (perfect equality)
- Rises toward **0.8-0.95** (extreme inequality)
- (0 = everyone equal, 1 = one person has everything)

### Agent Survival

- Greedy agents (higher stakes) tend to go bankrupt faster when unlucky
- Contrarian agents (lower stakes) survive longer but rarely get rich
- Final survivors are often lucky neutral/greedy agents who won early

---

## Key Insights

1. **Inequality is structural, not moral**: No agent is "better" or "worse" - they all follow rules
2. **Small advantages compound**: 5% bias → 90% wealth concentration
3. **Starting equal ≠ staying equal**: Randomness + bias = inevitable divergence
4. **Bankruptcy is absorbing**: Once you're out, you're out forever
5. **The rich really do get richer**: It's mathematically baked into the system

---

## Parameters You Can Adjust

### Basic Parameters

- **Number of Agents**: Population size (50-500)
- **Initial Wealth**: Starting amount (everyone equal)
- **Agent Style Ratios**: % of Greedy/Neutral/Contrarian
- **Rich Bias**: Advantage for richer agent (0-15%)
- **Simulation Speed**: Rounds processed per UI update (1-1000)

### Redistribution Policy Parameters

#### Wealth Tax

- **Enable/Disable**: Toggle wealth tax on or off
- **Tax Top %**: Which percentage of wealthiest agents to tax (1-50%, default 10%)
- **Tax Rate**: Percentage of wealth collected per round (0.1-10%, default 2%)

**How it works**: Each round, the top X% of agents by wealth are taxed at Y% rate. Collected taxes are tracked.

#### Universal Basic Income (UBI)

- **Enable/Disable**: Toggle UBI on or off
- **UBI Amount**: Fixed payment to all active agents per round ($0.1-10, default $1)

**How it works**: Every round, each active agent receives a fixed amount of wealth, regardless of their current wealth.

#### Safety Net

- **Enable/Disable**: Toggle safety net on or off
- **Minimum Wealth Floor**: Guaranteed minimum wealth ($1-50, default $10)

**How it works**: If an agent's wealth falls below the floor, it is automatically topped up to the minimum. Prevents complete bankruptcy.

---

## Policy Experiments

The simulation allows you to test whether interventions can counter natural inequality drift:

### Experiment Ideas

1. **Pure Market (No Policies)**

   - All policies disabled
   - Observe extreme concentration and high bankruptcy rate
   - Baseline for comparison

2. **Wealth Tax Only**

   - Enable tax on top 10% at 2%
   - Does it slow wealth concentration?
   - Can the rich still dominate?

3. **UBI Only**

   - Give everyone $1 per round
   - Does it prevent bankruptcies?
   - Does inequality still grow?

4. **Safety Net Only**

   - Set floor at $10
   - No one can go broke, but can inequality persist?
   - Does this change survival dynamics?

5. **Full Redistribution**

   - Enable all three policies
   - High tax rate + generous UBI + strong safety net
   - Can you maintain equality?

6. **Tax-Funded UBI**
   - Adjust tax rate and UBI amount to balance
   - Can redistribution be "revenue neutral"?

### Expected Outcomes

- **No intervention**: Gini → 0.9+, top 1% holds 30-50%, most agents bankrupt
- **Weak intervention**: Slower inequality growth but same endpoint
- **Strong intervention**: Can potentially maintain Gini < 0.4-0.5 indefinitely
- **Policy trade-offs**: Higher taxes may slow overall wealth growth but reduce inequality

---

## Why This Matters

This simple model mirrors real economic systems where:

- Small inherited advantages (wealth, connections, luck) compound
- "Fair" individual exchanges lead to unfair collective outcomes
- Without intervention (redistribution, safety nets), inequality grows naturally

Even with **identical starting wealth** and **symmetric rules**, the system inevitably produces a tiny wealthy elite and a large bankrupt majority.

### Policy Questions Explored

The redistribution mechanisms let you explore critical economic policy debates:

1. **Do wealth taxes reduce inequality?** Test different rates and thresholds
2. **Can UBI prevent poverty?** See if basic income keeps agents above bankruptcy
3. **Are safety nets enough?** Does a minimum floor change dynamics?
4. **What's the trade-off?** Do policies slow wealth accumulation while reducing inequality?
5. **Can policy overcome structure?** With the rich-get-richer bias built in, can intervention maintain equality?

This makes the simulation relevant to real-world debates about taxation, basic income, and welfare systems.

---

## Metrics Tracked

### Inequality Metrics

#### Gini Coefficient

Measures overall inequality:

- **0.0** = Perfect equality (everyone has the same)
- **1.0** = Perfect inequality (one person has everything)

#### Wealth Concentration

- **Top 10% Share**: Percentage of total wealth held by richest 10%
- **Top 1% Share**: Percentage of total wealth held by richest 1%

### Agent Metrics

#### Agent Survival

- Active agents remaining
- Bankruptcy count
- Survival rate by agent style

#### Wealth Distribution

Real-time histogram showing how wealth is spread across the population.

### Redistribution Metrics (when policies enabled)

- **Total Taxes Collected**: Cumulative amount collected via wealth tax
- **Total UBI Distributed**: Cumulative amount distributed to all agents
- **Safety Net Interventions**: Number of times agents were topped up to minimum floor

These metrics appear in a green-highlighted box when any policy is active.

---

## Technical Implementation

- **Framework**: Python Dash (interactive web application)
- **Visualization**: Plotly (real-time charts)
- **Model Type**: Agent-based simulation
- **Update Frequency**: 100ms (10 updates/second)
- **Simulation Speed**: 1-1000 rounds per update

---

**TL;DR**: Start everyone equal, flip slightly biased coins repeatedly → 1% owns everything. **BUT**: Can policy interventions prevent this outcome? Experiment to find out!
