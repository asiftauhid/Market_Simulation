import numpy as np
from dataclasses import dataclass
from typing import Literal, List, Tuple
from enum import Enum

class AgentStyle(Enum):
    GREEDY = "greedy"
    NEUTRAL = "neutral"
    CONTRARIAN = "contrarian"

@dataclass
class Agent:
    """Individual agent in wealth exchange model"""
    id: int
    style: AgentStyle
    wealth: float
    active: bool = True
    
    def get_risk_percentage(self) -> float:
        """Get percentage of wealth agent is willing to stake based on style"""
        if self.style == AgentStyle.GREEDY:
            return 0.30  # 30% stake
        elif self.style == AgentStyle.NEUTRAL:
            return 0.20  # 20% stake
        else:  # CONTRARIAN
            return 0.10  # 10% stake


class WealthInequalitySimulation:
    """Wealth inequality emergence simulation - yard-sale model"""
    
    def __init__(
        self,
        n_agents: int = 100,
        initial_wealth: float = 100.0,
        greedy_ratio: float = 0.33,
        neutral_ratio: float = 0.33,
        rich_bias: float = 0.05,  # Rich get richer advantage
        min_wealth: float = 0.1,
        # Redistribution policies
        wealth_tax_enabled: bool = False,
        wealth_tax_threshold: float = 0.10,  # Tax top 10%
        wealth_tax_rate: float = 0.02,  # 2% tax per round
        ubi_enabled: bool = False,
        ubi_amount: float = 1.0,  # Fixed amount per agent per round
        safety_net_enabled: bool = False,
        safety_net_floor: float = 10.0,  # Minimum wealth floor
    ):
        self.n_agents = n_agents
        self.initial_wealth = initial_wealth
        self.greedy_ratio = greedy_ratio
        self.neutral_ratio = neutral_ratio
        self.contrarian_ratio = 1.0 - greedy_ratio - neutral_ratio
        self.rich_bias = rich_bias
        self.min_wealth = min_wealth
        
        # Redistribution policies
        self.wealth_tax_enabled = wealth_tax_enabled
        self.wealth_tax_threshold = wealth_tax_threshold
        self.wealth_tax_rate = wealth_tax_rate
        self.ubi_enabled = ubi_enabled
        self.ubi_amount = ubi_amount
        self.safety_net_enabled = safety_net_enabled
        self.safety_net_floor = safety_net_floor
        
        # Initialize
        self.agents: List[Agent] = []
        self.wealth_history: List[List[float]] = []
        self.gini_history: List[float] = []
        self.active_count_history: List[int] = []
        self.top_10_percent_history: List[float] = []
        self.top_1_percent_history: List[float] = []
        self.current_round = 0
        
        # Redistribution tracking
        self.total_taxes_collected: float = 0.0
        self.total_ubi_distributed: float = 0.0
        self.safety_net_interventions: int = 0
        
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Create initial agent population - everyone starts equal"""
        for agent_id in range(self.n_agents):
            style = self._random_style()
            self.agents.append(Agent(
                id=agent_id,
                style=style,
                wealth=self.initial_wealth,
                active=True
            ))
    
    def _random_style(self) -> AgentStyle:
        """Randomly assign agent style based on ratios"""
        rand = np.random.random()
        if rand < self.greedy_ratio:
            return AgentStyle.GREEDY
        elif rand < self.greedy_ratio + self.neutral_ratio:
            return AgentStyle.NEUTRAL
        else:
            return AgentStyle.CONTRARIAN
    
    def reset(self):
        """Reset simulation to initial state"""
        self.agents: List[Agent] = []
        self.wealth_history: List[List[float]] = []
        self.gini_history: List[float] = []
        self.active_count_history: List[int] = []
        self.top_10_percent_history: List[float] = []
        self.top_1_percent_history: List[float] = []
        self.current_round = 0
        
        # Redistribution tracking
        self.total_taxes_collected = 0.0
        self.total_ubi_distributed = 0.0
        self.safety_net_interventions = 0
        
        self._initialize_agents()
        
        # Record initial state
        self._record_statistics()
    
    def _check_bankruptcy(self, agent: Agent):
        """Check if agent should be marked as bankrupt"""
        if agent.active and agent.wealth < self.min_wealth:
            agent.wealth = 0
            agent.active = False
    
    def _apply_wealth_tax(self):
        """Apply wealth tax to top X% of agents"""
        if not self.wealth_tax_enabled:
            return 0.0
        
        active_agents = [a for a in self.agents if a.active]
        if len(active_agents) == 0:
            return 0.0
        
        # Sort by wealth
        sorted_agents = sorted(active_agents, key=lambda a: a.wealth, reverse=True)
        
        # Determine how many agents to tax
        n_to_tax = max(1, int(len(sorted_agents) * self.wealth_tax_threshold))
        agents_to_tax = sorted_agents[:n_to_tax]
        
        # Collect taxes
        total_collected = 0.0
        for agent in agents_to_tax:
            tax_amount = agent.wealth * self.wealth_tax_rate
            agent.wealth -= tax_amount
            total_collected += tax_amount
        
        return total_collected
    
    def _distribute_ubi(self, tax_revenue: float = 0.0):
        """Distribute UBI to all active agents"""
        if not self.ubi_enabled:
            return 0.0
        
        active_agents = [a for a in self.agents if a.active]
        if len(active_agents) == 0:
            return 0.0
        
        # Calculate UBI amount (either fixed or from tax revenue)
        ubi_per_agent = self.ubi_amount
        
        # Optionally, can use tax revenue to fund UBI
        # ubi_per_agent = tax_revenue / len(active_agents) if tax_revenue > 0 else self.ubi_amount
        
        total_distributed = 0.0
        for agent in active_agents:
            agent.wealth += ubi_per_agent
            total_distributed += ubi_per_agent
        
        return total_distributed
    
    def _apply_safety_net(self):
        """Ensure no agent falls below safety net floor"""
        if not self.safety_net_enabled:
            return 0
        
        interventions = 0
        for agent in self.agents:
            if agent.active and agent.wealth < self.safety_net_floor:
                agent.wealth = self.safety_net_floor
                interventions += 1
        
        return interventions
    
    def _wealth_exchange(self, agent_a: Agent, agent_b: Agent):
        """
        Execute wealth exchange between two agents
        """
        # Get each agent's stake willingness
        stake_a = agent_a.get_risk_percentage() * agent_a.wealth
        stake_b = agent_b.get_risk_percentage() * agent_b.wealth
        
        # Actual stake is minimum of the two
        stake = min(stake_a, stake_b)
        
        if stake < 0.001:  # Too small, skip (lowered from 0.01 to allow low-wealth exchanges)
            return
        
        # Determine who is richer
        if agent_a.wealth > agent_b.wealth:
            rich_agent = agent_a
            poor_agent = agent_b
        else:
            rich_agent = agent_b
            poor_agent = agent_a
        
        # Rich-get-richer: richer agent has advantage
        win_prob_rich = 0.5 + self.rich_bias
        
        # Determine winner
        if np.random.random() < win_prob_rich:
            winner = rich_agent
            loser = poor_agent
        else:
            winner = poor_agent
            loser = rich_agent
        
        # Transfer wealth
        winner.wealth += stake
        loser.wealth -= stake
        
        # Check for bankruptcy
        self._check_bankruptcy(loser)
    
    def _calculate_gini(self, wealths: List[float]) -> float:
        """Calculate Gini coefficient"""
        if len(wealths) == 0:
            return 0.0
        
        wealths = np.array(sorted(wealths))
        n = len(wealths)
        
        if wealths.sum() == 0:
            return 0.0
        
        index = np.arange(1, n + 1)
        gini = (2 * np.sum(index * wealths)) / (n * wealths.sum()) - (n + 1) / n
        return gini
    
    def _calculate_top_wealth_share(self, wealths: List[float], top_percent: float) -> float:
        """Calculate what % of total wealth is owned by top X%"""
        if len(wealths) == 0:
            return 0.0
        
        total_wealth = sum(wealths)
        if total_wealth == 0:
            return 0.0
        
        sorted_wealths = sorted(wealths, reverse=True)
        n_top = max(1, int(len(wealths) * top_percent))
        top_wealth = sum(sorted_wealths[:n_top])
        
        return (top_wealth / total_wealth) * 100
    
    def _record_statistics(self):
        """Record current statistics"""
        active_agents = [a for a in self.agents if a.active]
        wealths = [a.wealth for a in active_agents]
        
        self.wealth_history.append(wealths.copy())
        self.active_count_history.append(len(active_agents))
        
        if len(wealths) > 0:
            gini = self._calculate_gini(wealths)
            self.gini_history.append(gini)
            
            top_10 = self._calculate_top_wealth_share(wealths, 0.10)
            self.top_10_percent_history.append(top_10)
            
            top_1 = self._calculate_top_wealth_share(wealths, 0.01)
            self.top_1_percent_history.append(top_1)
        else:
            self.gini_history.append(0.0)
            self.top_10_percent_history.append(0.0)
            self.top_1_percent_history.append(0.0)
    
    def step(self) -> bool:
        """Run one round of simulation. Returns True if simulation can continue."""
        # Get active agents
        active_agents = [a for a in self.agents if a.active]
        
        if len(active_agents) < 2:
            return False
        
        # Randomly select two distinct agents
        agent_a, agent_b = np.random.choice(active_agents, size=2, replace=False)
        
        # Execute wealth exchange
        self._wealth_exchange(agent_a, agent_b)
        
        # Apply redistribution policies
        taxes = self._apply_wealth_tax()
        self.total_taxes_collected += taxes
        
        ubi_distributed = self._distribute_ubi(taxes)
        self.total_ubi_distributed += ubi_distributed
        
        interventions = self._apply_safety_net()
        self.safety_net_interventions += interventions
        
        # Record statistics
        self._record_statistics()
        
        self.current_round += 1
        return True
    
    def get_current_results(self) -> dict:
        """Get current simulation results"""
        active_agents = [a for a in self.agents if a.active]
        
        # Group by style
        results_by_style = {}
        for style in AgentStyle:
            agents_of_style = [a for a in self.agents if a.style == style]
            active_of_style = [a for a in agents_of_style if a.active]
            
            if len(agents_of_style) > 0:
                survival_rate = len(active_of_style) / len(agents_of_style)
                avg_wealth = np.mean([a.wealth for a in active_of_style]) if active_of_style else 0
            else:
                survival_rate = 0
                avg_wealth = 0
            
            results_by_style[style.value] = {
                'total': len(agents_of_style),
                'active': len(active_of_style),
                'survival_rate': survival_rate,
                'avg_wealth': avg_wealth
            }
        
        # Current wealth distribution
        current_wealths = [a.wealth for a in active_agents]
        
        return {
            'gini_history': self.gini_history,
            'wealth_history': self.wealth_history,
            'active_count_history': self.active_count_history,
            'top_10_percent_history': self.top_10_percent_history,
            'top_1_percent_history': self.top_1_percent_history,
            'results_by_style': results_by_style,
            'current_wealths': current_wealths,
            'agents': self.agents,
            'n_rounds_completed': self.current_round,
            'bankrupt_count': len([a for a in self.agents if not a.active]),
            'total_taxes_collected': self.total_taxes_collected,
            'total_ubi_distributed': self.total_ubi_distributed,
            'safety_net_interventions': self.safety_net_interventions,
        }

