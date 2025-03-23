# WrestlingAI Project

This project uses OpenRouter's API to interact with the DeepSeek R1 model for AI-powered wrestling-related tasks.

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```
   Get your API key from [OpenRouter](https://openrouter.ai/keys)

4. Update the default headers in `src/ai_client.py` with your project details:
   - Set your GitHub repository URL in `HTTP-Referer`
   - Update the project name in `X-Title`

## Usage

Run the example script:
```bash
python src/ai_client.py
```

Use the AIClient in your own code:
```python
from src.ai_client import AIClient

client = AIClient()
response = client.generate_response(
    prompt="Your prompt here",
    model="deepseek/deepseek-r1:free",  # Optional: defaults to deepseek-r1:free
    max_tokens=1000,                     # Optional: defaults to 1000
    temperature=0.7                      # Optional: defaults to 0.7
)

print(response["content"])
```

## Features

- Easy integration with OpenRouter API
- Support for DeepSeek R1 model
- Configurable parameters (temperature, max tokens)
- Error handling and response formatting
- Environment variable configuration

## License

MIT # WrestlingAI
