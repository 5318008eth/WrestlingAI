import unittest
import logging
import os
import json
from datetime import date
from src.game.generator.character_generator import (
    CharacterGenerator, WWWCharacter, Move, 
    Relationship
)
from src.game.core.wrestling_archetypes import (
    Gender, Nationality, WrestlingStyle, Gimmick,
    STYLE_PHYSIQUES, STYLE_SYNERGIES, STYLE_MOVES
)
from src.game.core.wrestler_stats import (
    WrestlingStats, CareerStage, WrestlingRank, SubSkill,
    SUBSKILL_MAPPING
)
from enum import Enum, auto
from unittest.mock import MagicMock

# Set up logging
log_dir = "tests/logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{log_dir}/character_generator_test.log'),
        logging.StreamHandler()  # Also print to console
    ]
)

class Alignment(Enum):
    """Wrestler's alignment on the face/heel spectrum"""
    FACE = 100    # Pure good guy
    TWEENER = 0   # Neutral/ambiguous
    HEEL = -100   # Pure bad guy

class TestCharacterGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test class and create output directory"""
        cls.output_dir = "tests/output"
        if not os.path.exists(cls.output_dir):
            os.makedirs(cls.output_dir)
        logging.info("Starting Character Generator Tests")

    def setUp(self):
        """Set up test data"""
        logging.info(f"\nStarting test: {self._testMethodName}")
        self.generator = CharacterGenerator()
        self.technician = WWWCharacter(
            name="The Code Master",
            real_name="John Smith",
            birth_date="1990-01-01",
            gender=Gender.MALE,
            nationality=Nationality.AMERICAN,
            height=72.0,
            weight=200,
            physical_appearance="Lean athletic build, wears coding-themed gear",
            character_description="A former software engineer who uses his technical expertise in the ring",
            primary_style=WrestlingStyle.TECHNICAL,
            gimmick=Gimmick.MAT_TECHNICIAN,
            alignment=50,
            stats=WrestlingStats(
                body=3,
                look=3,
                real=4,
                work=5,
                fire=4,
                experience=8,
                fans=1000,
                career_stage=CareerStage.VETERAN,
                rank=WrestlingRank.NATIONAL,
                overness=70,
                momentum=50,
                fatigue=0,
                damage=0
            ),
            background="Former competitive programmer turned wrestler",
            entrance="Enters while typing on a mechanical keyboard"
        )
        
        self.monster = WWWCharacter(
            name="The Data Destroyer",
            real_name="Michael Johnson",
            birth_date="1988-06-15",
            gender=Gender.MALE,
            nationality=Nationality.AMERICAN,
            height=78.0,
            weight=300,
            physical_appearance="Massive build, wears black and red gear with circuit patterns",
            character_description="A mysterious entity that emerged from a corrupted database, using technology to destroy his opponents",
            primary_style=WrestlingStyle.POWERHOUSE,
            gimmick=Gimmick.MONSTER,
            alignment=-50,
            stats=WrestlingStats(
                body=5,
                look=3,
                real=4,
                work=3,
                fire=4,
                experience=10,
                fans=2000,
                career_stage=CareerStage.VETERAN,
                rank=WrestlingRank.NATIONAL,
                overness=80,
                momentum=60,
                fatigue=0,
                damage=0
            ),
            background="Mysterious entity that emerged from a corrupted database",
            entrance="Screens glitch out, lights flicker, enters through smoke",
            finisher=Move("Data Crash", "A power move that showcases raw strength", "Finisher"),
            signature_moves=[
                Move("System Overload", "A powerful slam that demonstrates pure power", "Signature"),
                Move("Memory Dump", "A power-based slam showing incredible force", "Signature")
            ],
            relationships=[],
            current_league="Global Wrestling Federation",
            previous_leagues=["Independent Wrestling Alliance"],
            titles_held=["World Championship"]
        )

    def tearDown(self):
        """Clean up after each test"""
        logging.info(f"Completed test: {self._testMethodName}\n")

    def save_test_output(self, data, filename):
        """Save test output to JSON file"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        logging.info(f"Saved test output to {filepath}")

    def test_create_basic_character(self):
        """Test creating a basic character with minimal attributes."""
        character = self.technician
        
        # Test basic attributes
        self.assertEqual(character.name, "The Code Master")
        self.assertEqual(character.primary_style, WrestlingStyle.TECHNICAL)
        self.assertEqual(character.alignment, 50)  # Face
        self.assertEqual(character.stats.body, 3)
        self.assertEqual(character.stats.look, 3)
        self.assertEqual(character.stats.real, 4)
        self.assertEqual(character.stats.work, 5)
        self.assertEqual(character.stats.fire, 4)
        
        # Test character sheet generation
        sheet = character.generate_character_sheet()
        self.assertIsInstance(sheet, str)
        self.assertIn("The Code Master", sheet)
        self.assertIn("STATS", sheet)
        self.assertIn("SUBSKILLS", sheet)

    def test_create_monster_heel(self):
        """Test creating a monster heel character."""
        character = self.monster
        
        # Test basic attributes
        self.assertEqual(character.name, "The Data Destroyer")
        self.assertEqual(character.primary_style, WrestlingStyle.POWERHOUSE)
        self.assertEqual(character.alignment, -50)  # Heel
        self.assertEqual(character.stats.body, 5)
        self.assertEqual(character.stats.look, 3)
        self.assertEqual(character.stats.real, 4)
        self.assertEqual(character.stats.work, 3)
        self.assertEqual(character.stats.fire, 4)
        
        # Test monster-specific attributes
        self.assertEqual(character.gimmick, Gimmick.MONSTER)
        self.assertIsNotNone(character.finisher)
        self.assertIsInstance(character.signature_moves, list)

    def test_name_generation(self):
        """Test wrestler name generation"""
        logging.info("\nStarting test: test_name_generation")
        name = self.generator.generate_name(Gender.MALE)
        self.assertIsInstance(name, str)
        self.assertGreater(len(name), 0)
        logging.info("Completed test: test_name_generation")

    def test_physical_attributes_generation(self):
        """Test physical attributes generation"""
        # Test powerhouse attributes
        self.generator.generate_wrestling_style = lambda: WrestlingStyle.POWERHOUSE
        demographics = self.generator.generate_demographics()
        self.assertIsInstance(demographics['height'], float)
        self.assertIsInstance(demographics['weight'], int)
        self.assertGreaterEqual(demographics['height'], STYLE_PHYSIQUES[WrestlingStyle.POWERHOUSE].min_height)
        self.assertLessEqual(demographics['height'], STYLE_PHYSIQUES[WrestlingStyle.POWERHOUSE].max_height)
        self.assertGreaterEqual(demographics['weight'], STYLE_PHYSIQUES[WrestlingStyle.POWERHOUSE].min_weight)
        self.assertLessEqual(demographics['weight'], STYLE_PHYSIQUES[WrestlingStyle.POWERHOUSE].max_weight)
        
        # Test high flyer attributes
        self.generator.generate_wrestling_style = lambda: WrestlingStyle.HIGH_FLYER
        demographics = self.generator.generate_demographics()
        self.assertIsInstance(demographics['height'], float)
        self.assertIsInstance(demographics['weight'], int)
        self.assertGreaterEqual(demographics['height'], STYLE_PHYSIQUES[WrestlingStyle.HIGH_FLYER].min_height)
        self.assertLessEqual(demographics['height'], STYLE_PHYSIQUES[WrestlingStyle.HIGH_FLYER].max_height)
        self.assertGreaterEqual(demographics['weight'], STYLE_PHYSIQUES[WrestlingStyle.HIGH_FLYER].min_weight)
        self.assertLessEqual(demographics['weight'], STYLE_PHYSIQUES[WrestlingStyle.HIGH_FLYER].max_weight)

    def test_display_character_sheets(self):
        """Display full character sheets for visual inspection."""
        logging.info("\nStarting test: test_display_character_sheets")
        print("\n=== THE CODE MASTER CHARACTER SHEET ===\n")
        print(self.technician.generate_character_sheet())
        print("\n=== THE DATA DESTROYER CHARACTER SHEET ===\n")
        print(self.monster.generate_character_sheet())
        logging.info("Completed test: test_display_character_sheets")

    def test_demographic_generation(self):
        """Test demographic information generation"""
        logging.info("\nStarting test: test_demographic_generation")
        demographics = self.generator.generate_demographics()
        self.assertIsInstance(demographics['nationality'], Nationality)
        self.assertIsInstance(demographics['gender'], Gender)
        self.assertIsInstance(demographics['height'], float)
        self.assertIsInstance(demographics['weight'], int)
        logging.info("Completed test: test_demographic_generation")

    def test_wrestling_style_generation(self):
        """Test wrestling style generation"""
        logging.info("\nStarting test: test_wrestling_style_generation")
        style = self.generator.generate_wrestling_style()
        self.assertIsInstance(style, WrestlingStyle)
        self.assertIn(style, WrestlingStyle)
        logging.info("Completed test: test_wrestling_style_generation")

    def test_alignment_generation(self):
        """Test alignment generation"""
        logging.info("\nStarting test: test_alignment_generation")
        alignments = []
        for _ in range(100):
            alignments.append(self.generator.generate_alignment())
        
        face_count = alignments.count(Alignment.FACE.value)
        heel_count = alignments.count(Alignment.HEEL.value)
        tweener_count = alignments.count(Alignment.TWEENER.value)
        
        # Verify reasonable distribution
        self.assertGreater(face_count, 20)  # At least 20% faces
        self.assertGreater(heel_count, 20)  # At least 20% heels
        self.assertGreater(tweener_count, 10)  # At least 10% tweeners
        logging.info("Completed test: test_alignment_generation")

    def test_stats_generation(self):
        """Test wrestling stats generation"""
        logging.info("\nStarting test: test_stats_generation")
        powerhouse_stats = self.generator.generate_stats(WrestlingStyle.POWERHOUSE)
        self.assertIsInstance(powerhouse_stats, WrestlingStats)
        self.assertGreater(powerhouse_stats.body, 3)  # Powerhouse should have high body stat
        
        technical_stats = self.generator.generate_stats(WrestlingStyle.TECHNICAL)
        self.assertIsInstance(technical_stats, WrestlingStats)
        self.assertGreater(technical_stats.work, 3)  # Technical should have high work stat
        logging.info("Completed test: test_stats_generation")

    def test_gimmick_generation(self):
        """Test gimmick generation"""
        logging.info("\nStarting test: test_gimmick_generation")
        gimmick = self.generator.generate_gimmick()
        self.assertIsInstance(gimmick, Gimmick)
        self.assertIn(gimmick, Gimmick)
        
        # Test gimmick with alignment influence
        heel_gimmick = self.generator.generate_gimmick(alignment=Alignment.HEEL.value)
        self.assertIsInstance(heel_gimmick, Gimmick)
        self.assertIn(heel_gimmick, Gimmick)
        logging.info("Completed test: test_gimmick_generation")

    def test_experience_generation(self):
        """Test experience level generation and career stats"""
        logging.info("\nStarting test: test_experience_generation")
        levels = [self.generator.generate_experience_level() for _ in range(100)]
        
        # Verify distribution
        rookie_pct = levels.count(CareerStage.ROOKIE) / len(levels)
        established_pct = levels.count(CareerStage.ESTABLISHED) / len(levels)
        veteran_pct = levels.count(CareerStage.VETERAN) / len(levels)
        
        # Verify reasonable distribution
        self.assertGreater(rookie_pct, 0.2)  # At least 20% rookies
        self.assertGreater(established_pct, 0.3)  # At least 30% established
        self.assertGreater(veteran_pct, 0.2)  # At least 20% veterans
        logging.info("Completed test: test_experience_generation")

    def test_career_progression(self):
        """Test career progression logic"""
        logging.info("\nStarting test: test_career_progression")
        rookie = WWWCharacter(
            name="The Rookie",
            real_name="John Doe",
            birth_date="2000-01-01",
            gender=Gender.MALE,
            nationality=Nationality.AMERICAN,
            height=72.0,
            weight=200,
            physical_appearance="Young and athletic",
            character_description="A promising young wrestler just starting their career",
            primary_style=WrestlingStyle.TECHNICAL,
            gimmick=Gimmick.MAT_TECHNICIAN,
            alignment=50,  # Face
            stats=WrestlingStats(
                body=2,
                look=2,
                real=2,
                work=2,
                fire=2,
                experience=0,
                fans=100,
                career_stage=CareerStage.ROOKIE,
                rank=WrestlingRank.LOCAL,
                overness=30,
                momentum=50,
                fatigue=0,
                damage=0
            ),
            background="Fresh out of wrestling school",
            entrance="Basic entrance with high energy"
        )
        
        # Test progression
        self.assertEqual(rookie.stats.career_stage, CareerStage.ROOKIE)
        rookie.stats.add_experience(2000)
        self.assertEqual(rookie.stats.career_stage, CareerStage.PROSPECT)
        logging.info("Completed test: test_career_progression")

    def test_complete_character_generation(self):
        """Test complete character generation"""
        logging.info("\nStarting test: test_complete_character_generation")
        logging.info("Testing complete character generation")
        
        from datetime import date
        
        # Test female character generation
        test_birth_date = date(1995, 1, 1)
        self.generator.generate_demographics = MagicMock(return_value={
            'gender': Gender.FEMALE,
            'nationality': Nationality.AMERICAN,
            'birth_date': test_birth_date,
            'height': 68.0,
            'weight': 150
        })
        
        female_character = self.generator.generate_character()
        
        # Verify basic attributes
        self.assertIsNotNone(female_character)
        self.assertIsInstance(female_character, WWWCharacter)
        self.assertEqual(female_character.gender, Gender.FEMALE)
        self.assertEqual(female_character.nationality, Nationality.AMERICAN)
        self.assertEqual(female_character.birth_date, test_birth_date)
        self.assertEqual(female_character.height, 68.0)
        self.assertEqual(female_character.weight, 150)
        
        # Verify AI-generated fields are present
        self.assertIsNotNone(female_character.real_name)
        self.assertIsNotNone(female_character.character_description)
        self.assertIsInstance(female_character.real_name, str)
        self.assertIsInstance(female_character.character_description, str)
        
        # Test male character generation
        test_birth_date = date(1990, 1, 1)
        self.generator.generate_demographics = MagicMock(return_value={
            'gender': Gender.MALE,
            'nationality': Nationality.CANADIAN,
            'birth_date': test_birth_date,
            'height': 72.0,
            'weight': 220
        })
        
        male_character = self.generator.generate_character()
        
        # Verify basic attributes
        self.assertIsNotNone(male_character)
        self.assertIsInstance(male_character, WWWCharacter)
        self.assertEqual(male_character.gender, Gender.MALE)
        self.assertEqual(male_character.nationality, Nationality.CANADIAN)
        self.assertEqual(male_character.birth_date, test_birth_date)
        self.assertEqual(male_character.height, 72.0)
        self.assertEqual(male_character.weight, 220)
        
        # Verify AI-generated fields are present
        self.assertIsNotNone(male_character.real_name)
        self.assertIsNotNone(male_character.character_description)
        self.assertIsInstance(male_character.real_name, str)
        self.assertIsInstance(male_character.character_description, str)
        
        logging.info("Completed test: test_complete_character_generation")

    def test_finisher_generation(self):
        """Test finisher move generation"""
        logging.info("\nStarting test: test_finisher_generation")
        style_finishers = {
            WrestlingStyle.POWERHOUSE: "power",
            WrestlingStyle.TECHNICAL: "technical",
            WrestlingStyle.HIGH_FLYER: "aerial",
            WrestlingStyle.SHOWMAN: "dramatic",
            WrestlingStyle.FIGHTER: "strike",
            WrestlingStyle.BRAWLER: "brawl",
            WrestlingStyle.HARDCORE: "hardcore",
            WrestlingStyle.CEREBRAL: "cerebral"
        }
        
        for style, expected in style_finishers.items():
            finisher = self.generator.generate_finisher(style)
            self.assertIsInstance(finisher, Move)
            self.assertEqual(finisher.move_type, "Finisher")
            self.assertIn(expected, finisher.description.lower())
        logging.info("Completed test: test_finisher_generation")

    def test_character_relationships(self):
        """Test character relationship generation"""
        logging.info("\nStarting test: test_character_relationships")
        characters = [
            self.generator.generate_character() for _ in range(5)
        ]
        
        relationships = self.generator.generate_relationships(characters)
        
        # Verify relationship structure
        for char_name, char_relationships in relationships.items():
            self.assertIsInstance(char_relationships, dict)
            for other_name, relationship in char_relationships.items():
                self.assertIsInstance(relationship, Relationship)
                self.assertEqual(relationship.wrestler_name, other_name)
                self.assertIn(relationship.relationship_type, ["Ally", "Rival", "Enemy", "Friend"])
                self.assertGreaterEqual(relationship.heat, -2)
                self.assertLessEqual(relationship.heat, 2)
        logging.info("Completed test: test_character_relationships")

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        logging.info("Completed all Character Generator Tests")

if __name__ == '__main__':
    unittest.main(verbosity=2) 