#!/usr/bin/python3

import rospy
from sensor_msgs.msg import Image

import picamera
import signal

stop_process = False

def signal_handler(signal, frame):
        global stop_process
        stop_process = True
signal.signal(signal.SIGINT, signal_handler)

RES = (640, 480)

# Class to process camera messages
class Stream(object):

    # Called when new image is available
    def write(self, data):
        
        # Create an image instance and publish
        img = Image()
        img.width = RES[0]
        img.height = RES[1]
        img.encoding = "yuv422"
        img.step = RES[0]
        img.data = data[:(RES[0] * RES[1])]
        
        pub_img.publish(img)
        
        
if __name__ == "__main__":

    # Set up node using NODENAME
    # Anonymous makes sure the node has a unique name by adding numbers to it
    rospy.init_node("camera")
    
    topic_name_image = rospy.get_param("topic_name_camera", "camera/image")
    
    res_width = rospy.get_param("~resolution/width", 640)
    res_height = rospy.get_param("~resolution/height", 480)
    RES = (res_width, res_height)
    fps = rospy.get_param("~fps", 50)
    
    # Set up ros publisher to publish on img topic, using Image message
    pub_img = rospy.Publisher(topic_name_image, Image, queue_size=1)

    # Start capturing camera images
    with picamera.PiCamera() as camera:
        rospy.loginfo("Start to streamming images of size = " + str(RES) + ", and FPS = " + str(fps))
        
        camera.resolution = RES
        camera.framerate = fps
        
        try:
            camera.start_recording(Stream(), format='yuv')
            while not stop_process:
                camera.wait_recording(1)
        except:
            pass
        
        rospy.loginfo("Program closing ...")
        camera.stop_recording()
        camera.close()