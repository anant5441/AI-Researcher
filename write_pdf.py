from langchain_core.tools import tool
from datetime import datetime
from pathlib import Path
import subprocess
import shutil
import re
import logging

logger = logging.getLogger(__name__)

@tool
def render_latex_pdf(latex_content: str) -> str:
    """
    Render a LaTeX document to PDF using Tectonic safely.
    Fallback: if Tectonic fails, generate PDF via Pandoc.
    """

    output_dir = Path("output").absolute()
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tex_file_path = output_dir / f"paper_{timestamp}.tex"
    pdf_file_path = output_dir / f"paper_{timestamp}.pdf"

    # Sanitize LaTeX input
    sanitized = re.sub(r"\\documentclass.*?\n", "", latex_content)
    sanitized = re.sub(r"\\usepackage.*?\n", "", sanitized)
    sanitized = re.sub(r"\\begin\{document\}", "", sanitized)
    sanitized = re.sub(r"\\end\{document\}", "", sanitized)

    preamble = r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{geometry}
\geometry{margin=1in}

\title{AI-Generated Research Paper}
\author{Automated Research Agent}
\date{\today}

\begin{document}
\maketitle
"""
    full_tex = preamble + sanitized + "\n\\end{document}"
    tex_file_path.write_text(full_tex, encoding="utf-8")

    # Try Tectonic
    try:
        if shutil.which("tectonic") is None:
            raise FileNotFoundError("Tectonic not installed in environment.")

        result = subprocess.run(
            ["tectonic", str(tex_file_path), "--outdir", str(output_dir)],
            cwd=output_dir,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Tectonic error:\n{result.stderr}")

        if not pdf_file_path.exists():
            raise FileNotFoundError("Tectonic did not create the PDF file.")

        logger.info(f"✅ Successfully generated PDF with Tectonic: {pdf_file_path}")
        return str(pdf_file_path)

    except Exception as e:
        logger.warning(f"⚠️ Tectonic failed: {e}")
        logger.info("🔁 Falling back to Pandoc-based PDF generation...")

        try:
            # Fallback: Markdown conversion
            md_content = re.sub(r"\$([^\$]+)\$", r"\\(\1\\)", sanitized)
            md_file = output_dir / f"paper_{timestamp}.md"
            md_file.write_text(md_content, encoding="utf-8")

            import pypandoc
            fallback_pdf_path = output_dir / f"paper_{timestamp}_fallback.pdf"

            pypandoc.convert_text(
                md_content,
                "pdf",
                format="md",
                outputfile=str(fallback_pdf_path),
                extra_args=["--standalone"],
            )

            if fallback_pdf_path.exists():
                logger.info(f"✅ Fallback PDF generated successfully: {fallback_pdf_path}")
                return str(fallback_pdf_path)
            else:
                raise FileNotFoundError("Pandoc fallback did not produce PDF.")

        except Exception as fallback_error:
            logger.error(f"❌ Both Tectonic and fallback failed: {fallback_error}")
            raise RuntimeError(
                "Failed to render PDF. Ensure Tectonic or Pandoc is installed."
            )
