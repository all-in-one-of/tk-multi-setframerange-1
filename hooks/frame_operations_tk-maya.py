# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import pymel.core as pm
import maya.cmds as cmds

import sgtk
from sgtk import TankError

HookBaseClass = sgtk.get_hook_baseclass()


class FrameOperation(HookBaseClass):
    """
    Hook called to perform a frame operation with the 
    current scene
    """
    
    def execute(self, operation, head_in_frame=None, in_frame=None, out_frame=None, tail_out_frame=None, **kwargs):
        """
        Main hook entry point
        
        :operation: String
                    Frame operation to perform
        
        :in_frame: int
                    in_frame for the current context (e.g. the current shot, 
                                                      current asset etc)
                    
        :out_frame: int
                    out_frame for the current context (e.g. the current shot, 
                                                      current asset etc)
                    
        :returns:   Depends on operation:
                    'set_frame_range' - Returns if the operation was succesfull
                    'get_frame_range' - Returns the frame range in the form (in_frame, out_frame)
        """

        if operation == "get_frame_range":
            current_in = cmds.playbackOptions(query=True, minTime=True)
            current_out = cmds.playbackOptions(query=True, maxTime=True)
            return (current_in, current_out)
        elif operation == "set_frame_range":
            # set frame ranges for plackback
            pm.playbackOptions(minTime=in_frame, 
                               maxTime=out_frame,
                               animationStartTime=in_frame,
                               animationEndTime=out_frame)
            
            # set frame ranges for rendering
            defaultRenderGlobals=pm.PyNode('defaultRenderGlobals')
            defaultRenderGlobals.startFrame.set(in_frame)
            defaultRenderGlobals.endFrame.set(out_frame)
            return True
