Agentic AI Researcher 🤖📑

An AI-powered autonomous research assistant that retrieves academic papers, analyzes them, and writes a structured research paper in PDF format.

🚀 Features

Accepts a research topic from the user.

Retrieves relevant academic papers using arXiv API.

Reads and extracts information from PDFs using PyPDF2.

Performs research and generates insights using LLMs (OpenAI, Gemini, Groq).

Writes and formats the final research paper into a downloadable PDF.

User-friendly Streamlit frontend for interaction.

🏗️ Technical Architecture

<!-- You can replace with your uploaded diagram -->

User Input (Streamlit UI): User provides a research topic.

AI Agent (LangGraph + LLMs): Orchestrates the research workflow.

Tools:

Browse articles

Scrape & analyze papers (arXiv + PyPDF2)

Perform research reasoning

Publish structured paper as PDF

Output: Downloadable Research Paper (PDF).

⚙️ Code Setup
Phase 1: Setup AI Agent & Tools

Setup tools:

Retrieve papers via arXiv tool

Read PDFs using PyPDF2

Write research paper to PDF

Setup LangGraph Agent with LLMs (OpenAI, Gemini, Groq).

Phase 2: Setup Frontend

Build frontend using Streamlit

User can ask questions & input topics

Display AI Agent’s response

Provide downloadable PDF of the research paper

Phase 3: Integration & Testing

Connect Agent with Streamlit frontend

Verify end-to-end workflow

Ensure paper generation & PDF export

🛠️ Tech Stack

Frontend: Streamlit

AI Orchestration: LangChain
, LangGraph

LLMs: OpenAI, Gemini, Groq

PDF Handling: PyPDF2

Research API: arXiv

📖 Example Workflow

User inputs: "Quantum Computing in Healthcare"

AI Agent retrieves relevant arXiv papers

Extracts and summarizes key findings

Drafts a structured research paper

Outputs a downloadable PDF

.

🤝 Contributing

Pull requests and contributions are welcome! Please open an issue for discussion before submitting major changes.

📜 License

MIT License © 2025