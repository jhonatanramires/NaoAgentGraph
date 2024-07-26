# /////////////////// THIRD-PARTY DEPENDENCIES ///////////////////////////////

# Dependencies for Type Annotations
from typing import Annotated
from typing_extensions import TypedDict

# Dependencies for Graph Tools
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition

# Dependencies for LLM Chat
from langchain_anthropic import ChatAnthropic
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

# Dependencies for Graph Display
from PIL import Image as PILImage
from IPython.display import Image, display
import io

# Dependencies for Memory Management
from langgraph.checkpoint.sqlite import SqliteSaver

# Dependencies for Messages Management (Human Node Depedend on this)
from langchain_core.messages import AIMessage, ToolMessage

#Dependencies for Text To Spech
import subprocess

# /////////////////// PROJECT-SPECIFIC DEPENDENCIES ///////////////////////////////
from dotenv import load_dotenv
import os

# Define la clase AgentHandler que maneja la lógica principal del agente conversacional
class AgentHandler:
    # Define una clase anidada State para tipar el estado del agente
    class State(TypedDict):
        messages: Annotated[list, add_messages]

    def __init__(self, api_key, tools, model_name, thread_id, memory=True, lang="en"):
        """
        Inicializa el AgentHandler con los parámetros necesarios.
        
        :param api_key: Clave API para el modelo de lenguaje
        :param tools: Herramientas disponibles para el agente
        :param model_name: Nombre del modelo de lenguaje a utilizar
        :param thread_id: ID único para el hilo de conversación
        :param memory: Si es True, se habilita la memoria persistente
        :param lang: Idioma para la síntesis de voz
        """
        self.set_cons(tools=tools, lang=lang, memory=memory)
        self.llm = ChatAnthropic(model_name=model_name, api_key=api_key)
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        if self.memory:
            self.checkpointer = SqliteSaver.from_conn_string("memory")
        self.graph = self._setup_graph()
        self.config = {"configurable": {"thread_id": f"{thread_id}"}}

    def set_cons(self, tools, lang, memory):
        """
        Establece las constantes del agente.
        
        :param tools: Herramientas disponibles
        :param lang: Idioma para la síntesis de voz
        :param memory: Bandera para habilitar/deshabilitar la memoria
        """
        self.tools = tools
        self.lang = lang
        self.memory = memory

    def _chatbot(self, state: State):
        """
        Función interna que maneja la lógica del chatbot.
        
        :param state: Estado actual del agente
        :return: Nuevo estado con la respuesta del modelo
        """
        messages = state["messages"]
        print("================================ Debug Messages ================================")
        print("Debug: Messages before LLM invocation:", messages[-1], end="\n\n")
        for message in messages:
            if isinstance(message, ToolMessage):
                print(message)
        result = self.llm_with_tools.invoke(messages)
        print("Debug: LLM response:", result, end="\n")
        return {"messages": [result]}
    
    def speak(self, text):
        """
        Sintetiza el texto a voz utilizando un ejecutable externo.
        
        :param text: Texto a sintetizar
        """
        print(f'afdskjlfñalkkfklakfsdksfjkl,speak_{self.lang}_arg.exe')
        speak_command = f'speak_{self.lang}_arg.exe "{text}"'
        process = subprocess.Popen(speak_command, stdout=subprocess.PIPE)
    
    def _setup_graph(self):
        """
        funcion interna que configura el grafo de estados para el flujo de conversación.
        
        :return: Grafo compilado
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
        else:
            return graph_builder.compile()

    def display_graph(self, graph):
        """
        Muestra una representación visual del grafo que se pase como argumento
        
        :param graph: Grafo a visualizar
        """
        try:
            img_data = graph.get_graph().draw_mermaid_png()
            if img_data:
                img = PILImage.open(io.BytesIO(img_data))
                img.show()
            else:
                print("The image was not generated correctly.")
        except Exception as e:
            print(f"Error generating the image: {e}")

    def chat(self):
        """
        Inicia un bucle de chat interactivo con el usuario.
        """
        while True:
            print("===============================================================================")
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            try:
                for event in self.graph.stream({"messages": [("user", user_input)]}, self.config, stream_mode="values"):
                    if isinstance(event["messages"][-1], AIMessage):
                        self.speak(event["messages"][-1].content)
                        pass
                    event["messages"][-1].pretty_print()
            except Exception as e:
                print(f"Error occurred: {e}")

# Clase NaoAgent que hereda de AgentHandler, específica para el robot NAO
class NaoAgent(AgentHandler):
    def __init__(self, api_key, tools, model_name, thread_id, memory=True, lang="es", nao_ip="127.0.0.1",nao_desc=""):
        """
        Inicializa un agente específico para el robot NAO.
        
        :param nao_ip: Dirección IP del robot NAO
        """
        super().__init__(api_key=api_key,tools=tools,model_name=model_name,thread_id=thread_id,memory=memory,lang=lang)
        self.nao_ip = nao_ip
        self.nao_desc = nao_desc

    def personality(self):
        print(self.nao_desc)

    def speak(self, text):
        """
        Sobrescribe el método speak para utilizar la síntesis de voz del robot NAO.
        
        :param text: Texto a sintetizar
        """
        speak_command = "python2 .\\Nao\\NaoSpeak.py  " + text
        print(speak_command)
        process = subprocess.Popen(speak_command.split(), stdout=subprocess.PIPE)

if __name__ == "__main__":
    # Dependencies for Custom Tools
    from tools import tools
    # Cargar las variables del archivo .env
    load_dotenv()

    # Acceder a las variables de entorno
    api_key = os.getenv('API_KEY')
    model_name = os.getenv('MODEL')
    chatbot = AgentHandler(api_key, tools, "claude-3-haiku-20240307", 1)
    #chatbot.display_graph()
    chatbot.chat()