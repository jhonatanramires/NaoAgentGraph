import sys
import codecs
import dotenv
import os

sys.path.append("C:\\Users\\Windows 10\\Pictures\\Nao\\lib")

# Cargar las variables del archivo .env
dotenv.load_dotenv("..\\.env")

# Acceder a las variables de entorno
naoip = os.getenv('NAO_IPS')

from naoqi import ALProxy

photoCaptureProxy = ALProxy("ALPhotoCapture", naoip, 9559)

photoCaptureProxy.setResolution(2)
photoCaptureProxy.setPictureFormat("jpg")
photoCaptureProxy.takePictures(3, "/home/nao/recordings/cameras/", "image")

