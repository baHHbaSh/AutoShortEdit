from kivy.app import App
from kivy.core.window import Window
from kivy.uix import gridlayout, textinput, filechooser, switch, label, slider, button, popup

import json
import os
from videoprops import get_video_properties
import statistics

Datas = ["", 0, 20]

class RenderSettings(App):
	RList = []
	MRes = []
	def build(self):
		n1 = label.Label(text="Выбор папки с highlight")
		n2 = label.Label(text="Количество подразделений для видео, нужен если длина видео слишком большая (обычно 60 моментов на видео)")
		n3 = label.Label(text="Количество одновременно нарезаемых видео (важно чтобы все видео поместились в ОЗУ)")
		Lay = gridlayout.GridLayout(cols=1)
		d = gridlayout.GridLayout(rows=1)
		self.DirFc = filechooser.FileChooserListView()
		data = ["", 0, 20, []]
		try:
			with open("l", "r", encoding="utf-8") as f:
				data = json.load(f)
		except:pass
		self.DirTi = textinput.TextInput(text=data[0], multiline=False)
		self.DirSw = switch.Switch()
		self.DSWL = label.Label(text="Вкл: выбор папки из встроенного проводника\nВыкл: выбор папки из ввода текста")
		[d.add_widget(w) for w in [self.DirFc, self.DirTi, self.DirSw, self.DSWL]]

		l = gridlayout.GridLayout(rows=1)
		self.Divides = slider.Slider(min=0, max=10, value=data[1], step=1)
		self.DC = label.Label(text=f"{self.Divides.value}")
		[l.add_widget(w) for w in [self.Divides, self.DC]]

		o = gridlayout.GridLayout(rows=1)
		self.ProcessCounter = slider.Slider(min=1, max=100, value=data[2], step=1)
		self.PC = label.Label(text=f"{self.ProcessCounter.value}")
		[o.add_widget(w) for w in [self.ProcessCounter, self.PC]]

		StartButton = button.Button(text="Проверка материала + Рендер")
		StartButton.on_release=self.ResolutionCheck

		[Lay.add_widget(w) for w in [n1, d, n2, l, n3, o, StartButton]]
		Lay.on_touch_move = self.OTM
		self.OTM()
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
	def ResolutionCheck(self):
		ResList = []
		MList = []
		for video in os.listdir(self.DirTi.text):
			if ".mp4" in video:
				v = get_video_properties(f"{self.DirTi.text}\\{video}")
				ResList.append((v["width"], v["height"]))
		[MList.append(ResList.count(c)) for c in set(ResList)]
		if len(MList) == 1: self.RenderRun()
		MainResolution = tuple(set(ResList))[MList.index(max(MList))]
		print(MainResolution)
		self.DelPP(sum(MList)-max(MList))
		self.RList = ResList
		self.MRes = MainResolution
	def DelPP(self, Count):
		l = gridlayout.GridLayout(cols=1)
		l.add_widget(label.Label(text=f"Обнаружены видео с иным разрешением в кол-ве{Count}, которые могут повредить выходной результат, удалить?"))
		s = gridlayout.GridLayout(rows=1)
		delete = button.Button(text="Удалить (рекоменд.)")
		delete.on_release = self.DeleteAndRun
		skip = button.Button(text="Оставить так")
		skip.on_release = self.RenderRun
		[s.add_widget(el) for el in [skip, delete]]
		l.add_widget(s)
		pp = popup.Popup(title="Внимание", content=l, size_hint=[.9,.9])
		pp.open()
	def DeleteAndRun(self):
		''' Depricated
		for index, Name in enumerate(os.listdir(self.DirTi.text)):
			if self.RList[index] != self.MRes:
				os.remove(f"{self.DirTi.text}\\{Name}")
		'''
		self.RenderRun()
RenderSettings().run()