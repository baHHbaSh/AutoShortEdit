from multiprocessing import Process
from random import shuffle, randint
from moviepy.editor import*
import json
import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"

try:
    with open(f"{os.getcwd()}/l", encoding="utf-8") as f:
        Datas = json.load(f)
except:
	input("You need Settings.exe")

class MVideoEditor:
	def run(self, Dir, Name, Time):
		try:
			Filename = f"{os.getcwd()}/tmp/{Name}".replace("\\", "/")
			Var = VideoFileClip(Dir+"/"+Name)
			Var = Var.subclip(round(0+20-Time/1.25), round(Var.duration-Var.duration/2+Time/2.25))
			Result = concatenate_videoclips([Var])
			Result.write_videofile(Filename)
		except:
			try:
				print("", end="\n")
				print("Миша, всё хуйня, давай по новой!\n\n\n")
				Filename = f"{os.getcwd()}/tmp/{Name}".replace("\\", "/")
				Var = VideoFileClip(Dir+"/"+Name)
				Var = Var.subclip(round(0+20-Time/1.25), round(Var.duration-Var.duration/2+Time/2.25))
				Result = concatenate_videoclips([Var])
				Result.write_videofile(Filename)
			except:
				print("", end="\n")
				print("Миша, всё хуйня, давай по новой!\n\n\n")
				try:
					Filename = f"{os.getcwd()}/tmp/{Name}".replace("\\", "/")
					Var = VideoFileClip(Dir+"/"+Name)
					Var = Var.subclip(round(0+20-Time/1.25), round(Var.duration-Var.duration/2+Time/2.25))
					Result = concatenate_videoclips([Var])
					Result.write_videofile(Filename)
				except:
					print("", end="\n")
					print("Проблемный какой-то ролик попался, сам с ним ебись")

class WorkDivider:
	def __init__(self, Dir, time, Divides, VDiv) -> None:
		#Чиним слэши
		self.Dir = Dir.replace("\\", "/")
		###
		self.ListVideo = []
		self.ListNameOfVideo = []

		###Создание tmp
		try:os.mkdir(f"{os.getcwd()}\\tmp")
		except: pass

		#Фильтр только .mp4 файлов
		for FileName in os.listdir(Dir):
			if ".mp4" in FileName:
				self.ListNameOfVideo.append(FileName)
		
		#Перемешиваем воизбежании повторений
		shuffle(self.ListNameOfVideo)

		VideoProcess = []
		#Постановка на "Конвеер"
		for Name in self.ListNameOfVideo:
			cv = MVideoEditor
			p = Process(None, cv.run, args=(cv, Dir, Name, time))
			VideoProcess.append(p)

		Div = len(VideoProcess) // VDiv
		NewList = []
		for Step in range(Div+1):
			NewList.append(VideoProcess[int(Step * (len(VideoProcess) / (Div + 1))) : int((Step + 1) * (len(VideoProcess) / (Div + 1)))])

		for y in NewList:
			for x in y:
				x.start()
			[proc.join() for proc in y]
			print("Партия процессов выполнена")
		
		#os.system("cls")
		print("\n\n\n\nОбрезка окончена\n\n\n\n")
		ConcatenitePsyevdo(Divides)

class ConcatenitePsyevdo:
	def __init__(self, Divides = 0):
		ListVideo = []
		for FileName in os.listdir(f"{os.getcwd()}\\tmp"):
			if ".mp4" in FileName:
				ListVideo.append(f"{os.getcwd()}\\tmp\\{FileName}")
		VideoProcesss = []
		#Постановка на "Конвеер"
		Count = 0
		for filename in os.listdir():
			if ".mp4" in filename and "AI" in filename:Count+= 1
		VName = []
		for Step in range(Divides + 1):
			Count += 1
			Name = f"AI{Count}.mp4"
			cv = ConcateniteVideos
			p = Process(target=cv.run, args=(cv, ListVideo[int(Step * (len(ListVideo) / (Divides + 1))) : int((Step + 1) * (len(ListVideo) / (Divides + 1)))], Name))
			VName.append(Name)
			p.start()
			VideoProcesss.append(p)
		[proc.join() for proc in VideoProcesss]
		print("\n\n\n\nМонтаж окончен\n\n\n\n")
		[os.remove(f"{os.getcwd()}\\tmp\\{Name}") for Name in os.listdir(f"{os.getcwd()}\\tmp")]
		os.rmdir(f"{os.getcwd()}\\tmp")
		data = ["", 0, 20, []]
		try:
			with open("l", "r", encoding="utf-8") as f:
				data = json.load(f)
		except:pass
		data[3] = VName
		try:
			with open("l", "w", encoding="utf-8") as f:
				json.dump(data, f)
		except:pass
		try:
			os.system(f"start {os.getcwd()}/Preview.py")
		except:
			os.system(f"start {os.getcwd()}/Preview.exe")

class ConcateniteVideos:
	def run(self, ListWithVideoFileClip, ResName):
		ListVideo = [VideoFileClip("Intro.mp4")]

		shuffle(ListWithVideoFileClip)

		[ListVideo.append(VideoFileClip(v)) for v in ListWithVideoFileClip]
		
		ListVideo.append(VideoFileClip("Outro.mp4"))
		Result = concatenate_videoclips(ListVideo)
		while 1:
			if os.path.isfile(os.getcwd()+f"\\{ResName}"):
				ResName="_"+ResName
			else:
				break
		Result.write_videofile(ResName)

class MontageVideo:
	CanStart = False
	def __init__(self):
		print("Initialized")
		print("Программа для автомонтажа видео из WarThunder, если у вас нет функции nvidia highlight, то программа вам не поможет")
		print("p.s. в последней версии нейронка была вырезана, т.к. просто обрезала видео по таймингам, при этом увеличивая время монтажа, теперь вместо нейронки, работает алгоритм")
	def run(self, Datas):
		Dir = Datas[0]
		Divides = Datas[1]
		VDiv = Datas[2]
		self.time = 6
		self.Dir = "F:/vid/Short/War Thunder/" if ((Dir is None) or (Dir == "")) else Dir
		self.Divides = Divides
		self.VDiv = VDiv
		WorkDivider(self.Dir, self.time, self.Divides, self.VDiv)

if __name__ == "__main__":
	M = MontageVideo()
	p = Process(target=M.run, args=[Datas])
	p.start()
	p.join()