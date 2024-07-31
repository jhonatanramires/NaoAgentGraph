from dotenv import load_dotenv
import os

from agent.agentHandler import NaoAgent, AgentHandler
from speechToText.whisperLoop import SpeechToText
from tools import tools

# Cargar las variables del archivo .env
load_dotenv()

# Acceder a las variables de entorno
api_key = os.getenv('API_KEY')
model_name = os.getenv('MODEL')
lang = os.getenv('AILANG')
thread_id = os.getenv('THREAD_ID')
nao_ip = os.getenv('NAO_IP')

print(api_key,model_name)

chatbot = AgentHandler(
  api_key=api_key,
  tools=tools,
  model_name=model_name,
  thread_id=thread_id,
  memory=True,
  lang='en',
)
nao_ip=nao_ip

#chatbot.display_graph(chatbot.graph)
#chatbot.display_graph(chatbot.llm_with_tools.get_graph())

#chatbot.chat()

try:
  recognizer = SpeechToText(Action=chatbot.prompt, trigger="realiza algo")
except Exception as e:
  print(f"Error during initialization: {e}")

recognizer.Loop()