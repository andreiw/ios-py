import appex
import urllib3
import os
import console

def main():
	if not appex.is_running_extension():
		print('This script is intended to be run from the sharing extension.')
		return
		
	url = appex.get_url()
	if not url:
		print('No URL?')
		return
		
	fname = url.split('/')[-1]
	fname = os.path.join(os.path.expanduser('~/Documents/Downloads'), fname)

	http = urllib3.PoolManager()
	response = http.request('GET', url)
	with open(fname, 'wb') as f:
		f.write(response.data)
	console.hud_alert('done')
	
if __name__ == '__main__':
	main()
