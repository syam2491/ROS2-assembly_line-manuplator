import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class ManipulatorController(Node):
    def __init__(self):
        super().__init__('manipulator_controller')
        self.publisher = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)
        self.timer = self.create_timer(4.0, self.move_manipulator)
        self.current_position_index = 0

        self.positions = [
            [0.0, 0.0, 0.0, 0.0, 3.14, -0.10, 1.35, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.55, -0.73, 1.35, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, -0.10, 1.35, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.62, -0.6, 1.24, 0.0],
            [3.14, -0.2, 1.35, 0.0, 1.62, -0.6, 1.24, 0.0],
            [1.55, -0.73, 1.35, 0.0, 1.62, -0.6, 1.24, 0.0],
            [0.0, -0.10, 1.35, 0.0, 1.62, -0.6, 1.24, 0.0],
            [1.52, -0.60, 1.35, 0.0, 1.62, -0.6, 1.24, 0.0]
        ]
        
    def move_manipulator(self):
        if self.current_position_index >= len(self.positions):
            self.get_logger().info("Manipulator reached the final position.")
            return

        position = self.positions[self.current_position_index]
        self.get_logger().info(f"Moving manipulator to position: {position}")

        trajectory = JointTrajectory()
        trajectory.joint_names = ['hip1', 'shoulder1', 'elbow1', 'wrist1', 'hip', 'shoulder', 'elbow', 'wrist']

        point = JointTrajectoryPoint()
        point.positions = position

        duration = Duration()
        duration.sec = 4  # Set the number of seconds
        duration.nanosec = 0  # Set the number of nanoseconds
        point.time_from_start = duration

        trajectory.points.append(point)
        self.publisher.publish(trajectory)

        self.current_position_index += 1

def main(args=None):
    rclpy.init(args=args)
    manipulator_controller = ManipulatorController()
    rclpy.spin(manipulator_controller)
    manipulator_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

