import streamlit as st
from ai_researcher2 import INITIAL_PROMPT, graph, config
from pathlib import Path
import logging
from langchain_core.messages import AIMessage

# -----------------------------------------------------------
# Setup Logging
# -----------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------
# Streamlit Page Config
# -----------------------------------------------------------
st.set_page_config(page_title="AI-Researcher", page_icon="📄")
st.title("📄 AI-Researcher")

# -----------------------------------------------------------
# Initialize Session State
# -----------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    logger.info("Initialized chat history")

if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

# -----------------------------------------------------------
# Chat Input
# -----------------------------------------------------------
user_input = st.chat_input("What research topic would you like to explore?")

if user_input:
    # Display user message
    st.chat_message("user").write(user_input)
    logger.info(f"User input: {user_input}")

    # Add to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Prepare chat input for the agent
    chat_input = {
        "messages": [{"role": "system", "content": INITIAL_PROMPT}] + st.session_state.chat_history
    }

    logger.info("Starting agent processing...")

    # Placeholder for streaming assistant responses
    assistant_placeholder = st.chat_message("assistant")
    response_box = assistant_placeholder.empty()

    full_response = ""
    pdf_path = None

    # -----------------------------------------------------------
    # Stream model output from LangGraph
    # -----------------------------------------------------------
    for s in graph.stream(chat_input, config, stream_mode="values"):
        message = s["messages"][-1]

        # Detect if render_latex_pdf tool returned output
        if "render_latex_pdf" in s:
            pdf_path = s["render_latex_pdf"]
            logger.info(f"✅ PDF generated and captured: {pdf_path}")

        # Log tool calls
        if getattr(message, "tool_calls", None):
            for tool_call in message.tool_calls:
                logger.info(f"🧩 Tool call: {tool_call['name']}")

        # Handle AI text messages
        if isinstance(message, AIMessage) and message.content:
            text_content = (
                message.content if isinstance(message.content, str) else str(message.content)
            )
            full_response += text_content + " "
            response_box.write(full_response)

    # -----------------------------------------------------------
    # After streaming completes
    # -----------------------------------------------------------
    if full_response:
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

    # -----------------------------------------------------------
    # Show Download Button (auto)
    # -----------------------------------------------------------
    if pdf_path:
        pdf_file_path = Path(pdf_path)
        if pdf_file_path.exists():
            st.session_state.pdf_path = str(pdf_file_path)
            st.success("✅ Research paper successfully generated!")

            with open(pdf_file_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download Research Paper PDF",
                    data=pdf_file,
                    file_name=pdf_file_path.name,
                    mime="application/pdf",
                    key="download_pdf"
                )
        else:
            st.warning("⚠️ PDF path detected, but file not found on disk.")
