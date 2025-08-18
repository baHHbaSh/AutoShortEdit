from multiprocessing import Process
from random import shuffle, randint
from moviepy import*
import json
import os
import traceback
from traceback import print_exc
os.environ["KIVY_NO_CONSOLELOG"] = "1"

try:
    with open(f"{os.getcwd()}/l", encoding="utf-8") as f:
        Datas = json.load(f)
except:
	print(traceback.print_exc())
	input("You need Settings.exe / .py")

class Colors:
    """
    Цвета для красивого вывода в консоль 🎨
    """
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def debug_print(message, type="info"):
    """
    Красивый вывод в консоль с цветами 🖨️
    
    Args:
        message (str): Сообщение для вывода
        type (str): Тип сообщения (инфа/успех/внимание/ошибка)
    """
    prefix = {
        "info": f"{Colors.BLUE}[ИНФА]{Colors.ENDC}",
        "success": f"{Colors.GREEN}[ГОТОВО]{Colors.ENDC}",
        "warning": f"{Colors.WARNING}[ВНИМАНИЕ]{Colors.ENDC}",
        "error": f"{Colors.FAIL}[ОШИБКА]{Colors.ENDC}"
    }
    print(f"{prefix.get(type, '[ДЕБАГ]')} {message}")

class MVideoEditor:
	"""
	Класс для обработки отдельных видеофайлов 🎥
	Обрезает и ресайзит каждый видос под нужный формат
	"""
	def run(self, Dir, Name, Time):
		"""
		Обработка одного видеофайла
		
		Args:
			Dir (str): Путь к папке с видосами
			Name (str): Имя видоса
			Time (float): Время для обрезки
		"""
		Filename = f"{os.getcwd()}/tmp/{Name}".replace("\\", "/")
		if Name in os.listdir(f"{os.getcwd()}/tmp"):
			debug_print(f"Файл {Filename} уже обработан, пропускаем", "warning")
		else:
			try:
				Var = VideoFileClip(Dir+"/"+Name)
				Var = Var.subclipped(round(0+20-Time/1.25), round(Var.duration-Var.duration/2+Time/2.25))
				Var = Var.resized(width=1920, height=1080)
				Var.write_videofile(Filename, fps=60)
			finally:
				# Закрываем видео и чистим память
				Var.close()
				del Var
				import gc
				gc.collect()

class WorkDivider:
	"""
	Распределяет работу между процессами для быстрой обработки 🚀
	Разбивает пачку видосов на части и параллелит обработку
	"""
	def __init__(self, Dir, time, Divides, VDiv) -> None:
		"""
		Args:
			Dir (str): Директория с видосами
			time (float): Время для обрезки
			Divides (int): Количество частей для разделения
			VDiv (int): Количество видео в одной части
		"""
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

		# Ограничиваем количество параллельных процессов
		MAX_PARALLEL = 4  # Или другое число в зависимости от твоего железа
		
		for y in NewList:
			# Запускаем не больше MAX_PARALLEL процессов одновременно
			for i in range(0, len(y), MAX_PARALLEL):
				batch = y[i:i+MAX_PARALLEL]
				for x in batch:
					x.start()
				[proc.join() for proc in batch]
				debug_print(f"Обработано {i+len(batch)} из {len(y)} видео в текущей пачке ✅", "success")
		
		debug_print("\n" + Colors.BOLD + "=== Обрезка завершена ===" + Colors.ENDC + "\n", "success")
		ConcatenitePsyevdo(Divides)

class ConcatenitePsyevdo:
	"""
	Склеивает обработанные видосы в финальный результат 🎬
	Распределяет склейку по процессам для ускорения
	"""
	def __init__(self, Divides = 0):
		"""
		Args:
			Divides (int): На сколько частей разбить склейку
		"""
		ListVideo = []
		for FileName in os.listdir(f"{os.getcwd()}\\tmp"):
			if ".mp4" in FileName:
				ListVideo.append(f"{os.getcwd()}\\tmp\\{FileName}")
		VideoProcesss = []
		#Постановка на "Конвеер"
		Indexes = []
		for filename in os.listdir(f"{os.getcwd()}"):
			if ".mp4" in filename and "AI" in filename:
				try:
					Indexes.append(int(filename.split(".")[0][2:]))
				except: print_exc()
		Count = max(Indexes)
		VName = []
		for Step in range(Divides + 1):
			Count += 1
			Name = f"AI{Count}.mp4"
			ConcateniteVideos().run(ListVideo[int(Step * (len(ListVideo) / (Divides + 1))) : int((Step + 1) * (len(ListVideo) / (Divides + 1)))], Name)
			VName.append(Name)
		debug_print("\n" + Colors.BOLD + "=== Монтаж завершён ===" + Colors.ENDC + "\n", "success")
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
	"""
	Непосредственно склеивает видосы в один файл 📼
	Перемешивает их для разнообразия
	"""
	def run(self, ListWithVideoFileClip, ResName):
		"""
		Args:
			ListWithVideoFileClip (list): Список путей к видео для склейки
			ResName (str): Имя выходного файла
		"""
		ListVideo = []
		shuffle(ListWithVideoFileClip)
		
		try:
			# Загружаем видео по одному
			for v in ListWithVideoFileClip:
				clip = VideoFileClip(v)
				ListVideo.append(clip)
			
			Result = concatenate_videoclips(ListVideo)
			while 1:
				if os.path.isfile(os.getcwd()+f"\\{ResName}"):
					ResName="_"+ResName
				else:
					break
			Result.write_videofile(ResName)
		
		finally:
			# Закрываем все видео и чистим память
			for clip in ListVideo:
				clip.close()
			if 'Result' in locals():
				Result.close()
			del ListVideo
			if 'Result' in locals():
				del Result
			import gc
			gc.collect()

class MontageVideo:
	"""
	Главный класс для запуска всего процесса монтажа 🎮
	Читает настройки и запускает обработку
	"""
	CanStart = False
	def __init__(self):
		debug_print(Colors.HEADER + "=== Программа для монтажа War Thunder ===" + Colors.ENDC, "info")
		debug_print("Эта программа поможет собрать нарезку из реплеев War Thunder", "info")
		debug_print("Примечание: Нейросеть была удалена в последней версии, так как она только обрезала видео по таймингу", "warning")
		debug_print("Теперь используется более эффективный алгоритм", "info")
	def run(self, Datas):
		"""
		Запускает процесс монтажа

		Args:
			Datas (list): Список с настройками [директория, количество разделений, количество видео в части]
		"""
		debug_print("Начинаем процесс монтажа... 🎬", "info")
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