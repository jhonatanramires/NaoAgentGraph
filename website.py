import streamlit as st
import os
from dotenv import load_dotenv, set_key
from agent.agentHandler import AgentHandler
from tools import tools
# Cargar las variables del archivo .env
load_dotenv('../.env')

LANGS = ["es: Español","en: English"]

# Acceder a las variables de entorno
st.session_state['chatbot_api_key'] = os.getenv('API_KEY')
st.session_state['model_name'] = os.getenv('MODEL')
lang = int(os.getenv('AILANG'))
thread_id = os.getenv('THREAD_ID')
nao_ip = os.getenv('NAO_IP')

chatbot = AgentHandler(
  api_key=st.session_state['chatbot_api_key'],
  tools=tools,
  model_name=st.session_state['model_name'],
  thread_id=thread_id,
  memory=True,
  lang="es",
)

def update():
  global UPDATE
  UPDATE = True

def updateEnv():
  global lang
  #set_key('./.env', env_var_name, env_var_value)
  set_key('../.env', "AILANG", str(LANGS.index(language)))
  lang = LANGS.index(language)

with st.sidebar:
    language = st.selectbox("Language of the Text To Speech",key="language",options=["es: Español","en: English"])
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    thread_id = st.text_input("Which memory you will use",key="thread_id")
    
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")
st.caption("🚀 A chatbot agent shown by Streamlit")

print(st.session_state)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = "OpenAI(api_key=openai_api_key)"
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    msg = chatbot.response(st.session_state.messages[-1]["content"])
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)