#!/usr/bin/env python3
"""
Test script to check OpenAI API key
"""

import os
import openai
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# If the key is not set or looks like a placeholder, try to read directly from .env file
if not api_key or api_key.startswith("your_api"):
    try:
        # Try to read directly from the .env file
        env_path = os.path.join(os.getcwd(), '.env')
        if os.path.exists(env_path):
            print(f"Reading API key directly from .env file: {env_path}")
            with open(env_path, 'r') as f:
                env_content = f.read()
                print(f"Raw .env content: {env_content}")
                # Look for OPENAI_API_KEY pattern
                match = re.search(r'OPENAI_API_KEY=([^\s"\']+)', env_content)
                if match:
                    api_key = match.group(1)
                    print(f"Extracted API key: {api_key[:8]}...{api_key[-4:]}")
    except Exception as e:
        print(f"Error reading API key from .env file: {e}")

if not api_key:
    print("No API key found!")
    exit(1)

print(f"Using API key: {api_key[:8]}...{api_key[-4:]}")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)

try:
    # Test a simple completion
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=10
    )
    
    print(f"SUCCESS! Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"ERROR: {e}") 