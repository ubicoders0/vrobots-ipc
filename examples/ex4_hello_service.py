from ubicoders_vrobots_ipc import req_srv_mission, req_srv_simparams
from ubicoders_vrobots_msgs import Vec3MsgT, MissionMsgT, VRSceneObjectT, SrvSimParamsMsgT
import time
if __name__ == "__main__":
    # pos = Vec3MsgT()
    # pos.x, pos.y, pos.z = 53.6, 180.5, -0.3

    # vrobot = VRSceneObjectT()
    # vrobot.objectType = "multirotor"
    # vrobot.position = pos

    # mission = MissionMsgT()
    # mission.vrobots =  [vrobot]   
    # mission.newMission = False

    # req_srv_mission(mission)

    # prop = SrvVRobotPhysicalPropertyMsgT()
    # prop.timestamp = time.time() * 1e3
    # prop.setMass = 3
    # prop.setMoi3x1 = [1, 1, 1]
    # req_srv_physical_property(prop)

    simParams = SrvSimParamsMsgT()
    simParams.timestamp = time.time() * 1e3
    simParams.setImgResolution = 360
    req_srv_simparams(simParams)