#------------------------------------------------------------------------------------------------------------------------------------
#
#   Author:     William Bourn
#   File:       Nano_Camera_Trap
#   Version:    1.00
#
#   Description:
#   The Nano_Camera_Trap library runs a program that utilizes hardware modules attached to a Nvidia Jetson Nano SBC to act as an
#   animal camera trap. A PIS (Pssive Infrared Sensor) is used to detect movement within the dual camera's field-of-view and the 
#   cameras record this action in a series of MP4 format video files.
#      
#------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------
#   Included Libraries
#------------------------------------------------------------------------------------------------------------------------------------

import os               #Used in error handling & video recording(threading)
import sys              #Used in error handling
import subprocess       #Used in camera recording(threading)
import signal           #Used in camera recording(threading)
import time

#------------------------------------------------------------------------------------------------------------------------------------
#   Constants & Global Variables
#------------------------------------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------------------------------------
#   Error Definitions
#------------------------------------------------------------------------------------------------------------------------------------

class ModuleNotFoundError(Exception):
    """
    Exception raised when a key module for the functioning of the camera trap is not found.

    @param module:              The module that is found to be missing
    @type module:               str
    """

    def __init__(self, module):
        self.module = module


#------------------------------------------------------------------------------------------------------------------------------------
#   Class Definitions
#------------------------------------------------------------------------------------------------------------------------------------

class Nano_Camera_Trap:
    """
    Class representing the whole camera trap setup.

    @param cam_0:               First CSI Camera
    @type cam_0:                CSI_Module

    @param cam_1:               Second CSI Camera
    @type cam_1:                CSI_Module

    @param pis:                 Passive Infrared Sensor
    @type pis:                  PIS_Module

    @param dir:                 The directory into which output video should be placed
    @type dir:                  str

    @param resolution:          The resolution of the video to be recorded as (width,height) of pixels
    @type                       (int,int)

    @param framerate:           The framerate of the video to be recorded in FPS (Frames Per Second)
    @type                       int

    @param rec_min_duration:    The enforced minimum duration of a recording session in seconds
    @type rec_min_duration:     float

    @param rec_max_duration:    The enforced maximum duration of a recording session in seconds
    @type rec_max_duration:     float

    @param active_threshold:    The duration in seconds during the start of recording for which activity must be detected. 
                                Recording is discarded if threshold is not met
    @type active_threshold:     float

    @param sleep_duration:      The enforced period of inactivity after a successful recording session in seconds
    @type sleep_duration:       float
    """


    def __init__(self, dir, resolution, framerate, rec_min_duration, rec_max_duration, active_threshold, sleep_duration):
        """
        Nano_Camera_Trap Constructor.
        
        @param dir:                 The directory into which output video should be placed
        @type dir:                  str

        @param resolution:          The resolution of the video to be recorded as (width,height) of pixels
        @type                       (int,int)

        @param framerate:           The framerate of the video to be recorded in FPS (Frames Per Second)
        @type                       int

        @param rec_min_duration:    The enforced minimum duration of a recording session in seconds
        @type rec_min_duration:     float

        @param rec_max_duration:    The enforced maximum duration of a recording session in seconds
        @type rec_max_duration:     float

        @param active_threshold:    The duration in seconds during the start of recording for which activity must be detected. 
                                    Recording is discarded if threshold is not met
        @type active_threshold:     float

        @param sleep_duration:      The enforced period of inactivity after a successful recording session in seconds
        @type sleep_duration:       float
        """
        
        try:
            self.cam_0 = CSI_Module(0, "cam_0")
            self.cam_1 = CSI_Module(1, "cam_1")
            self.pis = PIS_Module()

            self.dir = dir
            self.resolution = resolution
            self.framerate = framerate
            self.rec_min_duration = rec_min_duration
            self.rec_max_duration = rec_max_duration
            self.active_threshold = active_threshold
            self.sleep_duration = sleep_duration

        except ModuleNotFoundError as err:
            print("Error: %s Module Not Found. Ensure Connections Are Secure." %err.module)
            sys.exit(1)
        
        except os.error as error_type:
            raise error_type

    def start(self):
        """
        Start the camera trap.
        """
        pass       

    def start_Dual_Video_Capture(self):
        pass

    def stop_Dual_Video_Capture(self):
        pass
    


class CSI_Module:
    """
    Class representing a CSI camera module.

    @param id                   The CSI port number of the camera module
    @type id                    int

    @param name                 The plaintext name given to the camera module
    @type name                  str

    @param quiet                Enables the camera module's subprocess to print output to the command line
    @type quiet                 bool
    """

    def __init__(self, id, name, quiet = False):
        """
        CSI_Module Constructor.

        @param id                   The CSI port number of the camera module
        @type id                    int

        @param name                 The plaintext name given to the camera module
        @type name                  str

        @param quiet                Enables the camera module's subprocess to print output to the command line
        @type quiet                 bool

        @param running              Displays True whenever the process is running (i.e. video recording)
        @type                       bool
        """

        try:
            self.id = id
            self.name = name
            self.quiet = quiet

            #Empty process & Process flag
            self.pro = None
            self.running = False

            if self.is_Module_Valid() == False:
                raise ModuleNotFoundError(self.name)

        except os.error as error_type:
            raise error_type

    def is_Module_Valid(self):
        """
        Used to determine whether the CSI module is functioning.

        @return valid:              Value is True if module is working
        @rtype valid:               bool
        """
        #TODO: Implement this
        return True

    def start_Video_Capture(self, filename, resolution, framerate):
        """
        Start recording an MP4 video.
        """
        #TODO: Make this neater. Implement quiet mode.

        #Shut down process if it is still running
        if self.running == True:
            self.stop_Video_Capture()
            self.running = False
            time.sleep(1)

        #Generate process command
        command = ""

        #Select camera source
        command += "gst-launch-1.0 nvarguscamerasrc sensor-id=%d ! " %(self.id) 
        
        #Set resolution and framerate
        command += "'video/x-raw(memory:NVMM),width=%d,height=%d,framerate=%d/1,format=NV12' ! " %(resolution[0],resolution[1],framerate)

        #Convert raw input to MP4 format
        command += "nvv4l2h264enc ! h264parse ! mp4mux ! "

        #Record video in specified output file
        command += "filesink location=%s.mp4 -e" %(filename)

        #Start process
        self.running = True
        self.pro = subprocess.Popen(command, shell=True)
    

    def stop_Video_Capture(self):
        """
        Stop recording the MP4 video
        """
        #TODO: Make this neater. Implement None state functionality


        name = "gst-launch-1.0 nvarguscamerasrc sensor-id=%d" %(self.id)
        
        #Get the process ID
        pid = get_pid(name)

        print(pid)

        #Terminate process
        os.killpg(pid, signal.SIGINT)
        self.running = False

    
    

class PIS_Module:
    """
    Class representing a PIS Sensor module.

    @param name                 The plaintext name given to the camera module
    @type name                  str

    @param quiet                Enables the camera module's subprocess to print output to the command line
    @type quiet                 bool
    """

    def __init__(self):
        """
        PIS_Module Constructor.

        @param name                 The plaintext name given to the camera module
        @type name                  str

        @param quiet                Enables the camera module's subprocess to print output to the command line
        @type quiet                 bool
        """

        pass

    pass

#------------------------------------------------------------------------------------------------------------------------------------
#   Global Funtion Definitions
#------------------------------------------------------------------------------------------------------------------------------------

def get_pid(name):
    command = "pgrep -f '^%s'" %name
    pro = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = pro.communicate()
    print(out)

    return out


def system_Check():
    pass

def test():
    cam_1 = CSI_Module(0, "cam_1")
    cam_2 = CSI_Module(1, "cam_2")

    cam_1.start_Video_Capture("vid_test_1", (1280, 720), 30)
    cam_2.start_Video_Capture("vid_test_2", (1280, 720), 30)

    print("Started recording vid 1 & 2")

    time.sleep(10)

    cam_1.start_Video_Capture("vid_test_3", (1280, 720), 30)
    cam_2.start_Video_Capture("vid_test_4", (1280, 720), 30)

    print("Started recording vid 3 & 4")

    time.sleep(10)

    cam_1.stop_Video_Capture()
    cam_2.stop_Video_Capture()

    print("Finished")




#------------------------------------------------------------------------------------------------------------------------------------
#   Main Function Definitions
#------------------------------------------------------------------------------------------------------------------------------------

#TODO: Identify command line arguments and 
if __name__ == "__main__":
    
    test()