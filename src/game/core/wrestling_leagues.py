from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from .wrestling_organizations import (
    WrestlingWorld, WrestlingOrganization, OrganizationTier,
    EventSchedule, RosterRequirements, TIER_SCHEDULES, TIER_ROSTER_REQUIREMENTS
)
from ..generator.league_generator import generate_league
from ..generator.character_generator import WWWCharacter
from ..generator.match_generator import Storyline
import random

class Region(Enum):
    """Major wrestling regions of the world"""
    NORTH_AMERICA = auto()
    EUROPE = auto()
    JAPAN = auto()
    MEXICO = auto()
    UK = auto()
    AUSTRALIA = auto()
    OTHER_ASIA = auto()

class MarketSize(Enum):
    """Market size categories for different areas"""
    MAJOR = auto()      # Major metropolitan areas (NYC, Tokyo, London)
    LARGE = auto()      # Large cities (Chicago, Osaka, Manchester)
    MEDIUM = auto()     # Mid-sized cities (Portland, Nagoya, Glasgow)
    SMALL = auto()      # Smaller cities and large towns
    RURAL = auto()      # Rural areas and small towns

@dataclass
class Territory:
    """Defines a wrestling territory/market"""
    name: str
    region: Region
    market_size: MarketSize
    population: int
    active_promotions: int = 0
    max_promotions: int = 1

@dataclass
class League:
    """Represents a specific wrestling league/promotion"""
    organization: WrestlingOrganization
    territory: Territory
    founded_year: int
    tv_networks: List[str]
    streaming_platform: Optional[str]
    annual_revenue: float  # in millions USD
    championships: List[str]
    yearly_schedule: List[Dict]  # List of events with dates and match cards
    
    # Roster management
    main_roster: List[WWWCharacter] = field(default_factory=list)
    developmental_roster: List[WWWCharacter] = field(default_factory=list)
    champions: Dict[str, WWWCharacter] = field(default_factory=dict)
    tag_teams: List[Tuple[WWWCharacter, WWWCharacter, str]] = field(default_factory=list)  # (wrestler1, wrestler2, team_name)
    
    # Storyline tracking
    active_storylines: List[Storyline] = field(default_factory=list)
    completed_storylines: List[Storyline] = field(default_factory=list)
    
    # Show names
    weekly_show_name: Optional[str] = None
    secondary_show_name: Optional[str] = None
    
    def add_to_roster(self, wrestler: WWWCharacter, is_developmental: bool = False) -> None:
        """Add a wrestler to the roster"""
        if is_developmental:
            self.developmental_roster.append(wrestler)
        else:
            self.main_roster.append(wrestler)
    
    def remove_from_roster(self, wrestler: WWWCharacter) -> bool:
        """Remove a wrestler from the roster"""
        if wrestler in self.main_roster:
            self.main_roster.remove(wrestler)
            return True
        elif wrestler in self.developmental_roster:
            self.developmental_roster.remove(wrestler)
            return True
        return False
    
    def create_tag_team(self, wrestler1: WWWCharacter, wrestler2: WWWCharacter, team_name: str) -> bool:
        """Create a new tag team"""
        if wrestler1 in self.main_roster and wrestler2 in self.main_roster:
            self.tag_teams.append((wrestler1, wrestler2, team_name))
            return True
        return False
    
    def set_champion(self, championship: str, wrestler: WWWCharacter) -> bool:
        """Set a new champion"""
        if wrestler in self.main_roster and championship in self.championships:
            self.champions[championship] = wrestler
            return True
        return False
    
    def start_storyline(self, storyline: Storyline) -> bool:
        """Start a new storyline"""
        if all(w in self.main_roster for w in storyline.participants):
            self.active_storylines.append(storyline)
            return True
        return False
    
    def end_storyline(self, storyline: Storyline, resolution: str) -> None:
        """End an active storyline"""
        if storyline in self.active_storylines:
            storyline.resolution = resolution
            self.active_storylines.remove(storyline)
            self.completed_storylines.append(storyline)
    
    def get_available_roster(self, exclude_champions: bool = False) -> List[WWWCharacter]:
        """Get list of available wrestlers for booking"""
        available = self.main_roster.copy()
        if exclude_champions:
            available = [w for w in available if w not in self.champions.values()]
        return available

# Define major territories
MAJOR_TERRITORIES = {
    # North America
    "NYC": Territory("New York Metropolitan", Region.NORTH_AMERICA, MarketSize.MAJOR, 20_000_000, max_promotions=5),
    "LA": Territory("Los Angeles", Region.NORTH_AMERICA, MarketSize.MAJOR, 13_000_000, max_promotions=4),
    "CHI": Territory("Chicago", Region.NORTH_AMERICA, MarketSize.LARGE, 9_500_000, max_promotions=3),
    
    # Japan
    "TOKYO": Territory("Greater Tokyo", Region.JAPAN, MarketSize.MAJOR, 37_000_000, max_promotions=5),
    "OSAKA": Territory("Greater Osaka", Region.JAPAN, MarketSize.LARGE, 19_000_000, max_promotions=3),
    
    # Mexico
    "CDMX": Territory("Mexico City", Region.MEXICO, MarketSize.MAJOR, 21_000_000, max_promotions=4),
    
    # UK
    "LONDON": Territory("Greater London", Region.UK, MarketSize.MAJOR, 9_000_000, max_promotions=3),
    
    # Europe
    "PARIS": Territory("Paris Metropolitan", Region.EUROPE, MarketSize.MAJOR, 12_000_000, max_promotions=2),
    "BERLIN": Territory("Berlin Metropolitan", Region.EUROPE, MarketSize.LARGE, 6_000_000, max_promotions=2),
}

class WrestlingLeagues:
    """Manages specific wrestling leagues and promotions"""
    
    def __init__(self):
        self.world = WrestlingWorld()
        self.leagues: Dict[str, League] = {}
        self._initialize_major_promotions()
    
    def _initialize_major_promotions(self):
        """Initialize major wrestling promotions"""
        # Global Tier Promotions
        self._create_global_promotions()
        # International Tier Promotions
        self._create_international_promotions()
        # Major National Promotions
        self._create_national_promotions()
    
    def _create_global_promotions(self):
        """Create global tier promotions"""
        # Create 3 global promotions in major markets
        territories = ["NYC", "TOKYO", "LONDON"]
        for territory_key in territories:
            territory = MAJOR_TERRITORIES[territory_key]
            league = generate_league(territory, OrganizationTier.GLOBAL)
            self.leagues[league.organization.name] = league
    
    def _create_international_promotions(self):
        """Create international tier promotions"""
        # Create 5 international promotions
        territories = ["LA", "OSAKA", "CDMX", "PARIS", "BERLIN"]
        for territory_key in territories:
            territory = MAJOR_TERRITORIES[territory_key]
            league = generate_league(territory, OrganizationTier.INTERNATIONAL)
            self.leagues[league.organization.name] = league
    
    def _create_national_promotions(self):
        """Create national tier promotions"""
        # Create 2-3 national promotions per major region
        for region in Region:
            territories = [t for t in MAJOR_TERRITORIES.values() if t.region == region]
            if territories:
                num_promotions = random.randint(2, 3)
                for _ in range(num_promotions):
                    territory = random.choice(territories)
                    league = generate_league(territory, OrganizationTier.NATIONAL)
                    self.leagues[league.organization.name] = league
    
    def get_leagues_by_tier(self, tier: OrganizationTier) -> List[League]:
        """Get all leagues of a specific tier"""
        return [
            league for league in self.leagues.values()
            if league.organization.tier == tier
        ]
    
    def get_leagues_by_region(self, region: Region) -> List[League]:
        """Get all leagues in a specific region"""
        return [
            league for league in self.leagues.values()
            if league.territory.region == region
        ]
    
    def get_leagues_by_market_size(self, market_size: MarketSize) -> List[League]:
        """Get all leagues in markets of a specific size"""
        return [
            league for league in self.leagues.values()
            if league.territory.market_size == market_size
        ]
    
    def print_league_details(self, league_name: str) -> None:
        """Print detailed information about a specific league"""
        if league_name not in self.leagues:
            print(f"League {league_name} not found")
            return
            
        league = self.leagues[league_name]
        print(f"\n{league.organization.name} Details:")
        print("=" * 50)
        print(f"Tier: {league.organization.tier.name}")
        print(f"Territory: {league.territory.name} ({league.territory.region.name})")
        print(f"Founded: {league.founded_year}")
        print(f"TV Networks: {', '.join(league.tv_networks)}")
        print(f"Streaming: {league.streaming_platform or 'None'}")
        print(f"Annual Revenue: ${league.annual_revenue}M")
        print("\nChampionships:")
        for title in league.championships:
            print(f"- {title}")
        print("-" * 50) 