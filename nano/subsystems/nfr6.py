import numpy as np
import cv2
import time
import base64
import os
from PIL import Image


class FaceRecognition:
#initialize the detector with the input image of the camera and the model of detecting faces in frame
    def __init__(self):
        self.where = "/home/ism/ISM-Embedded/nano/"
        self.detector = cv2.FaceDetectorYN.create(
            self.where + "models/face_detection_yunet_2023mar.onnx",
            "",
            (1280, 960),
            0.9,
            0.3,
            5000,
        )
        #initialize the face encoder with a prebuilt model
        self.recognizer = cv2.FaceRecognizerSF.create(
            self.where + "models/face_recognition_sface_2021dec.onnx", ""
        )
        self.cap = None #reference to camera
        self.sampleNum = 0 #num photos
        self.features = [] #facial encoding features
        self.features_label = [] # holds labels based of user name
        self.running = False
        self.load_face()
        self.user_creation = None

    def load_face(self):
        path = self.where + "img" #file path to photo
        self.features = []
        self.features_label = []
        #searching through the array of reference photos and gathering the encoding from those
        imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
        for imagepath in imagepaths:
            if ".DS_Store" in imagepath:
                continue
            else:
                # faceImg= Image.open(imagepath).convert("RGB")
                faceImg = cv2.imread(imagepath)
                self.detector.setInputSize((faceImg.shape[1], faceImg.shape[0]))
                faces1 = self.detector.detect(faceImg)
                if faces1[1] is None:
                    continue
                face1align = self.recognizer.alignCrop(faceImg, faces1[1][0])
                self.features.append(self.recognizer.feature(face1align))
                self.features_label.append(os.path.split(imagepath)[-1].split(".")[0])

    # start grabbing images for user "name"
    def startImageTaking(self, name):
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.user_creation = name
        self.sampleNum = 0

    # close the camera
    def stopCreating(self):
        self.cap.release()
        user = self.user_creation
        self.user_creation = None
        return user

    # find faces and save them to the device, return camera image with box around detected face
    def creatingImages(self):
        if self.user_creation == None:
            return None
        user = self.user_creation
        ret, frame = self.cap.read()
        self.detector.setInputSize(
            (
                int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            )
        )
        faces = self.detector.detect(frame)
        if faces[1] is not None:
            for idx, face in enumerate(faces[1]):
                self.sampleNum = self.sampleNum + 1
                x = int(face[0])
                y = int(face[1])
                w = int(face[2])
                h = int(face[3])
                cv2.imwrite(
                    self.where + f"img/{user}." + str(self.sampleNum) + ".jpg",
                    frame[y : y + h, x : x + w],
                )
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                break
        # return None once we saved enough images
        if self.sampleNum > 10:
            return None

        # Convert the frame to base64 to display on frontend
        retval, buffer = cv2.imencode(".jpg", frame)
        jpg_as_text = base64.b64encode(buffer).decode("utf-8")

        return "data:image/jpeg;base64," + jpg_as_text

    # Turn off the camera
    def stop_recognition(self):
        self.running = False
        if self.cap != None:
            self.cap.release()

    def run_recognition(self):

        start = time.time()

        self.cap = cv2.VideoCapture(0) #webcam

        self.running = True
# get the size of the webcam for comparison for reference photos
        self.detector.setInputSize(
            (
                int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            )
        )

        user = None
        # compare the current frame with the reference photos and score how close it aligns to authenticate
        while self.running and (time.time() - start) < 10:
            has_frame, frame = self.cap.read()
            if not has_frame:
                self.cap.release()
                break
            faces = self.detector.detect(frame)
            if faces[1] is not None:
                for idx, face in enumerate(faces[1]):
                    face_align = self.recognizer.alignCrop(frame, face)
                    face_feature = self.recognizer.feature(face_align)
                    scores = []
                    for feature in self.features:
                        cosine_score = self.recognizer.match(
                            feature, face_feature, cv2.FaceRecognizerSF_FR_COSINE
                        )
                        scores.append(cosine_score)
                    cosine_sim = 0.363 #threshold of correctness

                    try:
                        if max(scores) >= cosine_sim:
                            user = np.argmax(scores)
                            self.running = False
                            self.cap.release()
                            return self.features_label[user]
                    except:
                        return None
        self.running = False
        self.cap.release()
        return None
