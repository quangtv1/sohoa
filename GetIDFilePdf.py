
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tabulate import tabulate
from urllib.parse import urlparse, parse_qs
# ...
# If modifying these scopes, delete the file token.pickle.

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    drive_Id="1xC7oNVF5jTxruho0Vk_jsNbUpdpsYlPW"
    folder_url = 'https://drive.google.com/drive/folders/1xC7oNVF5jTxruho0Vk_jsNbUpdpsYlPW'
    csv_file = 'list_all_pdf_phuong_lam.csv'

    service = get_gdrive_service()
    list_files_recursive(service, folder_url, drive_Id, csv_file)

def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    return build('drive', 'v3', credentials=creds)

def extract_folder_id(url):
    """extracts folder ID from Google Drive URL"""
    parsed_url = urlparse(url)
    path = parsed_url.path.strip('/')
    folder_id = None
    if path.startswith('drive/folders/'):
        folder_id = path.split('drive/folders/')[1].split('/')[0]
    elif path.startswith('folders/'):
        folder_id = path.split('folders/')[1].split('/')[0]
    return folder_id

def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"
    
def list_files_recursive(service, folder_url, drive_id, csv_file):
    """Recursively list all PDF files in the folder and its subfolders"""
    folder_id = extract_folder_id(folder_url)

    # List all files and subfolders in the folder
    results = service.files().list(
        corpora="drive",
        driveId=drive_id,
        includeItemsFromAllDrives=True,
        q=f"'{folder_id}' in parents and trashed=false",
        fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime, webViewLink)"
    ).execute()

    # Get the files and subfolders in the folder
    items = results.get('files', [])

    # List all files in the folder
    files = [item for item in items if item['mimeType'] == 'application/pdf']
    if files:
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            for file in files:
                id = file["id"]
                name = file["name"]
                parents = file.get("parents", "N/A")
                size = get_size_format(int(file.get("size", 0)))
                mime_type = file["mimeType"]
                modified_time = file["modifiedTime"]
                webView_link = file["webViewLink"]

                writer.writerow([id, name, parents, size, mime_type, modified_time, webView_link])

    # Recursively list files in subfolders
    subfolders = [item for item in items if item['mimeType'] == 'application/vnd.google-apps.folder']
    for subfolder in subfolders:
        subfolder_url = f"https://drive.google.com/drive/folders/{subfolder['id']}"
        list_files_recursive(service, subfolder_url, drive_id, csv_file)

if __name__ == '__main__':
    main()


