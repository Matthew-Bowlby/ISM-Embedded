import numpy as np
import cv2 



class FaceRecognition():

    def __init__(self):
        self.detector = cv2.FaceDetectorYN.create("models/face_detection_yunet_2023mar.onnx","",(320,320),.9,.3,5000)
        self.recognizer = cv2.FaceRecognizerSF.create("models/face_recognition_sface_2021dec.onnx","")
        self.cap = None
        self.features = []
        self.running=False
        self.load_face()
        
    def load_face(self):
        img1 = cv2.imread("img/1.jpg")
        im1w = int(img1.shape[1])
        im1h = int(img1.shape[0])
        self.detector.setInputSize((im1w,960))

        img1 = cv2.resize(img1,(im1w,960))


        faces1=self.detector.detect(img1)
        face1align= self.recognizer.alignCrop(img1, faces1[1][0])

        self.features.append(self.recognizer.feature(face1align))
    
    def stop_recognition(self):
        self.running=False
        # self.cap.release()

    def run_recognition(self):
        if self.running:
            return None
        self.cap = cv2.VideoCapture(0)
        self.running=True
        user = None
        while self.running:
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
                        self.cap.release()
                        return user
        return None
