from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Union
import random

class WrestlingStyle(Enum):
    POWERHOUSE = "Powerhouse"
    TECHNICAL = "Technical"
    HIGH_FLYER = "High Flyer"
    BRAWLER = "Brawler"
    SHOWMAN = "Showman"
    SUBMISSION = "Submission"

class MatchType(Enum):
    SINGLES = "Singles Match"
    TAG_TEAM = "Tag Team Match"
    TRIPLE_THREAT = "Triple Threat"
    FATAL_FOUR_WAY = "Fatal Four-Way"
    HARDCORE = "Hardcore Match"
    CAGE_MATCH = "Steel Cage Match"
    LADDER_MATCH = "Ladder Match"

class Psychology(Enum):
    AGGRESSIVE = "Aggressive"
    METHODICAL = "Methodical"
    OPPORTUNISTIC = "Opportunistic"
    RESILIENT = "Resilient"
    SHOWBOAT = "Showboat"

@dataclass
class WrestlingStats:
    # Physical Attributes
    strength: int = 0        # Raw power and lifting ability
    agility: int = 0        # Speed and acrobatic capability
    endurance: int = 0      # Stamina and ability to take punishment
    technique: int = 0      # Technical wrestling skill
    charisma: int = 0       # Crowd connection and mic skills
    
    # Performance Metrics
    momentum: int = 0       # Current match momentum
    fatigue: int = 0        # Accumulated tiredness
    injury: int = 0         # Current injury level
    
    # Career Stats
    experience: int = 0     # Career length and knowledge
    popularity: int = 0     # Fan support level
    
    def is_valid(self) -> bool:
        """Check if stats are within valid ranges."""
        base_stats = [self.strength, self.agility, self.endurance, 
                     self.technique, self.charisma]
        return all(0 <= stat <= 100 for stat in base_stats)

@dataclass
class Move:
    name: str
    description: str
    damage: int
    stamina_cost: int
    type: str  # Strike, Grapple, Aerial, Submission
    requirements: Dict[str, int] = field(default_factory=dict)
    effects: List[str] = field(default_factory=list)
    success_rate: int = 80  # Base success rate percentage
    
    def can_perform(self, wrestler: 'Wrestler') -> bool:
        """Check if a wrestler can perform this move based on requirements."""
        for stat, value in self.requirements.items():
            if getattr(wrestler.stats, stat, 0) < value:
                return False
        return wrestler.stats.fatigue <= 100 - self.stamina_cost

@dataclass
class Wrestler:
    # Basic Info
    name: str
    style: WrestlingStyle
    psychology: Psychology
    stats: WrestlingStats
    
    # Moveset
    signature_moves: List[Move]
    finisher: Move
    regular_moves: List[Move] = field(default_factory=list)
    
    # Match State
    is_legal: bool = True  # For tag team matches
    current_momentum: int = 50
    
    def choose_move(self, opponent: 'Wrestler', match_context: Dict) -> Move:
        """AI logic to choose the next move based on match situation."""
        available_moves = [move for move in self.regular_moves + self.signature_moves 
                         if move.can_perform(self)]
        
        if self.current_momentum >= 80 and self.finisher.can_perform(self):
            # Consider using finisher when momentum is high
            if random.random() < 0.7:  # 70% chance to attempt finisher
                return self.finisher
        
        # Filter moves based on wrestler's psychology
        if self.psychology == Psychology.AGGRESSIVE:
            # Prefer high damage moves
            available_moves.sort(key=lambda m: m.damage, reverse=True)
        elif self.psychology == Psychology.METHODICAL:
            # Prefer moves with lower stamina cost
            available_moves.sort(key=lambda m: m.stamina_cost)
        
        # Return a random move from the top 3 preferred moves
        return random.choice(available_moves[:3] if len(available_moves) > 3 else available_moves)

    def apply_move_effects(self, move: Move, success: bool):
        """Apply the effects of a move on the wrestler."""
        self.stats.fatigue += move.stamina_cost
        if success:
            self.current_momentum += 10
        else:
            self.current_momentum -= 5
        
        # Ensure values stay within bounds
        self.stats.fatigue = min(100, max(0, self.stats.fatigue))
        self.current_momentum = min(100, max(0, self.current_momentum))

@dataclass
class MatchState:
    match_type: MatchType
    participants: List[Wrestler]
    current_round: int = 1
    max_rounds: int = 20
    match_momentum: Dict[str, int] = field(default_factory=dict)
    special_conditions: List[str] = field(default_factory=list)
    
    def initialize_match(self):
        """Set up the initial match state."""
        self.match_momentum = {w.name: 50 for w in self.participants}
        for wrestler in self.participants:
            wrestler.current_momentum = 50
            wrestler.stats.fatigue = 0
    
    def is_match_over(self) -> bool:
        """Determine if the match should end."""
        # Check if max rounds reached
        if self.current_round >= self.max_rounds:
            return True
            
        # Check if any wrestler has achieved victory conditions
        for wrestler in self.participants:
            if wrestler.current_momentum >= 100:
                return True
                
        return False

    def update_match_state(self, attacker: Wrestler, defender: Wrestler, move: Move, success: bool):
        """Update the match state after a move is performed."""
        self.current_round += 1
        
        # Update momentum and fatigue
        attacker.apply_move_effects(move, success)
        if success:
            defender.current_momentum -= move.damage
            defender.stats.fatigue += move.damage // 2
        
        # Update match momentum dictionary
        self.match_momentum[attacker.name] = attacker.current_momentum
        self.match_momentum[defender.name] = defender.current_momentum 