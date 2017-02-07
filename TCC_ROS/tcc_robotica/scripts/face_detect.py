#!/usr/bin/env python

from tcc_robotica.srv import *
from fisher_faces.treinamento_fisher import *
from eigen_faces.treinamento_eigen import *
import rospy


EIGEN_FACES = 1
FISHER_FACES = 2

 
def manipula_deteccao_faces(req):
    if(req.tipo == EIGEN_FACES):	
        treinamento_eigen = TreinamentoEigen(req.nome)
        classificacao = treinamento_eigen.captura_de_images_treinamento_eigen()
        treinamento_eigen.treinamento_de_dados_eigenfaces()
        return UserResponse(classificacao)
    elif (req.tipo == FISHER_FACES):
        treinamento_fisher = TreinamentoFisher(req.nome)
        classificacao = treinamento_fisher.captura_de_images_treinamento_fisher()
        treinamento_fisher.treinamento_de_dados_fisherfaces()
        print classificacao
        return UserResponse(classificacao)
  

def face_detect():
    rospy.init_node('face_detect')
    s = rospy.Service('face_detect',User,manipula_deteccao_faces)
    rospy.spin()
 
if __name__ == "__main__":
    face_detect()

