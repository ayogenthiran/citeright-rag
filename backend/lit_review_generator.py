from backend.llm_client import call_llm
from typing import List, Dict, Any
import re

def generate_review(problem: str, papers: List[Dict[Any, Any]]) -> str:
    """Generate a literature review based on a problem statement and papers
    
    Args:
        problem: The research problem statement
        papers: List of paper dictionaries
        
    Returns:
        Generated literature review
    """
    if not papers:
        return "No papers available for review."
    
    try:
        # Extract citation information
        for paper in papers:
            # Extract year from published date if available
            if 'published' in paper and paper['published']:
                match = re.search(r'(\d{4})', paper['published'])
                paper['year'] = match.group(1) if match else 'n.d.'
            else:
                paper['year'] = 'n.d.'
                
            # Get first author's last name
            if 'authors' in paper and paper['authors']:
                first_author = paper['authors'][0]
                # Extract last name (assuming format is "First Last")
                last_name = first_author.split()[-1]
                paper['first_author_last'] = last_name
            else:
                paper['first_author_last'] = 'Unknown'
        
        # Create a more structured prompt
        abstracts = ""
        for i, paper in enumerate(papers):
            abstracts += f"Paper {i+1}:\n"
            abstracts += f"Title: {paper.get('title', 'Unknown')}\n"
            abstracts += f"Authors: {', '.join(paper.get('authors', ['Unknown']))}\n"
            abstracts += f"Year: {paper.get('year', 'n.d.')}\n"
            abstracts += f"Abstract: {paper.get('abstract', 'Not available')}\n\n"
        
        prompt = f"""
        Create a comprehensive literature review based on the following research problem and paper abstracts.
        
        Research Problem:
        {problem}

        Available Papers:
        {abstracts}

        Please structure the literature review with the following sections:
        1. Introduction: Provide context for the research problem.
        2. Current Approaches: Organize and discuss the different methodologies used across papers.
        3. Key Findings: Synthesize the main results and their implications.
        4. Research Gaps: Identify areas that need further investigation.
        5. Conclusion: Summarize the state of knowledge in this field.
        
        Use proper academic citation format [Author, Year] when referring to specific papers.
        Make connections between papers and highlight common themes or contradictions.
        """
        
        # Call LLM with appropriate parameters for longer content
        review = call_llm(prompt, max_tokens=2500, temperature=0.4)
        return review
        
    except Exception as e:
        print(f"Error generating literature review: {e}")
        return f"Error generating literature review: {str(e)}"