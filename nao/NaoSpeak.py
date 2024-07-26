import sys
import codecs
import dotenv
import os

sys.path.append("C:\\Users\\Windows 10\\Pictures\\Nao\\lib")

from naoqi import ALProxy

# Cargar las variables del archivo .env
dotenv.load_dotenv("..\\.env")

# Acceder a las variables de entorno
naoip = os.getenv('NAO_IPS')

tts = ALProxy("ALTextToSpeech", "169.254.219.188", 9559)

phrase = ""

for text in sys.argv:
    if text == sys.argv[0]:
        pass
    else:
        phrase += text + " "

phrase = phrase.decode('utf-8', 'ignore')
phrase = phrase.encode('utf-8', 'ignore')
tts.say(phrase)