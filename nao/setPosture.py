#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use goToPosture Method"""

import sys
import dotenv
import os

sys.path.append("C:\\Users\\Windows 10\\Pictures\\Nao\\lib")

import qi
import argparse

# Cargar las variables del archivo .env
dotenv.load_dotenv("..\\.env")

# Acceder a las variables de entorno
naoip = os.getenv('NAO_IP')

def main(session):
    """
    This example uses the goToPosture method.
    """
    # Get the service ALRobotPosture.

    posture_service = session.service("ALRobotPosture")

    posture_service.goToPosture(args.posture, 0.5)

    print posture_service.getPostureFamily()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--posture", type=str, default="Sit",
                    help="Naoqi port number")
   

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + naoip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + naoip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)