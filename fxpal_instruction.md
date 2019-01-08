## clone
Git clone https://github.com/FXPAL/darknet

## Environment installation 
Create conda env and install all the requirements in the darknet_requirement.txt file located in darknet main folder using the below command

Conda install --file=darknet_requirement.txt

## hack for telling nvcc to use gcc-5 (requirment for NVCC)
Go to /usr/local/cuda/bin folder and create a soft link pointing to gcc and g++ 5
ln -s /usr/bin/gcc-5 gcc
ln -s /usr/bin/g++-5 g++

## compiling
Go to darknet folder and use make command

----------It should compile without complains with GPU support----------

## Training and testing

./darknet detector train data_mitesh/obj.data cfg/yolov3-obj.cfg build/darknet/x64/darknet53.conv.74 -dont_show

./darknet detector test cfg/openimages.data cfg/yolov3-openimages.cfg weights/yolov3-openimages.weights -dont_show -ext_output < build/darknet/x64/data/train.txt >  result.txt


##NOTE:
For training and testing darknet has specific data format requirement. Refer to 
https://github.com/FXPAL/darknet/blob/master/README.md
