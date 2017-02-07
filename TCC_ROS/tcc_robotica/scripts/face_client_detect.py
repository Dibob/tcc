#!/usr/bin/env python

import sys
import rospy
from tcc_robotica.srv import *

def face_client(nome,tipo):
    rospy.wait_for_service('face_detect')
    try:
        faces = rospy.ServiceProxy('face_detect',User)
        resp1 = faces(nome,tipo)
        return resp1.classificacao
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


if __name__ == "__main__":
    tipo = 2
    nome = "diego"
    print face_client(nome,tipo)
     


    
    

    
