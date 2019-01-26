import os,sys
import time
# sys.path.append('/home/peter/darknet/python')
# sys.path.append('/home/peter/darknet')

# import darknet as dn
import pdb
import shutil
import numpy as np
import cv2
import argparse
from os import walk
import math
import re
import pickle
import matplotlib.pyplot as plt

# net = dn.load_net(b'/home/peter/darknet/cfg/pdq.cfg',b'/home/peter/darknet/pdq_3100.weights',0)
# meta = dn.load_meta(b'/home/peter/darknet/data/pdq_obj.data')

# folder = '/home/peter/Pictures'

def ensure_dir(result_file_path, file_name):
	directory_name = file_name.split('.')
	directory_name = result_file_path + directory_name[0]
	if not os.path.isdir(directory_name):
		os.makedirs(directory_name)

def parse_text_file(text_file, label_name, database):
	'''Get label file names'''
	with open(text_file) as f:
		for line in f:
			# print(line)
			line = line.rstrip('\n')
			temp = line.split(':')
			temp[0] = temp[0].replace('data_' + label_name,'data')
			# print('lenght of line: {} and line: {}'.format(len(temp),temp) )
			if len(temp) == 2: # have the line that has the key which is the image path
				mainkey = temp[0]
				if temp[0] in database.keys():
					inner_label_dict = database[temp[0]]
					inner_label_dict[label_name] = []
					database[temp[0]] = inner_label_dict
				else:
					inner_label_dict = {}
					inner_label_dict[label_name] = []
					database[temp[0]] = inner_label_dict
				# print('database is: {}'.format(database) )
			elif len(temp) == 10:
				# print('database in len 10: {}'.format(database) )
				# ['door', ' 91%', ' left_x', '  337', ' top_y', '  304', ' width', '  111', ' height', '  242 ']
				acc = int(temp[1].rstrip('%'))
				UL_x = int(temp[3])
				UL_y = int(temp[5])
				width = int(temp[7])
				height = int(temp[9])

				list_val = [UL_x, UL_y, width, height, acc]
				update_list = database[mainkey][label_name]
				update_list.append(list_val)
				database[mainkey][label_name] = update_list
	# print(database)
	return database

def pickle_save_database(result_file_path, database_save_name, database):
	pickle_file = result_file_path + database_save_name +'.pickle'
	try:
		with open(pickle_file, 'wb') as handle:
			pickle.dump(database, handle, protocol=pickle.HIGHEST_PROTOCOL)
	except Exception as e:
		print('Unable to save data to', database_save_name, ':', e)
		raise
	statinfo = os.stat(pickle_file)
	print('Compressed pickle size:', statinfo.st_size)

def pickle_load_database(result_file_path, database_save_name):
	pickle_file = result_file_path + database_save_name + '.pickle'
	with open(pickle_file, 'rb') as handle:
		database = pickle.load(handle)
	return database

def get_statistics(database):
	total_img = len(database)
	stat_label = {'door': 0, 'sign': 0, 'frames': 0, 'light': 0}
	stat_num = { '0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0, '15': 0}#, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0}
	for k, v in database.items():
		t_cnt = 0
		for k_i, val_i in v.items():
			if val_i is None:
				stat_num['0'] +=1
			else:
				t_cnt +=len(val_i)
		if str(t_cnt) in stat_num.keys():
			stat_num[str(t_cnt)] +=1
			if t_cnt > 6:
				print(k)
	print('statistics from total images: {}, {}'.format(total_img, stat_num))
	
	return stat_num

def generate_histogram(result_file_path, result_folder, stat_num):
	result_folder_path = result_file_path
	fig = plt.figure()
	width = 1     # gives histogram aspect to the bar diagram
	pos = np.arange(len(stat_num.keys()))
	ax = plt.axes()
	plt.bar(stat_num.keys(), stat_num.values(), width=width, color='g', edgecolor='black')
	plt.ylabel('frequency')
	plt.xlabel('Number of Labels in a single Image')
	fig.savefig(result_folder_path + 'hist.png')

	
	

def draw_boxes_on_image(result_file_path, result_folder, database):
	box_color_defn = {'door': (0, 0, 255), 'sign': (0, 255, 0), 'light': (255, 153, 255), 'frames': (255, 128, 0)} # door = red, sign = green, light = pink, frames = orange
	result_folder_path = result_file_path + result_folder + '/'
	for k,v in database.items():
		path = '../' + k
		image_save_name = k.split('/')
		result_image_name = result_folder_path + image_save_name[-1]
		# print('result image name: {}'.format(result_image_name))
		# print('key is: {}'.format(k))
		# print('label is: {}'.format(v))
		img = cv2.imread(path, cv2.IMREAD_COLOR) #load image in cv2
		# print('image shape: {}'.format(img.shape))
		for k_i, val_i in v.items():
			box_color = box_color_defn[k_i]
			if val_i is None:
				continue
			else:
				# print('path is: {}'.format(path) )
				for coord in val_i:
					# print('coord values: {}'.format(coord))
					UL_x = coord[0]
					UL_y = coord[1]
					width = coord[2]
					height = coord[3]
					LR_x = UL_x + width
					LR_y = UL_y + height
					cv2.rectangle(img,(UL_x,UL_y),(LR_x,LR_y),box_color,5)
					#put label on bounding box
					font = cv2.FONT_HERSHEY_SIMPLEX
					cv2.putText(img,k_i,(UL_x,UL_y),font,1,box_color,2,cv2.LINE_AA)
		cv2.imwrite(result_image_name,img) #wait until all the objects are marked and then write out.




if __name__ == '__main__':
	aparse = argparse.ArgumentParser(
		prog="draw boxes on images",
		description="todo ..")
	aparse.add_argument('--data_file_path',
						action='store',
						dest='data_file_path',
						default='../data_trajectory_fxpal/',
						type=str)
	aparse.add_argument('--result_file_path',
						action='store',
						dest='result_file_path',
						default='../data_trajectory_fxpal/results/',
						type=str)
	aparse.add_argument('--save_labeled_image_folder',
						action='store',
						dest='save_labeled_image_folder',
						default='img_w_plots',
						type=str)
	aparse.add_argument('--label_file_names',
						action='store',
						dest='label_file_names',
						default=['result_door.txt','result_sign.txt', 'result_frames.txt', 'result_light.txt'],
						type=list)
	aparse.add_argument('--combined_labeled_database_save_name',
						action='store',
						dest='combined_labeled_database_save_name',
						default='combinedresults',
						type=str)
	aparse.add_argument('--draw_boxes_flag',
						action='store',
						dest='draw_boxes_flag',
						default=False,
						type=bool)
	aparse.add_argument('--save_database_flag',
						action='store',
						dest='save_database_flag',
						default=True,
						type=bool)
	aparse.add_argument('--load_database_flag',
						action='store',
						dest='load_database_flag',
						default=True,
						type=bool)
	
	cmdargs = aparse.parse_args()
	data_file_path = cmdargs.data_file_path
	result_file_path = cmdargs.result_file_path
	save_labeled_image_folder = cmdargs.save_labeled_image_folder
	label_file_names = cmdargs.label_file_names
	combined_labeled_database_save_name = cmdargs.combined_labeled_database_save_name
	# result_folder = cmdargs.result_folder

	# file_name = cmdargs.file_name
	
	draw_boxes_flag = cmdargs.draw_boxes_flag
	save_database_flag = cmdargs.save_database_flag
	load_database_flag = cmdargs.load_database_flag
	
	database= {}
	for file in label_file_names:
		temp = re.split("[._]+",file)
		ensure_dir(result_file_path, save_labeled_image_folder)
		database = parse_text_file(result_file_path + file, temp[1], database)
	if save_database_flag:
		pickle_save_database(result_file_path, combined_labeled_database_save_name, database)
	if load_database_flag:
		database = pickle_load_database(result_file_path, combined_labeled_database_save_name)
	if draw_boxes_flag:
		draw_boxes_on_image(result_file_path, save_labeled_image_folder, database)
	stat_num = get_statistics(database)
	generate_histogram(result_file_path, save_labeled_image_folder, stat_num)

 