import logging
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

# Set up logging
logging.basicConfig(level=logging.INFO)

def create_google_doc(doc_title):
    """Creates a new Google Doc with the specified title."""
    if not isinstance(doc_title, str) or not doc_title.strip():
        raise ValueError(f"Invalid document title: {repr(doc_title)}")
    
    doc = {'title': doc_title.strip()}  # Trim whitespace
    doc = docs_service.documents().create(body=doc).execute()
    print(f"Created document with ID: {doc['documentId']}")
    return doc['documentId']

def append_text_to_doc(doc_id, text):
    """Appends text to a Google Doc, starting on a new page."""
    try:
        document = docs_service.documents().get(documentId=doc_id).execute()
        end_index = document.get('body').get('content')[-1].get('endIndex') - 1

        # Insert a page break before the new text
        requests = [{
            'insertPageBreak': {
                'location': {'index': end_index}  # Insert page break at the end of current content
            }
        }, {
            'insertText': {
                'location': {'index': end_index + 1},  # Adjust index to insert text after the page break
                'text': text
            }
        }]
        docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
        logging.info(f"Appended text to document ID: {doc_id}")
    except Exception as e:
        logging.error(f"Error appending text to document ID {doc_id}: {e}")

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
    
    try:
        volumes = extract_links(toc_url)
        for volume_number, volume_info in volumes.items():
            doc_id = create_google_doc(f"Volume {volume_number}")

            for chapter_title, chapter_url in volume_info['chapters'].items():
                logging.info(f"Processing chapter: {chapter_title} from URL: {chapter_url}")
                chapter_text = scrape_light_novel(chapter_url)
                append_text_to_doc(doc_id, chapter_text)

            share_document(doc_id, email_to_share)
    except Exception as e:
        logging.error(f"An error occurred in the main process: {e}")

if __name__ == "__main__":
    main()
