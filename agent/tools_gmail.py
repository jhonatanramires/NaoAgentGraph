from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langchain_google_community import GmailToolkit
# Can review scopes here https://developers.google.com/gmail/api/auth/scopes
# For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
# "https://www.googleapis.com/auth/gmail.send","https://www.googleapis.com/auth/gmail.compose",
credentials = get_gmail_credentials(
    token_file="./userData/gmailToken.json",
    scopes=["https://mail.google.com/","https://www.googleapis.com/auth/gmail.send","https://www.googleapis.com/auth/gmail.compose",],
    client_secrets_file="./utils/credentials.json",
)
api_resource = build_resource_service(credentials=credentials)

toolkit = GmailToolkit(api_resource=api_resource).get_tools()

print("a")

if __name__ == "__main__":
    for tool in toolkit:
        print(tool.name)
    # Crear un borrador de correo electrónico con los parámetros corregidos
    draft_response = toolkit[0].invoke({
        "message": "This is a test draft.",
        "to": ["test@example.com"],
        "subject": "Testing draft",
        "cc": ["cc_test@example.com"],  # Opcional: se puede omitir si no se necesita
        "bcc": ["bcc_test@example.com"]  # Opcional: se puede omitir si no se necesita
    })

    draft_response = toolkit[0].invoke({
        "message": "This is a test draft.",
        "to": ["test@example.com"],
        "subject": "Testing draft",
        "cc": ["cc_test@example.com"],  # Opcional: se puede omitir si no se necesita
        "bcc": ["bcc_test@example.com"]  # Opcional: se puede omitir si no se necesita
    })

    print("Draft created:", draft_response)