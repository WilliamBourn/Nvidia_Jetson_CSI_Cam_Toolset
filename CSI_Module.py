#-----------------------------------------------------------------------------------------------------------
#
#   Author:     William Bourn
#   File:       CSI_Camera.py
#   Version:    1.00
#
#   Description:
#   The CSI_Camera library contains tools and class definitions that support the implementation of video and
#   image capture using CSI(Camera Serial Interface) devices using GStreamer pipelines. This module was 
#   designed for use on the Nvidia_Jetson_Nano to be used with Raspberry Pi camera modules.
#      
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
#   Included Libraries
#-----------------------------------------------------------------------------------------------------------

#TODO: Give descriptions

import os       
import sys
import subprocess
import signal
import time

#-----------------------------------------------------------------------------------------------------------
#   Command Line Argument Parser
#-----------------------------------------------------------------------------------------------------------

#TODO: Add Command line arguments

#-----------------------------------------------------------------------------------------------------------
#   Constants
#-----------------------------------------------------------------------------------------------------------

#TODO: Add constants



#-----------------------------------------------------------------------------------------------------------
#   Class Definitions
#-----------------------------------------------------------------------------------------------------------

class CSI_Camera:
    """
    The CSI_Camera object is a software structure that corresponds to a physical CSI interfacing deviceand
    and is used for performing video and image capture using GStreamer pipelines.

    @param id:              CSI Port ID number of the device
    @type id:               int

    @param log_file:        The text file to which the output of the process is dumped
    @type log_file:         str

    @param process:         The currently active subprocess. Will be overridden in the case where a new
                            subprocess is initiated
    @type process:          Popen
    """

    def __init__(self, id, log_file):
        """
        CSI_Camera Constructor. 
        """

        self.process = None
        self.id = id
        self.log_file = log_file

    def start_Process(self, command, shell = True):
        """
        Set the process command and begin the subprocess. Overide the previous process
        """

        self.terminate_Process()
        self.process = subprocess.Popen(command, shell=shell, stdout=self.log_file)


    def terminate_Process(self):
        """
        Terminate the current process. Does nothing if process is not running
        """

        if self.process == None:
            return
        if self.is_Process_Running() == False:
            return

        #Get the process ID
        process_id = os.getpgid(self.process.pid)

        #Terminate process
        os.killpg(process_id, signal.SIGINT)

    def is_Process_Running(self):
        """
        Return True if process is ongoing.
        """

        if self.process.poll() == None:
            return True
        else:
            return False
    
    def video_Capture(self, filename, res_width, res_height, framerate, duration):
        """
        Record a fixed duration MP4 format video.
        """

        #Generate process command

        #Select camera source
        command = "gst-launch-1.0 nvarguscamerasrc sensor-id=%d ! " %(self.id) 
        
        #Set resolution and framerate
        command += "'video/x-raw(memory:NVMM),width=%d,height=%d,framerate=%d/1,format=NV12' ! " %(res_width,res_height,framerate)

        #Convert raw input to MP4 format
        command += "nvv4l2h264enc ! h264parse ! mp4mux ! "

        #Record video in specified output file
        command += "filesink location=%s.mp4 -e" %(filename)

        self.start_Process(command)
        time.sleep(duration)
        self.terminate_Process()

    def continuous_Video_Capture(self, filename, res_width, res_height, framerate):
        """
        The same, but requires explicit call to stop recording.
        """

        #Generate process command

        #Select camera source
        command = "gst-launch-1.0 nvarguscamerasrc sensor-id=%d ! " %(self.id) 
        
        #Set resolution and framerate
        command += "'video/x-raw(memory:NVMM),width=%d,height=%d,framerate=%d/1,format=NV12' ! " %(res_width,res_height,framerate)

        #Convert raw input to MP4 format
        command += "nvv4l2h264enc ! h264parse ! mp4mux ! "

        #Record video in specified output file
        command += "filesink location=%s.mp4 -e" %(filename)

        self.start_Process(command)

    def Image_Capture(self):
        pass



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
    cam2 = CSI_Camera_Module(1)

    cam1.start_Video_Capture("vid_test_1", 1280, 720, 30)
    cam2.start_Video_Capture("vid_test_2", 1280, 720, 30)

    time.sleep(10)

    cam1.terminate_Process()
    cam2.terminate_Process()


#-----------------------------------------------------------------------------------------------------------
#   Main Function Definition
#-----------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    test()