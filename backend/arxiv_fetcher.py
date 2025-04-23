import arxiv
import time
from typing import List, Dict, Any

def fetch_papers(keywords: List[str], seed_ids: List[str] = None, max_results: int = 20) -> List[Dict[Any, Any]]:
    """Fetch papers from ArXiv based on keywords and optional seed paper IDs
    
    Args:
        keywords: List of search keywords
        seed_ids: Optional list of ArXiv IDs for seed papers
        max_results: Maximum number of results to return
        
    Returns:
        List of paper details as dictionaries
    """
    results = []
    seen_ids = set()  # Track paper IDs to avoid duplicates
    
    try:
        # Create combined query for efficiency (using OR between keywords)
        combined_query = " OR ".join([f'"{keyword}"' for keyword in keywords])
        
        # Set up ArXiv client with retry settings
        client = arxiv.Client(
            page_size=max_results,
            delay_seconds=3,
            num_retries=3
        )
        
        # Search for papers
        search = arxiv.Search(
            query=combined_query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        # Process results
        for paper in client.results(search):
            if paper.entry_id not in seen_ids:
                seen_ids.add(paper.entry_id)
                
                # Convert to dictionary for easier manipulation
                results.append({
                    'id': paper.entry_id,
                    'title': paper.title,
                    'authors': [author.name for author in paper.authors],
                    'abstract': paper.summary,
                    'pdf_url': paper.pdf_url,
                    'published': paper.published.strftime('%Y-%m-%d') if hasattr(paper, 'published') else '',
                    'categories': paper.categories if hasattr(paper, 'categories') else [],
                    'comment': getattr(paper, 'comment', ''),
                    'journal_ref': getattr(paper, 'journal_ref', ''),
                    'doi': getattr(paper, 'doi', '')
                })
        
        # If seed IDs are provided, fetch them too
        if seed_ids and len(seed_ids) > 0:
            for paper_id in seed_ids:
                if paper_id not in seen_ids:
                    try:
                        # Clean up ID format if needed
                        if '/' in paper_id and 'arxiv.org' in paper_id:
                            # Extract ID from URL
                            paper_id = paper_id.split('/')[-1]
                            if '.pdf' in paper_id:
                                paper_id = paper_id.replace('.pdf', '')
                                
                        # Fetch single paper by ID
                        search = arxiv.Search(id_list=[paper_id])
                        for paper in client.results(search):
                            seen_ids.add(paper.entry_id)
                            
                            # Convert to dictionary
                            results.append({
                                'id': paper.entry_id,
                                'title': paper.title,
                                'authors': [author.name for author in paper.authors],
                                'abstract': paper.summary,
                                'pdf_url': paper.pdf_url,
                                'published': paper.published.strftime('%Y-%m-%d') if hasattr(paper, 'published') else '',
                                'categories': paper.categories if hasattr(paper, 'categories') else [],
                                'comment': getattr(paper, 'comment', ''),
                                'journal_ref': getattr(paper, 'journal_ref', ''),
                                'doi': getattr(paper, 'doi', '')
                            })
                    except Exception as e:
                        print(f"Error fetching seed paper {paper_id}: {e}")
        
        return results
        
    except Exception as e:
        print(f"Error searching ArXiv: {e}")
        return []  # Return empty list instead of failing