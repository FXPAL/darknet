import cv2
import os
import argparse
import re


def numericalSort(value):
	numbers = re.compile(r'(\d+)')
	parts = numbers.split(value)
	parts[1::2] = map(int, parts[1::2])
	return parts

if __name__ == '__main__':
	aparse = argparse.ArgumentParser(
		prog="create video from images",
		description="todo ..")
	aparse.add_argument('--img_file_path',
						action='store',
						dest='img_file_path',
						default='../data_trajectory_fxpal/results/img_w_plots/',
						type=str)
	aparse.add_argument('--video_path_save',
						action='store',
						dest='video_path_save',
						default='../data_trajectory_fxpal/results/',
						type=str)
	aparse.add_argument('--save_video_name',
						action='store',
						dest='save_video_name',
						default='trajectory_60fps.mp4',
						type=str)
	
	cmdargs = aparse.parse_args()
	img_file_path = cmdargs.img_file_path
	video_path_save = cmdargs.video_path_save
	save_video_name = cmdargs.save_video_name

	images = [img for img in sorted(os.listdir(img_file_path), key=numericalSort) if img.endswith(".png")]

	frame = cv2.imread(os.path.join(img_file_path, images[0]))
	height, width, layers = frame.shape

	video = cv2.VideoWriter(video_path_save + save_video_name,cv2.VideoWriter_fourcc(*'MJPG'), 60.0, (width, height))
	

	for idx, image in enumerate(images):
		# print(image)
		video.write(cv2.imread(os.path.join(img_file_path, image)))
		if idx % 500 == 0:
			print('processed {} images'.format(idx))

	cv2.destroyAllWindows()
	video.release()

