import cv2 as cv
import numpy as np

my_webcam = cv.VideoCapture(0)
known_user = cv.imread('it_is_i.jpg')
gray_user = cv.cvtColor(known_user, cv.COLOR_BGR2GRAY)
gray_user = cv.equalizeHist(gray_user)

face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')


recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read('face_recognition_model.yml')

while True:
    ret,frame = my_webcam.read()
    if not ret:
        break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame)

    for(x,y,w,h) in faces:
        
        face_roi = gray_frame[y:y+h,x:x+w]
        label, confidence = recognizer.predict(face_roi)
        if label == 1:  # Assuming label 1 corresponds to the known face
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv.putText(frame, 'Authenticated', (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv.putText(frame, 'Unrecognized', (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        
    cv.imshow('Face Recognition', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
         break

my_webcam.release()
cv.destroyAllWindows()