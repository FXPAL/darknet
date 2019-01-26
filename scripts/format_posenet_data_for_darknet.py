import os
import argparse
from os import walk
import shutil
import math



def parse_text_file(read_file_name, write_file_name):
	'''Get label file names'''
	file_lines = []
	file_write = open(write_file_name,'w') 
	with open(read_file_name) as f:
		for line in f:
			# print(line)
			# line = line.replace('.png','.txt')

			line = line.rstrip('\n')
			line = line.split(' ')
			print(line)
			file_write.write(line[0] + '\n')
			file_lines.append(line[0])
	file_write.close()
	# return file_names

if __name__ == '__main__':
	aparse = argparse.ArgumentParser(
		prog="format posenet data for darknet",
		description="todo ..")
	aparse.add_argument('--file_path',
						action='store',
						dest='file_path',
						default='../data_trajectory_fxpal/',
						type=str)
	aparse.add_argument('--file_path_save',
						action='store',
						dest='file_path_save',
						default='../data_trajectory_fxpal/',
						type=str)
	aparse.add_argument('--file_name',
						action='store',
						dest='file_name',
						default='13_rotated.txt',
						type=str)
	aparse.add_argument('--file_name_save',
						action='store',
						dest='file_name_save',
						default='train.txt',
						type=str)
	
	cmdargs = aparse.parse_args()
	file_path = cmdargs.file_path
	file_name = cmdargs.file_name
	file_path_save = cmdargs.file_path_save
	file_name_save = cmdargs.file_name_save


	read_file_name = file_path + file_name
	write_file_name = file_path_save + file_name_save
	label_file_names = parse_text_file(read_file_name, write_file_name)
	
