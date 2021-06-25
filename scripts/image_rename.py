from PIL import Image
import sys
import os
import random 
import string
import re

print(sys.argv)

def get_date_taken(path):
	exif = Image.open(path)._getexif()

	if exif is not None:
		return Image.open(path)._getexif()[36867]
	else:
		return None

for root, subFolders, files in os.walk(sys.argv[1]):
	# print("root", root)
	# print("subfolder", subFolders)
	# print("files", files)
	# print("++++++")

	

	for file in files:
		if file.lower().endswith(('.png', '.jpg', '.jpeg')): #('.png', '.jpg', '.jpeg', '.mov', '.mp4', '.avi', '.mkv')
			
			file_path = os.path.join(root, file)
			print(root)
			timestamp = get_date_taken(file_path)
			if timestamp is not None:
				extension = file_path.split(".")[-1]

				# print(timestamp)
				year = timestamp[0:4]
				month = timestamp[5:7]
				day = timestamp[8:10]
				hour = timestamp[11:13]
				minutes = timestamp[14:16]
				seconds = timestamp[17:19]
				# print(year)
				# print(month)
				# print(day)
				# print(hour)
				# print(minutes)
				# print(seconds)
				r = random.randint(1111, 9999) 
				# print(r)
				name = str(year)+str(month)+str(day) + "_" + str(hour)+str(minutes)+str(seconds) + "_" + str(r) + "." + extension.lower()
				print(name)
				pattern = str(year)+str(month)+str(day) + "_" + str(hour)+str(minutes)+str(seconds) + "_" + r"[0-9][0-9][0-9][0-9]"
				if re.search(pattern, file): # means that is has already been processed
					print("Pattern matched")
					print(pattern, "in", file)
				else:
					print("pattern not macthed")
					print(pattern, "not in", file)
					os.rename(file_path, os.path.join(root, name))