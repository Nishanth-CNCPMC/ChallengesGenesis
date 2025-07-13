import threading

class JointState:
    def __init__(self):
        self.lock = threading.Lock()
        self.joint_positions = {}

    def update(self, new_positions):
        with self.lock:
            self.joint_positions = new_positions.copy()

    def get(self):
        with self.lock:
            return self.joint_positions.copy()


# Global instance
shared_joint_state = JointState()

