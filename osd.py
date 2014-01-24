import bgui
from bge import logic, events

from pprint import pformat
from textwrap import wrap
from functools import partial

class PyDebugWidget(bgui.Frame):
	""" BGUI widget for printing debug info to game window. """
	def __init__(self, parent):
		super().__init__(parent, 'console', size=[1,1])
		self.frozen = True
		self.z_index = 1000000000
		
		self.frame = bgui.Frame(self, 'window', border=0)
		self.frame.colors = [(0, 0, 0, 0) for i in range(4)]
		self.frame.z_index = 0

		self.bg = bgui.Frame(self, 'bg', border=0)
		self.bg.colors = [(0, 0, 0, 0.5) for i in range(4)]
		self.bg.z_index = -1

		self.bg.size = [0, 0]
		self.bg.position = [0, 0.999]

		self.label = bgui.Label(self.frame, "label", text="", font=logic.expandPath("//UbuntuMono-B.ttf"), pt_size=29, pos=[0, 0], options=bgui.BGUI_DEFAULT)

		self.next_text = ""

		# self.last_time = 0

		# testing code 
		# strvar = "yadayadayada"
		# numvar = 1
		# self.log(strvar)
		# self.log(numvar)
		# self.log(self.frame.children)
		# self.log(self)
		# self.log({1: (1,2,3), 2: [4,5,6,[8,9,10]]}, pretty=True, nest=True)

	def run(self):
		""" Refresh the text in the console, and handle keyboard input to hide/show the console (CTRL+`). Add to BGUI system's run function """

		# Refresh the text
		self.label.text = self.next_text
		self._update()
		self.next_text = ""

		# hide/show the console
		if logic.keyboard.events[events.ACCENTGRAVEKEY]==1 and ( logic.keyboard.events[events.LEFTCTRLKEY]==2 or logic.keyboard.events[events.RIGHTCTRLKEY]==2 ):
			self.visible = not self.visible

	def log(self, info, pretty=False, nest=False):
		''' Add/update log entry

			Arguments:
			name -- the name for the entry. Used for log updating and is displayed for each entry
			info -- info to be displayed can be variable or string

			Keyword arguments
			pretty -- should dictionaries and objects be pretty-printed (default: False)
			nest -- should pretty-printed objects be printed in nested fomat (default: False)
		'''
		text = repr(info)
		if pretty:
			if nest:
				pprint_width = 1
			else:
				pprint_width = 108
			text = pformat(info, width=pprint_width, indent=2)
			print(text)
			text = text.replace("\n", "\n  ")
		else:
			text = wrap( text, 108 )
			text = "\n".join(text)
			print(text)
		text = "  " + text

		if len(self.next_text) > 0:
			self.next_text += "\n"

		self.next_text += text

	def _update(self):
		""" Update the formatting of the log """
		y_pos = 1 - 0.035
		
		if self.label.text != "":
			self.label.position = [0, y_pos]
			lines = self.label.text.count("\n")
			height = (lines+1)*0.029

			y_pos -= height

			self.bg.size = [1, 1-y_pos-0.01]
			self.bg.position = [0, y_pos+0.01]
		else:
			height = 0
			self.bg.size = [0, 0]
			self.bg.position = [0, 0]

class PyDebugOSD(bgui.System):
	""" A stand-alone BGUI system for running PyDebugOSD. Use only if not using BGUI elsewhere. """
	def __init__(self):
		bgui.System.__init__(self)
		self.console = PyDebugWidget(self)

	def run(self):
		""" Run per-frame callbacks and render the system """
		self.console.run()
		logic.getCurrentScene().post_draw = [self.render]

def main():
	obj = logic.getCurrentController().owner
	if 'log' not in obj:
		obj['log']= PyDebugOSD()
	obj['log'].run()