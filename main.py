from dotenv import load_dotenv
import os

from agent.agentHandler import AgentHandler
from tools import tools

# Cargar las variables del archivo .env
load_dotenv()

# Acceder a las variables de entorno
api_key = os.getenv('API_KEY')
model_name = os.getenv('MODEL')
lang = os.getenv('AILANG')
thread_id = os.getenv('THREAD_ID')

print(api_key,model_name)

chatbot = AgentHandler(
  api_key=api_key,
  tools=tools,
  model_name=model_name,
  thread_id=thread_id,
  memory=True,
  lang=lang
)

chatbot.display_graph(chatbot.graph)
chatbot.display_graph(chatbot.llm_with_tools.get_graph())
chatbot.chat()