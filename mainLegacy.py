print("Внимание, продукт сырой, сейчас пытаюсь сделать под него интерфейс. Главное то, что всё работает!")
import traceback
from threading import Thread
from random import shuffle
def CacheDelite():
	try:
		for Path in os.listdir(os.getcwd()+"/tmp"):
			os.remove(os.getcwd()+"/tmp" + "/" + Path)
	except FileNotFoundError:
		print(traceback.format_exc())
		try:
			os.mkdir(os.getcwd()+"/tmp")
		except: pass
CompilesFilesTolal = 0
def CompileFile(Dir, Time, Name, TargetDir):
	global CompilesFilesTolal
	Vi = VideoFileClip(Dir+"/"+Name)
	print(Time)
	Vi = Vi.subclip( round(0+20-Time/2), round(Vi.duration-Vi.duration/2+Time/2) )
	CompositeVideoClip([Vi]).write_videofile(TargetDir + "/" + Name)
	Vi.close()
	CompilesFilesTolal += 1
	os.system("cls")
	print(CompilesFilesTolal)
try:
	from moviepy.editor import*
	import os
	while 1:
		#Для людей
		Dir = input("Путь к видео ")
		Time = "a"
		while 1:
			try:
				Time = int(input("Итоговая длина сегмента от 0 до 40 сек (Рекомендую 4) "))
				if 0 > Time > 40:
					continue
			except:
				continue
			finally:
				break
		
		if Dir == "":
			Dir = "F:/vid/Short/War Thunder/"
		
		Dir = Dir.replace("\\", "/")
		
		ListVideo = [VideoFileClip("Intro.mp4")]
		ListNameOfVideo = []

		#Фильтр только .mp4 файлов
		for FileName in os.listdir(Dir):
			if ".mp4" in FileName:
				ListNameOfVideo.append(FileName)
		

				
		shuffle(ListNameOfVideo)
		#Монтаж видео
		for Name in ListNameOfVideo:
			Var = VideoFileClip(Dir+"/"+Name)
			Var = Var.subclip(round(0+20-Time/1.25), round(Var.duration-Var.duration/2+Time/2.25))
			ListVideo.append(Var)
			print(ListNameOfVideo.index(Name), "\n", Name)
		
		ListVideo.append(VideoFileClip("Outro.mp4"))

		Result = concatenate_videoclips(ListVideo)
		ResName = "AIautoEDIT.mp4"
		while 1:
			if os.path.isfile(os.getcwd()+f"/{ResName}"):
				ResName="_"+ResName
			else:
				break
		Result.write_videofile(ResName)
		break
except: print(traceback.format_exc()); input()
input("Выход")