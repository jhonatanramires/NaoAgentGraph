from langchain_community.chat_models import ChatOllama
from langchain.agents import create_xml_agent, AgentExecutor
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain import hub

# aña
from langchain.tools import BaseTool, StructuredTool, tool

class AgentHandler():
    def __init__(self,tools):
        #charge llm and format the system_message
        self.memory = ChatMessageHistory(session_id="test-session")
        self.llm = ChatOllama(model="gemma:2b")
        self.tools = tools
        prompt = hub.pull("richard-park/xml-agent-convo")
        
        # construct OpenAIFunctionAgent
        self.agent = create_xml_agent(
          llm=self.llm, 
          tools=self.tools, 
          prompt=prompt
        )
        
        #  creating agent executor
        self.agent_executor = AgentExecutor(
          agent=self.agent, 
          tools=self.tools, 
          verbose=True,
          return_intermediate_steps=True,
          handle_parsing_errors=True
        )
        self.agent_with_chat = RunnableWithMessageHistory(
            self.agent_executor,
            # This is needed because in most real world scenarios, a session id is needed
            # It isn't really used here because we are using a simple in memory ChatMessageHistory
            lambda session_id: self.memory,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    def run(self,prompt):
        return self.agent_with_chat.invoke({"input": prompt},config={"configurable": {"session_id": "<foo>"}},)['output']

if __name__ == "__main__":
  @tool
  def add(a: int) -> int:
      """Adds a and b.

      Args:
        a: first int,
        b: second int
      """
      return int(a) + 4
  
  tools = [add]

  agent = AgentHandler(tools=tools)
  agent.run("Hello world")