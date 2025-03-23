from typing import Dict, List, Optional, Union
import json
from dataclasses import dataclass, asdict, field
from enum import Enum
from datetime import date, datetime, timedelta
import random
import logging

from ..core.wrestling_archetypes import (
    Gender, Nationality, WrestlingStyle, Gimmick,
    STYLE_PHYSIQUES, STYLE_SYNERGIES, STYLE_MOVES
)
from ..core.wrestler_stats import (
    WrestlingStats, CareerStage, WrestlingRank, SubSkill,
    SUBSKILL_MAPPING
)

class Alignment(Enum):
    """Wrestler's alignment on the face/heel spectrum"""
    FACE = 100    # Pure good guy
    TWEENER = 0   # Neutral/ambiguous
    HEEL = -100   # Pure bad guy

@dataclass
class Relationship:
    wrestler_name: str
    relationship_type: str  # Ally, Rival, Manager, etc.
    heat: int  # -2 to +2
    description: str

@dataclass
class Move:
    name: str
    description: str
    move_type: str  # Basic, Advanced, Signature, Finisher
    requirements: Optional[Dict[str, Union[int, str]]] = None
    effects: Optional[Dict[str, Union[int, str]]] = None

@dataclass
class Stats:
    look: int  # Appearance and charisma
    power: int  # Physical strength
    real: int  # Authenticity and toughness
    work: int  # Wrestling ability
    heat: int  # Current storyline momentum

@dataclass
class Subskills:
    technical: int  # Technical wrestling ability
    brawling: int   # Brawling and striking
    aerial: int     # High-flying moves
    submission: int # Submission holds
    charisma: int   # Mic work and crowd interaction

@dataclass
class WWWCharacter:
    # Basic Info
    name: str  # Wrestling name
    real_name: str  # Real name of the wrestler
    birth_date: Union[str, date]  # Can accept either string or date
    gender: Gender
    nationality: Nationality
    height: float  # in inches
    weight: int    # in pounds
    physical_appearance: str
    character_description: str  # Detailed description of character's gimmick and personality
    
    # Career Info
    primary_style: WrestlingStyle
    gimmick: Gimmick
    alignment: int  # -100 to 100
    stats: WrestlingStats
    
    # Character Info
    background: str
    entrance: str
    
    # Optional Career Info
    secondary_style: Optional[WrestlingStyle] = None
    
    # Moves and Relationships
    signature_moves: List[Move] = field(default_factory=list)
    finisher: Optional[Move] = None
    relationships: List[Relationship] = field(default_factory=list)
    
    # Career Info
    current_league: Optional[str] = None
    previous_leagues: List[str] = field(default_factory=list)
    titles_held: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Convert birth_date string to date object if needed"""
        if isinstance(self.birth_date, str):
            self.birth_date = datetime.strptime(self.birth_date, "%Y-%m-%d").date()
    
    def to_dict(self) -> Dict:
        """Convert the character to a dictionary format."""
        # Calculate age from birth date
        today = date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        
        return {
            "basic_info": {
                "name": self.name,
                "birth_date": self.birth_date.strftime("%Y-%m-%d"),
                "age": age,
                "gender": self.gender.value,
                "nationality": self.nationality.value,
                "height": f"{self.height:.1f}\"",
                "weight": f"{self.weight}lbs",
                "physical_appearance": self.physical_appearance
            },
            "current_status": {
                "overness": self.stats.overness,
                "momentum": self.stats.momentum,
                "fatigue": self.stats.fatigue,
                "damage": self.stats.damage
            },
            "career": {
                "primary_style": self.primary_style.value,
                "secondary_style": self.secondary_style.value if self.secondary_style else None,
                "gimmick": self.gimmick.name,
                "alignment": self.alignment,
                "career_stage": self.stats.career_stage.name,
                "rank": self.stats.rank.name,
                "experience": self.stats.experience,
                "fans": self.stats.fans,
                "current_league": self.current_league,
                "previous_leagues": self.previous_leagues,
                "titles_held": self.titles_held
            },
            "stats": {
                "core_stats": self.stats.get_core_stats(),
                "subskills": self.stats.get_all_subskill_bonuses()
            },
            "character": {
                "background": self.background,
                "entrance": self.entrance
            }
        }

    def to_json(self) -> str:
        """Convert the character to a JSON string with proper formatting."""
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

    def generate_character_sheet(self) -> str:
        """Generate a formatted character sheet string."""
        # Calculate age
        today = date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
            
        sheet = f"""
=== BASIC INFORMATION ===
Name: {self.name} (Real Name: {self.real_name})
Date of Birth: {self.birth_date.strftime('%Y-%m-%d')} (Age: {age})
Gender: {self.gender.value}
Nationality: {self.nationality.value}
Height: {self.height:.1f}\"
Weight: {self.weight}lbs
Physical Appearance: {self.physical_appearance}

=== CHARACTER DESCRIPTION ===
{self.character_description}

=== CURRENT STATUS ===
Overness: {self.stats.overness}
Momentum: {self.stats.momentum}
Fatigue: {self.stats.fatigue}
Damage: {self.stats.damage}

=== CAREER INFORMATION ===
Primary Style: {self.primary_style.value}
Secondary Style: {self.secondary_style.value if self.secondary_style else 'None'}
Gimmick: {self.gimmick.name}
Alignment: {self.alignment}
Career Stage: {self.stats.career_stage.name}
Rank: {self.stats.rank.name}
Experience: {self.stats.experience}
Fans: {self.stats.fans}
Current League: {self.current_league}
Previous Leagues: {', '.join(self.previous_leagues) if self.previous_leagues else 'None'}
Titles Held: {', '.join(self.titles_held) if self.titles_held else 'None'}

=== CORE STATS ===
Body: {self.stats.body:+d}
Look: {self.stats.look:+d}
Real: {self.stats.real:+d}
Work: {self.stats.work:+d}
Fire: {self.stats.fire:+d}

=== SUBSKILLS ===
{chr(10).join(f"{skill.name}: {bonus:+d}" for skill, bonus in self.stats.get_all_subskill_bonuses().items())}

=== CHARACTER ===
Background: {self.background}
Entrance: {self.entrance}"""
        return sheet

class CharacterGenerator:
    def __init__(self):
        """Initialize the character generator with default settings."""
        self.name_prefixes = ["The", "Mr.", "Ms.", "Dr.", "King", "Queen"]
        self.name_suffixes = ["Jr.", "III", "X", "Prime", "2.0"]
        
    def generate_name(self, gender: Gender) -> str:
        """Generate a wrestling name based on gender."""
        prefix = random.choice(self.name_prefixes) if random.random() < 0.3 else ""
        suffix = random.choice(self.name_suffixes) if random.random() < 0.1 else ""
        
        if gender == Gender.MALE:
            base_names = ["Thunder", "Steel", "Iron", "Dragon", "Phoenix"]
        else:
            base_names = ["Storm", "Rose", "Diamond", "Phoenix", "Star"]
            
        name = random.choice(base_names)
        if prefix:
            name = f"{prefix} {name}"
        if suffix:
            name = f"{name} {suffix}"
        return name

    def generate_demographics(self) -> Dict:
        """Generate demographic information for a character."""
        # Generate random height based on style
        style = self.generate_wrestling_style()
        min_height = STYLE_PHYSIQUES[style].min_height
        max_height = STYLE_PHYSIQUES[style].max_height
        height = random.uniform(min_height, max_height)
        
        # Generate weight based on height and style
        min_weight = STYLE_PHYSIQUES[style].min_weight
        max_weight = STYLE_PHYSIQUES[style].max_weight
        weight = random.randint(min_weight, max_weight)
            
        # Generate birth date (18-45 years ago)
        today = datetime.now()
        age = random.randint(18, 45)
        birth_year = today.year - age
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)  # Using 28 to avoid month/leap year issues
        birth_date = date(birth_year, birth_month, birth_day)
            
        return {
            'birth_date': birth_date,
            'gender': random.choice([Gender.MALE, Gender.FEMALE]),
            'nationality': random.choice(list(Nationality)),
            'height': height,
            'weight': weight
        }

    def generate_wrestling_style(self) -> WrestlingStyle:
        """Generate a primary wrestling style."""
        return random.choice(list(WrestlingStyle))

    def generate_alignment(self) -> int:
        """Generate character alignment (-100 to 100)."""
        weights = {
            100: 0.4,    # 40% chance for face
            0: 0.2,      # 20% chance for tweener
            -100: 0.4    # 40% chance for heel
        }
        return random.choices(list(weights.keys()), list(weights.values()))[0]

    def generate_gimmick(self, alignment: Optional[int] = None) -> Gimmick:
        """Generate a character gimmick."""
        return random.choice(list(Gimmick))

    def generate_stats(self, style: WrestlingStyle) -> WrestlingStats:
        """Generate wrestling stats based on style."""
        # Base stats
        stats = {
            "body": random.randint(2, 4),
            "look": random.randint(2, 4),
            "real": random.randint(2, 4),
            "work": random.randint(2, 4),
            "fire": random.randint(2, 4)
        }
        
        # Style-based stat boosts
        style_boosts = {
            WrestlingStyle.POWERHOUSE: {"body": 2},
            WrestlingStyle.TECHNICAL: {"work": 2},
            WrestlingStyle.HIGH_FLYER: {"body": 1, "work": 1},
            WrestlingStyle.SHOWMAN: {"look": 2},
            WrestlingStyle.FIGHTER: {"real": 2},
            WrestlingStyle.BRAWLER: {"fire": 2},
            WrestlingStyle.HARDCORE: {"fire": 1, "real": 1},
            WrestlingStyle.CEREBRAL: {"work": 1, "real": 1}
        }
        
        # Apply style boosts
        for stat, boost in style_boosts[style].items():
            stats[stat] = min(5, stats[stat] + boost)
            
        return WrestlingStats(
            body=stats["body"],
            look=stats["look"],
            real=stats["real"],
            work=stats["work"],
            fire=stats["fire"],
            experience=random.randint(0, 10),
            fans=random.randint(100, 5000),
            career_stage=CareerStage.ROOKIE,
            rank=WrestlingRank.LOCAL,
            overness=random.randint(30, 70),
            momentum=50,
            fatigue=0,
            damage=0
        )

    def generate_character_description(self, demographics: Dict, style: WrestlingStyle, gimmick: Gimmick, alignment: int) -> Dict[str, str]:
        """Generate detailed character descriptions using AI."""
        from src.ai_client import AIClient
        
        # Create prompt for AI
        prompt = f"""Create a detailed wrestling character based on the following attributes:
- Wrestling Style: {style.value}
- Gimmick: {gimmick.name}
- Alignment: {alignment} (negative = heel, positive = face)
- Height: {demographics['height']} inches
- Weight: {demographics['weight']} lbs
- Gender: {demographics['gender'].value}
- Nationality: {demographics['nationality'].value}

You must respond with a valid JSON object containing exactly these fields:
{{
    "real_name": "string",
    "physical_appearance": "string",
    "character_description": "string"
}}

The response must be a single JSON object with no additional text or explanation. Make the character description engaging and fitting for their style and gimmick. Include details about their personality, motivations, and how they present themselves to the audience."""

        # Initialize AI client and get response
        try:
            ai_client = AIClient()
            response = ai_client.generate_response(
                prompt=prompt,
                model="deepseek/deepseek-r1:free",
                max_tokens=1000,
                temperature=0.7
            )
            
            if "error" in response:
                logging.error(f"AI generation error: {response['error']}")
                return {
                    "real_name": "Unknown",
                    "physical_appearance": "Standard wrestling attire",
                    "character_description": "A mysterious wrestler with an enigmatic presence"
                }
            
            # Parse the response content as JSON
            import json
            try:
                # Clean the response to ensure it's valid JSON
                content = response["content"].strip()
                if content.startswith("```json"):
                    content = content[7:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()
                
                character_data = json.loads(content)
                return character_data
            except json.JSONDecodeError as e:
                logging.error(f"Failed to parse AI response as JSON: {str(e)}")
                logging.error(f"Response content: {response['content']}")
                return {
                    "real_name": "Unknown",
                    "physical_appearance": "Standard wrestling attire",
                    "character_description": "A mysterious wrestler with an enigmatic presence"
                }
                
        except Exception as e:
            logging.error(f"Error in AI character generation: {str(e)}")
            return {
                "real_name": "Unknown",
                "physical_appearance": "Standard wrestling attire",
                "character_description": "A mysterious wrestler with an enigmatic presence"
            }

    def generate_character(self, gender: Gender = None) -> WWWCharacter:
        """Generate a complete wrestling character."""
        if gender is None:
            gender = random.choice(list(Gender))
            
        # Generate basic info
        demographics = self.generate_demographics()
        
        # Generate career info
        wrestling_style = self.generate_wrestling_style()
        experience_level = self.generate_experience_level()
        career_stats = self.generate_career_stats(experience_level)
        
        # Generate stats and subskills
        stats = self.generate_stats(wrestling_style)
        subskills = self.generate_subskills(wrestling_style)
        
        # Generate character info
        alignment = self.generate_alignment()
        gimmick = self.generate_gimmick(alignment)
        
        # Generate detailed character descriptions using AI
        character_desc = self.generate_character_description(
            demographics, wrestling_style, gimmick, alignment
        )
        
        background = self.generate_background(demographics, wrestling_style)
        entrance = self.generate_entrance(wrestling_style)
        
        # Create and return the character
        return WWWCharacter(
            name=self.generate_name(demographics['gender']),
            real_name=character_desc["real_name"],
            birth_date=demographics['birth_date'],
            gender=demographics['gender'],
            nationality=demographics['nationality'],
            height=demographics['height'],
            weight=demographics['weight'],
            physical_appearance=character_desc["physical_appearance"],
            character_description=character_desc["character_description"],
            primary_style=wrestling_style,
            gimmick=gimmick,
            alignment=alignment,
            stats=stats,
            background=background,
            entrance=entrance,
            finisher=self.generate_finisher(wrestling_style),
            signature_moves=[self.generate_finisher(wrestling_style)],
            relationships=[],
            current_league=None,
            previous_leagues=[],
            titles_held=[]
        )

    def generate_experience_level(self) -> CareerStage:
        """Generate experience level based on distribution."""
        weights = {
            CareerStage.ROOKIE: 0.3,      # 30% chance for rookies
            CareerStage.ESTABLISHED: 0.4,  # 40% chance for established
            CareerStage.VETERAN: 0.3       # 30% chance for veterans
        }
        return random.choices(
            list(weights.keys()),
            weights=list(weights.values())
        )[0]

    def generate_career_stats(self, experience_level: CareerStage) -> Dict:
        """Generate career statistics based on experience level."""
        leagues = [
            "Independent Wrestling Alliance",
            "Global Wrestling Federation",
            "National Wrestling Alliance",
            "Ring of Honor",
            "Impact Wrestling",
            "All Elite Wrestling",
            "New Japan Pro Wrestling"
        ]
        
        titles = [
            "World Championship",
            "Intercontinental Championship",
            "Tag Team Championship",
            "Television Championship",
            "Regional Championship"
        ]
        
        stats = {
            "current_league": random.choice(leagues),
            "previous_leagues": [],
            "titles_held": []
        }
        
        # Add previous leagues based on experience
        if experience_level.value >= CareerStage.ESTABLISHED.value:
            num_previous = random.randint(1, 3)
            stats["previous_leagues"] = random.sample(leagues, num_previous)
        
        # Add titles based on experience
        if experience_level.value >= CareerStage.VETERAN.value:
            num_titles = random.randint(1, 4)
            stats["titles_held"] = random.sample(titles, num_titles)
        
        return stats

    def generate_subskills(self, primary_style: WrestlingStyle) -> Subskills:
        """Generate subskills based on wrestling style."""
        # Base values
        skills = {
            'technical': random.randint(30, 70),
            'brawling': random.randint(30, 70),
            'aerial': random.randint(30, 70),
            'submission': random.randint(30, 70),
            'charisma': random.randint(30, 70)
        }
        
        # Style influences
        style_boosts = {
            WrestlingStyle.TECHNICAL: {'technical': 20, 'submission': 10},
            WrestlingStyle.POWERHOUSE: {'brawling': 20, 'technical': 10},
            WrestlingStyle.HIGH_FLYER: {'aerial': 20, 'brawling': 10},
            WrestlingStyle.SHOWMAN: {'charisma': 20, 'aerial': 10},
            WrestlingStyle.FIGHTER: {'brawling': 20, 'technical': 10},
            WrestlingStyle.BRAWLER: {'brawling': 20, 'charisma': 10},
            WrestlingStyle.HARDCORE: {'brawling': 20, 'charisma': 10},
            WrestlingStyle.CEREBRAL: {'technical': 20, 'charisma': 10}
        }
        
        # Apply primary style boosts
        if primary_style in style_boosts:
            for skill, boost in style_boosts[primary_style].items():
                skills[skill] = min(100, skills[skill] + boost)
        
        return Subskills(**skills)

    def generate_background(self, demographics: Dict, style: WrestlingStyle) -> str:
        """Generate a character background story."""
        backgrounds = {
            WrestlingStyle.POWERHOUSE: [
                "Former strongman competitor turned wrestler",
                "Natural athlete with incredible strength",
                "Trained in Olympic weightlifting before wrestling"
            ],
            WrestlingStyle.TECHNICAL: [
                "Amateur wrestling champion",
                "Trained in catch wrestling from a young age",
                "Studied under legendary technical wrestlers"
            ],
            WrestlingStyle.HIGH_FLYER: [
                "Gymnastics background led to high-flying style",
                "Trained in lucha libre in Mexico",
                "Parkour athlete turned wrestler"
            ],
            WrestlingStyle.SHOWMAN: [
                "Former stage performer",
                "Natural entertainer since childhood",
                "Trained in theater before wrestling"
            ],
            WrestlingStyle.FIGHTER: [
                "Former MMA fighter",
                "Boxing champion turned wrestler",
                "Martial arts expert"
            ],
            WrestlingStyle.BRAWLER: [
                "Street fighting background",
                "Bouncer turned wrestler",
                "Grew up fighting in tough neighborhoods"
            ],
            WrestlingStyle.HARDCORE: [
                "Underground wrestling veteran",
                "Deathmatch specialist",
                "Known for extreme matches"
            ],
            WrestlingStyle.CEREBRAL: [
                "Chess champion turned wrestler",
                "Strategic mastermind",
                "Known for psychological warfare"
            ]
        }
        
        return random.choice(backgrounds.get(style, ["Mysterious newcomer to the wrestling world"]))

    def generate_entrance(self, style: WrestlingStyle) -> str:
        """Generate an entrance description based on wrestling style."""
        entrances = {
            WrestlingStyle.POWERHOUSE: [
                "Enters with a display of raw strength",
                "Intimidating slow walk to the ring",
                "Demonstrates power by lifting heavy objects"
            ],
            WrestlingStyle.TECHNICAL: [
                "Professional and focused entrance",
                "Stretches and warms up during entrance",
                "Demonstrates technical moves on the way to the ring"
            ],
            WrestlingStyle.HIGH_FLYER: [
                "Acrobatic entrance with flips",
                "High-energy entrance with aerial moves",
                "Enters from the top rope"
            ],
            WrestlingStyle.SHOWMAN: [
                "Elaborate entrance with pyro",
                "Dramatic poses and crowd interaction",
                "Theatrical entrance with special effects"
            ],
            WrestlingStyle.FIGHTER: [
                "MMA-style entrance with fight team",
                "Intense shadow boxing entrance",
                "Martial arts demonstration"
            ],
            WrestlingStyle.BRAWLER: [
                "Aggressive entrance through the crowd",
                "Intimidating walk with mean mugging",
                "Ready to fight from the moment they appear"
            ],
            WrestlingStyle.HARDCORE: [
                "Enters with weapons",
                "Violent entrance through the crowd",
                "Destructive path to the ring"
            ],
            WrestlingStyle.CEREBRAL: [
                "Calculated and methodical entrance",
                "Mind games during entrance",
                "Strategic positioning during entrance"
            ]
        }
        
        return random.choice(entrances.get(style, ["Standard entrance to the ring"]))

    def generate_finisher(self, wrestling_style: WrestlingStyle) -> Move:
        """Generate a finisher move appropriate for the wrestling style."""
        style_finishers = {
            WrestlingStyle.POWERHOUSE: [
                ("Power Bomb", "A power move that showcases raw strength"),
                ("Press Slam", "A power slam that demonstrates pure strength"),
                ("Muscle Buster", "A power-based slam showing incredible force")
            ],
            WrestlingStyle.TECHNICAL: [
                ("Technical Masterlock", "A technical submission hold targeting multiple joints"),
                ("Wrestling Clinic", "A technical sequence of holds flowing into a submission"),
                ("Joint Manipulation", "A technical joint lock that forces submission")
            ],
            WrestlingStyle.HIGH_FLYER: [
                ("Phoenix Splash", "An aerial forward flip splash from great height"),
                ("Shooting Star Press", "An aerial backflip splash that defies gravity"),
                ("450 Splash", "An aerial rotating splash that showcases agility")
            ],
            WrestlingStyle.SHOWMAN: [
                ("Crowd Pleaser", "A dramatic showstopping move that electrifies the crowd"),
                ("Spotlight Moment", "A dramatic high-impact move that steals the show"),
                ("Grand Finale", "A dramatic sequence ending in a show-stopping pose")
            ],
            WrestlingStyle.FIGHTER: [
                ("Knockout Blow", "A strike move that ends the fight"),
                ("Roundhouse Finish", "A strike that shows fighting expertise"),
                ("Strike Combination", "A strike combination that leads to knockout")
            ],
            WrestlingStyle.BRAWLER: [
                ("Street Justice", "A brawl combination that ends fights"),
                ("Back Alley Brawl", "A brawl series of devastating strikes"),
                ("Bar Room Special", "A brawl sequence that shows street fighting skills")
            ],
            WrestlingStyle.HARDCORE: [
                ("Extreme Ending", "A hardcore finish using weapons and extreme tactics"),
                ("Deathmatch Special", "A hardcore move that ends matches"),
                ("Pain Threshold", "A hardcore finish that tests limits")
            ],
            WrestlingStyle.CEREBRAL: [
                ("Mind Games", "A cerebral finish that outsmarts the opponent"),
                ("Strategic Strike", "A cerebral sequence ending in victory"),
                ("Tactical Submission", "A cerebral submission that breaks both body and spirit")
            ]
        }
        
        if wrestling_style not in style_finishers:
            return Move("Basic Slam", "A powerful slam to the mat", "Finisher")
            
        name, description = random.choice(style_finishers[wrestling_style])
        return Move(name, description, "Finisher")

    def generate_multiple_finishers(self, count: int = 2, wrestling_style: Optional[WrestlingStyle] = None) -> List[Move]:
        """Generate multiple finisher moves."""
        finishers = []
        for _ in range(count):
            if wrestling_style:
                finisher = self.generate_finisher(wrestling_style)
            else:
                # If no style provided, randomly choose one
                finisher = self.generate_finisher(random.choice(list(WrestlingStyle)))
            finishers.append(finisher)
        return finishers

    def generate_relationships(self, characters: List[WWWCharacter]) -> Dict[str, Dict[str, Relationship]]:
        """Generate relationships between characters."""
        relationships = {}
        
        for char in characters:
            char_relationships = {}
            
            # Each character has a chance to form relationships with others
            for other in characters:
                if char != other and random.random() < 0.3:  # 30% chance
                    relationship_type = random.choice(["Ally", "Rival", "Enemy", "Friend"])
                    heat = random.randint(-2, 2)
                    description = self.generate_relationship_description(relationship_type, heat)
                    
                    char_relationships[other.name] = Relationship(
                        wrestler_name=other.name,
                        relationship_type=relationship_type,
                        heat=heat,
                        description=description
                    )
            
            if char_relationships:
                relationships[char.name] = char_relationships
        
        return relationships

    def generate_relationship_description(self, relationship_type: str, heat: int) -> str:
        """Generate a description for a relationship."""
        descriptions = {
            "Ally": [
                "Trusted training partner",
                "Tag team partner",
                "Mentor/student relationship",
                "Share mutual respect"
            ],
            "Rival": [
                "Competitive rivalry",
                "Long-standing feud",
                "Contested many matches",
                "Competing for titles"
            ],
            "Enemy": [
                "Bitter hatred",
                "Personal vendetta",
                "Betrayed alliance",
                "Opposing ideologies"
            ],
            "Friend": [
                "Close friends outside the ring",
                "Share similar backgrounds",
                "Support each other",
                "Travel partners"
            ]
        }
        
        base_desc = random.choice(descriptions.get(relationship_type, ["Complex relationship"]))
        
        # Add heat modifier
        if heat > 1:
            base_desc += " with strong positive feelings"
        elif heat > 0:
            base_desc += " with positive feelings"
        elif heat < -1:
            base_desc += " with intense animosity"
        elif heat < 0:
            base_desc += " with growing tension"
            
        return base_desc 