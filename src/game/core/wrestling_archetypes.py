from enum import Enum, auto
from typing import List, Dict, Optional, Set
from dataclasses import dataclass

class Gender(Enum):
    """Wrestler's gender"""
    MALE = "Male"
    FEMALE = "Female"

class Nationality(Enum):
    """Wrestler's nationality"""
    AMERICAN = "American"
    BRITISH = "British"
    CANADIAN = "Canadian"
    AUSTRALIAN = "Australian"
    NEW_ZEALAND = "New Zealand"
    JAPANESE = "Japanese"
    CHINESE = "Chinese"
    KOREAN = "Korean"
    INDIAN = "Indian"
    PAKISTANI = "Pakistani"
    AFGHAN = "Afghan"
    IRANIAN = "Iranian"

class WrestlingStyle(Enum):
    """Wrestling styles that define how a wrestler performs in the ring."""
    POWERHOUSE = "Powerhouse"         # Strong power moves, slams, and throws
    FIGHTER = "Fighter"               # Legitimate fighting background
    BRAWLER = "Brawler"              # Hard-hitting strikes and street fighting
    HARDCORE = "Hardcore"            # Extreme moves and hardcore wrestling
    CEREBRAL = "Cerebral"            # Psychological warfare and mind games
    TECHNICAL = "Technical"          # Technical wrestling and submissions
    HIGH_FLYER = "High-Flyer"        # Speed, aerial moves, and acrobatics
    SHOWMAN = "Showman"              # Charismatic performance and crowd work

@dataclass
class PhysicalRanges:
    min_height: float  # in inches
    max_height: float
    min_weight: int   # in pounds
    max_weight: int

STYLE_PHYSIQUES = {
    WrestlingStyle.POWERHOUSE: PhysicalRanges(
        min_height=78,  # 6'6"
        max_height=86,  # 7'2"
        min_weight=265,
        max_weight=400
    ),
    WrestlingStyle.FIGHTER: PhysicalRanges(
        min_height=70,  # 5'10"
        max_height=79,  # 6'7"
        min_weight=185,
        max_weight=265
    ),
    WrestlingStyle.BRAWLER: PhysicalRanges(
        min_height=70,  # 5'10"
        max_height=79,  # 6'7"
        min_weight=220,
        max_weight=300
    ),
    WrestlingStyle.HARDCORE: PhysicalRanges(
        min_height=70,  # 5'10"
        max_height=79,  # 6'7"
        min_weight=200,
        max_weight=280
    ),
    WrestlingStyle.CEREBRAL: PhysicalRanges(
        min_height=68,  # 5'8"
        max_height=78,  # 6'6"
        min_weight=200,
        max_weight=275
    ),
    WrestlingStyle.TECHNICAL: PhysicalRanges(
        min_height=68,  # 5'8"
        max_height=78,  # 6'6"
        min_weight=180,
        max_weight=250
    ),
    WrestlingStyle.HIGH_FLYER: PhysicalRanges(
        min_height=66,  # 5'6"
        max_height=72,  # 6'0"
        min_weight=160,
        max_weight=220
    ),
    WrestlingStyle.SHOWMAN: PhysicalRanges(
        min_height=68,  # 5'8"
        max_height=78,  # 6'6"
        min_weight=180,
        max_weight=280
    )
}

# Update style synergies
STYLE_SYNERGIES = {
    (WrestlingStyle.POWERHOUSE, WrestlingStyle.BRAWLER): 0.9,
    (WrestlingStyle.FIGHTER, WrestlingStyle.TECHNICAL): 0.95,
    (WrestlingStyle.FIGHTER, WrestlingStyle.BRAWLER): 0.9,
    (WrestlingStyle.BRAWLER, WrestlingStyle.HARDCORE): 0.95,
    (WrestlingStyle.HARDCORE, WrestlingStyle.HIGH_FLYER): 0.85,
    (WrestlingStyle.CEREBRAL, WrestlingStyle.TECHNICAL): 0.9,
    (WrestlingStyle.TECHNICAL, WrestlingStyle.HIGH_FLYER): 0.85,
    (WrestlingStyle.HIGH_FLYER, WrestlingStyle.SHOWMAN): 0.9,
    (WrestlingStyle.SHOWMAN, WrestlingStyle.CEREBRAL): 0.85,
    (WrestlingStyle.POWERHOUSE, WrestlingStyle.FIGHTER): 0.8,
    (WrestlingStyle.TECHNICAL, WrestlingStyle.CEREBRAL): 0.9,
    (WrestlingStyle.BRAWLER, WrestlingStyle.FIGHTER): 0.9
}

# Update move recommendations
STYLE_MOVES = {
    WrestlingStyle.POWERHOUSE: ["Power Bomb", "Slam", "Press", "Suplex", "Gorilla Press"],
    WrestlingStyle.FIGHTER: ["Strikes", "Submissions", "Takedowns", "MMA-Style Moves", "Legitimate Holds"],
    WrestlingStyle.BRAWLER: ["Clothesline", "Punch", "DDT", "Brawling Strikes", "Street Fighting Moves"],
    WrestlingStyle.HARDCORE: ["Weapon Strikes", "Table Spots", "Extreme Moves", "Chair Shots", "Hardcore Spots"],
    WrestlingStyle.CEREBRAL: ["Mind Games", "Psychological Tactics", "Strategic Moves", "Momentum Shifts", "Counter Wrestling"],
    WrestlingStyle.TECHNICAL: ["Chain Wrestling", "Submission Holds", "Technical Counters", "Mat Wrestling", "Joint Manipulation"],
    WrestlingStyle.HIGH_FLYER: ["Moonsault", "450 Splash", "Hurricanrana", "Diving Attacks", "High-Risk Moves"],
    WrestlingStyle.SHOWMAN: ["Signature Taunts", "Crowd Play", "Flash Moves", "Entertainment Spots", "Dramatic Sequences"]
}

class Gimmick(Enum):
    """Comprehensive list of wrestling gimmicks organized by style restrictions and general categories."""
    
    # POWERHOUSE Style-Locked Gimmicks
    MONSTER = auto()                # Unstoppable monster heel
    STRONGMAN = auto()              # Legitimate strength athlete
    GIANT = auto()                  # Size-based powerhouse
    
    # FIGHTER Style-Locked Gimmicks
    SHOOTER = auto()                # Legitimate fighting background
    PRIZE_FIGHTER = auto()          # Boxing/MMA crossover star
    MARTIAL_ARTIST = auto()         # Traditional martial arts background
    COMBAT_ATHLETE = auto()         # Athletic fighter with combat sports background
    
    # BRAWLER Style-Locked Gimmicks
    STREET_FIGHTER = auto()         # Underground fighting specialist
    BAR_ROOM_BRAWLER = auto()      # Tough bar fighter
    ENFORCER = auto()               # Mob/Gang enforcer type
    
    # HARDCORE Style-Locked Gimmicks
    DEATHMATCH_SPECIALIST = auto()  # Extreme hardcore wrestler
    GARBAGE_WRESTLER = auto()       # Weapons and blood specialist
    SADIST = auto()                 # Pain-loving extremist
    
    # CEREBRAL Style-Locked Gimmicks
    MASTERMIND = auto()             # Strategic genius
    MANIPULATOR = auto()            # Mind games specialist
    SOCIOPATH = auto()              # Sociopathic mastermind
    
    # TECHNICAL Style-Locked Gimmicks
    SUBMISSION_MASTER = auto()      # Submission specialist
    MAT_TECHNICIAN = auto()         # Pure wrestling technician
    CATCH_WRESTLER = auto()         # Old-school catch style

    # HIGH_FLYER Style-Locked Gimmicks
    LUCHA_LIBRE = auto()            # Mexican high-flying style
    DAREDEVIL = auto()              # Risk-taking high flyer
    ACROBAT = auto()                # Gymnastics-based style
    
    # SHOWMAN Style-Locked Gimmicks
    ROCK_STAR = auto()              # Music-based entertainer
    HOLLYWOOD_STAR = auto()         # Movie star personality
    PEACOCK = auto()                # Flamboyant showoff

    # General Gimmicks - Origin Based
    FOREIGN_MENACE = auto()         # Anti-American heel
    PATRIOT = auto()                # Pro-country patriot
    HOMETOWN_HERO = auto()          # Local favorite
    
    # Authority Based
    CORPORATE_BOSS = auto()         # Evil authority figure
    COMMISSIONER = auto()           # Authority position
    PEOPLE_CHAMP = auto()           # Anti-authority peoples champion
    
    # Wealth Based
    MILLION_DOLLAR = auto()         # Rich snob
    BLUE_COLLAR = auto()            # Working class hero
    SELF_MADE = auto()              # Rags to riches story
    
    # Supernatural/Mystical
    DARK_MESSIAH = auto()           # Supernatural evil force
    MYSTIC = auto()                 # Spiritual/mystical character
    CULTIST = auto()                # Cult leader/follower
    
    # Masked/Character
    MASKED_MYSTERY = auto()         # Unknown masked wrestler
    SUPERHERO = auto()              # Comic book style hero
    ANTIHERO = auto()               # Dark vigilante type
    
    # Military/Service
    MARINE = auto()                 # Military background
    FIRST_RESPONDER = auto()        # Police/Fire/EMT
    MERCENARY = auto()              # Soldier of fortune
    
    # Entertainment
    CELEBRITY = auto()              # Famous personality
    INFLUENCER = auto()             # Social media star
    COMEDIAN = auto()               # Comedy specialist
    
    # Personality Based
    NARCISSIST = auto()             # Self-obsessed
    REBEL = auto()                  # Anti-establishment
    PRODIGY = auto()                # Natural talent
    
    # Legacy/Family
    DYNASTY = auto()                # Wrestling family member
    LEGACY = auto()                 # Carrying on tradition
    PROTEGE = auto()                # Mentor's chosen one

    # Modern Culture
    GAMER = auto()                  # Video game culture
    HIPSTER = auto()                # Counter-culture
    TRENDSETTER = auto()            # Fashion/style icon
    
    # Attitude Era Inspired
    PARTY_ANIMAL = auto()           # Fun-loving partier
    STREET_THUG = auto()            # Urban tough guy
    OCCULTIST = auto()              # Dark arts practitioner

@dataclass
class GimmickRestrictions:
    """Restrictions for who can use a gimmick"""
    required_gender: Optional[Gender] = None
    required_style: Optional[WrestlingStyle] = None
    min_alignment: int = -100  # -100 pure heel to 100 pure face
    max_alignment: int = 100
    min_height: Optional[float] = None
    max_height: Optional[float] = None
    min_weight: Optional[int] = None
    max_weight: Optional[int] = None

# Define restrictions for each gimmick
GIMMICK_RESTRICTIONS = {
    # POWERHOUSE style-locked gimmicks
    Gimmick.MONSTER: GimmickRestrictions(
        required_style=WrestlingStyle.POWERHOUSE,
        min_height=76,  # 6'4"
        min_weight=300
    ),
    Gimmick.STRONGMAN: GimmickRestrictions(
        required_style=WrestlingStyle.POWERHOUSE,
        min_height=74,  # 6'2"
        min_weight=265
    ),
    Gimmick.GIANT: GimmickRestrictions(
        required_style=WrestlingStyle.POWERHOUSE,
        min_height=80,  # 6'8"
        min_weight=320
    ),
    
    # FIGHTER style-locked gimmicks
    Gimmick.SHOOTER: GimmickRestrictions(
        required_style=WrestlingStyle.FIGHTER
    ),
    Gimmick.PRIZE_FIGHTER: GimmickRestrictions(
        required_style=WrestlingStyle.FIGHTER
    ),
    Gimmick.COMBAT_ATHLETE: GimmickRestrictions(
        required_style=WrestlingStyle.FIGHTER
    ),
    
    # BRAWLER style-locked gimmicks
    Gimmick.STREET_FIGHTER: GimmickRestrictions(
        required_style=WrestlingStyle.BRAWLER
    ),
    Gimmick.BAR_ROOM_BRAWLER: GimmickRestrictions(
        required_style=WrestlingStyle.BRAWLER
    ),
    Gimmick.ENFORCER: GimmickRestrictions(
        required_style=WrestlingStyle.BRAWLER
    ),
    
    # HARDCORE style-locked gimmicks
    Gimmick.DEATHMATCH_SPECIALIST: GimmickRestrictions(
        required_style=WrestlingStyle.HARDCORE
    ),
    Gimmick.GARBAGE_WRESTLER: GimmickRestrictions(
        required_style=WrestlingStyle.HARDCORE
    ),
    Gimmick.SADIST: GimmickRestrictions(
        required_style=WrestlingStyle.HARDCORE,
        min_alignment=-100,
        max_alignment=-50
    ),
    
    # CEREBRAL style-locked gimmicks
    Gimmick.MASTERMIND: GimmickRestrictions(
        required_style=WrestlingStyle.CEREBRAL
    ),
    Gimmick.MANIPULATOR: GimmickRestrictions(
        required_style=WrestlingStyle.CEREBRAL,
        min_alignment=-100,
        max_alignment=-50
    ),
    Gimmick.SOCIOPATH: GimmickRestrictions(
        required_style=WrestlingStyle.CEREBRAL
    ),
    
    # TECHNICAL style-locked gimmicks
    Gimmick.SUBMISSION_MASTER: GimmickRestrictions(
        required_style=WrestlingStyle.TECHNICAL
    ),
    Gimmick.MAT_TECHNICIAN: GimmickRestrictions(
        required_style=WrestlingStyle.TECHNICAL
    ),
    Gimmick.CATCH_WRESTLER: GimmickRestrictions(
        required_style=WrestlingStyle.TECHNICAL
    ),
    
    # HIGH_FLYER style-locked gimmicks
    Gimmick.LUCHA_LIBRE: GimmickRestrictions(
        required_style=WrestlingStyle.HIGH_FLYER,
        max_height=72,  # 6'0"
        max_weight=220
    ),
    Gimmick.DAREDEVIL: GimmickRestrictions(
        required_style=WrestlingStyle.HIGH_FLYER,
        max_height=72,  # 6'0"
        max_weight=220
    ),
    Gimmick.ACROBAT: GimmickRestrictions(
        required_style=WrestlingStyle.HIGH_FLYER,
        max_height=72,  # 6'0"
        max_weight=220
    ),
    
    # SHOWMAN style-locked gimmicks
    Gimmick.ROCK_STAR: GimmickRestrictions(
        required_style=WrestlingStyle.SHOWMAN
    ),
    Gimmick.HOLLYWOOD_STAR: GimmickRestrictions(
        required_style=WrestlingStyle.SHOWMAN
    ),
    Gimmick.PEACOCK: GimmickRestrictions(
        required_style=WrestlingStyle.SHOWMAN
    ),
    
    # Alignment-locked gimmicks
    Gimmick.FOREIGN_MENACE: GimmickRestrictions(
        min_alignment=-100,
        max_alignment=-50
    ),
    Gimmick.PATRIOT: GimmickRestrictions(
        min_alignment=50,
        max_alignment=100
    ),
    Gimmick.CORPORATE_BOSS: GimmickRestrictions(
        min_alignment=-100,
        max_alignment=-50
    ),
    Gimmick.PEOPLE_CHAMP: GimmickRestrictions(
        min_alignment=50,
        max_alignment=100
    ),
    Gimmick.BLUE_COLLAR: GimmickRestrictions(
        min_alignment=50,
        max_alignment=100
    ),
    Gimmick.DARK_MESSIAH: GimmickRestrictions(
        min_alignment=-100,
        max_alignment=-50
    ),
    Gimmick.SUPERHERO: GimmickRestrictions(
        min_alignment=50,
        max_alignment=100
    ),
    
    # Physical requirement gimmicks
    Gimmick.MONSTER: GimmickRestrictions(
        min_height=76,  # 6'4"
        min_weight=280
    )
}

@dataclass
class Wrestler:
    """Physical attributes and basic info for a wrestler"""
    name: str
    gender: Gender
    height: float  # in inches
    weight: int    # in pounds
    style: WrestlingStyle
    gimmick: Gimmick
    alignment: int  # -100 to 100

    def can_use_gimmick(self, gimmick: Gimmick) -> bool:
        """Check if this wrestler can use a given gimmick"""
        if gimmick not in GIMMICK_RESTRICTIONS:
            return True
            
        restrictions = GIMMICK_RESTRICTIONS[gimmick]
        
        # Check gender restriction
        if restrictions.required_gender and restrictions.required_gender != self.gender:
            return False
            
        # Check style restriction
        if restrictions.required_style and restrictions.required_style != self.style:
            return False
            
        # Check alignment restriction
        if not (restrictions.min_alignment <= self.alignment <= restrictions.max_alignment):
            return False
            
        # Check physical restrictions
        if restrictions.min_height and self.height < restrictions.min_height:
            return False
        if restrictions.max_height and self.height > restrictions.max_height:
            return False
        if restrictions.min_weight and self.weight < restrictions.min_weight:
            return False
        if restrictions.max_weight and self.weight > restrictions.max_weight:
            return False
            
        return True

@dataclass
class Alignment:
    """Represents a wrestler's alignment on the heel-face spectrum"""
    value: int = 0  # -100 (Pure Heel) to 100 (Pure Face)
    
    @property
    def alignment_type(self) -> str:
        if self.value <= -35:
            return "Heel"
        elif self.value >= 35:
            return "Face"
        else:
            return "Tweener"
    
    def adjust(self, amount: int):
        """Adjust alignment value within bounds"""
        self.value = max(-100, min(100, self.value + amount))

@dataclass
class WrestlingPersona:
    """Complete wrestling character persona."""
    gimmick: 'Gimmick'
    style: WrestlingStyle
    gender: Gender
    alignment: Alignment
    secondary_style: Optional[WrestlingStyle] = None

@dataclass
class WrestlingPersona:
    """Complete wrestling character persona."""
    gimmick: Gimmick
    style: WrestlingStyle
    gender: Gender
    alignment: Alignment
    secondary_style: Optional[WrestlingStyle] = None
    
    def get_style_compatibility(self) -> float:
        """Calculate how well the wrestling styles fit together."""
        if not self.secondary_style:
            return 1.0
            
        # Define style synergies
        synergies = {
            (WrestlingStyle.POWERHOUSE, WrestlingStyle.BRAWLER): 0.9,
            (WrestlingStyle.TECHNICAL, WrestlingStyle.SUBMISSION): 0.95,
            (WrestlingStyle.HIGH_FLYER, WrestlingStyle.LUCHA_LIBRE): 0.95,
            (WrestlingStyle.STRIKER, WrestlingStyle.STRONG_STYLE): 0.9,
            (WrestlingStyle.ALL_ROUNDER, WrestlingStyle.TECHNICAL): 0.85,
            (WrestlingStyle.SHOWMAN, WrestlingStyle.HIGH_FLYER): 0.85,
            (WrestlingStyle.BRAWLER, WrestlingStyle.HARDCORE): 0.9,
        }
        
        # Check both orderings of the styles
        style_pair = (self.style, self.secondary_style)
        reverse_pair = (self.secondary_style, self.style)
        
        return synergies.get(style_pair, 0.7) or synergies.get(reverse_pair, 0.7)
    
    def get_gimmick_style_compatibility(self) -> float:
        """Calculate how well the gimmick fits with the wrestling style."""
        compatibilities = {
            # Physical-based gimmicks
            (Gimmick.MONSTER, WrestlingStyle.POWERHOUSE): 1.0,
            (Gimmick.MONSTER, WrestlingStyle.GIANT): 1.0,
            (Gimmick.SPEEDSTER, WrestlingStyle.HIGH_FLYER): 1.0,
            (Gimmick.SPEEDSTER, WrestlingStyle.LUCHA_LIBRE): 0.95,
            (Gimmick.TECHNICIAN, WrestlingStyle.TECHNICAL): 1.0,
            (Gimmick.TECHNICIAN, WrestlingStyle.SUBMISSION): 0.95,
            (Gimmick.POWERHOUSE, WrestlingStyle.POWERHOUSE): 1.0,
            (Gimmick.DAREDEVIL, WrestlingStyle.HIGH_FLYER): 1.0,
            
            # Personality-based gimmicks
            (Gimmick.CHARISMATIC, WrestlingStyle.SHOWMAN): 1.0,
            (Gimmick.SILENT_BADASS, WrestlingStyle.STRONG_STYLE): 0.9,
            (Gimmick.UNSTABLE, WrestlingStyle.HARDCORE): 0.9,
            
            # Special gimmicks
            (Gimmick.SUPERNATURAL, WrestlingStyle.POWERHOUSE): 0.8,
            (Gimmick.ENTERTAINER, WrestlingStyle.SHOWMAN): 1.0,
            (Gimmick.WARRIOR, WrestlingStyle.STRONG_STYLE): 0.9,
        }
        
        main_compat = compatibilities.get((self.gimmick, self.style), 0.7)
        if self.secondary_style:
            secondary_compat = compatibilities.get((self.gimmick, self.secondary_style), 0.7)
            return (main_compat + secondary_compat) / 2
        return main_compat
    
    def get_recommended_moves(self) -> List[str]:
        """Get a list of move types that fit this persona."""
        move_recommendations = {
            WrestlingStyle.POWERHOUSE: ["Power Bomb", "Slam", "Press", "Suplex"],
            WrestlingStyle.HIGH_FLYER: ["Moonsault", "450 Splash", "Hurricanrana", "Diving Attack"],
            WrestlingStyle.TECHNICAL: ["Suplex Variations", "Submission", "Counter", "Chain Wrestling"],
            WrestlingStyle.BRAWLER: ["Clothesline", "Punch", "DDT", "Brawling Strikes"],
            WrestlingStyle.SUBMISSION: ["Lock", "Hold", "Stretch", "Joint Manipulation"],
            WrestlingStyle.STRIKER: ["Kick", "Strike", "Chop", "Combination"],
            WrestlingStyle.SHOWMAN: ["Signature Taunt", "Crowd Play", "Flash Moves"],
            WrestlingStyle.HARDCORE: ["Weapon Strike", "Table Spot", "Extreme Moves"],
            WrestlingStyle.LUCHA_LIBRE: ["Springboard", "Rope Work", "Lucha Moves"],
            WrestlingStyle.STRONG_STYLE: ["Strong Strikes", "Fighting Spirit", "No-Sell Sequence"],
            WrestlingStyle.GIANT: ["Big Boot", "Chokeslam", "Power Moves"],
        }
        
        moves = move_recommendations.get(self.style, [])
        if self.secondary_style:
            moves.extend(move_recommendations.get(self.secondary_style, []))
        
        # Add gimmick-specific moves
        gimmick_moves = {
            Gimmick.MONSTER: ["Dominating Power Move", "Monster Spot"],
            Gimmick.SPEEDSTER: ["Quick Strike Combination", "Agility Showcase"],
            Gimmick.SUPERNATURAL: ["Mind Games", "Special Powers Spot"],
            Gimmick.ENTERTAINER: ["Crowd Interaction Spot", "Show-Off Sequence"],
        }
        
        if self.gimmick in gimmick_moves:
            moves.extend(gimmick_moves[self.gimmick])
        
        return list(set(moves))  # Remove duplicates

    def get_signature_move_types(self) -> List[str]:
        """Get recommended types of signature moves based on persona."""
        sig_move_types = {
            Gimmick.MONSTER: ["Devastating", "Dominating"],
            Gimmick.SPEEDSTER: ["Quick", "Agility"],
            Gimmick.SUPERNATURAL: ["Mind Games", "Special Powers"],
            Gimmick.ENTERTAINER: ["Crowd Interaction", "Show-Off"],
        }
        
        return sig_move_types.get(self.gimmick, ["Standard"]) 
        return sig_move_types.get(self.gimmick, ["Standard"]) 