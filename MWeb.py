import ui
import os
import urllib
import sound
import urllib3

class MyView (ui.View):
	@ui.in_background
	def will_close(self):
		p = self['web'].p
		if p:
			p.stop()
		pass

class midiDelegate (object):
	def webview_should_start_load(self,webview, url, nav_type):
		if url.endswith('.mid'):
			fname = url.split('/')[-1]
			fname = os.path.join(os.path.expanduser('~/Documents/Downloads'), fname)
			http = urllib3.PoolManager()
			response = http.request('GET', url)
			with open(fname, 'wb') as f:
				f.write(response.data)
			webview.p = sound.MIDIPlayer(fname)
			webview.p.play()
			return False
		return True

def midi_stop(obj):
	p = obj.superview.superview['web'].p
	if p:
		p.stop()
		
def go_back(obj):
	p = obj.superview.superview['web']
	p.go_back()
	
def go_fwd(obj):
	p = obj.superview.superview['web']
	p .go_forward()

v = ui.load_view('MWebUI')
w = v['web']
w.p = None
w.delegate = midiDelegate()
w.load_url('http://ingeb.org')

if ui.get_screen_size()[1] >= 768:
	v.present('sheet')
else:
	v.present(orientations=['portrait'])

