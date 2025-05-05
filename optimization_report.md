# CiteRight Optimization Report

## Summary of Optimizations

This document outlines the optimizations made to the CiteRight codebase to enhance performance and output quality using GPT-4.

## 1. Model Selection and Optimization

### Model Comparison
We evaluated several models for the literature review generation task:

| Model | Strengths | Weaknesses | Cost |
|-------|-----------|------------|------|
| GPT-4 | Best synthesis capabilities, stronger academic writing, deep reasoning | Highest cost, slightly slower | $$$$ |
| GPT-4o mini | Good balance of capabilities and cost, faster response | Less nuanced analysis | $$ |
| GPT-3.5 Turbo | Fastest, lowest cost | Limited synthesis capabilities, simpler output | $ |

**Selected Model: GPT-4**
- Provides the best quality for academic literature review synthesis
- Better able to identify patterns, connections, and research gaps
- Produces more scholarly output appropriate for academic contexts

## 2. Prompt Engineering Optimizations

### Literature Review Generation
- **Context Enhancement**: Added expert academic researcher framing
- **Structured Output**: Clear section requirements with paragraph count guidance
- **Synthesis Focus**: Explicit instructions to create coherent narratives
- **Academic Tone**: Requirements for scholarly tone and citation format

### Paper Summarization
- **Enhanced Analysis**: Request for methodology, findings, and relevance information
- **Improved Structure**: Clear categorization of each paper's contribution

### Keyword Generation
- **Domain Specificity**: Instructions to focus on technical and discipline-specific terminology
- **Format Control**: Clear examples and direct instructions for consistent output

## 3. Token Usage Optimization

| Component | Before | After |
|-----------|--------|-------|
| Abstract Length | 500 chars | 500 chars (with smart trimming) |
| Max Tokens (Review) | 1500 | 1800 |
| Max Tokens (Summary) | 200 | 200 |
| Temperature (Review) | 0.4 | 0.3 |

- **Smart Abstract Trimming**: Added logic to trim at sentence boundaries
- **Caching Implementation**: In-memory caching for LLM calls to reduce redundant API requests
- **Relevance Scoring**: Refined algorithm with title matches weighted higher than abstract matches

## 4. Paper Retrieval Enhancements

- **Relevance Threshold**: Lowered from 0.3 to 0.25 to include more potentially relevant papers
- **Title Weight**: Increased importance of keyword matches in the title
- **Seed Paper Handling**: Improved handling of seed papers with automatic maximum relevance scoring

## 5. Expected Impact

### Quality Improvements
- More sophisticated analysis of research methodologies
- Better identification of research gaps
- More coherent narrative flow between papers
- Proper academic citation and scholarly tone

### Performance Improvements
- Caching reduces redundant API calls
- Smart trimming reduces token usage while preserving meaning
- Better relevance scoring retrieves more applicable papers

### Cost Optimization
- While using GPT-4 increases per-token cost, other optimizations (caching, smart trimming) help manage overall costs
- Option to fall back to GPT-4o mini when cost is a priority

## 6. Testing and Evaluation

A custom test script (`test_citation.py`) was created to validate the pipeline with our optimizations. With a valid API key, this script:
1. Generates academic search keywords
2. Retrieves and ranks relevant papers
3. Produces a comprehensive literature review

The expected outcome is a high-quality, well-structured literature review suitable for academic purposes.

## 7. Future Optimization Opportunities

- Implement persistent caching to disk for even more efficiency
- Add vector embeddings for improved semantic paper matching
- Explore model fine-tuning for even better academic writing style
- Implement parallel processing for paper summarization 