import unittest
from src.game.core.wrestling_archetypes import (
    Gender, Nationality, WrestlingStyle, Gimmick,
    PhysicalRanges, Wrestler, GimmickRestrictions,
    STYLE_PHYSIQUES, STYLE_SYNERGIES, STYLE_MOVES,
    GIMMICK_RESTRICTIONS
)

class TestWrestlingArchetypes(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.test_wrestler = Wrestler(
            name="Test Wrestler",
            gender=Gender.MALE,
            height=72,  # 6'0"
            weight=220,
            style=WrestlingStyle.TECHNICAL,
            gimmick=Gimmick.SUBMISSION_MASTER,
            alignment=50  # Face
        )

    def test_wrestling_style_physiques(self):
        """Test physical requirements for different styles"""
        # Test powerhouse requirements
        powerhouse_range = STYLE_PHYSIQUES[WrestlingStyle.POWERHOUSE]
        self.assertTrue(powerhouse_range.min_height >= 78)  # At least 6'6"
        self.assertTrue(powerhouse_range.min_weight >= 265)
        
        # Test high flyer requirements
        highflyer_range = STYLE_PHYSIQUES[WrestlingStyle.HIGH_FLYER]
        self.assertTrue(highflyer_range.max_height <= 72)  # Max 6'0"
        self.assertTrue(highflyer_range.max_weight <= 220)
        
        # Test all styles have valid ranges
        for style in WrestlingStyle:
            physique = STYLE_PHYSIQUES[style]
            self.assertTrue(physique.min_height < physique.max_height)
            self.assertTrue(physique.min_weight < physique.max_weight)

    def test_style_synergies(self):
        """Test wrestling style compatibility"""
        # Test strong synergies
        self.assertGreaterEqual(
            STYLE_SYNERGIES.get((WrestlingStyle.FIGHTER, WrestlingStyle.TECHNICAL), 0),
            0.9
        )
        
        # Test all synergies are within valid range
        for synergy in STYLE_SYNERGIES.values():
            self.assertTrue(0 <= synergy <= 1)
        
        # Test symmetry of synergies
        for (style1, style2), value in STYLE_SYNERGIES.items():
            reverse_value = STYLE_SYNERGIES.get((style2, style1))
            if reverse_value:
                self.assertEqual(value, reverse_value)

    def test_style_moves(self):
        """Test move sets for different styles"""
        # Test each style has moves
        for style in WrestlingStyle:
            self.assertTrue(len(STYLE_MOVES[style]) > 0)
        
        # Test move uniqueness
        for style, moves in STYLE_MOVES.items():
            self.assertEqual(len(moves), len(set(moves)))  # No duplicate moves
            
        # Test move appropriateness
        self.assertTrue(any("Submission" in move for move in STYLE_MOVES[WrestlingStyle.TECHNICAL]))
        self.assertTrue(any("Power" in move for move in STYLE_MOVES[WrestlingStyle.POWERHOUSE]))
        self.assertTrue(any("Flying" in move or "Aerial" in move for move in STYLE_MOVES[WrestlingStyle.HIGH_FLYER]))

    def test_gimmick_restrictions(self):
        """Test gimmick restrictions"""
        # Test style-locked gimmicks
        monster_restrictions = GIMMICK_RESTRICTIONS[Gimmick.MONSTER]
        self.assertEqual(monster_restrictions.required_style, WrestlingStyle.POWERHOUSE)
        
        # Test alignment restrictions
        heel_gimmick = GIMMICK_RESTRICTIONS[Gimmick.FOREIGN_MENACE]
        self.assertTrue(heel_gimmick.max_alignment < 0)
        
        face_gimmick = GIMMICK_RESTRICTIONS[Gimmick.PATRIOT]
        self.assertTrue(face_gimmick.min_alignment > 0)
        
        # Test physical restrictions
        giant_restrictions = GIMMICK_RESTRICTIONS[Gimmick.GIANT]
        self.assertTrue(giant_restrictions.min_height >= 80)  # At least 6'8"
        self.assertTrue(giant_restrictions.min_weight >= 320)

    def test_wrestler_gimmick_compatibility(self):
        """Test wrestler compatibility with different gimmicks"""
        # Test valid gimmick
        self.assertTrue(self.test_wrestler.can_use_gimmick(Gimmick.SUBMISSION_MASTER))
        
        # Test invalid style gimmick
        self.assertFalse(self.test_wrestler.can_use_gimmick(Gimmick.MONSTER))
        
        # Test invalid physical gimmick
        self.assertFalse(self.test_wrestler.can_use_gimmick(Gimmick.GIANT))
        
        # Test alignment-based gimmick
        self.assertTrue(self.test_wrestler.can_use_gimmick(Gimmick.PATRIOT))
        self.assertFalse(self.test_wrestler.can_use_gimmick(Gimmick.FOREIGN_MENACE))

    def test_nationality_completeness(self):
        """Test nationality enumeration"""
        # Test basic nationality properties
        self.assertTrue(len(Nationality) >= 10)  # Should have at least 10 nationalities
        self.assertIn(Nationality.AMERICAN, Nationality)
        self.assertIn(Nationality.JAPANESE, Nationality)
        
        # Test string representation
        for nationality in Nationality:
            self.assertTrue(isinstance(nationality.value, str))
            self.assertTrue(len(nationality.value) > 0)

if __name__ == '__main__':
    unittest.main() 