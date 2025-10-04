from ubicoders_vrobots_ipc import ZenohNode, vrobot_client_runner


class MyOwnVRNode():
    def __init__(self,):
        self.setup()

    # follow the convention of VRobotNodeBase - setup and update.
    def setup(self):
        self.zenoh_node = ZenohNode(-123) # some negative number but unqiue - to avoid conflict with vrobot nodes
        self.zenoh_node.create_publisher("my/own/topic")

    def update(self):       
        self.zenoh_node.publish("my/own/topic", b"hello from my own node")

if __name__ == "__main__":
    vrobot_client_runner([MyOwnVRNode()])
