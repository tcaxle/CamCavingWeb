import sys
import os
import subprocess

# print(sys.argv)

# def thumbify():
# 	for root, subFolders, files in os.walk(os.path.realpath(sys.argv[1]))
# 		for file in files:
# 			if file.lower().endswith(('.png', '.jpg', '.jpeg')) and "_thumb." not in file:
# 				filename = os.path.join(root, file)
# 				# print(filename)
# 				basename = ".".join(filename.split(".")[0:-1])
# 				print(basename)
# 				extenstion = filename.split(".")[-1]
# 				# print(extenstion)
# 				# print('convert -sample 200x150 "{}" "{}_thumb.{}"'.format(filename, basename, extenstion))
# 				os.system('convert -sample 300x225 "{}" "{}_thumb.{}"'.format(filename, basename, extenstion))

def thumbify(file_in):
	file_in = os.path.realpath(file_in)
	basename = ".".join(file_in.split(".")[0:-1])
	# print(basename)
	extenstion = file_in.split(".")[-1]
	# print(extenstion)
	# print('convert -sample 200x150 "{}" "{}_thumb.{}"'.format(filename, basename, extenstion))
	os.system('convert -sample 300x225 "{}" "{}_thumb.{}"'.format(file_in, basename, extenstion))
