from kivy.app import App
from kivy.core.window import Window
from kivy.uix import gridlayout, textinput, filechooser, switch, label, slider, button

import json
import os

Datas = ["", 0, 20]

class RenderSettings(App):

	def build(self):
		n1 = label.Label(text="Выбор папки с highlight")
		n2 = label.Label(text="Количество подразделений для видео, нужен если длина видео слишком большая")
		n3 = label.Label(text="Количество одновременно нарезаемых видео (важно чтобы все видео поместились в ОЗУ)")
		Lay = gridlayout.GridLayout(cols=1)
		d = gridlayout.GridLayout(rows=1)
		self.DirFc = filechooser.FileChooserListView()
		data = ""
		try:
			with open("d", "r", encoding="utf-8") as f:
				data = f.read()
		except:pass
		self.DirTi = textinput.TextInput(text=data, multiline=False)
		self.DirSw = switch.Switch()
		self.DSWL = label.Label(text="Вкл: выбор папки из встроенного проводника\nВыкл: выбор папки из ввода текста")
		[d.add_widget(w) for w in [self.DirFc, self.DirTi, self.DirSw, self.DSWL]]

		l = gridlayout.GridLayout(rows=1)
		self.Divides = slider.Slider(min=0, max=10, value=0, step=1)
		self.DC = label.Label(text=f"{self.Divides.value}")
		[l.add_widget(w) for w in [self.Divides, self.DC]]

		o = gridlayout.GridLayout(rows=1)
		self.ProcessCounter = slider.Slider(min=1, max=100, value=20, step=1)
		self.PC = label.Label(text=f"{self.ProcessCounter.value}")
		[o.add_widget(w) for w in [self.ProcessCounter, self.PC]]

		StartButton = button.Button(text="Рендер")
		StartButton.on_release=self.RenderRun

		[Lay.add_widget(w) for w in [n1, d, n2, l, n3, o, StartButton]]
		Lay.on_touch_move = self.OTM
		return Lay
	def OTM(self, *_):
		global Datas
		self.DC.text = f"{int(self.Divides.value)}"
		Datas[1] = int(self.Divides.value)
		self.PC.text = f"{self.ProcessCounter.value}"
		Datas[2] = self.ProcessCounter.value
	def RenderRun(self):
		global Datas
		Datas[0] = self.DirFc.path if self.DirSw.active else self.DirTi.text
		with open("d", "w", encoding="utf-8") as f:
			f.write(Datas[0])
		with open("l", "w", encoding="utf-8") as f:
			json.dump(Datas, f)
		try:
			os.system(f"start {os.getcwd()}/Render.py")
		except:
			os.system(f"start {os.getcwd()}/Render.exe")
		Window.close()
RenderSettings().run()