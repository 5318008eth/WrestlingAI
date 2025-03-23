import unittest
from src.game.core.wrestler_stats import (
    CareerStage, WrestlingRank, SubSkill,
    WrestlingStats, SUBSKILL_MAPPING
)

class TestWrestlingStats(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.stats = WrestlingStats(
            body=3,
            look=4,
            real=2,
            work=5,
            fire=3,
            experience=5000,
            fans=50000,
            career_stage=CareerStage.ESTABLISHED,
            rank=WrestlingRank.NATIONAL
        )

    def test_core_stats_validation(self):
        """Test core stats validation"""
        # Test valid stats
        self.assertTrue(self.stats.is_valid())
        
        # Test invalid stats
        invalid_stats = WrestlingStats(
            body=6,  # Invalid: > 5
            look=4,
            real=2,
            work=-1,  # Invalid: < 0
            fire=3
        )
        self.assertFalse(invalid_stats.is_valid())

    def test_career_progression(self):
        """Test career stage progression"""
        stats = WrestlingStats()
        
        # Test rookie to prospect
        changed = stats.add_experience(1500)
        self.assertTrue(changed)
        self.assertEqual(stats.career_stage, CareerStage.PROSPECT)
        
        # Test no change when not enough experience
        changed = stats.add_experience(500)
        self.assertFalse(changed)
        self.assertEqual(stats.career_stage, CareerStage.PROSPECT)

    def test_fan_following(self):
        """Test fan following and rank changes"""
        stats = WrestlingStats()
        
        # Test rank increase
        changed = stats.update_fans(50000)
        self.assertTrue(changed)
        self.assertEqual(stats.rank, WrestlingRank.NATIONAL)
        
        # Test rank decrease
        changed = stats.update_fans(-45000)
        self.assertTrue(changed)
        self.assertEqual(stats.rank, WrestlingRank.REGIONAL)

    def test_match_status_updates(self):
        """Test match-related status updates"""
        # Test momentum changes
        self.stats.update_match_status(20, 10, 5)
        self.assertEqual(self.stats.momentum, 70)  # 50 + 20
        self.assertEqual(self.stats.fatigue, 10)
        self.assertEqual(self.stats.damage, 5)
        
        # Test bounds
        self.stats.update_match_status(50, 100, 100)
        self.assertEqual(self.stats.momentum, 100)  # Capped at 100
        self.assertEqual(self.stats.fatigue, 100)  # Capped at 100
        self.assertEqual(self.stats.damage, 100)  # Capped at 100

    def test_rest_function(self):
        """Test rest function"""
        self.stats.update_match_status(20, 50, 30)
        self.stats.rest()
        
        self.assertEqual(self.stats.momentum, 50)  # Reset to default
        self.assertEqual(self.stats.fatigue, 0)
        self.assertEqual(self.stats.damage, 0)

    def test_performance_bonus(self):
        """Test performance bonus calculation"""
        # Test base performance
        bonus = self.stats.get_performance_bonus()
        self.assertGreaterEqual(bonus, 0.5)
        self.assertLessEqual(bonus, 2.0)
        
        # Test with high fatigue/damage
        self.stats.update_match_status(0, 90, 90)
        fatigued_bonus = self.stats.get_performance_bonus()
        self.assertLess(fatigued_bonus, bonus)

    def test_subskill_system(self):
        """Test sub-skill system"""
        # Test sub-skill bonus calculation
        power_bonus = self.stats.get_subskill_bonus(SubSkill.POWER)
        self.assertEqual(power_bonus, self.stats.body - 2)
        
        # Test skill check
        success, margin = self.stats.skill_check(SubSkill.TECHNICAL, 10)
        self.assertIsInstance(success, bool)
        self.assertIsInstance(margin, int)
        
        # Test sub-skill mapping
        for subskill in SubSkill:
            self.assertIn(SUBSKILL_MAPPING[subskill], ['body', 'look', 'real', 'work', 'fire'])

    def test_promo_performance(self):
        """Test promo performance system"""
        quality, highlights = self.stats.perform_promo()
        
        self.assertIsInstance(quality, int)
        self.assertTrue(0 <= quality <= 100)
        self.assertIsInstance(highlights, list)
        
        # Test high charisma impact
        high_charisma = WrestlingStats(look=5)  # High look affects charisma
        high_quality, _ = high_charisma.perform_promo()
        self.assertGreater(high_quality, 50)

    def test_match_sequence(self):
        """Test match sequence system"""
        # Test easy sequence
        success, commentary = self.stats.perform_match_sequence(8)
        self.assertIsInstance(success, bool)
        self.assertIsInstance(commentary, list)
        
        # Test difficult sequence
        hard_success, hard_commentary = self.stats.perform_match_sequence(18)
        self.assertIsInstance(hard_success, bool)
        self.assertIsInstance(hard_commentary, list)

    def test_comeback_system(self):
        """Test comeback system"""
        # Test normal comeback
        success, description = self.stats.attempt_comeback()
        self.assertIsInstance(success, bool)
        self.assertIsInstance(description, str)
        
        # Test comeback while damaged
        self.stats.update_match_status(0, 0, 60)  # Add damage
        damaged_success, damaged_description = self.stats.attempt_comeback()
        self.assertIsInstance(damaged_success, bool)
        self.assertIsInstance(damaged_description, str)

if __name__ == '__main__':
    unittest.main() 