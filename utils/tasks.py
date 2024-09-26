import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/tasks"]

def getCredentials():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("./utils/token.json"):
    creds = Credentials.from_authorized_user_file("./utils/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "./utils/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("./utils/token.json", "w") as token:
      token.write(creds.to_json())

  return creds

def main():
  """Shows basic usage of the Tasks API.
  Prints the title and ID of the first 10 task lists.
  """
  creds = getCredentials()
  
if __name__ == "__main__":
  main()