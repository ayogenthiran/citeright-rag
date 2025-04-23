import streamlit as st
from frontend.streamlit_ui import CiteRightUI
from backend.orchestrator import run_pipeline

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