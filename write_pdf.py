# Step1: Install tectonic & Import deps
from langchain_core.tools import tool
from datetime import datetime
from pathlib import Path
import subprocess
import shutil

@tool
def render_latex_pdf(latex_content: str) -> str:
    """Render a LaTeX document to PDF.

    Args:
        latex_content: The main body of the LaTeX document (sections, math, references)

    Returns:
        Path to the generated PDF document
    """

    if shutil.which("tectonic") is None:
        raise RuntimeError("tectonic is not installed. Install it first on your system.")

    try:
        # Step2: Create output directory
        output_dir = Path("output").absolute()
        output_dir.mkdir(exist_ok=True)

        # Step3: Generate unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tex_filename = f"paper_{timestamp}.tex"
        pdf_filename = f"paper_{timestamp}.pdf"

        tex_file_path = output_dir / tex_filename
        pdf_file_path = output_dir / pdf_filename

        # Step4: Build complete LaTeX document
        preamble = r"""
\documentclass{article}
\usepackage{amsmath, amssymb}
\usepackage[utf8]{inputenc}
\usepackage{hyperref}
\title{AI Research Paper}
\date{\today}

\begin{document}
\maketitle
"""
        ending = r"""
\end{document}
"""
        full_tex = preamble + latex_content + ending

        # Step5: Write LaTeX to .tex file
        tex_file_path.write_text(full_tex, encoding="utf-8")

        # Step6: Run tectonic to compile LaTeX → PDF
        result = subprocess.run(
            ["tectonic", str(tex_file_path), "--outdir", str(output_dir)],
            cwd=output_dir,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Tectonic failed:\n{result.stderr}")

        if not pdf_file_path.exists():
            raise FileNotFoundError("PDF file was not generated")

        print(f"✅ Successfully generated PDF at {pdf_file_path}")
        return str(pdf_file_path)

    except Exception as e:
        print(f"❌ Error rendering LaTeX: {str(e)}")
        raise
