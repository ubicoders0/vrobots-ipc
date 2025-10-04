from ubicoders_vrobots_ipc import ZenohNode, vrobot_client_runner

class MyOwnVRNode():
    def __init__(self,):
        self.setup()

    # listener callback function
    def listener_callback(self, sample):
        topic: str = sample.key_expr
        payload: bytes = sample.payload.to_bytes()
        print(f"Received data: {payload.decode('utf-8')}")

    # this will be called at ctrl+c, otherwise, the terminal may freeze.    
    def shutdown(self):
        self.zenoh_node.shutdown()

    # follow the convention of VRobotNodeBase - setup and update.
    def setup(self):
        self.zenoh_node = ZenohNode(-123) # some negative number but unqiue - to avoid conflict with vrobot nodes
        self.zenoh_node.create_subscriber("my/own/topic", self.listener_callback)


    def update(self):       
        # do some cool stuff here
        pass

if __name__ == "__main__":
    vrobot_client_runner([MyOwnVRNode()])
