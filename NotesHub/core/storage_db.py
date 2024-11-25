
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from django.conf import settings
from googleapiclient.errors import HttpError


supported_file_types = ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf', 'txt', 'html', 'xml']

SCOPES = ['https://www.googleapis.com/auth/drive']

creds = service_account.Credentials.from_service_account_file(
    settings.GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)

def getFolderId():
    query = "mimeType='application/vnd.google-apps.folder' and name='{0}'".format(settings.GOOGLE_DRIVE_STORAGE_MEDIA_ROOT)
    try:
        response = service.files().list(q=query, spaces='drive').execute()
        files = response.get('files', [])
        if files:
            # Folder exists, return its ID
            return files[0]['id']
        else:
            # Folder doesn't exist, create it
            file_metadata = {
                'name': 'notes',
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = service.files().create(body=file_metadata, fields='id').execute()
            return folder.get('id')
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None
    
def makeFilesPublic(fileId):
    try:
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        service.permissions().create(
            fileId=fileId,
            body=permission
        ).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
        raise


def uploadToDrive(filename, filepath):

    folderId = getFolderId()

    if folderId is None:
        print("Unable to find or create notes folder.")
        return None, None, None
    print("filename: ", filename)
    print("filepath: ", filepath)
    file_metadata = {
        'name': filename,
        'parents': [folderId],  # Place the file in the "notes" folder
        # 'mimeType': 'application/vnd.google-apps.file'
    }
    media = MediaFileUpload(filepath)
    # https://drive.google.com/uc?id=1y96EvPmitSfJYmJatGOUbGEpypZvqyrs&export=download
    #  https://drive.google.com/file/d/1y96EvPmitSfJYmJatGOUbGEpypZvqyrs/view?usp=drivesdk
    try:
        drivefile = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        # change file permission to public
        makeFilesPublic(drivefile.get('id'))

        file_type = filename.split('.')[-1]

        download_url = 'https://drive.google.com/uc?id={0}&export=download'.format(drivefile.get('id'))
        preview_url = 'https://drive.google.com/file/d/{0}/preview?usp=drivesdk'.format(drivefile.get('id'))
        thumbnail_url = ''
        if file_type in supported_file_types:
            thumbnail_url = 'https://drive.google.com/thumbnail?authuser=0&id={0}'.format(drivefile.get('id'))
        return download_url, thumbnail_url, preview_url
        
    except Exception as error:
        print(f'Error occurred: {error}')
        return None, None, None

