#! /usr/bin/env python
import rospy
from std_msgs.msg import String
import subprocess
import sys
import argparse
import os
import time
from qr_new import decode
from subprocess import PIPE
import pexpect

fn = sys.argv[1]


def talker(): 
	pub = rospy.Publisher('chatter', String, queue_size=10)
	rospy.init_node('talker')
	r = rospy.Rate(10) # 10hz


	print (os.path.abspath(fn))
	#proc = subprocess.Popen(["python qr_new.py "+os.path.abspath(fn)],stdout=PIPE,shell=True)
	child = pexpect.spawn("python qr_new.py "+os.path.abspath(fn),timeout=None)
	child.maxsize = 1
	child.expect("init done")
	line= child.before

	while not rospy.is_shutdown():
		pub.publish(line)
		print (line)
		r.sleep()

if __name__ == '__main__':
     try:
 	    talker()
     except rospy.ROSInterruptException:
	     pass