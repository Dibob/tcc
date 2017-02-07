#!/usr/bin/env python

from tcc_robotica.srv import *
from std_msgs.msg import Bool
from std_msgs.msg import UInt16
import rospy
import os


class Arduino:
    def __init__(self):
        self.publica_servo_motor = ""
        self.pub_ar_condicionado = ""
        self.pub_radio = ""

    def publica_arduino(self,req):
        self.pub_servo_motor.publish(req.servo_angulo)
        self.pub_ar_condicionado.publish(req.nivel_arcondicionado)
        self.pub_radio.publish(req.radio)
        return UpdatePerfil(True) 

    def init_topicos(self):
        self.pub_servo_motor = rospy.Publisher('servo_motor',   UInt16,queue_size=10)
        self.pub_ar_condicionado = rospy.Publisher('ar_condicionado',UInt16,queue_size=10)
        self.pub_radio = rospy.Publisher('radio',Bool,queue_size=10)   



    def executar(self):
        rospy.init_node('arduino')
        s = rospy.Service('arduino',UpdatePerfil,self.publica_arduino)
        rospy.spin()

if __name__ == "__main__":
    arduino = Arduino()
    arduino.init_topicos()    
    arduino.executar()

