import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

class AIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        # Configure the client
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            default_headers={
                "HTTP-Referer": "https://github.com/yourusername/wrestlingai",  # Replace with your actual repo
                "X-Title": "WrestlingAI Project"  # Replace with your project name
            }
        )

    def generate_response(
        self,
        prompt: str,
        model: str = "deepseek/deepseek-r1:free",
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate a response using the OpenRouter API.
        
        Args:
            prompt (str): The input prompt for the model
            model (str): The model to use (default: deepseek-r1:free)
            max_tokens (int): Maximum number of tokens to generate
            temperature (float): Sampling temperature (0.0 to 1.0)
            
        Returns:
            Dict[str, Any]: The API response
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return {
                "content": response.choices[0].message.content,
                "model": response.model,
                "usage": response.usage.model_dump()
            }
        except Exception as e:
            return {"error": str(e)}

def main():
    # Example usage
    client = AIClient()
    prompt = "What are the key elements of professional wrestling?"
    
    response = client.generate_response(prompt)
    if "error" in response:
        print(f"Error: {response['error']}")
    else:
        print("Model Response:")
        print(response["content"])
        print("\nModel Used:", response["model"])
        print("Token Usage:", response["usage"])

if __name__ == "__main__":
    main() 