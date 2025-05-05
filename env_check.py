#!/usr/bin/env python3
"""
Script to debug environment variable loading
"""

import os
import sys
from dotenv import load_dotenv, find_dotenv

# Print Python version and current working directory
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")

# Check for .env file
env_file = find_dotenv()
if env_file:
    print(f"Found .env file at: {env_file}")
    # Show raw content
    with open(env_file, 'r') as f:
        print(f"Raw .env content: {f.read()}")
else:
    print("No .env file found!")

# Load environment variables
print("\nLoading environment variables...")
load_dotenv()

# Check OPENAI_API_KEY
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"OPENAI_API_KEY loaded: {api_key[:8]}...{api_key[-4:]}")
    print(f"OPENAI_API_KEY length: {len(api_key)}")
else:
    print("OPENAI_API_KEY not found in environment variables!")

# Check all environment variables with OPENAI in name
print("\nAll OPENAI-related environment variables:")
for key, value in os.environ.items():
    if "OPENAI" in key:
        print(f"{key}: {value[:8]}...{value[-4:] if len(value) > 12 else value}") 