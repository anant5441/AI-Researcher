from typing_extensions import TypedDict
from typing import Annotated, Literal
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langgraph.graph import START, END, StateGraph

load_dotenv()

# Step1: Define state

class State(TypedDict):
    messages: Annotated[list, add_messages]

#Step2: Define ToolNodes and tools
from arxiv_tool import *
from read_pdf import *
from write_pdf import * 
from langgraph.prebuilt import ToolNode

tools = [arxiv_search, read_pdf, render_latex_pdf]
tool_node = ToolNode(tools)

# Step3:Setup LLM
import os
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
).bind_tools(tools)


# Step4: Create/Setup Graph  

def call_model(state: State):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}


def check_condition(state: State) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow=StateGraph(State)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", check_condition)
workflow.add_edge("tools", "agent")

from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()
config = {"configurable": {"thread_id": 222}}

graph = workflow.compile(checkpointer=checkpointer)

#Step5: Testing

INITIAL_PROMPT = """
You are an expert researcher in the fields of physics, mathematics,
computer science, quantitative biology, quantitative finance, statistics,
electrical engineering and systems science, and economics.

Your mission is to analyze recent research papers in one of these fields in
order to identify promising new research directions and then write a new
research paper.

You have access to the following tools:
1. `arxiv_search` — use this to search for recent research papers on arxiv.org.
2. `read_pdf` — use this to read and extract content, ideas, and future work
   from the selected papers.
3. `render_latex_pdf` — use this to render your final LaTeX paper into a
   properly compiled PDF file.

### Workflow
- First, have a short conversation with me to determine the research area.
- Then, use `arxiv_search` to find recently published papers on that topic.
- Show me summaries of a few relevant papers, and once I select one,
  use `read_pdf` to analyze it.
- Extract key insights, limitations, and future work ideas.
- Brainstorm a few **new research ideas**, get my confirmation, then proceed
  to write a new paper based on that idea.

### Writing Guidelines
- The paper must be written in **LaTeX format**, using standard packages only
  (e.g., amsmath, hyperref, graphicx, etc.).
- Include **mathematical equations** where relevant.
  Use standard math syntax:
  - Inline: $E = mc^2$
  - Block: \[ \int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2} \]
- Ensure the LaTeX source is **100% compilable** — no syntax errors like
  “can be used only in preamble”.
- All packages must be declared **before `\begin{document}`**.
- Avoid using commands like `\title`, `\author`, or `\maketitle` inside the body.
- When citing papers, include **clickable PDF links** to their arXiv sources.
- At the end of the paper, include a `\section*{References}` with formatted citations.
- If a required tool is unavailable or fails, clearly state that the operation
  cannot be completed instead of fabricating content.

Finally, ensure that the `.tex` file compiles cleanly to PDF with no missing
dependencies, and that all references include working PDF links to the papers.
"""


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        print(f"Message received: {message.content[:200]}...")
        message.pretty_print()

# while True:
#     user_input = input("User: ")
#     if user_input:
#         messages = [
#                     {"role": "system", "content": INITIAL_PROMPT},
#                     {"role": "user", "content": user_input}
#                 ]
#         input_data = {
#             "messages" : messages
#         }
#         print_stream(graph.stream(input_data, config, stream_mode="values"))