import cv2
import numpy as np
import smtplib
from playsound import playsound
CONFIDENCE_THRESHOLD = 0.4
NMS_THRESHOLD = 0.5
flag = 0
c=0
cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
while cap.isOpened(): 
    ret, frame = cap.read()
    frame = np.array(frame)
    class_names = []
    with open("coco.names", "r") as f:
        class_names = [cname.strip() for cname in f.readlines()]
    colors = np.random.uniform(0,255,size=(len(class_names),3))
    net = cv2.dnn.readNet("custom-yolov4-tiny-detector_best.weights", "custom-yolov4-tiny-detector.cfg")
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(640, 640), scale=1/255, swapRB=True)
    classes, scores, boxes = model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    for (classid, score, box) in zip(classes, scores, boxes):
        color=colors[classid[0]]
        name = class_names[classid[0]]
        label = "%s : %f" % (class_names[classid[0]], score)
        cv2.rectangle(frame, box,color, 2)
        cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255), 2)
        print(type(label))
        if(name=="Fire"):
        	playsound('audio.mp3')
        	c+=1
    cv2.imshow('frame',frame)
    if(c>0 and flag==0):
    	sender_email = 'infiltrationalert@gmail.com'
    	rec_email= 'rohit@codebugged.com'
    	password='infiltration@1'
    	message = 'Subject: {}\n\n{}'.format("Fire Alert!", 'Dear User, There is a fire detected in your Enterprise.')
    	server=smtplib.SMTP('smtp.gmail.com',587)
    	server.starttls()
    	server.login(sender_email, password)
    	print('login sucess')
    	server.sendmail(sender_email,rec_email,message)
    	print('Email has been sent to',rec_email)
    	flag = 1
    	print(message)
    if cv2.waitKey(10) & 0xFF == ord('q'):
    	cap.release()
    	cv2.destroyAllWindows()
    	break 