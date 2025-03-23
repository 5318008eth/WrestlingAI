import sys
import os
from pathlib import Path
import unittest

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from ai_client import AIClient

class TestWWWRPGAdvancedMechanics(unittest.TestCase):
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

    def test_special_match_types(self):
        prompt = """You are an expert on the World Wide Wrestling RPG tabletop game.
        Explain in detail how to run special match types:
        1. How do Ladder/TLC matches work mechanically?
        2. What are the rules for Steel Cage matches?
        3. How do you handle Battle Royale/Royal Rumble matches?
        4. What are the mechanics for Hardcore/No DQ matches?
        5. How do Championship matches differ from regular matches?
        6. What special rules apply to these match types?
        
        Please be specific to the WWWRPG system rules, not general wrestling knowledge."""
        
        response = self.client.generate_response(
            prompt,
            max_tokens=2000,
            temperature=0.7
        )
        success = self._process_response(response, "Special Match Types Test")
        self.assertTrue(success, "API request failed")

    def test_advanced_moves(self):
        prompt = """You are an expert on the World Wide Wrestling RPG tabletop game.
        Detail the advanced move systems:
        1. How do wrestlers gain and use Advanced Moves?
        2. What are some examples of Advanced Moves for each playbook?
        3. How do Advanced Moves interact with basic moves?
        4. What are the requirements for unlocking Advanced Moves?
        5. How do Advanced Moves affect match dynamics?
        6. Can you explain any special Advanced Move combinations?
        
        Please be specific to the WWWRPG system rules, not general wrestling knowledge."""
        
        response = self.client.generate_response(
            prompt,
            max_tokens=2000,
            temperature=0.7
        )
        success = self._process_response(response, "Advanced Moves Test")
        self.assertTrue(success, "API request failed")

    def test_booking_mechanics(self):
        prompt = """You are an expert on the World Wide Wrestling RPG tabletop game.
        Explain the booking and storyline mechanics:
        1. How does the Creative/Booking system work?
        2. What mechanics govern feuds and storylines?
        3. How are championships and title changes handled?
        4. What are the rules for managing stables and factions?
        5. How do you create and maintain long-term storylines?
        6. What mechanics exist for backstage politics and influence?
        
        Please be specific to the WWWRPG system rules, not general wrestling knowledge."""
        
        response = self.client.generate_response(
            prompt,
            max_tokens=2000,
            temperature=0.7
        )
        success = self._process_response(response, "Booking Mechanics Test")
        self.assertTrue(success, "API request failed")

    def test_gimmick_specific_rules(self):
        prompt = """You are an expert on the World Wide Wrestling RPG tabletop game.
        Detail the specific rules for each gimmick/playbook:
        1. What are the unique mechanics for The Monster?
        2. How do The Veteran's special abilities work?
        3. What makes The High Flyer's moveset different?
        4. How does The Anti-Hero's mechanics reflect their character?
        5. What special rules apply to The Manager?
        6. How do different gimmicks interact with each other?
        
        Please be specific to the WWWRPG system rules, not general wrestling knowledge."""
        
        response = self.client.generate_response(
            prompt,
            max_tokens=2000,
            temperature=0.7
        )
        success = self._process_response(response, "Gimmick Specific Rules Test")
        self.assertTrue(success, "API request failed")

    def test_advancement_system(self):
        prompt = """You are an expert on the World Wide Wrestling RPG tabletop game.
        Explain the character advancement system:
        1. How do wrestlers gain experience and level up?
        2. What options are available when advancing?
        3. How does advancement affect stats and moves?
        4. What are the long-term character development options?
        5. How do championship reigns affect advancement?
        6. What are the mechanics for retiring or changing gimmicks?
        
        Please be specific to the WWWRPG system rules, not general wrestling knowledge."""
        
        response = self.client.generate_response(
            prompt,
            max_tokens=2000,
            temperature=0.7
        )
        success = self._process_response(response, "Advancement System Test")
        self.assertTrue(success, "API request failed")

    def test_tag_team_mechanics(self):
        prompt = """You are an expert on the World Wide Wrestling RPG tabletop game.
        Detail the tag team wrestling mechanics:
        1. How do tag team matches work mechanically?
        2. What are the rules for tag team moves and combinations?
        3. How do tag team relationships affect gameplay?
        4. What special moves are available to tag teams?
        5. How does tag team advancement work?
        6. What are the mechanics for breaking up or forming tag teams?
        
        Please be specific to the WWWRPG system rules, not general wrestling knowledge."""
        
        response = self.client.generate_response(
            prompt,
            max_tokens=2000,
            temperature=0.7
        )
        success = self._process_response(response, "Tag Team Mechanics Test")
        self.assertTrue(success, "API request failed")

if __name__ == '__main__':
    unittest.main(verbosity=2) 