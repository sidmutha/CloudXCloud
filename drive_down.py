#!usr/bin/python

import httplib2
import pprint
from operator import itemgetter as iG
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from apiclient import errors
import mimetypes 
import webbrowser as w

CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'

OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

#FILENAME = 'drive_down.py'

def grunt_work():
	flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
	authorize_url = flow.step1_get_authorize_url()
	w.open(authorize_url, new = 2)
	code = raw_input().strip()
	credentials = flow.step2_exchange(code)

	http = httplib2.Http()
	http = credentials.authorize(http)

	drive_service = build('drive', 'v2', http = http)
	return drive_service

def upload_file(filename, drive_service):
	mimetype = mimetypes.guess_type(filename)[0]
	media_body = MediaFileUpload(filename, mimetype = mimetype, resumable = True)
	body = {
			'title': filename.split('/')[-1],
			'description': '',
			'mimeType': mimetype
			}
	file = drive_service.files().insert(body = body, media_body =
			media_body).execute()
	pprint.pprint(file)

def download_file(filename, drive_service):
	files = drive_service.files().list(q = 'title="%s"' % filename, maxResults = 10).execute()
	files = files.get('items')
	for f in files:
		#print f.get('title')
		#if f.get('title') is filename:
		download_url = f.get('downloadUrl')
		if download_url:
			resp, content = drive_service._http.request(download_url)
			if resp.status == 200:
				with open(filename, 'w') as fil:
					fil.write(content)
					print fil
			else:
				print 'An error! %s' % resp
		else:
			print 'No URL'

def list_files(drive_service):
	files = drive_service.files().list().execute()
	files = files.get('items')
	all_files = []
	for f in files:
		if f[u'mimeType'] is not u'application/vnd.google-apps.folder':
			all_files.append((f, False))
		else:
			all_files.append((f, True))
	return all_files

def list_file_titles(drive_service):
	l = retrieve_all_files(drive_service)
	names = []
	for i in l:
		if not i.get(u'labels').get(u'trashed'):
			names.append((i[u'title'], i[u'parents'], i[u'mimeType'] == u'application/vnd.google-apps.folder', i[u'id'], i.get(u'downloadUrl')))
	return names

def list_in_root(drive_service):

	l = list_file_titles(drive_service)
	things = []
	for i in l:
		for p in i[1]:
			if p.get(u'isRoot'):
				things.append(i)
	
	return things

def get_space(drive_service):
	o = drive_service.about().get().execute()
	return ((int(o['quotaBytesUsed']) ,int(o['quotaBytesTotal'])))


def retrieve_all_files(service):
  """Retrieve a list of File resources.

  Args:
    service: Drive API service instance.
  Returns:
    List of File resources.
  """
  result = []
  page_token = None
  while True:
    try:
      param = {}
      if page_token:
        param['pageToken'] = page_token
      files = service.files().list(**param).execute()
      
      result.extend(files['items'])
      page_token = files.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      break
  
  #result = sorted(result, key = iG(u''))
  return result

def delete_file(fId, drive_service):
	print(fId)
	drive_service.files().trash(fileId = fId).execute()
