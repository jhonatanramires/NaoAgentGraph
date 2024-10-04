# Dependencies for Graph Tools
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages

# Dependencies for Graph Display
from PIL import Image as PILImage
from IPython.display import Image, display
import io

# Dependencies for Type Annotations
from typing import Annotated
from typing_extensions import TypedDict

class State(TypedDict):
  messages: Annotated[list, add_messages]

def hello(a):
  print(a)

tools = []

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", hello)
tool_node = ToolNode(tools)
graph_builder.add_node("tools", tool_node)
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("tools", "chatbot")
graph = graph_builder.compile()
print(graph)
try:
  #img_data = graph.get_graph().draw_mermaid_png()
  img_data = graph.get_graph().draw_mermaid_png()
  print("hello")
  if img_data:
    img = PILImage.open(io.BytesIO(img_data))
    img.show()
  else:
    print("The image was not generated correctly.")
except Exception as e:
    print(f"Error generating the image: {e}")