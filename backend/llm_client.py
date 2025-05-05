import os
import openai
import hashlib
import json
import re
from typing import Dict, Any, Optional
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# If the key is not set or looks like a placeholder, try to read directly from .env file
if not api_key or api_key.startswith("your_api"):
    try:
        # Try to read directly from the .env file
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                env_content = f.read()
                # Look for OPENAI_API_KEY pattern
                match = re.search(r'OPENAI_API_KEY=([^\s"\']+)', env_content)
                if match:
                    api_key = match.group(1)
    except Exception as e:
        print(f"Error reading API key from .env file: {e}")

if not api_key or api_key.startswith("your_api"):
    raise ValueError("Valid OPENAI_API_KEY not found. Please set it in your .env file.")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)

# In-memory cache for LLM responses
_llm_cache: Dict[str, str] = {}

def call_llm(prompt: str, model: str = "gpt-4", temperature: float = 0.3, max_tokens: int = 1500, use_cache: bool = True) -> str:
    """Call the language model to generate a response with caching
    
    Args:
        prompt: The prompt to send to the LLM
        model: The model to use (defaults to 'gpt-4')
        temperature: Controls randomness (0-1)
        max_tokens: Maximum tokens in the response
        use_cache: Whether to use cached responses (default True)
        
    Returns:
        Generated text as string
    """
    # Create a cache key based on inputs
    if use_cache:
        cache_key = _create_cache_key(prompt, model, temperature, max_tokens)
        
        # Check if we have a cached response
        cached_response = _get_cached_response(cache_key)
        if cached_response is not None:
            return cached_response
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        result = response.choices[0].message.content
        
        # Cache the response if caching is enabled
        if use_cache:
            _cache_response(cache_key, result)
        
        return result
        
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        return f"Error generating content: {str(e)}"

def _create_cache_key(prompt: str, model: str, temperature: float, max_tokens: int) -> str:
    """Create a unique cache key for the given parameters"""
    # Create a dictionary of parameters
    params = {
        "prompt": prompt,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    # Convert to a stable string representation and hash it
    params_str = json.dumps(params, sort_keys=True)
    return hashlib.md5(params_str.encode()).hexdigest()

def _get_cached_response(cache_key: str) -> Optional[str]:
    """Get a cached response if available"""
    return _llm_cache.get(cache_key)

def _cache_response(cache_key: str, response: str) -> None:
    """Cache a response"""
    _llm_cache[cache_key] = response

def clear_cache() -> None:
    """Clear the LLM response cache"""
    _llm_cache.clear()

