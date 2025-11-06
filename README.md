# Agentic AI Researcher 🤖📑

An autonomous research assistant that searches arXiv, reads PDFs, reasons with an LLM, and writes a structured LaTeX paper compiled to PDF.

### 🚀 Features
- **arXiv Search**: Search and retrieve recent academic papers from arXiv
- **PDF Reading**: Extract and analyze text content from PDF papers using PyPDF2
- **AI Reasoning**: Leverage Google Gemini models for research analysis and paper generation
- **LaTeX Generation**: Automatically generate properly formatted LaTeX documents
- **PDF Compilation**: Compile LaTeX to PDF using Tectonic with automatic error handling
- **Streamlit UI**: Interactive chat interface with real-time streaming and PDF download
- **Memory & State**: Persistent conversation state using LangGraph checkpoints

### 🛠️ Tech Stack
- **Frontend**: `streamlit` - Interactive web UI
- **Orchestration**: `langchain`, `langgraph` - Agent workflow management
- **LLM**: `langchain-google-genai` (Gemini 2.5 Flash/Pro)
- **PDF Reading**: `PyPDF2` - Extract text from PDF files
- **PDF Generation**: `tectonic` - Modern LaTeX compiler
- **Papers API**: arXiv Atom API - Academic paper search

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
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Linux/Mac
pip install langchain langchain-core langchain-google-genai langgraph pypdf2 python-dotenv requests streamlit
```

Environment variables (create `.env` in project root):
```bash
GOOGLE_API_KEY=your_gemini_api_key
```

## Running

### 1) Streamlit UI (Recommended)
```bash
streamlit run frontend.py
```

The Streamlit interface provides:
- **Interactive Chat**: Real-time conversation with the AI researcher
- **Streaming Responses**: See responses as they're generated
- **PDF Download**: Automatic download button when a paper is generated
- **Tool Call Logging**: Monitor which tools are being used in the terminal

**Workflow in Streamlit:**
1. Enter a research topic (e.g., "quantum computing in healthcare")
2. The agent searches arXiv for relevant papers
3. Select papers to analyze
4. The agent reads PDFs and extracts insights
5. Generate new research ideas based on findings
6. Write and compile a LaTeX paper to PDF
7. Download the generated PDF directly from the UI

### 2) CLI Mode
There are two CLI variants:

**Option A: Simple ReAct Agent** (`ai_researcher.py`)
- Uses LangGraph's `create_react_agent` for simplified agent creation
- Model: Gemini 2.5 Pro
- Good for quick testing

**Option B: Custom LangGraph** (`ai_researcher2.py`) ⭐ Recommended
- Custom state management with memory checkpoints
- Model: Gemini 2.5 Flash (faster, cost-effective)
- More control over agent behavior
- Used by the Streamlit frontend

To use CLI mode, uncomment the while loop at the bottom of the script:
```bash
python ai_researcher.py
# or
python ai_researcher2.py
```
Then type your research topic or instructions when prompted.

## Output

Generated files are saved in the `output/` directory with timestamps:
- `paper_YYYYMMDD_HHMMSS.tex` - LaTeX source file
- `paper_YYYYMMDD_HHMMSS.pdf` - Compiled PDF document

The LaTeX files include:
- Proper document structure with preamble
- Mathematical equations support (amsmath, amssymb)
- Hyperlinks for references
- Automatic title page generation
- Sanitized content (duplicate preambles removed automatically)

## Project Structure

```
AI-Researcher/
├── ai_researcher.py          # Simple ReAct agent (CLI)
├── ai_researcher2.py         # Custom LangGraph agent (used by Streamlit)
├── frontend.py               # Streamlit web interface
├── arxiv_tool.py             # arXiv search tool with XML parsing
├── read_pdf.py               # PDF text extraction tool
├── write_pdf.py              # LaTeX to PDF compilation tool
├── output/                   # Generated papers (.tex and .pdf)
├── pyproject.toml            # Project dependencies
└── .env                      # Environment variables (create this)
```

### Key Components

- **`arxiv_tool.py`**: Searches arXiv API, parses XML responses, returns paper metadata (title, authors, summary, PDF links)
- **`read_pdf.py`**: Downloads PDFs from URLs and extracts text content page by page
- **`write_pdf.py`**: Sanitizes LaTeX content, adds proper preamble, compiles to PDF using Tectonic
- **`ai_researcher2.py`**: Main agent with LangGraph workflow, tool routing, and memory checkpoints
- **`frontend.py`**: Streamlit UI that streams agent responses and provides PDF download functionality

## Example Usage

### Basic Research Workflow

1. **Start the Streamlit app:**
   ```bash
   streamlit run frontend.py
   ```

2. **In the chat, ask about a research topic:**
   ```
   I want to research quantum machine learning algorithms
   ```

3. **The agent will:**
   - Search arXiv for relevant papers
   - Present summaries of recent papers
   - Wait for you to select papers to analyze
   - Read and extract key insights from PDFs
   - Propose new research directions
   - Write a complete LaTeX paper
   - Compile it to PDF
   - Provide a download button

### Advanced: Direct Paper Generation

You can also ask the agent to directly write a paper:
```
Search for papers on transformer architectures, read the top 3 papers, 
and write a new research paper on efficient attention mechanisms.
```

## Troubleshooting

### Tectonic not found / PDF not generated
- **Check installation**: Run `tectonic --version` in your terminal
- **Windows installation**:
  - Scoop: `scoop install tectonic`
  - Chocolatey: `choco install tectonic`
  - Manual: Download from [tectonic-typesetting.github.io](https://tectonic-typesetting.github.io/)
- **PATH issues**: Ensure `tectonic` is in your system PATH
- **Check logs**: The tool will print error messages if compilation fails

### arXiv search returns no results
- **Invalid characters**: The tool rejects queries with `()" ` characters
- **Solution**: Use simpler topic names (e.g., "quantum computing" instead of "quantum computing (2024)")
- **Try different keywords**: Some topics may have limited recent papers

### PDF text extraction is incomplete
- **Scanned PDFs**: PyPDF2 cannot extract text from image-based PDFs
- **Complex layouts**: Multi-column or heavily formatted PDFs may lose formatting
- **Large files**: Very long papers may take time to process
- **Alternative**: The agent will work with whatever text it can extract

### Streamlit shows no responses
- **API Key**: Verify `.env` file contains `GOOGLE_API_KEY=your_key_here`
- **Check terminal**: Look for error messages or tool call logs
- **Network issues**: Ensure you can reach Google's API servers
- **Model availability**: Verify your API key has access to Gemini 2.5 Flash/Pro

### LaTeX compilation errors
- **Check output files**: Inspect the `.tex` file in `output/` directory
- **Common issues**:
  - Missing packages (should be auto-added by the tool)
  - Invalid math syntax
  - Unescaped special characters
- **Sanitization**: The tool automatically removes duplicate preambles, but complex LaTeX may need manual fixes
- **Reference**: See `latex_error.html` for common LaTeX issues and examples

### Memory/State issues
- **Thread ID**: The agent uses a fixed thread ID (222) for persistence
- **Reset**: Restart the Streamlit app to clear conversation history
- **CLI mode**: Each run starts fresh (no persistence in CLI mode)


## How It Works

### Agent Workflow

1. **User Input**: Research topic or instruction
2. **arXiv Search**: Agent searches for recent papers using `arxiv_search` tool
3. **Paper Selection**: User selects papers of interest (in interactive mode)
4. **PDF Reading**: Agent downloads and extracts text using `read_pdf` tool
5. **Analysis**: LLM analyzes content, identifies gaps, and proposes new research directions
6. **Paper Writing**: Agent generates LaTeX content with proper formatting
7. **PDF Compilation**: `render_latex_pdf` tool sanitizes LaTeX and compiles to PDF
8. **Output**: Generated PDF is saved and made available for download

### Tool Integration

The agent uses three main tools:
- **`arxiv_search(topic: str)`**: Returns list of papers with metadata
- **`read_pdf(url: str)`**: Extracts text content from PDF URLs
- **`render_latex_pdf(latex_content: str)`**: Compiles LaTeX to PDF, returns file path

### LaTeX Sanitization

The `render_latex_pdf` tool automatically:
- Removes duplicate `\documentclass` and `\usepackage` declarations
- Strips `\begin{document}`, `\end{document}`, and `\maketitle` from content
- Adds proper preamble with required packages
- Ensures compilable LaTeX structure

## Security & Costs

- **API Usage**: All API calls to Gemini are billed to your Google Cloud account
- **Rate Limits**: Be aware of API rate limits for your account tier
- **Costs**: Gemini 2.5 Flash is more cost-effective than Pro for most tasks
- **Secrets**: Never commit `.env` files or API keys to version control
- **Production**: Use environment variables or secret management services in production

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly (especially LaTeX compilation)
5. Submit a pull request

For major changes, please open an issue first to discuss the proposed changes.

## License

MIT License © 2025
