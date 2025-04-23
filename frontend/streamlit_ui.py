import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.orchestrator import run_pipeline

class CiteRightUI:
    def __init__(self):
        # Initialize session state
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.results = None
    
    def render(self):
        """Render the UI components"""
        
        st.markdown("<h1 style='text-align: center;'>📚 CiteRight – Literature Review Assistant</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Generate comprehensive literature reviews with minimal input</p>", unsafe_allow_html=True)
        
        # Split screen into two columns for input and output
        col1, col2 = st.columns([1, 2])
        
        # Input column
        with col1:
            st.subheader("Research Details")
            
            title = st.text_input("Title of your paper", 
                                 help="Enter the title of your research paper")
            
            problem = st.text_area("Problem Statement / Research Notes", 
                                  height=150,
                                  help="Describe your research problem or provide notes")
            
            seeds = st.text_area("Seed Papers (optional)", 
                                help="Enter arXiv IDs or URLs, one per line")
            
            seed_papers = [s.strip() for s in seeds.split("\n") if s.strip()]
            
            # Generate button
            generate_btn = st.button("Generate Literature Review", 
                                    type="primary")
            
            # Process when button is clicked
            if generate_btn:
                # Validate inputs
                if not title:
                    st.error("Please enter a paper title")
                elif not problem:
                    st.error("Please enter a problem statement")
                else:
                    with st.spinner("Generating literature review... This may take a few minutes."):
                        try:
                            # Direct call to run_pipeline without threading
                            result = run_pipeline({
                                "title": title,
                                "problem": problem,
                                "seed_papers": seed_papers if seed_papers else []
                            })
                            
                            # Store the result in session state
                            st.session_state.results = result
                            
                            # Success message will appear below
                            st.success("Literature review generated successfully!")
                            
                            # Rerun to display results in the right column
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
        
        # Results column
        with col2:
            if st.session_state.results:
                results = st.session_state.results
                
                if isinstance(results, str):
                    # Handle simple string result (for compatibility with old run_pipeline)
                    st.subheader("Literature Review")
                    st.write(results)
                    
                else:
                    # Handle structured result object
                    if results.get("status") == "error":
                        st.error(f"Error: {results.get('error')}")
                        
                    elif results.get("status") == "no_papers":
                        st.warning("No papers found")
                        st.write(results.get("review", "No review available"))
                        
                    else:
                        # Display results
                        st.subheader("Literature Review")
                        st.write(results.get("review", ""))
                        
                        # Display keywords if available
                        if "keywords" in results and results["keywords"]:
                            st.subheader("Keywords Used")
                            kw_cols = st.columns(min(len(results["keywords"]), 5))
                            for i, kw in enumerate(results["keywords"]):
                                col_idx = i % 5
                                with kw_cols[col_idx]:
                                    st.info(kw)
                        
                        # Display papers if available
                        if "papers" in results and results["papers"]:
                            st.subheader("Referenced Papers")
                            for i, paper in enumerate(results["papers"]):
                                with st.expander(f"{i+1}. {paper.get('title', 'Unknown title')}"):
                                    if "authors" in paper:
                                        st.write(f"**Authors:** {', '.join(paper['authors'])}")
                                    if paper.get('published'):
                                        st.write(f"**Published:** {paper['published']}")
                                    
                                    if "abstract" in paper:
                                        st.write("**Abstract:**")
                                        st.write(paper['abstract'])
                                    
                                    if paper.get('pdf_url'):
                                        st.markdown(f"[View Paper]({paper['pdf_url']})")
            else:
                st.info("Enter your research details and click 'Generate Literature Review' to start")
                
                # Show example
                with st.expander("See an example"):
                    st.markdown("""
                    **Example input:**
                    
                    **Title:** Benefits of Regular Exercise on Mental Health
                    
                    **Problem Statement:** What are the psychological benefits of regular physical exercise on mental health, particularly for reducing symptoms of depression and anxiety? Looking for studies that examine the frequency, intensity, and types of exercise that show the most significant effects.
                    
                    **Seed Papers:**
                    (Leave empty for a simple test)
                    """)

# Create and render the UI
if __name__ == "__main__":
    ui = CiteRightUI()
    ui.render()