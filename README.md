# CiteRight

CiteRight is an LLM-powered tool designed to streamline literature reviews and academic research by fetching, analyzing, and synthesizing relevant papers from arXiv. This system helps researchers create comprehensive literature reviews from minimal input, saving valuable time in the research process.

![CiteRight Screenshot](assets/screenshot.png)

## Features

- **Automated Literature Reviews**: Generate structured, academic-quality literature reviews from a title and problem statement
- **Intelligent Keyword Generation**: Extract optimal search keywords using GPT-4
- **Smart Paper Retrieval**: Search arXiv with relevance-based paper ranking
- **Comprehensive Analysis**: Identify research gaps, methodologies, and key findings across papers
- **Academic Citations**: Proper citation formatting for referenced papers
- **User-Friendly Interface**: Clean Streamlit UI for easy interaction

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/citeright-rag.git
   cd citeright-rag
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Running CiteRight

Launch the Streamlit interface:
```bash
streamlit run main.py
```

Navigate to the provided URL (typically http://localhost:8501) to access the application.

## Usage

1. **Enter Research Details**:
   - Type your paper title
   - Describe your research problem or notes
   - (Optional) Add arXiv IDs or URLs for seed papers

2. **Generate Literature Review**:
   - Click "Generate Literature Review"
   - Wait for the system to:
     - Generate optimal search keywords
     - Find relevant papers on arXiv
     - Analyze and synthesize the information

3. **Review the Output**:
   - Read the structured literature review
   - Explore referenced papers
   - See the keywords used in the search

## Architecture

CiteRight follows a modular pipeline architecture:

1. **Frontend** (Streamlit UI): Collects user input and displays results
2. **Keyword Generator**: Uses GPT-4 to create optimal search terms
3. **Paper Fetcher**: Queries arXiv API and ranks papers by relevance
4. **Literature Review Generator**: Synthesizes a structured review using LLM
5. **Orchestrator**: Coordinates the end-to-end process

## Configuration

CiteRight uses GPT-4 by default for optimal quality but can be configured to use different models for cost optimization. Edit the `backend/llm_client.py` file to change models:

## Acknowledgments

- [OpenAI](https://openai.com/) for their powerful GPT models
- [arXiv](https://arxiv.org/) for providing access to research papers
- [Streamlit](https://streamlit.io/) for the simple yet powerful UI framework
