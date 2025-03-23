import unittest
from unittest.mock import patch, MagicMock
import os
from src.ai_client import AIClient

class TestAIClient(unittest.TestCase):
    def setUp(self):
        """Set up test environment variables"""
        os.environ['OPENROUTER_API_KEY'] = 'test_key'
        self.client = AIClient()

    def test_init_without_api_key(self):
        """Test initialization without API key"""
        with patch.dict(os.environ, clear=True):
            with self.assertRaises(ValueError):
                AIClient()

    @patch('openai.OpenAI')
    def test_generate_response_success(self, mock_openai):
        """Test successful response generation"""
        # Mock the OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
        mock_response.model = "test-model"
        mock_response.usage.model_dump.return_value = {"total_tokens": 100}
        
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        response = self.client.generate_response("Test prompt")
        
        self.assertEqual(response["content"], "Test response")
        self.assertEqual(response["model"], "test-model")
        self.assertEqual(response["usage"], {"total_tokens": 100})

    @patch('openai.OpenAI')
    def test_generate_response_error(self, mock_openai):
        """Test error handling in response generation"""
        mock_openai.return_value.chat.completions.create.side_effect = Exception("API Error")
        
        response = self.client.generate_response("Test prompt")
        self.assertIn("error", response)
        self.assertEqual(response["error"], "API Error")

    @patch('openai.OpenAI')
    def test_generate_response_parameters(self, mock_openai):
        """Test parameter handling in generate_response"""
        self.client.generate_response(
            prompt="Test prompt",
            model="custom-model",
            max_tokens=500,
            temperature=0.5
        )
        
        mock_openai.return_value.chat.completions.create.assert_called_with(
            model="custom-model",
            messages=[{"role": "user", "content": "Test prompt"}],
            max_tokens=500,
            temperature=0.5
        )

    def test_client_configuration(self):
        """Test client configuration"""
        self.assertEqual(self.client.api_key, "test_key")
        self.assertIsNotNone(self.client.client)

if __name__ == '__main__':
    unittest.main() 