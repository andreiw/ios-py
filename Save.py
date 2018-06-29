import appex
import shutil
import console
import os

def main():
	if not appex.is_running_extension():
		print('This script is intended to be run from the sharing extension.')
		return

	name = appex.get_attachments()[0]
	if not name:
		console.hud_alert('Nothing to save?')
		return
	shutil.copy(name, os.path.expanduser('~/Documents/Downloads/'))
	console.hud_alert('done')
	
if __name__ == '__main__':
	main()
