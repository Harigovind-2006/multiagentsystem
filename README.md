# Auto-Research Pipeline 🤖📚

An automated, multi-stage AI research assistant built with [LangChain](https://python.langchain.com/) and OpenAI. This project takes any topic as input and orchestrates a team of AI agents to search the web, scrape content, write a draft, critique it, and finally publish a polished, professional research report.

## Features

This project utilizes a sequential pipeline of specialized AI agents:
1. **Search Agent**: Uses the [Tavily API](https://tavily.com/) to scout the web for the most relevant, up-to-date sources and snippets.
2. **Reader Agent**: Scrapes the identified URLs (via `BeautifulSoup` and `requests`) to extract deeper, cleaner context.
3. **Writer Chain**: Drafts a structured research report containing an Introduction, Key Findings, Analysis, Conclusion, and Citations.
4. **Critic Chain**: Acts as an objective reviewer, evaluating the draft out of 10 and offering specific strengths and areas to improve.
5. **Reviewer Chain**: Implements the critic's feedback to rewrite, refine, and produce the **Final Polished Report**.

## Prerequisites

- Python 3.11+
- [OpenAI API Key](https://platform.openai.com/api-keys)
- [Tavily API Key](https://tavily.com/)

## Installation

1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd langchain-project
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

## Usage

Run the main pipeline script:
```bash
python pipeline.py
```

When prompted, enter your desired research topic. The CLI will output the process phase-by-phase and deliver the final drafted report!

## Technologies Used

- **LangChain Core & Agents**: For chaining prompts and orchestrating tools.
- **OpenAI (`gpt-4o-mini`)**: Powers the intelligence and reasoning of the agents.
- **Tavily API**: Specialized search engine optimized for AI agents.
- **BeautifulSoup**: Used for cleaning and scraping HTML content.

## License

This project is open-source and available under the [MIT License](LICENSE).
