from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

from pydrive.drive import GoogleDrive

drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'title': 'Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
file1.SetContentString('Hello World!') # Set content of the file from given string.
file1.Upload()


params = {
    'gdrive_folder_id' : '1FumjvqmkvENsulhJzOQvNN5KGX7EeVNn', # the ID of gdrive folder to get data from
    'data_dir' : 'C:/Users/njcy8/Documents/Projects/gs_fromDrive_2_bq/data_dl', # the path to download the gdrive data to e.g. '/content/data'
    'sheet_names' : ['HW','TRUG','BUN'], # These are the sheet names for each spreadsheet to read in as pandas dataframe
}

# choose a local (colab) directory to store the data.
local_download_path = os.path.expanduser(params['data_dir'])
try:
  os.makedirs(local_download_path)
except: pass

# 2. Auto-iterate using the query syntax
#    https://developers.google.com/drive/v2/web/search-parameters
file_list = drive.ListFile(
    {'q': f"'{params['gdrive_folder_id']}' in parents"}).GetList()

for f in file_list:
  # 3. Create & download by id.
  print('title: %s, id: %s' % (f['title'], f['id']))
  fname = os.path.join(local_download_path, f['title'])
  print('downloading to {}'.format(fname))
  f_ = drive.CreateFile({'id': f['id']})
  f_.GetContentFile(fname)

