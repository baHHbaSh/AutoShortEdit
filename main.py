from multiprocessing import Process
import traceback
from random import shuffle, randint
from moviepy.editor import*
import os


class MVideoEditor:
	def run(self, Dir, Name, Time):
		Filename = f"{os.getcwd()}/tmp/{Name}".replace("\\", "/")
		Var = VideoFileClip(Dir+"/"+Name)
		Var = Var.subclip(round(0+20-Time/1.25), round(Var.duration-Var.duration/2+Time/2.25))
		Result = concatenate_videoclips([Var])
		Result.write_videofile(Filename)

class WorkDivider:
	def __init__(self, Dir, time, Divides) -> None:
		#Чиним слэши
		self.Dir = Dir.replace("\\", "/")
		###
		self.ListVideo = []
		self.ListNameOfVideo = []

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
			p.start()
			VideoProcess.append(p)
		
		[proc.join() for proc in VideoProcess]
		os.system("cls")
		print("\n\n\n\nОбрезка окончена\n\n\n\n")
		ConcatenitePsyevdo(Dir, Divides)

class ConcatenitePsyevdo:
	def __init__(self, Dir=None, Divides = 0):
		ListVideo = []
		try:os.mkdir(f"{Dir}\\tmp")
		except:pass
		for FileName in os.listdir(f"{os.getcwd()}\\tmp"):
			if ".mp4" in FileName:
				ListVideo.append(f"{os.getcwd()}\\tmp\\{FileName}")
		
		if Divides > 0:#3 это 4 видосия по 10 моментов (если всего 40)
			VideoProcesss = []
			#Постановка на "Конвеер"
			for Step in range(Divides + 1):
				cv = ConcateniteVideos
				p = Process(target=cv.run, args=(cv, ListVideo[int(Step * (len(ListVideo) / (Divides + 1))) : int((Step + 1) * (len(ListVideo) / (Divides + 1)))]))
				p.start()
				VideoProcesss.append(p)
			
			[proc.join() for proc in VideoProcesss]
			print("\n\n\n\nМонтаж окончен\n\n\n\n")
		else:
			ConcateniteVideos(ListVideo)

class ConcateniteVideos:
	def run(self, ListWithVideoFileClip):
		ListVideo = [VideoFileClip("Intro.mp4")]

		[ListVideo.append(VideoFileClip(v)) for v in ListWithVideoFileClip]
		
		ListVideo.append(VideoFileClip("Outro.mp4"))
		Result = concatenate_videoclips(ListVideo)
		ResName = f"AI{randint(0,99999999999999999999999999999999999)}.mp4"
		while 1:
			if os.path.isfile(os.getcwd()+f"\\{ResName}"):
				ResName="_"+ResName
			else:
				break
		Result.write_videofile(ResName)

class MontageVideo:
	def __init__(self, Dir=None, Divides=0):
		self.time = 6
		self.Dir = "F:/vid/Short/War Thunder/" if Dir is None else Dir
		self.Divides = Divides
	def run(self):
		WorkDivider(self.Dir, self.time, self.Divides)
	
if __name__ == "__main__":
	print("Открываю окно")
	Montage = MontageVideo(input("Путь до видосиев"), int(input("Кол-во подразделений"))).run()