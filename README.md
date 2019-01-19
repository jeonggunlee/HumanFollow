# Object-Following-Car-Image-Prcessing
An object following 4WD robot.

* **Software**:
   - Python 
   - OpenCV
   - Arduino IDE
   
* **Hardware**:
   - Raspberry pi 2
   - Arduino Uno
   - 4WD robot chasis

* File Structure:
   - README.md : 지금 보고 있는 화일이다. 프로젝트에 대한 설명이 기술되어 있다.
   - Test Car.py: 자동차에 제어 신호 전달하는 부분에 대한 간단한 Test
   - arduino_code.ino: 라즈베리파이 보드로 부터 받은 제어 신호에 따라 모터를 제어하여 물체를 따라갈 수 있게 한다.
   - car_v1.py: 메인 코드
   - haarcascade_fullbody.xml: 물체 인식에 사용되는 머신러닝 모델 화일

*  *  *
 다음은 사람의 몸을 검출하고 검출된 위치에 따라 모터 제어를 통해 검출된 Object를 따라다니는 Python 코드이다. 사람의 몸 검출을 위해 OpenCV library를 사용하였다.
 
```python
import numpy as np
import cv2
import serial

# 모터 제어를 위한 아두이노와의 통신을 위해 사용
ser = serial.Serial('COM10', 9600)

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
        
        if x+w > ((width/4)*3):
            ser.write(str(3));
        elif x < width/4:
            ser.write(str(2));

        if h < prevHeight:
            ser.write(str(1));
            prevHeight = h
        if h < 250:
            ser.write(str(1));
            
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
```

