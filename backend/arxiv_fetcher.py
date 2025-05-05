import arxiv
import time
from typing import List, Dict, Any
import re
from collections import Counter

def fetch_papers(keywords: List[str], seed_ids: List[str] = None, max_results: int = 20, min_relevance_score: float = 0.05) -> List[Dict[Any, Any]]:
    """Fetch papers from ArXiv based on keywords and optional seed paper IDs
    
    Args:
        keywords: List of search keywords
        seed_ids: Optional list of ArXiv IDs for seed papers
        max_results: Maximum number of results to return
        min_relevance_score: Minimum relevance score (0-1) for filtering papers
        
    Returns:
        List of paper details as dictionaries
    """
    raw_results = []
    seen_ids = set()  # Track paper IDs to avoid duplicates
    
    try:
        # Create combined query for efficiency (using OR between keywords)
        combined_query = " OR ".join([f'"{keyword}"' for keyword in keywords])
        print(f"[DEBUG] ArXiv search query: {combined_query}")
        
        # Set up ArXiv client with retry settings
        client = arxiv.Client(
            page_size=max_results * 2,  # Fetch more papers to filter later
            delay_seconds=3,
            num_retries=3
        )
        
        # Search for papers
        search = arxiv.Search(
            query=combined_query,
            max_results=max_results * 2,  # Fetch more papers to filter later
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        # Process results
        print(f"[DEBUG] Searching ArXiv for papers...")
        result_count = 0
        for paper in client.results(search):
            result_count += 1
            if paper.entry_id not in seen_ids:
                seen_ids.add(paper.entry_id)
                print(f"[DEBUG] Found paper: {paper.title}")
                
                # Convert to dictionary for easier manipulation
                raw_results.append({
                    'id': paper.entry_id,
                    'title': paper.title,
                    'authors': [author.name for author in paper.authors],
                    'abstract': _trim_abstract(paper.summary),
                    'pdf_url': paper.pdf_url,
                    'published': paper.published.strftime('%Y-%m-%d') if hasattr(paper, 'published') else '',
                    'categories': paper.categories if hasattr(paper, 'categories') else [],
                    'comment': getattr(paper, 'comment', ''),
                    'journal_ref': getattr(paper, 'journal_ref', ''),
                    'doi': getattr(paper, 'doi', '')
                })
        
        print(f"[DEBUG] Initial search found {result_count} papers, {len(raw_results)} after deduplication")
        
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
                            
                            # Convert to dictionary and mark as seed paper (always include)
                            paper_dict = {
                                'id': paper.entry_id,
                                'title': paper.title,
                                'authors': [author.name for author in paper.authors],
                                'abstract': _trim_abstract(paper.summary),
                                'pdf_url': paper.pdf_url,
                                'published': paper.published.strftime('%Y-%m-%d') if hasattr(paper, 'published') else '',
                                'categories': paper.categories if hasattr(paper, 'categories') else [],
                                'comment': getattr(paper, 'comment', ''),
                                'journal_ref': getattr(paper, 'journal_ref', ''),
                                'doi': getattr(paper, 'doi', ''),
                                'is_seed': True,
                                'relevance_score': 1.0  # Max relevance for seed papers
                            }
                            raw_results.append(paper_dict)
                    except Exception as e:
                        print(f"Error fetching seed paper {paper_id}: {e}")
        
        # Score and filter papers
        scored_results = calculate_relevance_scores(raw_results, keywords)
        
        # Filter by relevance score and sort by score (descending)
        scored_results = [p for p in scored_results if p.get('is_seed', False) or p.get('relevance_score', 0) >= min_relevance_score]
        scored_results.sort(key=lambda p: p.get('relevance_score', 0), reverse=True)
        
        # Cap to max_results
        final_results = scored_results[:max_results]
        print(f"[DEBUG] Returning {len(final_results)} papers after relevance filtering (min score: {min_relevance_score})")
        return final_results
        
    except Exception as e:
        print(f"[DEBUG] Error searching ArXiv: {e}")
        return []  # Return empty list instead of failing

def calculate_relevance_scores(papers: List[Dict[Any, Any]], keywords: List[str]) -> List[Dict[Any, Any]]:
    """Calculate relevance score for each paper based on keyword matches
    
    Args:
        papers: List of paper dictionaries
        keywords: List of search keywords
        
    Returns:
        Papers with added relevance scores
    """
    print(f"[DEBUG] Calculating relevance scores for {len(papers)} papers")
    
    # Process keywords to handle variations
    processed_keywords = []
    for keyword in keywords:
        # Add the original keyword
        processed_keywords.append(keyword.lower())
        
        # Add variations (e.g., "machine learning" from "machine learning in healthcare")
        parts = keyword.lower().split()
        if len(parts) > 2:
            for i in range(len(parts) - 1):
                for j in range(i + 2, min(i + 5, len(parts) + 1)):
                    processed_keywords.append(" ".join(parts[i:j]))
    
    print(f"[DEBUG] Using {len(processed_keywords)} processed keywords: {', '.join(processed_keywords)}")
    
    # Extract parts of papers to search in
    for i, paper in enumerate(papers):
        if 'is_seed' in paper and paper['is_seed']:
            # Skip calculation for seed papers - already set to 1.0
            print(f"[DEBUG] Paper {i+1}: '{paper.get('title')}' is a seed paper, score = 1.0")
            continue
            
        # Prepare normalized text for matching
        title = paper.get('title', '').lower()
        abstract = paper.get('abstract', '').lower()
        
        # Count keyword matches
        matches = 0
        total_possible = len(processed_keywords)
        
        for keyword in processed_keywords:
            # Convert keyword to regex pattern (case insensitive)
            # Handle multi-word keywords by allowing word boundaries or partial matches
            keyword_pattern = re.compile(r'\b' + re.escape(keyword.lower()) + r'\b', re.IGNORECASE)
            
            # Check for matches in title (weighted higher)
            title_matches = len(re.findall(keyword_pattern, title))
            # Check for matches in abstract
            abstract_matches = len(re.findall(keyword_pattern, abstract))
            
            # Weight title matches higher than abstract matches
            weighted_matches = (title_matches * 3) + abstract_matches
            matches += min(weighted_matches, 4)  # Cap to avoid over-influence of repeated terms
        
        # Calculate final score (0 to 1)
        relevance_score = matches / (total_possible * 4)  # Normalize to 0-1 range
        relevance_score = min(relevance_score * 1.5, 1.0)  # Boost scores but cap at 1.0
        paper['relevance_score'] = relevance_score
        print(f"[DEBUG] Paper {i+1}: '{paper.get('title')}' score = {paper['relevance_score']:.2f}")
        
    return papers

def _trim_abstract(abstract: str, max_length: int = 500) -> str:
    """Trim abstract to reduce token usage
    
    Args:
        abstract: Original abstract text
        max_length: Maximum length to keep
        
    Returns:
        Trimmed abstract
    """
    if not abstract:
        return "Not available"
        
    if len(abstract) <= max_length:
        return abstract
        
    # Find a good breaking point (end of sentence) near max_length
    last_period = abstract[:max_length].rfind('.')
    if last_period > max_length * 0.7:  # If we can get at least 70% of max_length
        return abstract[:last_period+1]
    else:
        # If no good sentence break, just cut at max_length
        return abstract[:max_length] + "..."