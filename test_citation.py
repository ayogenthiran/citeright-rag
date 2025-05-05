#!/usr/bin/env python3
"""
Test script for CiteRight to evaluate the optimized code
"""

import os
import time
import re
from dotenv import load_dotenv
from backend.keyword_generator import generate_keywords
from backend.arxiv_fetcher import fetch_papers
from backend.lit_review_generator import generate_review

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
            with open(env_path, 'r') as f:
                env_content = f.read()
                # Look for OPENAI_API_KEY pattern
                match = re.search(r'OPENAI_API_KEY=([^\s"\']+)', env_content)
                if match:
                    api_key = match.group(1)
                    os.environ["OPENAI_API_KEY"] = api_key
    except Exception as e:
        print(f"Error reading API key from .env file: {e}")

if not api_key or api_key.startswith("your_api"):
    print("Valid OPENAI_API_KEY not found! Please set it in your .env file.")
    exit(1)

print(f"Using API key: {api_key[:8]}...{api_key[-4:]}")

# Test data
test_title = "The Impact of Machine Learning on Healthcare"
test_problem = """
How are machine learning algorithms being used to improve healthcare outcomes, 
particularly in diagnostic accuracy and personalized treatment plans? 
I'm interested in recent advances, current limitations, and ethical considerations.
"""

def run_test():
    """Run a complete test of the CiteRight pipeline"""
    
    print(f"\n{'=' * 80}")
    print(f"TESTING CITERIGHT WITH GPT-4 OPTIMIZATION")
    print(f"{'=' * 80}")
    
    # Step 1: Generate keywords
    print("\n1. GENERATING KEYWORDS...")
    start_time = time.time()
    try:
        keywords = generate_keywords(test_title, test_problem)
        print(f"✓ Generated {len(keywords)} keywords in {time.time() - start_time:.2f} seconds")
        print(f"Keywords: {', '.join(keywords)}")
    except Exception as e:
        print(f"✗ Error generating keywords: {e}")
        return
    
    # Step 2: Fetch papers
    print("\n2. FETCHING PAPERS...")
    start_time = time.time()
    try:
        # Don't use seed papers for this test
        papers = fetch_papers(keywords, max_results=10)  # Increased to 10 for better coverage
        print(f"✓ Found {len(papers)} papers in {time.time() - start_time:.2f} seconds")
        
        # Display paper titles
        for i, paper in enumerate(papers, 1):
            print(f"  {i}. {paper.get('title')} ({paper.get('relevance_score', 'N/A'):.2f})")
    except Exception as e:
        print(f"✗ Error fetching papers: {e}")
        return
    
    # Step 3: Generate review
    print("\n3. GENERATING LITERATURE REVIEW...")
    start_time = time.time()
    try:
        review = generate_review(test_problem, papers)
        print(f"✓ Generated review in {time.time() - start_time:.2f} seconds")
        
        # Display review
        print("\n" + "=" * 80)
        print("LITERATURE REVIEW RESULT:")
        print("=" * 80 + "\n")
        print(review)
        print("\n" + "=" * 80)
    except Exception as e:
        print(f"✗ Error generating review: {e}")
        return
    
    print("\nTEST COMPLETED SUCCESSFULLY")

if __name__ == "__main__":
    run_test() 