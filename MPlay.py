import ui
import sound
import os
import console
import threading
import sys
import time
import queue
import enum

class StateControl(enum.Enum):
	PLAY = 1
	STOP = 2
	NEXT = 3
	KILL = 4

class PlayState (object):
	def __init__(self, view):
		'@type view: ui.View'
		self.v = view
		self.q = queue.Queue()
		self.files = None
		self.p = None
		self.path = None
		self.loop = True
		self.playing = False
		self.update_view()
		self.t = PlayThread(self)
		self.t.start()
	def next_file(self):
		loop = False
		while True:
			if self.files is None:
				if loop:
					return None
				self.files = os.scandir(os.path.expanduser('~/Documents/Downloads'))
				loop = True
			f = next(self.files, None)
			if f is None:
				self.files = None
				if state.loop:
					continue
				return None
			if not f.is_file():
				continue
			name, ext = os.path.splitext(f.name)
			if ext != '.mid':
				continue
			return f.path		
		
	def lets_play(self):
		self.q.put(StateControl.PLAY)
	def lets_stop(self):
		self.q.put(StateControl.STOP)
	def lets_next(self):
		self.q.put(StateControl.NEXT)
	def terminate(self):
		self.q.put(StateControl.KILL)
		self.t.join()
	def update_view(self):
		self.v.set_needs_display()
	def stop(self):
		if self.p:
			self.p.stop()
		self.playing = False
		self.update_view()
	def play(self):
		if not self.p:
			self.prepare_next()
		if self.p:
			self.p.current_time = 0
			self.p.play()
			self.playing = True
			self.update_view()
	def prepare_next(self):
		self.p = None
		self.path = self.next_file()
		if self.path:
			self.p = sound.MIDIPlayer(os.path.expanduser(self.path))
	def next(self):
		self.stop()
		self.prepare_next()
		self.update_view()
		if self.p:
			self.play()

class PlayThread(threading.Thread):
	def __init__(self, state):
		threading.Thread.__init__(self)
		self.state = state
	def deq(self):
		if self.state.p and self.state.p.current_time >= self.state.p.duration:
			return StateControl.NEXT
		if self.state.playing and self.state.q.empty():
			return None
		else:
			return self.state.q.get()
			
	def run(self):
		while True:
			what = self.deq()
			if what is None:
				time.sleep(0.25)
				continue
			elif what == StateControl.STOP:
				self.state.stop()
			elif what == StateControl.KILL:
				self.state.stop()
				return
			elif what == StateControl.PLAY:
				self.state.play()
			else:
				self.state.next()
		
class MyView (ui.View):
	@ui.in_background
	def will_close(self):
		state.terminate()
		pass
	def draw(self):
		if state.path:
			self.name = os.path.basename(state.path)
		else:
			self.name = 'MIDI player'
		if not state.playing:
			self['play'].enabled = True
			self['stop'].enabled = False
			self['next'].enabled = False
			console.set_idle_timer_disabled(False)
		else:
			self['play'].enabled = False
			self['stop'].enabled = True
			self['next'].enabled = True
			console.set_idle_timer_disabled(True)

def play_hit(sender):
	'@type sender: ui.Button'
	state.lets_play()

def stop_hit(sender):
	'@type sender: ui.Button'
	state.lets_stop()

def next_hit(sender):
	'@type sender: ui.Button'
	state.lets_next()

v = ui.load_view('MPlayUI')
state = PlayState(v)

if ui.get_screen_size()[1] >= 768:
	v.present('sheet')
else:
	v.present(orientations=['portrait'])

