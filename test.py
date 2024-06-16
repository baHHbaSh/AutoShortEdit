import os
Count = 0
for filename in os.listdir():
	if ".mp4" in filename and "AI" in filename:Count+= 1