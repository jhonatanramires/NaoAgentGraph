from langchain_core.tools import tool
from langchain_community.tools import HumanInputRun
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import sys
from agent.tools_weather import get_temperature, get_apparent_temperature, get_day_or_night, get_full_weather_report, get_precipitation, get_rain, get_relative_humidity, get_showers, get_snowfall
import os

sys.path.append("..\\utils")

import subprocess

load_dotenv()

tavily_api_key = os.getenv('TAVILY_API_KEY')

search = TavilySearchResults(tavily_api_key=tavily_api_key)

def postureNao(posture):
    Nao_command = "python2 .\\Nao\\setPosture.py " + str(posture)
    process = subprocess.Popen(Nao_command.split(), stdout=subprocess.PIPE)
    return "success"

@tool 
def set_posture_to(posture: str) -> str:
    """Usefull function when ask you for take or go to a posture only if the posture is in the following array ["StandInit","SitRelax","StandZero","LyingBelly","LyingBack","Stand","Crouch","Sit"]
       :param posture: posture to do must be a string not list or anything else
    """
    postureNao(posture)
    return "posture done"

@tool 
def say_joke(joke: str) -> str:
    """Usefull function when ask you for tell a joke you must pass the joke as argument but you must ASK before using this function to human concern"""
    print("JAJAJAJ JOKE",joke,"====================")
    return "joke sucessfully said"

def get_input() -> str:
    print("Insert your text. Enter 'q' or press Ctrl-D (or Ctrl-Z on Windows) to end.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "q":
            break
        contents.append(line)
    return "\n".join(contents)

human = HumanInputRun(input_func=get_input)

tools = [
  set_posture_to, 
  say_joke, 
  get_temperature, get_apparent_temperature, get_day_or_night, get_full_weather_report, get_precipitation, get_rain, get_relative_humidity, get_showers, get_snowfall,
  human,
  search 
]

if __name__ == "__main__":   
    #postureNao("Crouch")
    print(search.invoke({"query": "What happened in the latest burning man floods"}))
