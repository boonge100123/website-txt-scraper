from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up the credentials
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "Y:/python api project/api information/website-txt-scraper-a0dffbd93641.json"  # Forward slashes

# Authenticate and create the service
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
docs_service = build('docs', 'v1', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

def create_google_doc(doc_title):
    """Creates a new Google Doc with the specified title."""
    doc = {
        'title': doc_title
    }
    doc = docs_service.documents().create(body=doc).execute()
    print(f"Created document with ID: {doc['documentId']}")
    return doc['documentId']

def share_document(document_id, email):
    """Shares the created document with the specified email address."""
    permission = {
        'type': 'user',
        'role': 'writer',  # Change to 'reader' for read-only access
        'emailAddress': email
    }

    # Share the document
    drive_service.permissions().create(
        fileId=document_id,
        body=permission,
        fields='id'
    ).execute()
    print(f"Document shared with {email} successfully!")

if __name__ == "__main__":
    document_name = "test My New Google Document"
    email_to_share = "jebeboone@gmail.com"  # Replace with your Google account email

    # Create a new document
    document_id = create_google_doc(document_name)

    # Share the document with the specified email
    share_document(document_id, email_to_share)
