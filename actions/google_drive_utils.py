import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = r'D:\python\Face matching\credentials.json'  # Update with your file

# Authenticate Google Drive API
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

def download_images_from_drive(folder_id, local_folder="downloaded_images"):
    """ Downloads only missing images from Google Drive """
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    existing_files = set(os.listdir(local_folder))
    query = f"'{folder_id}' in parents and mimeType contains 'image/'"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    image_paths = []
    for file in files:
        file_name = file['name']
        file_path = os.path.join(local_folder, file_name)

        if file_name in existing_files:
            print(f"🔹 {file_name} already exists. Skipping download.")
            image_paths.append(file_path)
            continue

        file_id = file['id']
        request = drive_service.files().get_media(fileId=file_id)
        
        with open(file_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

        print(f"✅ Downloaded {file_name}")
        image_paths.append(file_path)

    return image_paths
