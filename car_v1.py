import numpy as np
import cv2
import serial

# 모터 제어를 위한 아두이노와의 통신을 위해 사용
ser = serial.Serial('COM10', 9600)
   # 1 : Forward
   # 2 : Left
   # 3 : Right
   # 4 : Backward


# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
# https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#
# [haarcascade_fullbody.xml]에 사람의 몸을 검출하기 위한 머신러닝 모델이 저장되어 있으며, 이에 따른 검출을 진행한다.
humanObject_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')

cap = cv2.VideoCapture(1)
counter = 0
prevHeight = 320

while True:    
    ret, img = cap.read()
    width, height, channels = img.shape
    # width: 화면의 넓이
    # height: 화면의 높이
    # channels: RGB 채널
    
    # 컬러 영상을 흑백 영상으로 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    body = humanObject_cascade.detectMultiScale(gray)

    # 검출되는 body의 수가 다수개 있을 수 있다.
    for (x,y,w,h) in body:  # 검출된 body에 대해서 - 하나의 body 검출을 가정
        if h > prevHeight:
            prevHeight = h
            
        # 검출된 body를 Boxing
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        
        if x+w > ((width/4)*3): # Object의 오른쪽 위치가 화면 영상의 3/4 보다 크면: 오른쪽으로 치우쳐 있으면
            ser.write(str(3));  # RIGHT -> 오른쪽으로 움직여라!
        elif x < width/4:       # Object의 왼쪽 위치가 화면 영상의 1/4보다 작으면: 왼쪽으로 치우쳐 있으면
            ser.write(str(2));  # LEFT  -> 왼쪽으로 움직여라!

        if h < prevHeight:  # Object의 높이가 작으면
            ser.write(str(1));  # FORWARD : 앞으로 가라!
            prevHeight = h
        if h < 250:         # Object의 높이가 250보다 작으면
            ser.write(str(1));  # FORWARD : 앞으로 가라!
        
        # 추가해야할 사항: Object의 높이가 너무 크다면 뒤로 가라!
        # if h > 지정된 최대 크기:
        #     ser.write(str(4));  # BACKWARD : 로 가라!
        
        # Boxing된 object
        추출하기
        # roi_gray = gray[y:y+h, x:x+w]
        # roi_color = img[y:y+h, x:x+w]

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
