from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class OrganizationTier(Enum):
    """Wrestling organization tiers based on size and reach"""
    INDIE_LOCAL = 1      # Local indie promotions (city/small region)
    INDIE_REGIONAL = 2   # Larger indie promotions (state/large region)
    NATIONAL = 3         # Major national promotions
    INTERNATIONAL = 4    # Multi-country promotions
    GLOBAL = 5          # Worldwide major promotions

class EventType(Enum):
    """Types of wrestling events"""
    HOUSE_SHOW = 1      # Non-televised local events
    TV_SHOW = 2         # Regular television broadcasts
    SPECIAL_EVENT = 3   # Bigger special events (like WWE Clash of Champions)
    PPV = 4            # Major pay-per-view events

@dataclass
class EventSchedule:
    """Defines how often different types of events occur"""
    house_shows_per_week: int = 0
    tv_shows_per_week: int = 0
    special_events_per_year: int = 0
    ppvs_per_year: int = 0

@dataclass
class RosterRequirements:
    """Minimum roster size requirements"""
    min_main_roster: int
    min_midcard: int
    min_jobbers: int
    max_total_roster: int

@dataclass
class WrestlingOrganization:
    """Represents a wrestling promotion/organization"""
    name: str
    tier: OrganizationTier
    schedule: EventSchedule
    roster_reqs: RosterRequirements
    current_roster_size: int = 0
    active: bool = True
    tv_deal: bool = False
    streaming_platform: bool = False

# Define standard schedules for each tier
TIER_SCHEDULES = {
    OrganizationTier.INDIE_LOCAL: EventSchedule(
        house_shows_per_week=1,
        tv_shows_per_week=0,
        special_events_per_year=4,
        ppvs_per_year=0
    ),
    OrganizationTier.INDIE_REGIONAL: EventSchedule(
        house_shows_per_week=2,
        tv_shows_per_week=1,
        special_events_per_year=6,
        ppvs_per_year=2
    ),
    OrganizationTier.NATIONAL: EventSchedule(
        house_shows_per_week=3,
        tv_shows_per_week=1,
        special_events_per_year=8,
        ppvs_per_year=4
    ),
    OrganizationTier.INTERNATIONAL: EventSchedule(
        house_shows_per_week=4,
        tv_shows_per_week=2,
        special_events_per_year=10,
        ppvs_per_year=8
    ),
    OrganizationTier.GLOBAL: EventSchedule(
        house_shows_per_week=5,
        tv_shows_per_week=2,
        special_events_per_year=12,
        ppvs_per_year=12
    )
}

# Define roster requirements for each tier
TIER_ROSTER_REQUIREMENTS = {
    OrganizationTier.INDIE_LOCAL: RosterRequirements(
        min_main_roster=4,      # Small core main event scene
        min_midcard=6,          # Basic midcard
        min_jobbers=5,          # Local enhancement talent
        max_total_roster=20     # Smaller roster due to sharing talent
    ),
    OrganizationTier.INDIE_REGIONAL: RosterRequirements(
        min_main_roster=6,      # Regional stars
        min_midcard=10,         # Solid midcard
        min_jobbers=8,          # Regular enhancement talent
        max_total_roster=35     # Medium roster with some sharing
    ),
    OrganizationTier.NATIONAL: RosterRequirements(
        min_main_roster=12,     # Full main event division
        min_midcard=20,         # Strong midcard division
        min_jobbers=18,         # Full jobber roster
        max_total_roster=65     # Large dedicated roster
    ),
    OrganizationTier.INTERNATIONAL: RosterRequirements(
        min_main_roster=15,     # Elite main event scene
        min_midcard=30,         # Deep midcard division
        min_jobbers=25,         # Complete enhancement division
        max_total_roster=90     # Very large roster
    ),
    OrganizationTier.GLOBAL: RosterRequirements(
        min_main_roster=20,     # Massive main event scene
        min_midcard=40,         # Huge midcard division
        min_jobbers=30,         # Full enhancement division
        max_total_roster=120    # Massive exclusive roster
    )
}

# Estimated number of promotions per tier globally
PROMOTIONS_PER_TIER = {
    OrganizationTier.INDIE_LOCAL: 1500,    # Numerous small local promotions worldwide
    OrganizationTier.INDIE_REGIONAL: 250,  # Significant regional presence
    OrganizationTier.NATIONAL: 30,         # Major national promotions
    OrganizationTier.INTERNATIONAL: 8,     # Large international promotions
    OrganizationTier.GLOBAL: 3            # WWE, AEW, NJPW level
}

# Average number of promotions a wrestler works for by tier
TYPICAL_PROMOTIONS_PER_WRESTLER = {
    OrganizationTier.INDIE_LOCAL: 3,      # Wrestlers typically work for multiple local promotions
    OrganizationTier.INDIE_REGIONAL: 2,   # Often work for couple regional promotions
    OrganizationTier.NATIONAL: 1.5,       # Might do some indie dates
    OrganizationTier.INTERNATIONAL: 1.2,  # Occasional special appearances
    OrganizationTier.GLOBAL: 1.0         # Exclusive contracts
}

class WrestlingWorld:
    """Manages all wrestling organizations and their interactions"""
    
    def __init__(self):
        self.organizations: Dict[str, WrestlingOrganization] = {}
        
    def create_organization(self, name: str, tier: OrganizationTier) -> WrestlingOrganization:
        """Create a new wrestling organization"""
        org = WrestlingOrganization(
            name=name,
            tier=tier,
            schedule=TIER_SCHEDULES[tier],
            roster_reqs=TIER_ROSTER_REQUIREMENTS[tier]
        )
        self.organizations[name] = org
        return org
    
    def get_available_spots(self, min_tier: OrganizationTier) -> List[WrestlingOrganization]:
        """Get organizations with roster spots available at or above the specified tier"""
        return [
            org for org in self.organizations.values()
            if org.tier.value >= min_tier.value
            and org.current_roster_size < org.roster_reqs.max_total_roster
        ]
    
    def get_organizations_by_tier(self, tier: OrganizationTier) -> List[WrestlingOrganization]:
        """Get all organizations of a specific tier"""
        return [org for org in self.organizations.values() if org.tier == tier]

    def calculate_weekly_events(self) -> Dict[EventType, int]:
        """Calculate total weekly events across all organizations"""
        totals = {event_type: 0 for event_type in EventType}
        
        for org in self.organizations.values():
            if not org.active:
                continue
                
            totals[EventType.HOUSE_SHOW] += org.schedule.house_shows_per_week
            totals[EventType.TV_SHOW] += org.schedule.tv_shows_per_week
            totals[EventType.SPECIAL_EVENT] += org.schedule.special_events_per_year / 52
            totals[EventType.PPV] += org.schedule.ppvs_per_year / 52
            
        return totals

    def estimate_total_roster_spots(self) -> Dict[OrganizationTier, Dict[str, int]]:
        """
        Estimate total roster spots available in the wrestling world by tier.
        Returns detailed breakdown of roster spots needed.
        """
        detailed_spots = {}
        total_wrestlers = 0
        
        for tier in OrganizationTier:
            reqs = TIER_ROSTER_REQUIREMENTS[tier]
            num_promotions = PROMOTIONS_PER_TIER[tier]
            
            # Calculate totals for this tier
            main_roster_total = reqs.min_main_roster * num_promotions
            midcard_total = reqs.min_midcard * num_promotions
            jobber_total = reqs.min_jobbers * num_promotions
            tier_total = main_roster_total + midcard_total + jobber_total
            
            detailed_spots[tier] = {
                'promotions': num_promotions,
                'main_roster_spots': main_roster_total,
                'midcard_spots': midcard_total,
                'jobber_spots': jobber_total,
                'total_spots': tier_total
            }
            
            total_wrestlers += tier_total
            
        # Add total to the output
        detailed_spots['TOTAL_WRESTLERS_NEEDED'] = total_wrestlers
        return detailed_spots

    def calculate_actual_wrestlers_needed(self) -> Dict[str, int]:
        """
        Calculate the actual number of unique wrestlers needed, accounting for
        wrestlers working multiple promotions at indie levels.
        """
        spots = self.estimate_total_roster_spots()
        total_spots = spots.pop('TOTAL_WRESTLERS_NEEDED')
        actual_wrestlers = 0
        
        for tier in OrganizationTier:
            tier_data = spots[tier]
            # Divide total spots by average promotions per wrestler
            actual_tier_wrestlers = int(tier_data['total_spots'] / TYPICAL_PROMOTIONS_PER_WRESTLER[tier])
            actual_wrestlers += actual_tier_wrestlers
        
        return {
            'total_roster_spots': total_spots,
            'unique_wrestlers_needed': actual_wrestlers
        }

    def print_detailed_requirements(self) -> None:
        """Print detailed breakdown of wrestler requirements including shared spots"""
        spots = self.estimate_total_roster_spots()
        total_spots = spots.pop('TOTAL_WRESTLERS_NEEDED')
        actual = self.calculate_actual_wrestlers_needed()
        
        print("\nDETAILED WRESTLING WORLD BREAKDOWN:")
        print("=" * 50)
        
        for tier in OrganizationTier:
            tier_data = spots[tier]
            print(f"\n{tier.name} TIER:")
            print(f"Number of promotions: {tier_data['promotions']}")
            print(f"Average promotions per wrestler: {TYPICAL_PROMOTIONS_PER_WRESTLER[tier]}")
            print(f"Total roster spots: {tier_data['total_spots']}")
            print(f"Breakdown:")
            print(f"  Main Event: {tier_data['main_roster_spots']}")
            print(f"  Midcard: {tier_data['midcard_spots']}")
            print(f"  Enhancement: {tier_data['jobber_spots']}")
            actual_wrestlers = int(tier_data['total_spots'] / TYPICAL_PROMOTIONS_PER_WRESTLER[tier])
            print(f"Estimated unique wrestlers: {actual_wrestlers}")
            print("-" * 30)
        
        print(f"\nTOTAL ROSTER SPOTS: {total_spots}")
        print(f"ESTIMATED UNIQUE WRESTLERS: {actual['unique_wrestlers_needed']}") 