from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langchain_google_community import GmailToolkit

# Can review scopes here https://developers.google.com/gmail/api/auth/scopes
# For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
credentials = get_gmail_credentials(
    token_file="gmailToken.json",
    scopes=["https://mail.google.com/","https://www.googleapis.com/auth/gmail.send","https://www.googleapis.com/auth/gmail.compose",],
    client_secrets_file="./utils/credentials.json",
)
api_resource = build_resource_service(credentials=credentials)

toolkit = GmailToolkit(api_resource=api_resource).get_tools()

tools = [toolkit]

if __name__ == "__main__":
  print(tools)