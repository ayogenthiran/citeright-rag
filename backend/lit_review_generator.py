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
        
        # If we have too many papers, process in batches
        if len(papers) > 5:  # Adjust this threshold based on your testing
            return _generate_review_in_batches(problem, papers)
        else:
            # Original implementation for small number of papers
            abstracts = ""
            for i, paper in enumerate(papers):
                abstracts += f"Paper {i+1}:\n"
                abstracts += f"Title: {paper.get('title', 'Unknown')}\n"
                abstracts += f"Authors: {', '.join(paper.get('authors', ['Unknown']))}\n"
                abstracts += f"Year: {paper.get('year', 'n.d.')}\n"
                # Use a shorter version of the abstract to save tokens
                abstract = paper.get('abstract', 'Not available')
                if len(abstract) > 500:  # Restored to 500 for GPT-4
                    abstract = abstract[:500] + "..."
                abstracts += f"Abstract: {abstract}\n\n"
            
            prompt = f"""You are an expert academic researcher creating a literature review. 
            
Research Problem: {problem}

Papers:
{abstracts}

Task: Generate a comprehensive literature review that synthesizes the given papers.

Response format:
1. Introduction (1-2 paragraphs): Context, importance, and scope of the research problem
2. Current Approaches (2-3 paragraphs): Methodologies across papers, organized by themes or approaches
3. Key Findings (2-3 paragraphs): Synthesize major results and their implications
4. Research Gaps (1-2 paragraphs): Identify unanswered questions and areas needing further investigation
5. Conclusion (1 paragraph): Summarize the state of knowledge and future directions

Guidelines:
- Use proper academic citation format [Author, Year] when referencing specific papers
- Identify connections, agreements, and contradictions between papers
- Focus on synthesizing information rather than summarizing individual papers
- Maintain an objective, scholarly tone 
- Provide depth of analysis appropriate for an expert audience
"""
            
            # GPT-4 can handle more tokens
            review = call_llm(prompt, max_tokens=1800, temperature=0.3)
            return review
        
    except Exception as e:
        print(f"Error generating literature review: {e}")
        return f"Error generating literature review: {str(e)}"

def _generate_review_in_batches(problem: str, papers: List[Dict[Any, Any]]) -> str:
    """Process papers in batches to avoid token limits
    
    Args:
        problem: The research problem statement
        papers: List of paper dictionaries
        
    Returns:
        Generated literature review
    """
    try:
        # Step 1: Summarize each paper individually first
        paper_summaries = []
        for paper in papers:
            # Create a mini-prompt for each paper
            mini_prompt = f"""Analyze this academic paper and provide a concise summary for a literature review.

Title: {paper.get('title', 'Unknown')}
Authors: {', '.join(paper.get('authors', ['Unknown']))}
Year: {paper.get('year', 'n.d.')}
Abstract: {paper.get('abstract', 'Not available')}

Provide:
1. Main methodology/approach (1-2 sentences)
2. Key findings and contributions (1-2 sentences)
3. Relevance to the research domain (1 sentence)
"""
            summary = call_llm(mini_prompt, max_tokens=200, temperature=0.3)
            paper_summaries.append({
                'title': paper.get('title', 'Unknown'),
                'authors': paper.get('authors', ['Unknown']),
                'first_author_last': paper.get('first_author_last', 'Unknown'),
                'year': paper.get('year', 'n.d.'),
                'summary': summary
            })
        
        # Step 2: Create a review from the summaries
        summaries_text = ""
        for i, paper in enumerate(paper_summaries):
            summaries_text += f"Paper {i+1}:\n"
            summaries_text += f"Title: {paper['title']}\n"
            summaries_text += f"Authors: {', '.join(paper['authors'])}\n"
            summaries_text += f"Year: {paper['year']}\n"
            summaries_text += f"Summary: {paper['summary']}\n\n"
        
        # Generate the combined review
        prompt = f"""You are an expert academic researcher creating a comprehensive literature review from paper summaries.

Research Problem: {problem}

Paper Summaries:
{summaries_text}

Task: Generate a scholarly literature review that synthesizes these paper summaries and identifies the current state of knowledge.

Response format:
1. Introduction (1-2 paragraphs): Context, importance, and scope of the research problem
2. Current Approaches (2-3 paragraphs): Group and compare methodologies by themes
3. Key Findings (2-3 paragraphs): Synthesize results and implications across papers
4. Research Gaps (1-2 paragraphs): Identify areas requiring further investigation
5. Conclusion (1 paragraph): Summarize state of knowledge and future directions

Guidelines:
- Use proper academic citation format [Author, Year]
- Highlight patterns, agreements, and contradictions between papers
- Create a coherent narrative rather than listing individual paper summaries
- Maintain an objective, scholarly tone
- Provide depth of analysis appropriate for an expert audience
"""
        
        review = call_llm(prompt, max_tokens=1800, temperature=0.3)
        return review
        
    except Exception as e:
        print(f"Error generating batched review: {e}")
        return f"Error generating literature review: {str(e)}"