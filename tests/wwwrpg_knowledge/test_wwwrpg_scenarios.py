import sys
import os
from pathlib import Path
import unittest

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from ai_client import AIClient

class TestWWWRPGScenarios(unittest.TestCase):
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

    def test_injury_retirement(self):
        prompt = """You are an expert on the World Wide Wrestling RPG tabletop game.
        Explain how to handle injury and retirement scenarios:
        1. What are the mechanics for serious injuries?
        2. How do career-threatening injuries work?
        3. What are the rules for retirement angles?
        4. How do injury angles affect storylines?
        5. What mechanics exist for returning from injury?
        6. How do you handle permanent stat changes from injuries?
        
        Please be specific to the WWWRPG system rules, not general wrestling knowledge."""
        
        response = self.client.generate_response(
            prompt,
            max_tokens=2000,
            temperature=0.7
        )
        success = self._process_response(response, "Injury and Retirement Test")
        self.assertTrue(success, "API request failed")

    def test_championship_storylines(self):
        prompt = """You are an expert on the World Wide Wrestling RPG tabletop game.
        Detail how to run championship storylines:
        1. How do you establish a new championship?
        2. What are the mechanics for title defenses?
        3. How do you handle multiple championship scenarios?
        4. What are the rules for vacating titles?
        5. How do tournament mechanics work?
        6. What special rules apply to championship storylines?
        
        Please be specific to the WWWRPG system rules, not general wrestling knowledge."""
        
        response = self.client.generate_response(
            prompt,
            max_tokens=2000,
            temperature=0.7
        )
        success = self._process_response(response, "Championship Storylines Test")
        self.assertTrue(success, "API request failed")

    def test_faction_warfare(self):
        prompt = """You are an expert on the World Wide Wrestling RPG tabletop game.
        Explain how to run faction warfare storylines:
        1. What are the mechanics for creating factions?
        2. How do multi-person matches work?
        3. What are the rules for faction vs faction feuds?
        4. How do you handle betrayals and turns?
        5. What mechanics exist for faction leadership?
        6. How do you manage multiple storylines within factions?
        
        Please be specific to the WWWRPG system rules, not general wrestling knowledge."""
        
        response = self.client.generate_response(
            prompt,
            max_tokens=2000,
            temperature=0.7
        )
        success = self._process_response(response, "Faction Warfare Test")
        self.assertTrue(success, "API request failed")

    def test_gimmick_changes(self):
        prompt = """You are an expert on the World Wide Wrestling RPG tabletop game.
        Detail how to handle gimmick changes:
        1. What are the mechanics for changing gimmicks?
        2. How do you handle face/heel turns?
        3. What rules govern character evolution?
        4. How do you transition between playbooks?
        5. What happens to existing relationships and moves?
        6. How do you maintain continuity during changes?
        
        Please be specific to the WWWRPG system rules, not general wrestling knowledge."""
        
        response = self.client.generate_response(
            prompt,
            max_tokens=2000,
            temperature=0.7
        )
        success = self._process_response(response, "Gimmick Changes Test")
        self.assertTrue(success, "API request failed")

    def test_special_events(self):
        prompt = """You are an expert on the World Wide Wrestling RPG tabletop game.
        Explain how to run special wrestling events:
        1. How do you structure tournament events?
        2. What are the mechanics for season finales?
        3. How do you handle invasion angles?
        4. What rules exist for special attraction matches?
        5. How do you manage multiple storyline climaxes?
        6. What mechanics exist for major show dynamics?
        
        Please be specific to the WWWRPG system rules, not general wrestling knowledge."""
        
        response = self.client.generate_response(
            prompt,
            max_tokens=2000,
            temperature=0.7
        )
        success = self._process_response(response, "Special Events Test")
        self.assertTrue(success, "API request failed")

    def test_creative_control(self):
        prompt = """You are an expert on the World Wide Wrestling RPG tabletop game.
        Detail the creative control mechanics:
        1. How does creative control work mechanically?
        2. What are the rules for backstage influence?
        3. How do you handle creative disputes?
        4. What mechanics exist for booking power?
        5. How do championships affect creative control?
        6. What are the limits of creative control?
        
        Please be specific to the WWWRPG system rules, not general wrestling knowledge."""
        
        response = self.client.generate_response(
            prompt,
            max_tokens=2000,
            temperature=0.7
        )
        success = self._process_response(response, "Creative Control Test")
        self.assertTrue(success, "API request failed")

if __name__ == '__main__':
    unittest.main(verbosity=2) 