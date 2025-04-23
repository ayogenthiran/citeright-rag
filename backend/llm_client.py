import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)

def call_llm(prompt, model="gpt-4", temperature=0.3, max_tokens=1500):
    """Call the language model to generate a response
    
    Args:
        prompt: The prompt to send to the LLM
        model: The model to use (defaults to 'gpt-4')
        temperature: Controls randomness (0-1)
        max_tokens: Maximum tokens in the response
        
    Returns:
        Generated text as string
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        return f"Error generating content: {str(e)}"

