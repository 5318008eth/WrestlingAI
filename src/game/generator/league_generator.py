import random
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from ..core.wrestling_leagues import Region, MarketSize, Territory, League, OrganizationTier
from ..core.wrestling_organizations import WrestlingOrganization

class LeagueNameGenerator:
    """Generates realistic wrestling promotion names"""
    
    PREFIXES = [
        "Elite", "Supreme", "Global", "United", "World", "International", "National",
        "Premier", "All", "Pro", "Pure", "Classic", "Modern", "Next", "Ultimate"
    ]
    
    CORE_TERMS = [
        "Wrestling", "Sports Entertainment", "Combat", "Grappling", "Fighting Spirit",
        "Warriors", "Athletes", "Fighters", "Competition", "Action"
    ]
    
    SUFFIXES = [
        "Federation", "Alliance", "Association", "Network", "Union", "Coalition",
        "Entertainment", "Promotions", "Championship Wrestling", "Athletics"
    ]
    
    REGIONAL_PREFIXES = {
        Region.NORTH_AMERICA: ["American", "North American", "Canadian", "Continental"],
        Region.EUROPE: ["European", "Euro", "Continental", "Western"],
        Region.JAPAN: ["Japanese", "Rising Sun", "Eastern", "Pacific"],
        Region.MEXICO: ["Mexican", "Latino", "Lucha", "Aztec"],
        Region.UK: ["British", "English", "Royal", "Commonwealth"],
        Region.AUSTRALIA: ["Australian", "Pacific", "Southern", "Oceanic"],
        Region.OTHER_ASIA: ["Asian", "Eastern", "Orient", "Pacific Rim"]
    }
    
    @classmethod
    def generate_name(cls, region: Region, tier: OrganizationTier) -> str:
        """Generate a promotion name based on region and tier"""
        if random.random() < 0.3 and region in cls.REGIONAL_PREFIXES:
            prefix = random.choice(cls.REGIONAL_PREFIXES[region])
        else:
            prefix = random.choice(cls.PREFIXES)
        
        core = random.choice(cls.CORE_TERMS)
        
        # Higher tier promotions are more likely to have a suffix
        suffix_chance = {
            OrganizationTier.GLOBAL: 0.9,
            OrganizationTier.INTERNATIONAL: 0.8,
            OrganizationTier.NATIONAL: 0.7,
            OrganizationTier.INDIE_REGIONAL: 0.4,
            OrganizationTier.INDIE_LOCAL: 0.2
        }
        
        if random.random() < suffix_chance[tier]:
            suffix = random.choice(cls.SUFFIXES)
            return f"{prefix} {core} {suffix}"
        
        return f"{prefix} {core}"

class ChampionshipGenerator:
    """Generates championship titles for promotions"""
    
    TITLE_PREFIXES = [
        "World", "Universal", "Global", "International", "National",
        "Continental", "Regional", "Heritage", "Legacy", "Premier"
    ]
    
    TITLE_TYPES = [
        "Heavyweight", "Championship", "Grand", "Crown", "Supreme",
        "Elite", "Warrior", "Fighting", "Battle", "Glory"
    ]
    
    SECONDARY_TITLES = [
        "Television", "Internet", "Heritage", "Continental", "Pride",
        "Fighting Spirit", "Warrior", "Champion's", "Challenger's"
    ]
    
    SPECIALTY_TITLES = [
        "Cruiserweight", "Junior Heavyweight", "Light Heavyweight",
        "Technical", "Strong Style", "High Flying", "Hardcore",
        "Submission", "Strike Force", "Power"
    ]
    
    @classmethod
    def generate_championships(cls, tier: OrganizationTier, region: Region) -> List[str]:
        """Generate appropriate championships based on promotion tier"""
        titles = []
        
        # Main Championship
        if tier in [OrganizationTier.GLOBAL, OrganizationTier.INTERNATIONAL]:
            prefix = random.choice(["World", "Universal", "Global"])
        else:
            prefix = random.choice(cls.TITLE_PREFIXES)
        
        main_title = f"{prefix} {random.choice(cls.TITLE_TYPES)} Championship"
        titles.append(main_title)
        
        # Secondary Titles
        num_secondary = {
            OrganizationTier.GLOBAL: 3,
            OrganizationTier.INTERNATIONAL: 2,
            OrganizationTier.NATIONAL: 2,
            OrganizationTier.INDIE_REGIONAL: 1,
            OrganizationTier.INDIE_LOCAL: 0
        }[tier]
        
        for _ in range(num_secondary):
            title = f"{random.choice(cls.SECONDARY_TITLES)} Championship"
            titles.append(title)
        
        # Specialty Title
        if tier in [OrganizationTier.GLOBAL, OrganizationTier.INTERNATIONAL, OrganizationTier.NATIONAL]:
            title = f"{random.choice(cls.SPECIALTY_TITLES)} Championship"
            titles.append(title)
        
        # Tag Team Titles
        if tier != OrganizationTier.INDIE_LOCAL or random.random() < 0.3:
            titles.append("Tag Team Championships")
        
        # Trios Titles (more common in Mexico)
        if region == Region.MEXICO and random.random() < 0.4:
            titles.append("Trios Championships")
        
        return titles

class MediaGenerator:
    """Generates media distribution details"""
    
    TV_NETWORKS = {
        Region.NORTH_AMERICA: [
            "Victory Sports Network", "Action Sports TV", "Combat Network",
            "Elite Sports Channel", "Prime Athletics", "Championship TV"
        ],
        Region.EUROPE: [
            "EuroSport Plus", "Continental TV", "Fight Network EU",
            "Premium Sports", "Victory Channel Europe"
        ],
        Region.JAPAN: [
            "Fighting Spirit TV", "Rising Sun Sports", "Combat TV Japan",
            "Victory Network Japan", "Elite Sports JP"
        ],
        Region.MEXICO: [
            "Lucha TV", "Combate Network", "Latino Sports",
            "Victory Deportes", "Elite Lucha"
        ],
        Region.UK: [
            "British Combat Sports", "Victory TV UK", "Fight Network UK",
            "Premium Wrestling Channel", "Elite Sports Britain"
        ]
    }
    
    STREAMING_PLATFORMS = [
        "VictoryNOW", "EliteFightPass", "CombatZone+", "WrestleStream",
        "FightPass Premium", "PowerSlam Network", "GrappleVision"
    ]
    
    @classmethod
    def generate_media_distribution(cls, tier: OrganizationTier, region: Region) -> Tuple[List[str], str]:
        """Generate TV networks and streaming platform based on tier and region"""
        networks = []
        streaming = None
        
        # TV Networks
        if tier in [OrganizationTier.GLOBAL, OrganizationTier.INTERNATIONAL]:
            num_networks = random.randint(2, 3)
        elif tier == OrganizationTier.NATIONAL:
            num_networks = random.randint(1, 2)
        elif tier == OrganizationTier.INDIE_REGIONAL:
            num_networks = 1 if random.random() < 0.3 else 0
        else:
            num_networks = 0
        
        if region in cls.TV_NETWORKS and num_networks > 0:
            networks = random.sample(cls.TV_NETWORKS[region], num_networks)
        
        # Streaming Platform
        streaming_chance = {
            OrganizationTier.GLOBAL: 1.0,
            OrganizationTier.INTERNATIONAL: 0.8,
            OrganizationTier.NATIONAL: 0.6,
            OrganizationTier.INDIE_REGIONAL: 0.2,
            OrganizationTier.INDIE_LOCAL: 0.0
        }
        
        if random.random() < streaming_chance[tier]:
            streaming = random.choice(cls.STREAMING_PLATFORMS)
        
        return networks, streaming

def generate_annual_revenue(tier: OrganizationTier, market_size: MarketSize) -> float:
    """Generate realistic annual revenue based on tier and market size"""
    base_revenue = {
        OrganizationTier.GLOBAL: (800, 1500),
        OrganizationTier.INTERNATIONAL: (100, 300),
        OrganizationTier.NATIONAL: (20, 80),
        OrganizationTier.INDIE_REGIONAL: (2, 10),
        OrganizationTier.INDIE_LOCAL: (0.1, 1)
    }[tier]
    
    market_multiplier = {
        MarketSize.MAJOR: 1.2,
        MarketSize.LARGE: 1.0,
        MarketSize.MEDIUM: 0.8,
        MarketSize.SMALL: 0.6,
        MarketSize.RURAL: 0.4
    }[market_size]
    
    base = random.uniform(base_revenue[0], base_revenue[1])
    return round(base * market_multiplier, 2)

def generate_founding_year(tier: OrganizationTier) -> int:
    """Generate a realistic founding year based on tier"""
    current_year = datetime.now().year
    
    # Older promotions tend to be higher tier
    min_age = {
        OrganizationTier.GLOBAL: 20,
        OrganizationTier.INTERNATIONAL: 15,
        OrganizationTier.NATIONAL: 10,
        OrganizationTier.INDIE_REGIONAL: 5,
        OrganizationTier.INDIE_LOCAL: 1
    }[tier]
    
    max_age = {
        OrganizationTier.GLOBAL: 70,
        OrganizationTier.INTERNATIONAL: 50,
        OrganizationTier.NATIONAL: 30,
        OrganizationTier.INDIE_REGIONAL: 20,
        OrganizationTier.INDIE_LOCAL: 10
    }[tier]
    
    return current_year - random.randint(min_age, max_age)

class EventScheduleGenerator:
    """Generates realistic event schedules for promotions"""
    
    EVENT_PREFIXES = [
        "Super", "Mega", "Ultimate", "Grand", "Royal", "Elite", "Premium",
        "Maximum", "Extreme", "Total", "Pure", "Classic", "Legacy"
    ]
    
    EVENT_NAMES = [
        "Showdown", "Collision", "Uprising", "Revolution", "Destiny",
        "Glory", "Impact", "Mayhem", "Warfare", "Triumph", "Ascension",
        "Dominion", "Rebellion", "Genesis", "Conquest", "Victory"
    ]
    
    SPECIAL_EVENTS = {
        "New Year": ["New Year's Revolution", "New Year's Showdown", "Genesis"],
        "Spring": ["Spring Stampede", "Spring Warfare", "Cherry Blossom Battle"],
        "Summer": ["Summer Slam", "Summer Heat", "Midsummer Mayhem"],
        "Fall": ["Fall Brawl", "Autumn Glory", "Harvest of Pain"],
        "Winter": ["Winter Warriors", "Frozen Fury", "December Destruction"]
    }
    
    PPV_MATCH_COUNTS = {
        OrganizationTier.GLOBAL: (8, 10),        # 8-10 matches
        OrganizationTier.INTERNATIONAL: (7, 9),   # 7-9 matches
        OrganizationTier.NATIONAL: (6, 8),        # 6-8 matches
        OrganizationTier.INDIE_REGIONAL: (5, 7),  # 5-7 matches
        OrganizationTier.INDIE_LOCAL: (4, 6)      # 4-6 matches
    }
    
    TV_MATCH_COUNTS = {
        OrganizationTier.GLOBAL: (5, 7),         # 5-7 matches
        OrganizationTier.INTERNATIONAL: (4, 6),   # 4-6 matches
        OrganizationTier.NATIONAL: (4, 5),        # 4-5 matches
        OrganizationTier.INDIE_REGIONAL: (3, 4),  # 3-4 matches
        OrganizationTier.INDIE_LOCAL: (3, 3)      # Always 3 matches
    }
    
    @classmethod
    def generate_event_name(cls, month: int, is_ppv: bool) -> str:
        """Generate an event name based on the month and type"""
        # Special seasonal events
        if month == 1:
            return random.choice(cls.SPECIAL_EVENTS["New Year"])
        elif month in [3, 4]:
            return random.choice(cls.SPECIAL_EVENTS["Spring"])
        elif month in [6, 7, 8]:
            return random.choice(cls.SPECIAL_EVENTS["Summer"])
        elif month in [9, 10]:
            return random.choice(cls.SPECIAL_EVENTS["Fall"])
        elif month == 12:
            return random.choice(cls.SPECIAL_EVENTS["Winter"])
        
        # Regular events
        if is_ppv:
            prefix = random.choice(cls.EVENT_PREFIXES)
            name = random.choice(cls.EVENT_NAMES)
            return f"{prefix} {name}"
        else:
            return "Weekly Show"  # This would be replaced with the show's actual name
    
    @classmethod
    def generate_match_card(cls, tier: OrganizationTier, is_ppv: bool) -> Dict:
        """Generate a match card structure for an event"""
        if is_ppv:
            min_matches, max_matches = cls.PPV_MATCH_COUNTS[tier]
        else:
            min_matches, max_matches = cls.TV_MATCH_COUNTS[tier]
        
        num_matches = random.randint(min_matches, max_matches)
        
        # Generate match card structure
        card = {
            "total_matches": num_matches,
            "championship_matches": 0,
            "promo_segments": 0,
            "interview_segments": 0,
            "special_segments": 0
        }
        
        # Add segments based on show type and tier
        if is_ppv:
            card["championship_matches"] = min(3, num_matches // 3)
            card["promo_segments"] = random.randint(1, 2)
            card["special_segments"] = random.randint(0, 1)
        else:
            card["championship_matches"] = min(1, num_matches // 4)
            card["promo_segments"] = random.randint(2, 3)
            card["interview_segments"] = random.randint(1, 2)
        
        return card
    
    @classmethod
    def generate_yearly_schedule(cls, tier: OrganizationTier, region: Region) -> List[Dict]:
        """Generate a full year's schedule of events"""
        schedule = []
        current_year = datetime.now().year
        
        # Define schedule patterns based on tier
        weekly_shows = tier in [OrganizationTier.GLOBAL, OrganizationTier.INTERNATIONAL, OrganizationTier.NATIONAL]
        ppv_count = {
            OrganizationTier.GLOBAL: 12,          # Monthly PPVs
            OrganizationTier.INTERNATIONAL: 6,     # Bi-monthly PPVs
            OrganizationTier.NATIONAL: 4,          # Quarterly PPVs
            OrganizationTier.INDIE_REGIONAL: 2,    # Semi-annual shows
            OrganizationTier.INDIE_LOCAL: 1        # Annual show
        }[tier]
        
        # Generate PPV events
        ppv_months = sorted(random.sample(range(1, 13), ppv_count))
        for month in ppv_months:
            # Generate a weekend date for the PPV
            day = random.randint(1, 28)  # Avoid month boundary issues
            if day % 7 <= 2:  # Ensure it's a weekend
                day = day + (6 - (day % 7))
            
            event_date = datetime(current_year, month, day)
            
            schedule.append({
                "date": event_date,
                "name": cls.generate_event_name(month, True),
                "type": "PPV",
                "card": cls.generate_match_card(tier, True)
            })
        
        # Generate weekly shows if applicable
        if weekly_shows:
            # Pick a day of the week for the show (1 = Monday, etc.)
            show_day = random.randint(1, 5)  # Monday to Friday
            
            # Generate shows for the whole year
            current_date = datetime(current_year, 1, 1)
            while current_date.year == current_year:
                # Skip if it's a PPV week
                is_ppv_week = any(
                    abs((event["date"] - current_date).days) <= 3 
                    for event in schedule if event["type"] == "PPV"
                )
                
                if not is_ppv_week and current_date.weekday() == show_day:
                    schedule.append({
                        "date": current_date,
                        "name": "Weekly Show",
                        "type": "TV",
                        "card": cls.generate_match_card(tier, False)
                    })
                
                current_date += timedelta(days=1)
        
        return sorted(schedule, key=lambda x: x["date"])

class ShowNameGenerator:
    """Generates names for weekly wrestling shows"""
    
    SHOW_PREFIXES = [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
    ]
    
    SHOW_NAMES = [
        "Night", "Fight", "Action", "Power", "Thunder", "Warfare",
        "Mayhem", "Fury", "Showdown", "Collision", "Rampage"
    ]
    
    SECONDARY_SHOW_NAMES = [
        "Evolution", "Underground", "Velocity", "Heat", "Elevation",
        "Dark", "Level Up", "Rising", "Next Level", "Ignition"
    ]
    
    @classmethod
    def generate_show_names(cls, region: Region, tier: OrganizationTier) -> Tuple[str, Optional[str]]:
        """Generate primary and optional secondary show names"""
        # Primary show name
        if tier in [OrganizationTier.GLOBAL, OrganizationTier.INTERNATIONAL]:
            # Use day-based name for top promotions
            prefix = random.choice(cls.SHOW_PREFIXES)
            name = random.choice(cls.SHOW_NAMES)
            primary = f"{prefix} {name}"
        else:
            # Use simple name for smaller promotions
            primary = f"{random.choice(cls.SHOW_NAMES)}"
        
        # Secondary show (only for larger promotions)
        secondary = None
        if tier in [OrganizationTier.GLOBAL, OrganizationTier.INTERNATIONAL]:
            secondary = random.choice(cls.SECONDARY_SHOW_NAMES)
        
        return primary, secondary

def generate_league(territory: Territory, tier: OrganizationTier) -> League:
    """Generate a complete fictional wrestling league"""
    name = LeagueNameGenerator.generate_name(territory.region, tier)
    organization = WrestlingOrganization(name=name, tier=tier)
    
    tv_networks, streaming = MediaGenerator.generate_media_distribution(tier, territory.region)
    championships = ChampionshipGenerator.generate_championships(tier, territory.region)
    annual_revenue = generate_annual_revenue(tier, territory.market_size)
    founded_year = generate_founding_year(tier)
    yearly_schedule = EventScheduleGenerator.generate_yearly_schedule(tier, territory.region)
    
    # Generate show names
    weekly_show, secondary_show = ShowNameGenerator.generate_show_names(territory.region, tier)
    
    return League(
        organization=organization,
        territory=territory,
        founded_year=founded_year,
        tv_networks=tv_networks,
        streaming_platform=streaming,
        annual_revenue=annual_revenue,
        championships=championships,
        yearly_schedule=yearly_schedule,
        weekly_show_name=weekly_show,
        secondary_show_name=secondary_show
    ) 