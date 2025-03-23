from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Tuple
import random

class CareerStage(Enum):
    """Career progression stages"""
    ROOKIE = 1          # Just starting out
    PROSPECT = 2        # Showing promise
    ESTABLISHED = 3     # Reliable performer
    VETERAN = 4         # Seasoned professional
    STAR = 5           # Major draw
    LEGEND = 6         # All-time great

class WrestlingRank(Enum):
    """Wrestling ranks based on fan appeal"""
    LOCAL = 1           # Local/regional scene (max 100 positions)
    REGIONAL = 2       # Local/regional scene (max 100 positions)
    NATIONAL = 3       # National recognition (max 50 positions)
    INTERNATIONAL = 4  # Known internationally (max 25 positions)
    GLOBAL = 5        # Worldwide superstar (max 10 positions)
    ICON = 6          # Transcendent megastar (max 3 positions)

class SubSkill(Enum):
    """Sub-skills that are influenced by core stats"""
    
    # BODY-based skills (Physical capabilities)
    POWER = auto()           # Raw strength for power moves
    AGILITY = auto()         # Speed and acrobatic ability
    STAMINA = auto()         # Match endurance and cardio
    TOUGHNESS = auto()       # Ability to take physical punishment
    STRIKING = auto()        # Strike execution and impact
    
    # LOOK-based skills (Presentation and charisma)
    PRESENCE = auto()        # Command attention and aura
    CHARISMA = auto()        # Natural charm and connection
    ACTING = auto()          # Facial expressions and body language
    
    # REAL-based skills (Authenticity and adaptation)
    SHOOT = auto()           # Legitimate fighting ability/presentation
    IMPROVISATION = auto()   # Adapting to unexpected situations
    CROWD_READING = auto()   # Understanding audience reactions
    TIMING = auto()          # Knowing when to do what
    RING_AWARENESS = auto()  # Spatial awareness and positioning
    
    # WORK-based skills (Wrestling ability)
    TECHNICAL = auto()       # Pure wrestling execution
    SELLING = auto()         # Making moves look impactful
    PSYCHOLOGY = auto()      # Match story progression
    SPOTS = auto()           # Creating memorable moments
    SAFETY = auto()          # Protecting self and opponent
    CALLING = auto()         # Match coordination
    
    # FIRE-based skills (Heart and intensity)
    INTENSITY = auto()       # Emotional investment
    RESILIENCE = auto()      # Fighting through adversity
    COMEBACK = auto()        # Rallying when down

# Map sub-skills to their primary stat
SUBSKILL_MAPPING = {
    # BODY sub-skills
    SubSkill.POWER: 'body',
    SubSkill.AGILITY: 'body',
    SubSkill.STAMINA: 'body',
    SubSkill.TOUGHNESS: 'body',
    SubSkill.STRIKING: 'body',
    
    # LOOK sub-skills
    SubSkill.PRESENCE: 'look',
    SubSkill.CHARISMA: 'look',
    SubSkill.ACTING: 'look',
    
    # REAL sub-skills
    SubSkill.SHOOT: 'real',
    SubSkill.IMPROVISATION: 'real',
    SubSkill.CROWD_READING: 'real',
    SubSkill.TIMING: 'real',
    SubSkill.RING_AWARENESS: 'real',
    
    # WORK sub-skills
    SubSkill.TECHNICAL: 'work',
    SubSkill.SELLING: 'work',
    SubSkill.PSYCHOLOGY: 'work',
    SubSkill.SPOTS: 'work',
    SubSkill.SAFETY: 'work',
    SubSkill.CALLING: 'work',
    
    # FIRE sub-skills
    SubSkill.INTENSITY: 'fire',
    SubSkill.RESILIENCE: 'fire',
    SubSkill.COMEBACK: 'fire'
}

@dataclass
class WrestlingStats:
    """Core wrestling statistics and attributes"""
    
    # Core Stats (0-5 range)
    body: int = 2        # Physical strength and athletic ability
    look: int = 2        # "It" factor, charisma, and star power
    real: int = 2        # Breaking kayfabe and working reality into stories
    work: int = 2        # Technical skill and in-ring storytelling
    fire: int = 2        # Mental fortitude, passion, and intensity
    
    # Career Progress
    experience: int = 0   # Total career experience points
    fans: int = 0        # Fan following (determines rank)
    career_stage: CareerStage = CareerStage.ROOKIE  # Current career stage
    rank: WrestlingRank = WrestlingRank.REGIONAL    # Current competition level
    
    # Current Status (0-100 range)
    overness: int = 50    # Current popularity
    momentum: int = 50    # Match momentum
    fatigue: int = 0      # Current tiredness
    damage: int = 0       # Accumulated damage

    # Experience thresholds for career stages
    CAREER_THRESHOLDS = {
        CareerStage.ROOKIE: 0,
        CareerStage.PROSPECT: 1000,
        CareerStage.ESTABLISHED: 3000,
        CareerStage.VETERAN: 6000,
        CareerStage.STAR: 10000,
        CareerStage.LEGEND: 15000
    }

    # Fan thresholds for ranks (based on social media metrics)
    RANK_THRESHOLDS = {
        WrestlingRank.LOCAL: 0,
        WrestlingRank.REGIONAL: 1000,        # Starting point
        WrestlingRank.NATIONAL: 10_000,   # Established national presence
        WrestlingRank.INTERNATIONAL: 100_000,  # Known internationally
        WrestlingRank.GLOBAL: 1_000_000,  # Major worldwide star
        WrestlingRank.ICON: 10_000_000    # Transcendent megastar
    }

    # Maximum positions available per rank
    RANK_POSITION_LIMITS = {
        WrestlingRank.LOCAL: 100,      # Local/regional scene
        WrestlingRank.REGIONAL: 50,       # National recognition
        WrestlingRank.NATIONAL: 25,   # International stars
        WrestlingRank.INTERNATIONAL: 10,         # Global superstars
        WrestlingRank.GLOBAL: 3,             # Legendary status
        WrestlingRank.ICON: 1
    }
    
    def get_core_stats(self) -> Dict[str, int]:
        """Get all core stats."""
        return {
            'body': self.body,
            'look': self.look,
            'real': self.real,
            'work': self.work,
            'fire': self.fire
        }
    
    def get_status_values(self) -> Dict[str, int]:
        """Get all current status values."""
        return {
            'overness': self.overness,
            'momentum': self.momentum,
            'fatigue': self.fatigue,
            'damage': self.damage
        }
    
    def get_progress_values(self) -> Dict[str, str]:
        """Get all progress tracking values."""
        return {
            'career_stage': self.career_stage.name,
            'experience': str(self.experience),
            'fans': str(self.fans),
            'rank': self.rank.name
        }
    
    def calculate_overall_rating(self) -> int:
        """Calculate wrestler's overall rating based on core stats."""
        # Weights for each core stat
        weights = {
            'body': 1.0,
            'look': 1.2,
            'real': 0.8,
            'work': 1.2,
            'fire': 1.1
        }
        
        # Calculate weighted sum
        weighted_sum = sum(getattr(self, stat) * weight 
                         for stat, weight in weights.items())
        
        # Convert from 0-5 scale to 0-100 scale
        max_possible = sum(5 * weight for weight in weights.values())
        return int((weighted_sum / max_possible) * 100)
    
    def is_valid(self) -> bool:
        """Check if all stats are within valid ranges."""
        # Check core stats (0-5 range)
        core_stats_valid = all(0 <= getattr(self, stat) <= 5 
                             for stat in ['body', 'look', 'real', 'work', 'fire'])
        
        # Check status values (0-100 range)
        status_valid = all(0 <= getattr(self, stat) <= 100 
                         for stat in ['overness', 'momentum', 'fatigue', 'damage'])
        
        # Check incremental values (non-negative)
        progress_valid = all(getattr(self, stat) >= 0 
                           for stat in ['experience', 'fans'])
        
        return core_stats_valid and status_valid and progress_valid
    
    def add_experience(self, amount: int) -> bool:
        """Add experience points and check for career stage advancement."""
        self.experience += amount
        
        # Check for career stage advancement
        for stage in reversed(list(CareerStage)):
            if self.experience >= self.CAREER_THRESHOLDS[stage] and stage.value > self.career_stage.value:
                self.career_stage = stage
                return True
        
        return False
    
    def update_fans(self, amount: int) -> bool:
        """
        Update fan count and check for rank changes.
        Returns True if rank changed.
        """
        old_rank = self.rank
        self.fans = max(0, self.fans + amount)  # Can lose fans
        
        # Check for rank changes (up or down)
        for rank in reversed(list(WrestlingRank)):
            if self.fans >= self.RANK_THRESHOLDS[rank]:
                self.rank = rank
                break
        
        # Increase overness based on positive fan gain
        if amount > 0:
            overness_boost = min(5, amount // 1000)  # Max 5 point boost
            self.overness = min(100, self.overness + overness_boost)
        
        return self.rank != old_rank
    
    def update_match_status(self, momentum_change: int, fatigue_change: int, damage_change: int):
        """Update match-related status values."""
        self.momentum = max(0, min(100, self.momentum + momentum_change))
        self.fatigue = max(0, min(100, self.fatigue + fatigue_change))
        self.damage = max(0, min(100, self.damage + damage_change))
    
    def rest(self):
        """Reset match-related status values after match."""
        self.momentum = 50
        self.fatigue = 0
        self.damage = 0
    
    def get_performance_bonus(self) -> float:
        """Calculate performance multiplier based on current stats."""
        # Base multiplier starts at 1.0
        multiplier = 1.0
        
        # Add bonuses based on core stats
        if self.work >= 15: multiplier += 0.2
        if self.look >= 15: multiplier += 0.15
        if self.fire >= 15: multiplier += 0.2  # High fire helps push through fatigue/damage
        
        # Reduced penalties for high fire
        fatigue_threshold = 85 if self.fire >= 15 else 75
        damage_threshold = 85 if self.fire >= 15 else 75
        
        # Penalty for high fatigue/damage
        if self.fatigue >= fatigue_threshold: multiplier -= 0.1
        if self.damage >= damage_threshold: multiplier -= 0.15
        
        return max(0.5, multiplier)  # Minimum 0.5x multiplier

    def get_subskill_bonus(self, subskill: SubSkill) -> int:
        """Calculate bonus for a specific sub-skill based on core stat."""
        core_stat = SUBSKILL_MAPPING[subskill]
        stat_value = getattr(self, core_stat)
        
        # Convert 0-5 stat to -2 to +2 bonus range
        return stat_value - 2

    def skill_check(self, subskill: SubSkill, difficulty: int = 10) -> Tuple[bool, int]:
        """
        Perform a skill check for a specific sub-skill.
        Returns (success, margin) where margin is how much the check succeeded/failed by.
        
        difficulty ranges:
        5-9: Easy (basic moves, simple promos)
        10-14: Medium (signature spots, good promos)
        15-19: Hard (complex sequences, great promos)
        20+: Legendary (career-defining moments)
        """
        # Roll d20
        roll = random.randint(1, 20)
        
        # Get stat bonus
        bonus = self.get_subskill_bonus(subskill)
        
        # Calculate total
        total = roll + bonus
        
        # Calculate success and margin
        success = total >= difficulty
        margin = total - difficulty
        
        return success, margin

    def get_subskills_by_stat(self, stat: str) -> List[SubSkill]:
        """Get all sub-skills associated with a core stat."""
        return [skill for skill, stat_name in SUBSKILL_MAPPING.items() 
                if stat_name == stat]

    def get_all_subskill_bonuses(self) -> Dict[SubSkill, int]:
        """Get bonuses for all sub-skills."""
        return {skill: self.get_subskill_bonus(skill) 
                for skill in SubSkill}

    def perform_promo(self) -> Tuple[int, List[str]]:
        """
        Simulate a promo performance using relevant sub-skills.
        Returns (quality, highlights) where quality is 0-100 and highlights are notable moments.
        """
        highlights = []
        base_score = 50
        
        # Check charisma
        success, margin = self.skill_check(SubSkill.CHARISMA, 12)
        if success:
            base_score += margin * 2
            if margin > 5:
                highlights.append("Connected with the crowd")
        
        # Check acting ability
        success, margin = self.skill_check(SubSkill.ACTING, 12)
        if success:
            base_score += margin * 2
            if margin > 5:
                highlights.append("Delivered a captivating performance")
        
        # Check intensity
        success, margin = self.skill_check(SubSkill.INTENSITY, 10)
        if success:
            base_score += margin
            if margin > 5:
                highlights.append("Showed intense emotion")
        
        # Check improvisation if needed
        if random.random() < 0.3:  # 30% chance of needing to improvise
            success, margin = self.skill_check(SubSkill.IMPROVISATION, 12)
            if success:
                base_score += margin * 1.5
                if margin > 5:
                    highlights.append("Handled unexpected moment perfectly")
            else:
                base_score -= abs(margin)
                if margin < -5:
                    highlights.append("Struggled with unexpected moment")
        
        return min(100, max(0, base_score)), highlights

    def perform_match_sequence(self, difficulty: int) -> Tuple[bool, List[str]]:
        """
        Attempt a wrestling sequence of given difficulty.
        Returns (success, commentary) where commentary describes what happened.
        """
        commentary = []
        
        # Always check safety first
        safety_success, safety_margin = self.skill_check(SubSkill.SAFETY, difficulty)
        if not safety_success:
            commentary.append("Executed unsafely")
            return False, commentary
        
        # Check technical ability
        tech_success, tech_margin = self.skill_check(SubSkill.TECHNICAL, difficulty)
        if not tech_success:
            commentary.append("Struggled with execution")
            return False, commentary
        
        # Check timing
        timing_success, timing_margin = self.skill_check(SubSkill.TIMING, difficulty - 2)
        if not timing_success:
            commentary.append("Timing was off")
            return False, commentary
        
        # Calculate overall quality
        total_margin = safety_margin + tech_margin + timing_margin
        
        # Add spot quality if it's a signature spot
        if difficulty >= 15:
            spot_success, spot_margin = self.skill_check(SubSkill.SPOTS, difficulty)
            if spot_success:
                total_margin += spot_margin
                if spot_margin > 5:
                    commentary.append("Created a memorable moment")
        
        # Determine overall quality
        if total_margin > 15:
            commentary.append("Executed perfectly")
        elif total_margin > 10:
            commentary.append("Executed excellently")
        elif total_margin > 5:
            commentary.append("Executed well")
        else:
            commentary.append("Completed the sequence")
        
        return True, commentary

    def attempt_comeback(self) -> Tuple[bool, str]:
        """
        Attempt a comeback sequence when in trouble.
        Returns (success, description).
        """
        # Check comeback ability
        success, margin = self.skill_check(SubSkill.COMEBACK, 15)
        
        # Check resilience if damaged
        if self.damage > 50:
            resilience_success, resilience_margin = self.skill_check(SubSkill.RESILIENCE, 12)
            if not resilience_success:
                return False, "Too hurt to mount a comeback"
        
        if success:
            if margin > 10:
                return True, "Incredible comeback that brought the crowd to their feet"
            elif margin > 5:
                return True, "Successfully fought back into the match"
            else:
                return True, "Managed to mount a comeback"
        
        return False, "Unable to turn the tide" 