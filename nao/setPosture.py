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

arp = ALProxy("ALRobotPosture", "169.254.219.188", 9559)

posture = ""

if sys.argv[1]:
    posture = sys.argv[1]
else:
    posture = "Sit"


arp.goToPosture(posture, 0.5)