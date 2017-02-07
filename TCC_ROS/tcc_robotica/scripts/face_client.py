#!/usr/bin/env python

import sys
import rospy
from tcc_robotica.srv import *

def face_client(tipo):
    rospy.wait_for_service('face_reco')
    try:
        faces = rospy.ServiceProxy('face_reco',FaceValues)
        resp1 = faces(tipo)
        return resp1.nome
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


if __name__ == "__main__":
    tipo = 2
    print  "usuario encontrado %s"%face_client(tipo)
     


    
    

    
