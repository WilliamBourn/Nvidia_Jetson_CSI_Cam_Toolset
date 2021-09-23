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

import pygst
pygst.require(“0.10”)
import gst
import pygtk
import gtk

from os import error
import sys
import threading

#-----------------------------------------------------------------------------------------------------------
#   Command Line Argument Parser
#-----------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------
#   Constants
#-----------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------
#   Class Definitions
#-----------------------------------------------------------------------------------------------------------

class GStreamer_Pipeline:
    """
    Object containing an entire GStreamer pipeline command and functions to modify the pipeline.

    @param pipeline_stages:     List of pipeline stages
    @type pipeline_stages:      List(str)
    """

    def __init__(self, pipeline_stages = []):
        """
        GStreamer_Pipeline Constructor. Default arguments create an empty pipeline.

        @param pipeline_stages:     List of pipeline stages
        @type pipeline_stages:      List(str)
        """
        self.pipeline_stages = pipeline_stages

    def get_Pipeline_Stages(self):
        """
        Retrieve the raw list element containing the pipeline stages.

        @return pipeline_stages:    List of pipeline stages
        @rtype pipeline_stages:     list(str)
        """
        return self.pipeline_stages

    def append_Pipeline_Stage(self, stage):
        """
        Add a stage to the end of the pipeline.

        @param stage:               String argument for the appended pipeline stage
        @type stage:                str
        """
        self.pipeline_stages.append(stage)

    def insert_Pipeline_stage(self, index, stage):
        """
        Add a stage to the specified index of the pipeline.

        @param index:               Index to insert the stage into
        @type index:                int

        @param stage:               String argument for the appended pipeline stage
        @type stage:                str
        """
        self.pipeline_stages.insert(index, stage)

    def delete_Pipeline_Stage(self, index):
        """
        Remove the stage at the specified index from the pipeline.

        @param index:               Index to remove the stage from
        @type index:                int
        """
        self.pipeline_stages.pop(index)
    
    def generate_Pipeline_String(self):
        """
        Return a fully formatted pipeline string

        @return pipeline_string:    Formatted pipeline string
        @rtype pipeline_string:     str
        """
        #Create empty string for return value
        pipeline_string = ""

        #Iterate through stage list and insert pipeline stage sepparators
        for i in range(len(self.pipeline_stages)):
            pipeline_string = pipeline_string + self.pipeline_stages[i]

            #Ignore sepparator on final member of list
            if(i != len(self.pipeline_stages)):
                pipeline_string = pipeline_string + " ! "
        
        #Return formatted string
        return pipeline_string

class CSI_Camera:
    """
    Object that controls the functionality of a CSI camera with a specified pipeline.
    """

    def __init__(self, pipeline = None):
        """
        CSI_Camera Constructor. Default arguments creates an object with no pipeline loaded.

        @param pipeline:        Initial loaded pipeline
        @type pipeline:         GStreamer_Pipeline

        @param running:         Value is true while pipeline is active
        @type running:          bool
        """
        try:
            self.pipeline = None
            self.load_Pipeline(pipeline)
            self.running = False
            self.video_cap = None
        except error as error_type:
            raise error_type

    def load_Pipeline(self, pipeline):
        """
        Load a pipeline into the camera. Will overide the current pipeline.

        @param pipeline:        Pipeline to be loaded
        @type pipeline:         GStreamer_Pipeline
        """
        try:
            #Throw a TypeError if pipeline is not the correct type
            if((pipeline != None)&(type(pipeline) != GStreamer_Pipeline)):
                
                raise TypeError
            elif(pipeline == None):
                self.pipeline = None
            else:
                self.pipeline = pipeline
        except TypeError:
            print("Error: pipeline is not of type GStreamer_Pipeline")
            raise TypeError
        except error as error_type:
            raise error_type
    
    def start_Pipeline(self):
        """
        Begin execution of the loaded pipeline.
        """
        pass

    def stop_Pipeline(self):
        """
        End execution of the loaded pipeline.
        """
        pass


class Test:
    def __init__(self):
        self.pipeline = gst.Pipeline(“mypipeline”)

        self.cam_src = gst.element_factory_make("nvarguscamerasrc sensor-id=0", "cam_src")
        self.pipeline.add(self.cam_src)

        self.cam_parm = gst.element_factory_make("'video/x-raw(memory:NVMM),width=1920,height=1080,format=NV12,framerate=30/1'", "cam_parm")
        self.pipeline.add(self.cam_parm)

        self.enc = gst.element_factory_make("nvv4l2h264enc", "enc")
        self.pipeline.add(self.enc)

        self.parse = gst.element_factory_make("h264parse", "parse")
        self.pipeline.add(self.parse)

        self.mux = gst.element_factory_make("mp4mux", "mux")
        self.pipeline.add(self.cam_src)

        self.file_sink = gst.element_factory_make("filesink location=test.mp4", "file_sink")
        self.pipeline.add(self.cam_src)

        self.cam_src.link(self.cam_parm)
        self.cam_parm.link(self.enc)
        self.enc.link(self.parse)
        self.parse.link(self.mux)
        self.mux.link(self.file_sink)

        self.pipeline.set_state(gst.STATE_PLAYING)






#-----------------------------------------------------------------------------------------------------------
#   Global Function Definitions
#-----------------------------------------------------------------------------------------------------------

def test():
    """
    Test function. Determines if all the features of this toolset are working as intended.
    """
    pass

#-----------------------------------------------------------------------------------------------------------
#   Main Function Definition
#-----------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    start=Test()
    gtk.main()
