from backend.llm_client import call_llm

def generate_keywords(title, problem):
    """Generate search keywords for a research topic
    
    Args:
        title: The title of the research paper
        problem: The problem statement or research notes
        
    Returns:
        List of search keywords
    """
    if not title or not problem:
        raise ValueError("Title and problem statement are required")
        
    # Construct a more specific prompt to get well-formatted response
    prompt = f"""Generate 5-7 precise academic search keywords for this research topic.
Return ONLY a comma-separated list of keywords without numbering, explanation, or additional text.

TITLE: {title}
PROBLEM: {problem}

Example good response format: "keyword1, keyword2, keyword3, keyword4, keyword5"
"""
    
    try:
        response = call_llm(prompt, temperature=0.3)
        
        # First, try to parse as comma-separated list
        if "," in response:
            return [k.strip() for k in response.split(",") if k.strip()]
            
        # If that doesn't work, try to parse as a line-by-line list
        lines = [line.strip() for line in response.split("\n") if line.strip()]
        
        # Remove any numbering or bullet points from lines
        cleaned_lines = []
        for line in lines:
            # Handle numbered lists
            if ". " in line and line.split(". ")[0].isdigit():
                cleaned_lines.append(line.split(". ", 1)[1])
            # Handle bullet points
            elif line.startswith("•") or line.startswith("-") or line.startswith("*"):
                cleaned_lines.append(line[1:].strip())
            else:
                cleaned_lines.append(line)
        
        return cleaned_lines
        
    except Exception as e:
        print(f"Error generating keywords: {e}")
        # Return some default keywords based on title as fallback
        return [title.strip()]