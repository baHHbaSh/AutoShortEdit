import ffmpeg
import os

def get_video_resolution(filepath):
	try:
		probe = ffmpeg.probe(filepath)
		video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
		if not video_streams:
			raise ValueError('No video stream found')

		video_stream = video_streams[0]
		width = video_stream['width']
		height = video_stream['height']
		return width, height
	except ffmpeg.Error as e:
		print(f"An error occurred: {e}")
		return None

# Пример использования
for i in os.listdir("F:\\vid\\Short\\War Thunder"):
	if ".mp4" in i:
		print(f"F:\\vid\\Short\\War Thunder\\{i}")
		resolution = get_video_resolution(f"F:\\vid\\Short\\War Thunder\\{i}")
		if resolution:
			print(f'Resolution: {resolution[0]}x{resolution[1]}')
		else:
			print("Could not determine resolution.")