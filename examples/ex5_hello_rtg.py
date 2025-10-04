from ubicoders_vrobots_ipc import VRobotNodeBase, vrobot_client_runner
#===================================
# add this line
from ubicoders_vrobots_ipc import RTGPub 
#===================================

class VRobotNode(VRobotNodeBase):
    def __init__(self, sysId:int = 0):
        super().__init__(sysId)

    def setup(self):
        #===================================
        # add this line
        self.rtg = RTGPub(topic_name=f"vr/{self.sysId}/rtg")
        #===================================

    def update(self):       
        if self.read_new_states(): 
            ts = self.state.timestamp
            pos = self.state.linPos
            elapsed_sec = (ts - self.first_ts) / 1000.0
            print(f"State t={elapsed_sec} pos=({pos.x:.2f},{pos.y:.2f},{pos.z:.2f})")
            #===================================
            # add this line
            self.rtg.publish(elapsed_sec, [pos.x, pos.y, pos.z])
            #===================================

if __name__ == "__main__":
    vrobot_client_runner([VRobotNode(sysId=0)])
