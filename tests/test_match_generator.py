import unittest
from datetime import datetime, timedelta
from src.game.generator.match_generator import (
    MatchType, MatchStipulation, MatchParticipant,
    Match, StorylineType, Storyline, MatchGenerator
)
from src.game.generator.character_generator import WWWCharacter, Alignment
from src.game.core.wrestling_organizations import WrestlingOrganization
from src.game.core.wrestling_leagues import Region

class TestMatchGenerator(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.generator = MatchGenerator()
        self.test_participants = [
            MatchParticipant(id=1, name="Test Wrestler 1", is_heel=True),
            MatchParticipant(id=2, name="Test Wrestler 2", is_heel=False),
            MatchParticipant(id=3, name="Test Wrestler 3", is_heel=True),
            MatchParticipant(id=4, name="Test Wrestler 4", is_heel=False)
        ]

    def test_match_type_generation(self):
        """Test match type generation"""
        # Test singles match type
        match_type = self.generator.generate_match_type(2)
        self.assertEqual(match_type, MatchType.SINGLES)
        
        # Test tag team match type
        match_type = self.generator.generate_match_type(4)
        self.assertEqual(match_type, MatchType.TAG_TEAM)
        
        # Test multi-person match type
        match_type = self.generator.generate_match_type(6)
        self.assertIn(match_type, [MatchType.BATTLE_ROYAL, MatchType.MULTI_MAN])

    def test_stipulation_generation(self):
        """Test match stipulation generation"""
        # Test championship match stipulation
        stip = self.generator.generate_stipulation(is_championship=True)
        self.assertEqual(stip, MatchStipulation.CHAMPIONSHIP)
        
        # Test rivalry match stipulation
        stip = self.generator.generate_stipulation(is_rivalry=True)
        self.assertIn(stip, [
            MatchStipulation.NO_DQ,
            MatchStipulation.CAGE_MATCH,
            MatchStipulation.LAST_MAN_STANDING
        ])
        
        # Test regular match stipulation
        stip = self.generator.generate_stipulation()
        self.assertIsInstance(stip, MatchStipulation)

    def test_match_duration_generation(self):
        """Test match duration generation"""
        # Test PPV main event duration
        duration = self.generator.generate_match_duration(
            is_ppv=True,
            is_main_event=True
        )
        self.assertGreaterEqual(duration, 20)
        self.assertLessEqual(duration, 60)
        
        # Test TV match duration
        duration = self.generator.generate_match_duration(
            is_ppv=False,
            is_main_event=False
        )
        self.assertGreaterEqual(duration, 5)
        self.assertLessEqual(duration, 30)

    def test_match_generation(self):
        """Test complete match generation"""
        # Test singles match generation
        singles_match = self.generator.generate_match(
            participants=self.test_participants[:2],
            is_ppv=True,
            is_main_event=True
        )
        
        self.assertIsInstance(singles_match, Match)
        self.assertEqual(singles_match.match_type, MatchType.SINGLES)
        self.assertEqual(len(singles_match.participants), 2)
        self.assertGreater(singles_match.duration, 0)
        
        # Test tag team match generation
        tag_match = self.generator.generate_match(
            participants=self.test_participants,
            is_ppv=False,
            is_main_event=False
        )
        
        self.assertIsInstance(tag_match, Match)
        self.assertEqual(tag_match.match_type, MatchType.TAG_TEAM)
        self.assertEqual(len(tag_match.participants), 4)
        self.assertGreater(tag_match.duration, 0)

    def test_storyline_generation(self):
        """Test storyline generation"""
        # Test championship storyline
        storyline = self.generator.generate_storyline(
            participants=self.test_participants[:2],
            storyline_type=StorylineType.CHAMPIONSHIP
        )
        
        self.assertIsInstance(storyline, Storyline)
        self.assertEqual(storyline.storyline_type, StorylineType.CHAMPIONSHIP)
        self.assertEqual(len(storyline.participants), 2)
        self.assertIsInstance(storyline.description, str)
        
        # Test rivalry storyline
        storyline = self.generator.generate_storyline(
            participants=self.test_participants[:2],
            storyline_type=StorylineType.RIVALRY
        )
        
        self.assertIsInstance(storyline, Storyline)
        self.assertEqual(storyline.storyline_type, StorylineType.RIVALRY)
        self.assertEqual(len(storyline.participants), 2)
        self.assertIsInstance(storyline.description, str)

    def test_match_card_generation(self):
        """Test match card generation"""
        # Test PPV match card
        ppv_card = self.generator.generate_match_card(
            roster=self.test_participants,
            is_ppv=True,
            organization=WrestlingOrganization.GLOBAL,
            region=Region.NORTH_AMERICA
        )
        
        self.assertIsInstance(ppv_card, list)
        self.assertGreater(len(ppv_card), 5)  # PPVs should have multiple matches
        self.assertTrue(any(match.is_main_event for match in ppv_card))
        
        # Test TV match card
        tv_card = self.generator.generate_match_card(
            roster=self.test_participants,
            is_ppv=False,
            organization=WrestlingOrganization.NATIONAL,
            region=Region.NORTH_AMERICA
        )
        
        self.assertIsInstance(tv_card, list)
        self.assertLess(len(tv_card), len(ppv_card))
        self.assertTrue(any(match.is_main_event for match in tv_card))

    def test_participant_availability(self):
        """Test participant availability tracking"""
        # Generate a match
        match = self.generator.generate_match(
            participants=self.test_participants[:2],
            is_ppv=True,
            is_main_event=True
        )
        
        # Check that participants are marked as used
        for participant in match.participants:
            self.assertTrue(self.generator.is_participant_used(participant.id))
        
        # Reset availability
        self.generator.reset_participant_availability()
        
        # Check that participants are available again
        for participant in match.participants:
            self.assertFalse(self.generator.is_participant_used(participant.id))

    def test_match_quality_calculation(self):
        """Test match quality calculation"""
        # Generate matches with different parameters
        high_quality_match = self.generator.generate_match(
            participants=self.test_participants[:2],
            is_ppv=True,
            is_main_event=True
        )
        
        regular_match = self.generator.generate_match(
            participants=self.test_participants[2:],
            is_ppv=False,
            is_main_event=False
        )
        
        # Calculate quality scores
        high_quality_score = self.generator.calculate_match_quality(high_quality_match)
        regular_quality_score = self.generator.calculate_match_quality(regular_match)
        
        # PPV main events should generally score higher
        self.assertGreater(high_quality_score, regular_quality_score)
        
        # Quality scores should be within valid range
        self.assertGreaterEqual(high_quality_score, 0)
        self.assertLessEqual(high_quality_score, 100)
        self.assertGreaterEqual(regular_quality_score, 0)
        self.assertLessEqual(regular_quality_score, 100)

if __name__ == '__main__':
    unittest.main() 