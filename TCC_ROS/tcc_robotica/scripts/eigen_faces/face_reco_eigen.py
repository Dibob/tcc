import numpy as np
import cv2
import sys
import os

RESIZE_FACTOR = 5
VALOR_DETEC = 50

class EigenFaces:

    def __init__(self):
        cascPath = "src/tcc_robotica/haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(cascPath)
        self.diretorio_faces = 'src/tcc_robotica/faces'
        self.modelo_eigen_train = cv2.createEigenFaceRecognizer()
        self.pessoas = []
        self.USER_DETECT = False
        self.indice_confidence = 0 
        self.quantidade_frames = 0      

    def carregar_dados(self):
        names = {}
        key = 0
        for (subdirs, dirs, files) in os.walk(self.diretorio_faces):
            for subdir in dirs:
                names[key] = subdir
                key += 1
        self.names = names
        self.modelo_eigen_train.load('src/tcc_robotica/eigen_trained_data.xml')

    def executar(self):
        video_capture = cv2.VideoCapture(0)
        while True:
            ret, frame = video_capture.read()
            img = np.array(frame)
            self.pessoas = self.processar_imagem(img)
            self.quantidade_frames = self.quantidade_frames+1  
            print self.pessoas  
            if self.pessoas:
                nome_pessoa = self.pessoas[0]
                print self.pessoas[0]
                if not nome_pessoa == "Pessoa Desconhecida":
		    video_capture.release()
                    cv2.destroyAllWindows()
                    return nome_pessoa
               
            if not self.pessoas and self.quantidade_frames >VALOR_DETEC:
                return "desconhecido"    

    def processar_imagem(self, inImg):
        person = ""
        persons = []
        usuarios = []   
       
        frame = cv2.flip(inImg,1)
        resized_width, resized_height = (112, 92)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)        
        gray_resized = cv2.resize(gray, (gray.shape[1]/RESIZE_FACTOR, gray.shape[0]/RESIZE_FACTOR))        
        faces = self.face_cascade.detectMultiScale(
                gray_resized,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                )
      
        for i in range(len(faces)):
            face_i = faces[i]
            x = face_i[0] * RESIZE_FACTOR
            y = face_i[1] * RESIZE_FACTOR
            w = face_i[2] * RESIZE_FACTOR
            h = face_i[3] * RESIZE_FACTOR
            face = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face, (resized_width, resized_height))
	    taxa_confianca = self.modelo_eigen_train.predict(face_resized)
	    
            if taxa_confianca[1]<3500:
                person = self.names[taxa_confianca[0]]
                self.indice_confidence = taxa_confianca[1]
            else: 
                person = "Pessoa Desconhecida"        

            persons.append(person)

        return persons




