import streamlit as st
import os
import re
from dotenv import load_dotenv
from frontend.streamlit_ui import CiteRightUI
from backend.orchestrator import run_pipeline

# Load environment variables
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
        st.error(f"Error reading API key from .env file: {e}")

# Ensure API key is set
if not api_key or api_key.startswith("your_api"):
    st.error("Valid OpenAI API key is not found. Please set it in your .env file.")
    st.stop()

# Configure the page
st.set_page_config(
    page_title="CiteRight - Literature Review Generator",
    page_icon="📚",
    layout="wide"
)

# Initialize and render UI
ui = CiteRightUI()
user_input = ui.render()

# Process input if submitted
if user_input:
    try:
        with st.spinner("Generating literature review..."):
            result = run_pipeline(user_input)
            
            # Display the review
            st.markdown("### 📄 Literature Review")
            st.write(result)
            
            # You could expand this to show more details if your
            # run_pipeline function returns a dictionary instead of just the review
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.warning("Please check your inputs and try again.")