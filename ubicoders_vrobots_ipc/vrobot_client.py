import time
import zenoh
from ubicoders_vrobots_ipc.node_iox2_utils import ImageResolution
from .vrobot_node import VRobotNodeBase,VRobotState, VRobotClient
import cv2
from .rtg_pub import RTGPub

class VRobotNode(VRobotNodeBase):
    def __init__(self, sysId:int = 0):
        super().__init__(sysId)
        self.setup()
        self.start_time = 0

    def setup(self):
        self.rtg = RTGPub(topic_name=f"vr/{self.sysId}/rtg")
        # self.state, self.imgStateLeft, self.imgStateRight, self.imgStateDown = self.initialize()
        cv2.namedWindow("CamLeft", cv2.WINDOW_NORMAL)   # make resizable window
        cv2.resizeWindow("CamLeft", 640, 360)
        cv2.namedWindow("CamRight", cv2.WINDOW_NORMAL)   # make resizable window
        cv2.resizeWindow("CamRight", 640, 360)
        cv2.namedWindow("CamDown", cv2.WINDOW_NORMAL)   # make resizable window
        cv2.resizeWindow("CamDown", 640, 360)
        
        self.register_img_subscriber("left")
        self.register_img_subscriber("right")
        self.register_img_subscriber("down")
        isNewState, state = self.read_new_states(self.state)
        self.start_time = state.timestamp if isNewState else 0
        print(f"Start time: {self.start_time}")

    def update(self):
        isNewState, state = self.read_new_states(self.state)
        if isNewState:
            self.state = state
            ts = self.state.timestamp
            pos = self.state.linPos
            elapsed_sec = (ts - self.start_time) / 1000.0
            print(f"State t={elapsed_sec} pos=({pos.x:.2f},{pos.y:.2f},{pos.z:.2f})")
            self.rtg.publish(elapsed_sec, [pos.x, pos.y, pos.z])

        isNewImgLeft, imgStateLeft = self.read_new_image("left")
        if isNewImgLeft:
            self.imgStateLeft = imgStateLeft
            # print(f"Image ts={self.imgStateLeft.ts}")
            cv2.imshow("CamLeft", self.imgStateLeft.image_data)
            cv2.waitKey(1)

        isNewImgRight, imgStateRight = self.read_new_image("right")
        if isNewImgRight:
            self.imgStateRight = imgStateRight
            # print(f"Image ts={self.imgStateRight.ts}")
            cv2.imshow("CamRight", self.imgStateRight.image_data)
            cv2.waitKey(1)

        isNewImgDown, imgStateDown = self.read_new_image("down")
        if isNewImgDown:
            self.imgStateDown = imgStateDown
            # print(f"Image 2 ts={self.imgStateDown.ts}")
            cv2.imshow("CamDown", self.imgStateDown.image_data)
            cv2.waitKey(1)


def main():
    vrclient = VRobotClient()
    vrclient.add_vrobot_node(VRobotNode(sysId=0))
    try:
        while True:
            vrclient.update()            
            time.sleep(0.02)
    finally:
        print(f"Shutting down...")
        vrclient.shutdown()

if __name__ == "__main__":
    main()
