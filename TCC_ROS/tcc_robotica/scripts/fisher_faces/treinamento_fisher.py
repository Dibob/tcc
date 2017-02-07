import numpy as np
import cv2
import sys
import os

FREQ_DIV = 5  
FATOR_REDIMENSIONAMENTO = 4
VALOR_TREINAMENTO = 10

class TreinamentoFisher:
    def __init__(self,nome):
        cascPath = "src/tcc_robotica/haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(cascPath)
        self.diretorio_imagens_faces = 'src/tcc_robotica/faces'
        self.nome = nome
        self.caminho_da_pasta = os.path.join(self.diretorio_imagens_faces, self.nome)
        if not os.path.isdir(self.caminho_da_pasta):
            os.mkdir(self.caminho_da_pasta)
        self.modelo = cv2.createFisherFaceRecognizer()
	self.numero_imagens_capturadas = 0
        self.contador_de_tempo = 0

    def captura_de_images_treinamento_fisher(self):
        video_capture = cv2.VideoCapture(0)
        while True:
            self.contador_de_tempo += 1
            ret, frame = video_capture.read()
            img = np.array(frame)
            condicao_treinamento =self.processa_imagem_capturada(img)
            print condicao_treinamento
	    if condicao_treinamento:
                video_capture.release()
                return condicao_treinamento


    def processa_imagem_capturada(self, img):
        frame = cv2.flip(img,1)
        redimensiona_largura,redimensiona_altura = (112, 92)        
        if self.numero_imagens_capturadas < VALOR_TREINAMENTO:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
            gray_resized = cv2.resize(gray, (gray.shape[1]/FATOR_REDIMENSIONAMENTO, gray.shape[0]/FATOR_REDIMENSIONAMENTO))        
            faces = self.face_cascade.detectMultiScale(
                gray_resized,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                )
            if len(faces) > 0:
                areas = []
                for (x, y, w, h) in faces: 
                    areas.append(w*h)
                max_area, idx = max([(val,idx) for idx,val in enumerate(areas)])
                face_sel = faces[idx]
            
                x = face_sel[0] * FATOR_REDIMENSIONAMENTO
                y = face_sel[1] * FATOR_REDIMENSIONAMENTO
                w = face_sel[2] * FATOR_REDIMENSIONAMENTO
                h = face_sel[3] * FATOR_REDIMENSIONAMENTO

                face = gray[y:y+h, x:x+w]
                rosto_redimensionado = cv2.resize(face, (redimensiona_largura, redimensiona_altura))
                img_no = sorted([int(fn[:fn.find('.')]) for fn in os.listdir(self.caminho_da_pasta) if fn[0]!='.' ]+[0])[-1] + 1       
                if self.contador_de_tempo % FREQ_DIV == 0:
                    cv2.imwrite('%s/%s.png' % (self.caminho_da_pasta, img_no), rosto_redimensionado)
                    self.numero_imagens_capturadas += 1
                    print "Obtendo  imagens:", self.numero_imagens_capturadas

        elif self.numero_imagens_capturadas == VALOR_TREINAMENTO:
            return True
           
	

    def ver_quantidade_adequada_faces(self):
        existem_faces = 0
        for (subdirs, dirs, files) in os.walk(self.diretorio_imagens_faces):
            for subdir in dirs:
                existem_faces += 1

        if existem_faces > 1:
            return True
        else:
            return False

    def treinamento_de_dados_fisherfaces(self):
        imgs = []
        tags = []
        index = 0

        for (subdirs, dirs, files) in os.walk(self.diretorio_imagens_faces):
            for subdir in dirs:
                img_path = os.path.join(self.diretorio_imagens_faces, subdir)
                for fn in os.listdir(img_path):
                    path = img_path + '/' + fn
                    tag = index
                    imgs.append(cv2.imread(path, 0))
                    tags.append(int(tag))
                index += 1
        (imgs, tags) = [np.array(item) for item in [imgs, tags]]

        self.modelo.train(imgs, tags)
        self.modelo.save('src/tcc_robotica/fisher_trained_data.xml')



