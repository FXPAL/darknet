import os
import argparse
from os import walk
import shutil
import math



def parse_text_file(text_file):
	'''Get label file names'''
	file_names = []
	
	with open(text_file) as f:
		for line in f:
			# print(line)
			line = line.replace('.png','.txt')
			line = line.rstrip('\n')
			print(line)
			file_names.append(line)
	return file_names

def check_bounded_boxes(label_file_names, file_path):
	
	a= 0.0
	error_cnt = 0
	total_cnt = 0
	for file_name in label_file_names:
		temp = file_name.split('/')
		label_file = file_path + 'img/' + temp[-1]
		with open(label_file) as f:
			for line in f:
				total_cnt +=1
				# print(line)
				line = line.rstrip('\n')
				temp = line.split(' ')
				# print(temp)
				once_flag = 0
				for idx, val in enumerate(temp):
					if idx == 0:
						continue
					val = float(val)
					# print(val)

					if math.isclose(val, 0.0, abs_tol=0.09):
						if once_flag == 0:
							error_cnt +=1	
							once_flag = 1
						
						print('#############zero value detected')
						print(label_file)
						print(val)
					# elif val < -0.00:
					# 	print('#############negative value detected')
					# 	print(label_file)
					# 	print(val)
					# else:
					# 	print('{} FILE OK'.format(label_file))
	print('total cnt: {}, error count: {}'.format(total_cnt,error_cnt))

def extract_specific_labels(label_file_names, file_path, save_file_path, extract_label):
	
	a= 0.0
	label_cnt = 0
	total_cnt = 0
	file_cnt = 0
	for file_name in label_file_names:
		file_cnt +=1
		temp = file_name.split('/')
		label_file = file_path + 'img/' + temp[-1]
		label_save_path = save_file_path + 'img/' + temp[-1]
		file_write = open(label_save_path,'w') 
		with open(label_file) as f:
			for line in f:
				total_cnt +=1
				lines = line.rstrip('\n')
				temp = lines.split(' ')
				if int(temp[0]) is extract_label:
					label_cnt +=1
					print('label: {}  found in file : {}'.format(extract_label, label_file))
					for idx,t in enumerate(temp):
						if idx == 0:
							file_write.write(str(0) + ' ')
						elif idx == len(temp)-1:
							file_write.write(t + '\n')
						else:
							file_write.write(t + ' ')
	print('file cnt: {} total label cnt: {}, label count for {}: {}'.format(file_cnt,total_cnt, extract_label, label_cnt))
	file_write.close()
	# exit(0)


def check_label_distribution(label_file_names, file_path):

	label_distribution = {}
	for file_name in label_file_names:
		temp = file_name.split('/')
		label_file = file_path + 'img/' + temp[-1]
		with open(label_file) as f:
			for line in f:
				# print(line)
				line = line.rstrip('\n')
				temp = line.split(' ')
				# print(temp)
				once_flag = 0
				if temp[0] in label_distribution:
					label_distribution[temp[0]] += 1
				else:
					label_distribution[temp[0]] = 1
	print('label label_distribution: {}'.format(label_distribution))

if __name__ == '__main__':
	aparse = argparse.ArgumentParser(
		prog="check bounded boxes",
		description="todo ..")
	aparse.add_argument('--file_path',
						action='store',
						dest='file_path',
						default='../data/',
						type=str)
	aparse.add_argument('--file_path_save',
						action='store',
						dest='file_path_save',
						default='../data_light/',
						type=str)
	aparse.add_argument('--file_name',
						action='store',
						dest='file_name',
						default='train.txt',
						type=str)
	aparse.add_argument('--check_label_distribution_flag',
						action='store',
						dest='check_label_distribution_flag',
						default=False,
						type=bool)
	aparse.add_argument('--extract_label_flag',
						action='store',
						dest='extract_label_flag',
						default=False,
						type=bool)
	aparse.add_argument('--check_bounded_boxes_flag',
						action='store',
						dest='check_bounded_boxes_flag',
						default=False,
						type=bool)
	aparse.add_argument('--extract_label',
						action='store',
						dest='extract_label',
						default=2,
						type=int)

	cmdargs = aparse.parse_args()
	file_path = cmdargs.file_path
	file_name = cmdargs.file_name
	read_file_name = file_path + file_name
	label_file_names = parse_text_file(read_file_name)
	save_file_path = cmdargs.file_path_save
	check_bounded_boxes_flag = cmdargs.check_bounded_boxes_flag
	check_label_distribution_flag = cmdargs.check_label_distribution_flag
	extract_label_flag = cmdargs.extract_label_flag
	extract_label = cmdargs.extract_label
	if check_bounded_boxes_flag:
		check_bounded_boxes(label_file_names, file_path)
	if check_label_distribution_flag:
		check_label_distribution(label_file_names, file_path)
	if extract_label_flag:
		extract_specific_labels(label_file_names, file_path, save_file_path, extract_label)
	else:
		print('pick atleast one operation')


