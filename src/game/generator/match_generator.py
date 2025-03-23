from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
from .character_generator import WWWCharacter, Alignment
from datetime import timedelta

class MatchType(Enum):
    """Types of matches available"""
    SINGLES = "Singles Match"
    TAG_TEAM = "Tag Team Match"
    TRIPLE_THREAT = "Triple Threat Match"
    FATAL_FOUR_WAY = "Fatal Four-Way Match"
    SIX_MAN_TAG = "Six-Man Tag Team Match"
    BATTLE_ROYAL = "Battle Royal"
    TOURNAMENT = "Tournament Match"
    
class MatchStipulation(Enum):
    """Special match stipulations"""
    NORMAL = "Normal Rules"
    NO_DQ = "No Disqualification"
    FALLS_COUNT_ANYWHERE = "Falls Count Anywhere"
    LADDER = "Ladder Match"
    CAGE = "Steel Cage Match"
    SUBMISSION = "Submission Match"
    IRON_MAN = "Iron Man Match"
    LAST_MAN_STANDING = "Last Man Standing"
    
@dataclass
class MatchParticipant:
    """Represents a wrestler or team in a match"""
    wrestler: WWWCharacter
    team_name: Optional[str] = None
    is_champion: bool = False
    
@dataclass
class Match:
    """Represents a complete match"""
    match_type: MatchType
    stipulation: MatchStipulation
    participants: List[MatchParticipant]
    championship: Optional[str] = None
    duration: timedelta = timedelta(minutes=15)
    story_description: str = ""
    
class StorylineType(Enum):
    """Types of storylines"""
    RIVALRY = "Personal Rivalry"
    CHAMPIONSHIP = "Championship Pursuit"
    BETRAYAL = "Tag Team Betrayal"
    REDEMPTION = "Redemption Arc"
    INVASION = "Invasion Angle"
    TOURNAMENT = "Tournament Story"
    
@dataclass
class Storyline:
    """Tracks an ongoing storyline"""
    storyline_type: StorylineType
    participants: List[WWWCharacter]
    description: str
    start_date: datetime
    planned_duration_weeks: int
    heat_level: int = 0  # -5 to +5
    resolution: Optional[str] = None

class MatchGenerator:
    """Generates matches and storylines"""
    
    @staticmethod
    def generate_match_duration(match_type: MatchType, is_ppv: bool) -> timedelta:
        """Generate appropriate match duration"""
        base_times = {
            MatchType.SINGLES: (10, 15),
            MatchType.TAG_TEAM: (12, 18),
            MatchType.TRIPLE_THREAT: (15, 20),
            MatchType.FATAL_FOUR_WAY: (15, 25),
            MatchType.SIX_MAN_TAG: (15, 25),
            MatchType.BATTLE_ROYAL: (20, 30),
            MatchType.TOURNAMENT: (15, 25)
        }
        
        min_time, max_time = base_times[match_type]
        if is_ppv:
            min_time += 5
            max_time += 10
            
        minutes = random.randint(min_time, max_time)
        return timedelta(minutes=minutes)
    
    @staticmethod
    def select_stipulation(participants: List[MatchParticipant], storyline: Optional[Storyline] = None) -> MatchStipulation:
        """Select appropriate stipulation based on participants and storyline"""
        if not storyline:
            return MatchStipulation.NORMAL
            
        # Map storyline types to likely stipulations
        stipulation_map = {
            StorylineType.RIVALRY: [
                MatchStipulation.NO_DQ,
                MatchStipulation.LAST_MAN_STANDING,
                MatchStipulation.CAGE
            ],
            StorylineType.CHAMPIONSHIP: [
                MatchStipulation.NORMAL,
                MatchStipulation.IRON_MAN,
                MatchStipulation.LADDER
            ],
            StorylineType.BETRAYAL: [
                MatchStipulation.CAGE,
                MatchStipulation.NO_DQ,
                MatchStipulation.FALLS_COUNT_ANYWHERE
            ]
        }
        
        possible_stipulations = stipulation_map.get(storyline.storyline_type, [MatchStipulation.NORMAL])
        return random.choice(possible_stipulations)
    
    @classmethod
    def generate_match(cls, 
                      available_roster: List[WWWCharacter],
                      match_type: Optional[MatchType] = None,
                      championship: Optional[str] = None,
                      storyline: Optional[Storyline] = None,
                      is_ppv: bool = False) -> Match:
        """Generate a complete match"""
        if not match_type:
            match_type = random.choice(list(MatchType))
            
        # Determine number of participants needed
        participants_needed = {
            MatchType.SINGLES: 2,
            MatchType.TAG_TEAM: 4,
            MatchType.TRIPLE_THREAT: 3,
            MatchType.FATAL_FOUR_WAY: 4,
            MatchType.SIX_MAN_TAG: 6,
            MatchType.BATTLE_ROYAL: 8,
            MatchType.TOURNAMENT: 2
        }[match_type]
        
        # Select participants (prioritize storyline participants if available)
        selected_participants = []
        if storyline:
            storyline_wrestlers = storyline.participants[:participants_needed]
            selected_participants = [MatchParticipant(w) for w in storyline_wrestlers]
            
        # Fill remaining spots
        while len(selected_participants) < participants_needed:
            wrestler = random.choice(available_roster)
            if wrestler not in [p.wrestler for p in selected_participants]:
                selected_participants.append(MatchParticipant(wrestler))
        
        # Generate match details
        stipulation = cls.select_stipulation(selected_participants, storyline)
        duration = cls.generate_match_duration(match_type, is_ppv)
        
        # Generate story description
        story = ""
        if storyline:
            story = f"Part of the {storyline.description} storyline"
        
        return Match(
            match_type=match_type,
            stipulation=stipulation,
            participants=selected_participants,
            championship=championship,
            duration=duration,
            story_description=story
        )
    
    @classmethod
    def generate_card(cls,
                     roster: List[WWWCharacter],
                     championships: List[str],
                     active_storylines: List[Storyline],
                     is_ppv: bool) -> List[Match]:
        """Generate a full card of matches"""
        card = []
        used_wrestlers = set()
        
        # Championship matches first
        for title in championships:
            if is_ppv or random.random() < 0.2:  # 20% chance of title match on TV
                available = [w for w in roster if w not in used_wrestlers]
                match = cls.generate_match(
                    available_roster=available,
                    championship=title,
                    is_ppv=is_ppv
                )
                card.append(match)
                used_wrestlers.update([p.wrestler for p in match.participants])
        
        # Storyline matches next
        for storyline in active_storylines:
            if all(w not in used_wrestlers for w in storyline.participants):
                available = [w for w in roster if w not in used_wrestlers]
                match = cls.generate_match(
                    available_roster=available,
                    storyline=storyline,
                    is_ppv=is_ppv
                )
                card.append(match)
                used_wrestlers.update([p.wrestler for p in match.participants])
        
        # Fill remaining card with regular matches
        target_matches = 8 if is_ppv else 5
        while len(card) < target_matches:
            available = [w for w in roster if w not in used_wrestlers]
            if len(available) < 2:
                break
                
            match = cls.generate_match(
                available_roster=available,
                is_ppv=is_ppv
            )
            card.append(match)
            used_wrestlers.update([p.wrestler for p in match.participants])
        
        return card 