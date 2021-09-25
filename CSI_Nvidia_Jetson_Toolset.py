#-----------------------------------------------------------------------------------------------------------
#
#   Author:     William Bourn
#   File:       CSI_Nvidia_Jetson_Toolset.py
#   Version:    1.00
#
#   Description:
#   A library of functions for capturing footage using CSI cameras on a Nvidia Jetson Nano. Toolset was
#   designed specifically for Pi Noir(No-Infrared) 2 CSI cameras.
#      
#-----------------------------------------------------------------------------------------------------------

#TO DO: Define common errors with custome error types
#TO DO: Define pipeline class and functionality
#TO DO: Define camera class and functionality

#-----------------------------------------------------------------------------------------------------------
#   Included Libraries
#-----------------------------------------------------------------------------------------------------------


import os
import sys
import subprocess
import signal
import time

#-----------------------------------------------------------------------------------------------------------
#   Command Line Argument Parser
#-----------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------
#   Constants
#-----------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------
#   Class Definitions
#-----------------------------------------------------------------------------------------------------------


class CSI_Camera_Module:
    """
    Class representing a CSI(Camera Serial Interface) device connected to the Jetson Nano. Contains 
    functionality for taking pictures and videos using the device.

    @param sensor_id:       CSI Port ID of the camera device
    @type sensor_id:        int

    @param process:         The currently active subprocess. Starting a new subprocess will override the 
                            current process
    @type process:          Popen
    """

    def __init__(self, sensor_id):
        """
        CSI_Camera_Module Constructor.
        """
        self.sensor_id = sensor_id
        self.process = None

    def start_Frame_Capture(self, filename, res):
        """
        Start a subprocess that captures a single frame and outputs a JPEG file.

        @param filename:        The name of the output JPEG file
        @type filename:         str

        @param res:             Resolution of the image (Scale goes from 2-12)         
        @type res:              int

        @param flip:            Indicates whether the orientation of the camera should be inverted
        @type flip:             bool
        """

        process_command = "nvgstcapture-1.0 --sensor-id=%d --image-res=%d --automate --capture-auto --start-time=1 --file-name=%s" %(self.sensor_id, res, filename)

        #Start the subprocess
        self.process = subprocess.Popen(process_command, shell=True)



    def start_Video_Capture(self, filename, width, height, framerate):
        """
        Start a subprocess that captures a video and outputs a MP4 file.

        @param filename:        The name of the output MP4 file
        @type filename:         str

        @param width:           The resolution width of the output video
        @type width:            int

        @param height:          The resolution height of the output video
        @type height:           int

        @param framerate:       The framerate of the output video
        @type framerate:        int

        """

        process_command = "gst-launch-1.0 nvarguscamerasrc sensor-id=%d ! 'video/x-raw(memory:NVMM),width=%d,height=%d,framerate=%d/1,format=NV12' ! nvv4l2h264enc ! h264parse ! mp4mux ! filesink location=%s.mp4 -e" %(self.sensor_id, width, height, framerate, filename)

        #Start the subprocess
        self.process = subprocess.Popen(process_command, shell=True)

    def terminate_Process(self):
        """
        Terminate the ongoing subprocess
        """
        
        os.killpg(os.getpgid(self.process.pid), signal.SIGINT)





#-----------------------------------------------------------------------------------------------------------
#   Global Function Definitions
#-----------------------------------------------------------------------------------------------------------

def test():

    cam1 = CSI_Camera_Module(0)
    #cam2 = CSI_Camera_Module(1)

    cam1.start_Video_Capture("vid_test_1", 1920, 1080, 30)
    #cam2.start_Video_Capture("vid_test_2", 1920, 1080, 30)

    time.sleep(10)

    cam1.terminate_Process()
    #cam2.terminate_Process()


#-----------------------------------------------------------------------------------------------------------
#   Main Function Definition
#-----------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    test()