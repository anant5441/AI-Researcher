# Agentic AI Researcher 🤖📑

An autonomous research assistant that searches arXiv, reads PDFs, reasons with an LLM, and writes a structured LaTeX paper compiled to PDF.

### 🚀 Features
- Search recent papers on arXiv
- Extract text from PDFs (PyPDF2)
- Reasoning and drafting with LLMs (Gemini / others via LangChain)
- One-click PDF generation from LaTeX (Tectonic)
- Streamlit chat UI

### 🛠️ Tech Stack
- **Frontend**: `streamlit`
- **Orchestration**: `langchain`, `langgraph`
- **LLM**: `langchain-google-genai` (Gemini)
- **PDF**: `PyPDF2` (reading), `tectonic` (LaTeX → PDF)
- **Papers API**: arXiv Atom API

## Prerequisites
- Python ≥ 3.13 (see `.python-version` / `pyproject.toml`)
- A Google API key for Gemini: set `GOOGLE_API_KEY`
- LaTeX engine: `tectonic` (required at runtime to compile PDFs)

Install Tectonic on Windows:
- With Scoop: `scoop install tectonic`
- With Chocolatey: `choco install tectonic`
- Or download from the official site: `https://tectonic-typesetting.github.io/`

## Setup
You can use `uv` (recommended, lockfile provided) or `pip`.

Using uv:
```bash
uv sync
```

Using pip:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r <(uv pip compile pyproject.toml)
```

Environment variables (create `.env` in project root):
```bash
GOOGLE_API_KEY=your_gemini_api_key
```

## Running
### 1) Streamlit UI
```bash
streamlit run frontend.py
```
Interacts via chat, searches arXiv, reads PDFs, and can render a paper to PDF.

### 2) CLI (simple loop)
There are two variants:
- `ai_researcher.py`: ReAct agent using `create_react_agent`
- `ai_researcher2.py`: Custom LangGraph with tool routing

Run either script and type a topic or instruction when prompted:
```bash
python ai_researcher.py
# or
python ai_researcher2.py
```

## Output
Generated files are saved in the `output/` directory, e.g.:
- `paper_YYYYMMDD_HHMMSS.tex`
- `paper_YYYYMMDD_HHMMSS.pdf`

## Project Structure (high level)
- `arxiv_tool.py`: arXiv search tool and XML parsing
- `read_pdf.py`: Reads remote PDFs and extracts text (PyPDF2)
- `write_pdf.py`: Renders LaTeX to PDF via Tectonic
- `ai_researcher.py`: ReAct-style agent wiring
- `ai_researcher2.py`: LangGraph agent with tool routing and memory
- `frontend.py`: Streamlit chat interface
- `output/`: Generated `.tex` and `.pdf`

## Troubleshooting
- Tectonic not found / PDF not generated
  - Ensure `tectonic` is installed and on PATH. Run `tectonic --version`.
  - Windows: install via Scoop (`scoop install tectonic`) or Chocolatey (`choco install tectonic`).

- arXiv search returns no results
  - The tool forbids certain characters `()" ` in queries. Try a simpler topic.

- PDF text extraction is incomplete
  - Some PDFs are scanned or have complex layouts. Results may vary with PyPDF2.

- Streamlit shows no responses
  - Check `.env` contains a valid `GOOGLE_API_KEY`.
  - Watch terminal logs for tool calls and errors.


## Security & Costs
- API calls to Gemini incur usage against your Google account.
- Never commit secrets. Use `.env` locally and secret managers in production.

## Contributing
PRs are welcome. For significant changes, open an issue first to discuss scope and design.

## License
MIT License © 2025


