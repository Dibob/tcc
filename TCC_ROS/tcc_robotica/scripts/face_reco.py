#!/usr/bin/env python

from tcc_robotica.srv import *
from eigen_faces.face_reco_eigen import *
from fisher_faces.face_recog_fisher import *
from std_msgs.msg import Bool
from std_msgs.msg import UInt16
import rospy
import os

EIGEN_FACES = 1
FISHER_FACES = 2

def handle_faces_reco(req):
    print req.tipo
   
    if(req.tipo == EIGEN_FACES):
        eigen = EigenFaces()
        eigen.carregar_dados()
        name  = eigen.executar()
	return FaceValuesResponse(name)  
        
    elif(req.tipo == FISHER_FACES):
        fisher = FisherFaces()
        fisher.carregar_dados()
        name = fisher.executar()
        return FaceValuesResponse(name) 
	

def face_reco():
    rospy.init_node('face_reco')
    s = rospy.Service('face_reco',FaceValues, handle_faces_reco)
    rospy.spin()

if __name__ == "__main__":
    face_reco()

