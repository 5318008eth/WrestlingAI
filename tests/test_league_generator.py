import unittest
from datetime import datetime
from src.game.generator.league_generator import (
    LeagueNameGenerator, ChampionshipGenerator,
    MediaGenerator, EventScheduleGenerator,
    ShowNameGenerator, generate_league
)
from src.game.core.wrestling_leagues import (
    Region, MarketSize, Territory
)
from src.game.core.wrestling_organizations import WrestlingOrganization

class TestLeagueGenerator(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.territory = Territory(
            name="Test Territory",
            region=Region.NORTH_AMERICA,
            market_size=MarketSize.LARGE,
            population=10000000,
            active_promotions=5,
            max_promotions=10
        )

    def test_league_name_generation(self):
        """Test league name generation"""
        generator = LeagueNameGenerator()
        
        # Test name generation for different regions
        na_name = generator.generate_name(Region.NORTH_AMERICA, WrestlingOrganization.GLOBAL)
        self.assertIsInstance(na_name, str)
        self.assertGreater(len(na_name), 0)
        
        japan_name = generator.generate_name(Region.JAPAN, WrestlingOrganization.INTERNATIONAL)
        self.assertIsInstance(japan_name, str)
        self.assertGreater(len(japan_name), 0)
        
        # Test uniqueness
        names = set()
        for _ in range(10):
            name = generator.generate_name(Region.NORTH_AMERICA, WrestlingOrganization.GLOBAL)
            names.add(name)
        self.assertGreater(len(names), 5)  # At least 6 unique names

    def test_championship_generation(self):
        """Test championship generation"""
        generator = ChampionshipGenerator()
        
        # Test global promotion championships
        global_titles = generator.generate_championships(WrestlingOrganization.GLOBAL, Region.NORTH_AMERICA)
        self.assertIsInstance(global_titles, list)
        self.assertGreater(len(global_titles), 3)  # Should have multiple titles
        
        # Test local promotion championships
        local_titles = generator.generate_championships(WrestlingOrganization.INDIE_LOCAL, Region.NORTH_AMERICA)
        self.assertIsInstance(local_titles, list)
        self.assertLessEqual(len(local_titles), 3)  # Should have fewer titles

    def test_media_generation(self):
        """Test media distribution generation"""
        generator = MediaGenerator()
        
        # Test global promotion media
        tv_network, streaming = generator.generate_media_distribution(
            WrestlingOrganization.GLOBAL,
            Region.NORTH_AMERICA
        )
        self.assertIsInstance(tv_network, str)
        self.assertIsInstance(streaming, list)
        self.assertGreater(len(streaming), 0)
        
        # Test local promotion media
        local_tv, local_streaming = generator.generate_media_distribution(
            WrestlingOrganization.INDIE_LOCAL,
            Region.NORTH_AMERICA
        )
        self.assertIn(local_tv, [None, ""])  # Local promotions might not have TV
        self.assertLessEqual(len(local_streaming), 1)

    def test_event_schedule_generation(self):
        """Test event schedule generation"""
        generator = EventScheduleGenerator()
        
        # Test global promotion schedule
        global_schedule = generator.generate_yearly_schedule(
            WrestlingOrganization.GLOBAL,
            Region.NORTH_AMERICA
        )
        self.assertIsInstance(global_schedule, list)
        self.assertGreater(len(global_schedule), 50)  # Should have weekly shows + PPVs
        
        # Verify event structure
        event = global_schedule[0]
        self.assertIn('date', event)
        self.assertIn('name', event)
        self.assertIn('type', event)
        self.assertIn('match_card', event)
        
        # Test local promotion schedule
        local_schedule = generator.generate_yearly_schedule(
            WrestlingOrganization.INDIE_LOCAL,
            Region.NORTH_AMERICA
        )
        self.assertLess(len(local_schedule), len(global_schedule))

    def test_show_name_generation(self):
        """Test show name generation"""
        generator = ShowNameGenerator()
        
        # Test weekly show names
        weekly_name = generator.generate_weekly_show_name(Region.NORTH_AMERICA)
        self.assertIsInstance(weekly_name, str)
        self.assertGreater(len(weekly_name), 0)
        
        # Test secondary show names
        secondary_name = generator.generate_secondary_show_name(Region.NORTH_AMERICA)
        self.assertIsInstance(secondary_name, str)
        self.assertGreater(len(secondary_name), 0)
        
        # Test uniqueness
        names = set()
        for _ in range(10):
            name = generator.generate_weekly_show_name(Region.NORTH_AMERICA)
            names.add(name)
        self.assertGreater(len(names), 5)  # At least 6 unique names

    def test_complete_league_generation(self):
        """Test complete league generation"""
        # Test global promotion generation
        global_league = generate_league(
            self.territory,
            WrestlingOrganization.GLOBAL,
            current_year=datetime.now().year
        )
        
        # Verify league structure
        self.assertIsNotNone(global_league.name)
        self.assertIsNotNone(global_league.territory)
        self.assertIsNotNone(global_league.founding_year)
        self.assertIsNotNone(global_league.championships)
        self.assertIsNotNone(global_league.yearly_schedule)
        self.assertGreater(len(global_league.championships), 0)
        self.assertGreater(len(global_league.yearly_schedule), 0)
        
        # Test local promotion generation
        local_league = generate_league(
            self.territory,
            WrestlingOrganization.INDIE_LOCAL,
            current_year=datetime.now().year
        )
        
        # Verify simpler structure for local promotion
        self.assertLess(len(local_league.championships), len(global_league.championships))
        self.assertLess(len(local_league.yearly_schedule), len(global_league.yearly_schedule))

    def test_revenue_generation(self):
        """Test revenue generation for different tiers"""
        # Test global promotion revenue
        global_revenue = generate_league(
            self.territory,
            WrestlingOrganization.GLOBAL,
            current_year=datetime.now().year
        ).annual_revenue
        
        # Test international promotion revenue
        intl_revenue = generate_league(
            self.territory,
            WrestlingOrganization.INTERNATIONAL,
            current_year=datetime.now().year
        ).annual_revenue
        
        # Test national promotion revenue
        national_revenue = generate_league(
            self.territory,
            WrestlingOrganization.NATIONAL,
            current_year=datetime.now().year
        ).annual_revenue
        
        # Verify revenue hierarchy
        self.assertGreater(global_revenue, intl_revenue)
        self.assertGreater(intl_revenue, national_revenue)

if __name__ == '__main__':
    unittest.main() 