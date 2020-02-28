# Yolo Demo

The yolov3.weights file was split using the command:  

split -b 60M -d -a 3 yolov3.weights yolov3.weights.  

The yolov3.weights file can be reassembed using the command:  

cat yolov3.weights.* > yolov3.weights  

