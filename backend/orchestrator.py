from backend.keyword_generator import generate_keywords
from backend.arxiv_fetcher import fetch_papers
from backend.lit_review_generator import generate_review
from typing import Dict, Any, List, Optional, Callable

class Orchestrator:
    """Main coordinator for the CiteRight workflow"""
    
    def __init__(self):
        """Initialize the orchestrator"""
        # State tracking
        self.current_state = {
            "status": "idle",
            "keywords": [],
            "papers": [],
            "review": "",
            "progress": 0,
            "status_message": "",
            "error": None
        }
    
    def process(self, 
                title: str, 
                problem: str, 
                seed_papers: List[str] = None, 
                callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Process the complete pipeline
        
        Args:
            title: Research paper title
            problem: Problem statement or research notes
            seed_papers: Optional list of seed paper IDs or URLs
            callback: Optional callback function to report progress
            
        Returns:
            Dictionary with results
        """
        # Initialize state for new run
        self.current_state = {
            "status": "processing",
            "title": title,
            "problem": problem,
            "keywords": [],
            "papers": [],
            "review": "",
            "progress": 0,
            "status_message": "Starting process...",
            "error": None
        }
        
        # Report initial state
        if callback:
            callback(self.current_state)
        
        try:
            # Validate inputs
            if not title or not isinstance(title, str):
                raise ValueError("Title is required and must be a string")
            
            if not problem or not isinstance(problem, str):
                raise ValueError("Problem statement is required and must be a string")
            
            # Step 1: Generate keywords
            self._update_state("Generating keywords...", 10, callback)
            keywords = generate_keywords(title, problem)
            self.current_state["keywords"] = keywords
            self._update_state(f"Generated {len(keywords)} keywords", 30, callback)
            
            # Step 2: Fetch papers
            self._update_state("Searching for relevant papers...", 40, callback)
            papers = fetch_papers(keywords, seed_papers or [])
            
            # Check if we found papers
            if not papers:
                self._update_state("No papers found for the given keywords", 50, callback)
                self.current_state["status"] = "no_papers"
                self.current_state["review"] = "No relevant papers found. Try different keywords or add seed papers."
                return self.current_state
            
            # Process paper information
            paper_info = []
            for paper in papers:
                paper_info.append({
                    "title": paper.get("title", "Unknown"),
                    "authors": paper.get("authors", []),
                    "abstract": paper.get("abstract", "Not available"),
                    "pdf_url": paper.get("pdf_url", ""),
                    "published": paper.get("published", "")
                })
            
            self.current_state["papers"] = paper_info
            self._update_state(f"Found {len(papers)} relevant papers", 60, callback)
            
            # Step 3: Generate literature review
            self._update_state("Generating literature review...", 70, callback)
            review = generate_review(problem, papers)
            self.current_state["review"] = review
            
            # Mark process as complete
            self.current_state["status"] = "completed"
            self._update_state("Literature review completed", 100, callback)
            
            return self.current_state
            
        except Exception as e:
            # Handle any errors
            self.current_state["status"] = "error"
            self.current_state["error"] = str(e)
            self._update_state(f"Error: {str(e)}", self.current_state["progress"], callback)
            return self.current_state
    
    def _update_state(self, message: str, progress: int, callback: Optional[Callable] = None):
        """Update the current state and report via callback
        
        Args:
            message: Status message
            progress: Progress percentage (0-100)
            callback: Optional callback function
        """
        self.current_state["status_message"] = message
        self.current_state["progress"] = progress
        
        if callback:
            callback(self.current_state)

# For compatibility with your original code
def run_pipeline(user_input):
    """Legacy function for backward compatibility"""
    orchestrator = Orchestrator()
    result = orchestrator.process(
        title=user_input["title"],
        problem=user_input["problem"],
        seed_papers=user_input.get("seed_papers", [])
    )
    return result["review"]