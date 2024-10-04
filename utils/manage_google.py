from os import path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/tasks"]
def sing_in(cred_path,dir_path):
  creds = None
  # Function that create the credentials of the account signed in
  if path.exists(f"{dir_path}/token.json"):
    creds = Credentials.from_authorized_user_file(f"{dir_path}/token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          cred_path, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(f"{dir_path}/token.json", "w") as token:
      token.write(creds.to_json())

if __name__ == "__main__":
  sing_in("./credentials.json","./test/userData")