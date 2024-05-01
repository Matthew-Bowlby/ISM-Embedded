import numpy as np
import cv2 
import time
import base64
import os
from PIL import Image
class FaceRecognition():

    def __init__(self):
        self.where ='/home/ism/ISM-Embedded/nano/'
        self.detector = cv2.FaceDetectorYN.create(self.where+"models/face_detection_yunet_2023mar.onnx","",(1280,960),.9,.3,5000)
        self.recognizer = cv2.FaceRecognizerSF.create(self.where+"models/face_recognition_sface_2021dec.onnx","")
        self.cap = None
        self.features = []
        self.features_label=[]
        self.running=False
        self.load_face()
        self.user_creation = None
    def load_face(self):
        path=self.where+"img"
        imagepaths=[os.path.join(path,f) for f in os.listdir(path)]
        for imagepath in imagepaths:
            if ".DS_Store" in imagepath:
                continue
            else:
                faceImg= Image.open(imagepath).convert("RGB")
                self.detector.setInputSize((faceImg.size[0],faceImg.size[1]))
                faces1=self.detector.detect(faceImg)
                face1align= self.recognizer.alignCrop(faceImg, faces1[1][0])
                self.features.append(self.recognizer.feature(face1align))
                self.features_label.append(os.path.split(imagepath)[-1].split('.')[0])



    def startImageTaking(self,name):
        print("starting cam")
        self.cap=cv2.VideoCapture(0)
        self.running=True
        self.user_creation=name
    def stopCreating(self):
        self.cap.release()
        user = self.user_creation
        self.user_creation=None
        return user
    def creatingImages(self):
        print("req image")
        if self.user_creation == None:
            return None
        sampleNum=0
        user=self.user_creation
        ret, frame = self.cap.read()
        #gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        self.detector.setInputSize((int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        faces=self.detector.detect(frame)
        if faces[1] is not None:
            for idx, face in enumerate(faces[1]):
                sampleNum=sampleNum+1
                x= face[0]
                y=face[1]
                w=face[2]
                h=face[3]
                cv2.imwrite(self.where+f"img/{user}."+str(sampleNum)+".jpg",frame[y:y+h,x:x+w])
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                #cv2.waitKey(100)
                print(sampleNum)
                break
        # cv2.imshow("Face",img)
        # cv2.waitKey(1)
        if(sampleNum>50):
            return None
        # Convert the frame to base64
        retval, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        return "data:image/jpeg;base64," + jpg_as_text
    
    def stop_recognition(self):
        self.running=False
        # self.cap.release()

    def run_recognition(self):
        if self.running:
           return None
        start = time.time()
        self.cap = cv2.VideoCapture(0)
        self.running=True
        user = None
        while self.running and (time.time()-start) < 10:
            print("Looking...")
            has_frame,frame = self.cap.read()
            if not has_frame:
                self.cap.release()
                break
            faces = self.detector.detect(frame)
            if faces[1] is not None:
                for idx,face in enumerate(faces[1]):
                    face_align = self.recognizer.alignCrop(frame,face)
                    face_feature = self.recognizer.feature(face_align)
                    scores=[]
                    for feature in self.features:
                        cosine_score = self.recognizer.match(feature, face_feature, cv2.FaceRecognizerSF_FR_COSINE)
                        scores.append(cosine_score)
                    cosine_sim = .363

                    if max(scores) >= cosine_sim:
                        user = np.argmax(scores)
                        print(f"User recognizer {user}")
                        self.running=False
                        self.cap.release()
                        return self.features_label[user]
        self.running = False
        self.cap.release()
        return None
