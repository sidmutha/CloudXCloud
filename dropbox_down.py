from dropbox import client, rest, session
import webbrowser as w

APP_KEY = 'YOUR_APP_KEY' #insert your app key and secret
APP_SECRET = 'YOUR_APP_SECRET'
ACCESS_TYPE = 'dropbox'  # could be 'dropbox' or 'app_folder'

sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

request_token = sess.obtain_request_token()

url = sess.build_authorize_url(request_token)
w.open(url, new = 2)
#print "url: ", url

print "Visit. Allow. Enter."
raw_input()

access_token = sess.obtain_access_token(request_token)

client = client.DropboxClient(sess)
c_a_info = client.account_info()
print "Linked: ", c_a_info

def get_space():
	quota = c_a_info[u'quota_info'][u'quota']
	shared = c_a_info[u'quota_info'][u'shared']
	normal = c_a_info[u'quota_info'][u'normal']
	used = shared + normal
	return (used, quota)
	

def upload_file(src, dest):
	with open(src) as f:
		response = client.put_file(dest, f)
		print "uploaded: ", response

def download_file(src, dest):
	with open(dest, 'w') as fil:
		f = client.get_file(src)
		fil.write(f.read())
		print fil

def list_files(src):
	response = client.metadata(src)
	#print "Response:\n" + response
	return response

def list_filenames(src):
	response = list_files(src)
	names = []
	for f in response[u'contents']:
		names.append((f[u'path'],f[u'is_dir']))
	return names
def delete_file(src):
	client.file_delete(src)
