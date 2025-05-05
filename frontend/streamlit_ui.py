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
        
        # Custom CSS for a more modern look
        st.markdown("""
        <style>
        .main-header {
            font-size: 4.2rem;
            font-weight: 800;
            color: #1E3A8A;
            margin-bottom: 0.5rem;
            letter-spacing: -0.05em;
        }
        .sub-header {
            font-size: 1.4rem;
            color: #4B5563;
            margin-bottom: 2rem;
        }
        .section-header {
            font-size: 1.5rem;
            font-weight: 600;
            color: #1E3A8A;
            margin-top: 1rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: none;
        }
        .result-container {
            padding: 1.5rem;
            background-color: #F9FAFB;
            border-radius: 0.5rem;
            border: 1px solid #E5E7EB;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Main header with logo and title - BIGGER TITLE
        st.markdown("<div class='main-header' style='text-align: center;'>📚 CiteRight</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-header' style='text-align: center;'>AI-Powered Literature Review Assistant</div>", unsafe_allow_html=True)
        
        # Split screen into two columns for input and output
        col1, col2 = st.columns([1, 2])
        
        # Input column
        with col1:
            st.markdown("<div class='section-header'>Research Details</div>", unsafe_allow_html=True)
            
            title = st.text_input("Title of your paper", 
                                 placeholder="Enter the title of your research paper")
            
            problem = st.text_area("Problem Statement / Research Notes", 
                                  height=150,
                                  placeholder="Describe your research problem or provide notes")
            
            seeds = st.text_area("Seed Papers (optional)", 
                                placeholder="Enter arXiv IDs or URLs, one per line")
            
            seed_papers = [s.strip() for s in seeds.split("\n") if s.strip()]
            
            # Generate button with improved styling
            generate_btn = st.button("Generate Literature Review", 
                                    type="primary", 
                                    use_container_width=True)
            
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
                    st.markdown("<div class='section-header'>Literature Review</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='result-container'>{results}</div>", unsafe_allow_html=True)
                    
                else:
                    # Handle structured result object
                    if results.get("status") == "error":
                        st.error(f"Error: {results.get('error')}")
                        
                    elif results.get("status") == "no_papers":
                        st.warning("No papers found")
                        st.write(results.get("review", "No review available"))
                        
                    else:
                        # Display results
                        st.markdown("<div class='section-header'>Literature Review</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='result-container'>{results.get('review', '')}</div>", unsafe_allow_html=True)
                        
                        # Display keywords if available
                        if "keywords" in results and results["keywords"]:
                            st.markdown("<div class='section-header'>Keywords Used</div>", unsafe_allow_html=True)
                            kw_cols = st.columns(min(len(results["keywords"]), 5))
                            for i, kw in enumerate(results["keywords"]):
                                col_idx = i % 5
                                with kw_cols[col_idx]:
                                    st.info(kw)
                        
                        # Display papers if available
                        if "papers" in results and results["papers"]:
                            st.markdown("<div class='section-header'>Referenced Papers</div>", unsafe_allow_html=True)
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
                # Minimal clean placeholder - no instructions text
                st.markdown("""
                <div style="display: flex; justify-content: center; align-items: center; height: 70vh; text-align: center;">
                    <div>
                        <div style="font-size: 5rem; margin-bottom: 1.5rem;">📝</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Create and render the UI
if __name__ == "__main__":
    ui = CiteRightUI()
    ui.render()