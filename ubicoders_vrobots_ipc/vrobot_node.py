import ctypes
import sys
import traceback
import numpy as np
from typing import Callable, Dict, Tuple, Optional, Any, List
from ubicoders_vrobots_msgs.states_msg_helper import VRobotState, StatesMsg, StatesMsgT
from .node_iox2 import ImageResolution, Iox2Node
from .node_zenoh import ZenohNode
import cv2
from .node_iox2_utils import *


class VRobotClient:
    def __init__(self):
        self.vrnode_list = []

    def add_vrobot_node(self, vrnode: Any):
        self.vrnode_list.append(vrnode)

    def update(self):
        for vrnode in self.vrnode_list:
            vrnode.update()

    def shutdown(self):
        for vrnode in self.vrnode_list:
            vrnode.shutdown()


class VRobotNodeBase:
    def __init__(self, sysId:int = 0, max_states_history:int = 10, image_resolution: ImageResolution = ImageResolution.P720):
        self.image_resolution = image_resolution
        self.sysId = sysId
        self.zenoh_node = ZenohNode(sysId)
        self.zenoh_node.create_publisher(f"vr/{self.sysId}/cmd")
        self.zenoh_node.create_subscriber(f"vr/{self.sysId}/states", self.states_listener)
        # states and image data can be stored here as needed max size = 10
        self.max_states_history = max_states_history
        self.states: List[VRobotState] = []

        # iox2 node for image subscriptions
        self.iox2_node = Iox2Node(sysId, 10)
        self.iox2_node.create_image_subscriber("left", self.image_resolution)
        self.iox2_node.create_image_subscriber("right", self.image_resolution)
        self.iox2_node.create_image_subscriber("down", self.image_resolution)

        self.state = VRobotState()
        
        # self.imgStateLeft = get_image_state_type(self.image_resolution)()
        # self.imgStateRight = get_image_state_type(self.image_resolution)()
        # self.imgStateDown = get_image_state_type(self.image_resolution)()
        self.imgStates = dict()


    def register_img_subscriber(self, cam_side:str):
        self.iox2_node.create_image_subscriber(cam_side, self.image_resolution)
        self.imgStates[cam_side] = get_image_state_type(self.image_resolution)()
        return self.imgStates[cam_side]

        
    def states_listener(self, sample: any):
        try:
            topic: str = sample.key_expr
            payload: bytes = sample.payload.to_bytes()

            if StatesMsg.StatesMsgBufferHasIdentifier(payload, 0) is False:
                return
            
            statesMsgT = StatesMsgT.InitFromPackedBuf(payload, 0)
            
            # VRobotState = ubicoders' wrapper to pretty print
            states: VRobotState = VRobotState(statesMsgT)
            self.states.append(states)
            
            if len(self.states) > self.max_states_history:
                self.states.pop(0)


        except Exception as e:
            self.shutdown()
            print(f"[VRobotNode] Error in states_listener for sysId={self.sysId}: {e}")
        

    def read_new_states(self, state: VRobotState) -> Tuple[bool, Optional[VRobotState]]:
        try:
            if len(self.states) == 0:
                return False, VRobotState()
            return self.states[-1].timestamp > state.timestamp, self.states[-1]
        except Exception as e:
            self.shutdown()
            print(f"[VRobotNode] Exception in read_new_states for sysId={self.sysId}:", flush=True)
            return False, VRobotState()

    def read_new_image(self, cam_side:str) -> Tuple[bool, Optional[ImageState720p]]:
        img_state = self.iox2_node.get_image_data(cam_side, self.image_resolution)
        if img_state is None:
            return False, get_image_state_type(self.image_resolution)()
        if (img_state.ts > self.imgStates[cam_side].ts):
            self.imgStates[cam_side] = img_state
            return True, img_state
        return False, img_state


    def publish_cmd(self, cmd_data: bytes):
        self.zenoh_node.publish(f"vr/{self.sysId}/cmd", cmd_data)


    def shutdown(self):
        
        self.zenoh_node.shutdown()
        self.iox2_node.shutdown()