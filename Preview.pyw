import json
import os
from datetime import datetime

from kivy.app import App
from kivy.core.window import Window
from kivy.uix import gridlayout, label, slider, button, video


class Application(App):
	def build(self):
		tmp = []
		for Path in os.listdir():
			if not ".mp4" in Path:
				continue
			tmp.append([datetime.fromtimestamp(os.path.getmtime(os.getcwd()+"\\"+Path)).strftime("%B|%d|%Y"), Path])

		now = datetime.now().strftime("%B|%d|%Y")

		VideoNameList = []

		for data in tmp:
			if data[0] == now: VideoNameList.append(data[1])

		print(VideoNameList)

		Lay = gridlayout.GridLayout(cols=1)

		VidNamesLay = gridlayout.GridLayout(rows=1)
		[VidNamesLay.add_widget(button.Button(text=Name, on_release=self.OpenVideo)) for Name in VideoNameList]

		VidLay = gridlayout.GridLayout(cols=1)
		self.VideoPlayer = video.Video(source=f"{os.getcwd()}\\{VideoNameList[0]}")
		self.VideoPlayer.state = "play"

		[VidLay.add_widget(w) for w in []]

		[Lay.add_widget(w) for w in [VidNamesLay, VidLay]]

		return Lay
	def OpenVideo(self, Widget):
		self.VideoPlayer.source=f"{os.getcwd()}\\{Widget.text}"
Application().run()