from typing import List, Dict, Tuple, Optional
import random
from ..core.mechanics import Wrestler, Move, MatchState, MatchType

class MatchEngine:
    def __init__(self, match_state: MatchState):
        self.match_state = match_state
        self.commentary: List[str] = []
        self.match_highlights: List[Dict] = []
    
    def simulate_round(self) -> Tuple[bool, Optional[Wrestler]]:
        """Simulate one round of the match."""
        # Determine who has control
        active_wrestlers = [w for w in self.match_state.participants if w.is_legal]
        if len(active_wrestlers) < 2:
            return True, active_wrestlers[0] if active_wrestlers else None
            
        # Select wrestlers for this exchange
        attacker = self._select_attacker(active_wrestlers)
        defender = self._select_defender(active_wrestlers, attacker)
        
        # Choose and execute move
        move = attacker.choose_move(defender, {
            'round': self.match_state.current_round,
            'momentum': self.match_state.match_momentum,
            'special_conditions': self.match_state.special_conditions
        })
        
        success = self._resolve_move(attacker, defender, move)
        
        # Update match state
        self.match_state.update_match_state(attacker, defender, move, success)
        
        # Generate commentary
        self._generate_commentary(attacker, defender, move, success)
        
        # Check for match end
        if self.match_state.is_match_over():
            winner = max(active_wrestlers, key=lambda w: w.current_momentum)
            return True, winner
            
        return False, None
    
    def _select_attacker(self, active_wrestlers: List[Wrestler]) -> Wrestler:
        """Select which wrestler will attempt a move."""
        # Weight selection by current momentum
        weights = [w.current_momentum for w in active_wrestlers]
        return random.choices(active_wrestlers, weights=weights, k=1)[0]
    
    def _select_defender(self, active_wrestlers: List[Wrestler], attacker: Wrestler) -> Wrestler:
        """Select which wrestler will defend against the move."""
        defenders = [w for w in active_wrestlers if w != attacker]
        return random.choice(defenders)
    
    def _resolve_move(self, attacker: Wrestler, defender: Wrestler, move: Move) -> bool:
        """Determine if a move succeeds or fails."""
        base_chance = move.success_rate
        
        # Modify success chance based on stats and conditions
        modifiers = [
            (attacker.stats.technique - defender.stats.technique) * 2,  # Technical difference
            -attacker.stats.fatigue // 10,  # Fatigue penalty
            (attacker.current_momentum - defender.current_momentum) // 10  # Momentum advantage
        ]
        
        final_chance = base_chance + sum(modifiers)
        final_chance = min(95, max(5, final_chance))  # Keep between 5% and 95%
        
        return random.randint(1, 100) <= final_chance
    
    def _generate_commentary(self, attacker: Wrestler, defender: Wrestler, move: Move, success: bool):
        """Generate commentary for the current action."""
        if success:
            if move == attacker.finisher:
                comment = f"{attacker.name} hits their finisher, {move.name}! This could be it!"
            elif move in attacker.signature_moves:
                comment = f"{attacker.name} connects with their signature {move.name}!"
            else:
                comment = f"{attacker.name} successfully performs {move.name} on {defender.name}."
        else:
            comment = f"{defender.name} manages to counter {attacker.name}'s attempt at {move.name}!"
        
        self.commentary.append(comment)
        
        # Add to highlights if it's a significant moment
        if move == attacker.finisher or move in attacker.signature_moves or not success:
            self.match_highlights.append({
                'round': self.match_state.current_round,
                'attacker': attacker.name,
                'defender': defender.name,
                'move': move.name,
                'success': success,
                'commentary': comment
            })
    
    def simulate_match(self) -> Dict:
        """Simulate the entire match from start to finish."""
        self.match_state.initialize_match()
        
        while True:
            is_finished, winner = self.simulate_round()
            if is_finished:
                break
        
        return {
            'winner': winner.name if winner else None,
            'rounds': self.match_state.current_round,
            'highlights': self.match_highlights,
            'commentary': self.commentary,
            'final_momentum': self.match_state.match_momentum
        } 