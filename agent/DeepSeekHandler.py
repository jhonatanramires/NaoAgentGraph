# /////////////////// THIRD-PARTY DEPENDENCIES ///////////////////////////////

# Dependencies for Type Annotations
from typing import Annotated
from typing_extensions import TypedDict

# Dependencies for Graph Tools
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# Dependencies for LLM Chat - CHANGED TO DEEPSEEK
from langchain_deepseek import ChatDeepSeek

# Dependencies for Graph Display
from PIL import Image as PILImage
import io

# Dependencies for Memory Management
from langgraph.checkpoint.sqlite import SqliteSaver

# Dependencies for Messages Management
from langchain_core.messages import AIMessage, ToolMessage

# /////////////////// PROJECT-SPECIFIC DEPENDENCIES ///////////////////////////////
from dotenv import load_dotenv
import os

class DeepSeekAgentHandler:
    class State(TypedDict):
        messages: Annotated[list, add_messages]

    def __init__(self, api_key, tools, model_name, thread_id, memory=True):
        """
        Initialize the DeepSeek AgentHandler
        
        :param api_key: DeepSeek API key
        :param tools: Tools available to the agent
        :param model_name: DeepSeek model name (e.g., deepseek-chat)
        :param thread_id: Unique conversation thread ID
        :param memory: Enable persistent memory
        """
        self.tools = tools
        self.llm = ChatDeepSeek(model_name=model_name, api_key=api_key)
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.memory = memory
        
        if self.memory:
            self.checkpointer = SqliteSaver.from_conn_string("memory")
        
        self.graph = self._setup_graph()
        self.config = {"configurable": {"thread_id": f"{thread_id}"}}

    def _chatbot(self, state: State):
        """
        Internal function handling chatbot logic
        
        :param state: Current agent state
        :return: New state with model response
        """
        messages = state["messages"]
        result = self.llm_with_tools.invoke(messages)
        return {"messages": [result]}

    def _setup_graph(self):
        """
        Configure the state graph for conversation flow
        
        :return: Compiled graph
        """
        graph_builder = StateGraph(self.State)
        graph_builder.add_node("chatbot", self._chatbot)
        tool_node = ToolNode(self.tools)
        graph_builder.add_node("tools", tool_node)
        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("tools", "chatbot")
        
        if self.memory:
            return graph_builder.compile(checkpointer=self.checkpointer)
        return graph_builder.compile()

    def display_graph(self):
        """
        Display visual representation of the agent graph
        """
        try:
            img_data = self.graph.get_graph().draw_mermaid_png()
            if img_data:
                img = PILImage.open(io.BytesIO(img_data))
                img.show()
        except Exception as e:
            print(f"Error generating graph image: {e}")

    def prompt(self, user_input):
        """
        Process user input and return agent response
        
        :param user_input: User's message
        :return: Agent's response
        """
        try:
            for event in self.graph.stream(
                {"messages": [("user", user_input)]},
                self.config,
                stream_mode="values"
            ):
                if isinstance(event["messages"][-1], AIMessage):
                    return event["messages"][-1].content
        except Exception as e:
            print(f"Error processing prompt: {e}")
            return "Sorry, I encountered an error processing your request."
    
    def chat(self):
        """
        Start interactive chat session
        """
        print("DeepSeek Agent - Interactive Mode (type 'exit' to quit)")
        while True:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            response = self.prompt(user_input)
            print(f"Agent: {response}")

if __name__ == "__main__":
    # Example usage:
    load_dotenv()
    
    # DeepSeek credentials
    api_key = os.getenv('DEEPSEEK_API_KEY')
    model_name = "deepseek-chat"  # Example model name
    
    # Sample tools (replace with actual tools implementation)
    from langchain_community.tools import WikipediaQueryRun
    from langchain_community.utilities import WikipediaAPIWrapper
    tools = [WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())]
    
    # Create agent
    agent = DeepSeekAgentHandler(
        api_key=api_key,
        tools=tools,
        model_name=model_name,
        thread_id="demo_thread",
        memory=True
    )
    
    # Start interactive chat
    agent.chat()