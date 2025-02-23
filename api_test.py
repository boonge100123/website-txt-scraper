from google.oauth2 import service_account
from googleapiclient.discovery import build
from link_scraper import extract_links
from link_to_txt_scraper import scrape_light_novel

# Set up the credentials
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "Y:/python api project/api information/website-txt-scraper-a0dffbd93641.json"

# Authenticate and create the service
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
docs_service = build('docs', 'v1', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

def create_google_doc(doc_title):
    """Creates a new Google Doc with the specified title."""
    if not isinstance(doc_title, str) or not doc_title.strip():
        raise ValueError(f"Invalid document title: {repr(doc_title)}")
    
    doc = {'title': doc_title.strip()}  # Trim whitespace
    doc = docs_service.documents().create(body=doc).execute()
    print(f"Created document with ID: {doc['documentId']}")
    return doc['documentId']

def append_text_to_doc(doc_id, text):
    """Appends text to a Google Doc."""
    # Get the current document to find the end
    document = docs_service.documents().get(documentId=doc_id).execute()
    end_index = document.get('body').get('content')[-1].get('endIndex') - 1  # Get the end index

    requests = [{
        'insertText': {
            'location': {'index': end_index},
            'text': text
        }
    }]
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()

def share_document(document_id, email):
    """Shares the created document with the specified email address."""
    permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': email
    }
    drive_service.permissions().create(
        fileId=document_id,
        body=permission,
        fields='id'
    ).execute()
    print(f"Document shared with {email} successfully!")

def main():
    toc_url = "https://cclawtranslations.home.blog/kawaikereba-hentai-demo-suki-ni-natte-kuremasu-ka-toc/"
    email_to_share = "jebeboone@gmail.com"
    
    # Extract links
    volumes = extract_links(toc_url)
    
    for volume_number, volume_info in volumes.items():
        doc_id = create_google_doc(f"Volume {volume_number}")  # Use "Volume {volume_number}" for the title
        
        # Loop through chapters and scrape text
        for chapter_title, chapter_url in volume_info['chapters'].items():
            print(chapter_url)  # Optional: Print the chapter URLs
            chapter_text = scrape_light_novel(chapter_url)  # Get the text for the chapter
            append_text_to_doc(doc_id, chapter_text)  # Append the text to the document

        # Share the document after all chapters are added
        share_document(doc_id, email_to_share)

if __name__ == "__main__":
    main()
