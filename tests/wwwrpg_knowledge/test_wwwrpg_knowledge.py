import sys
import os
from pathlib import Path
import unittest

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from ai_client import AIClient

class TestWWWRPGKnowledge(unittest.TestCase):
    def setUp(self):
        self.client = AIClient()
        
    def _process_response(self, response, test_name):
        print(f"\n=== {test_name} ===")
        if "error" in response:
            print(f"Error: {response['error']}")
            return False
        
        print(response.get("content", "No content returned"))
        if "usage" in response:
            print("\nToken Usage:", response["usage"])
        return True
        
    def test_character_creation(self):
        prompt = """You are an expert on the World Wide Wrestling RPG tabletop game. 
        Please explain the character creation process in detail.
        Include information about:
        1. Available character archetypes/gimmicks (list and describe at least 4)
        2. Stats and what they mean (explain each stat's purpose)
        3. The step-by-step process of creating a new wrestler
        4. How moves and special abilities work
        5. How to set up relationships with other wrestlers
        
        Please be specific to the WWWRPG system, not general wrestling knowledge."""
        
        response = self.client.generate_response(
            prompt,
            max_tokens=2000,
            temperature=0.7
        )
        success = self._process_response(response, "Character Creation Test")
        self.assertTrue(success, "API request failed")
        
    def test_game_mechanics(self):
        prompt = """You are an expert on the World Wide Wrestling RPG tabletop game.
        Explain the core game mechanics in detail:
        1. How does the basic move system work? Include examples of basic moves.
        2. What are the core mechanics for wrestling matches?
        3. How does the audience and heat system function?
        4. What are the basic moves available to all wrestlers?
        5. How do special moves and finishers work?
        6. Explain the momentum and injury systems
        
        Please be specific to the WWWRPG system rules, not general wrestling knowledge."""
        
        response = self.client.generate_response(
            prompt,
            max_tokens=2000,
            temperature=0.7
        )
        success = self._process_response(response, "Game Mechanics Test")
        self.assertTrue(success, "API request failed")

    def test_match_structure(self):
        prompt = """You are an expert on the World Wide Wrestling RPG tabletop game.
        Describe in detail how to run a wrestling match:
        1. How is a match structured from start to finish?
        2. What are the different ways to win?
        3. How do wrestlers interact with each other during matches?
        4. What role does the GM play during matches?
        5. How do you handle interference, managers, and tag team matches?
        6. How does commentary and audience reaction work?
        
        Please be specific to the WWWRPG system rules, not general wrestling knowledge."""
        
        response = self.client.generate_response(
            prompt,
            max_tokens=2000,
            temperature=0.7
        )
        success = self._process_response(response, "Match Structure Test")
        self.assertTrue(success, "API request failed")

    def test_creative(self):
        prompt = """You are an expert on the World Wide Wrestling RPG tabletop game.
        Create a detailed example wrestling character following the WWWRPG system:
        1. Their gimmick and background story
        2. Their complete stats and special moves (use the actual WWWRPG stats)
        3. Their relationships with other wrestlers
        4. Their signature moves and finishing move
        5. Their look and entrance
        6. Their wrestling style and character traits
        
        Make this character unique and interesting while following WWWRPG rules."""
        
        response = self.client.generate_response(
            prompt,
            max_tokens=2000,
            temperature=0.8  # Slightly higher temperature for creativity
        )
        success = self._process_response(response, "Creative Character Example Test")
        self.assertTrue(success, "API request failed")

if __name__ == '__main__':
    unittest.main(verbosity=2) 