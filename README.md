# Multi-Agent Research System

A Streamlit research assistant that uses LangChain agents and chains to search
the web, read a relevant source, draft a report, and critique the result.

## Features

- Searches for recent information with Tavily and returns up to five results.
- Selects a relevant URL and extracts article text using Trafilatura, with Readability and BeautifulSoup fallbacks.
- Drafts a structured report with an introduction, at least three key findings, a conclusion, and sources.
- Reviews the report with a score, strengths, areas to improve, and a verdict.
- Shows raw search and scraped content and lets you download the report as Markdown.
- Displays progress through the search, reader, writer, and critic stages.

## Requirements

- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/)
- A Tavily API key
- A Groq API key

## Setup

From the project root, install the dependencies:

```powershell
uv sync
```

Create a `.env` file in the project root and add your API keys:

```dotenv
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
```

The chat model is configured through Groq's OpenAI-compatible API using the
`openai/gpt-oss-20b` model identifier. Keep `.env` private and do not commit
your API keys.

## Run the app

```powershell
uv run streamlit run src/multi_agent_research_system/app.py
```

Open the local URL printed by Streamlit, enter a research topic, and select
**Run Research Pipeline**. The completed report appears below the pipeline and
can be downloaded as a `.md` file.

## Research flow

1. **Search:** LangChain invokes the Tavily search tool for recent sources.
2. **Reader:** A second agent chooses a relevant URL and invokes the page extraction tool. Extracted page content is limited to 5,000 characters.
3. **Writer:** The chat model combines the search results and extracted content into a structured report.
4. **Critic:** The chat model evaluates the report and returns a score, strengths, improvements, and a one-line verdict.

Search, scraping, and model calls require working credentials and network access.
The available information and report quality depend on the sources returned by
the search service and the accessibility of those pages.
