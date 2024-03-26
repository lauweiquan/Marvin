import numpy as np
import rclpy
from rclpy.node import Node
from custom_interfaces.msg import PoseLandmark
from std_msgs.msg import Float64
from .vector import vector_from_points, calculate_angle, project_vector_onto_plane

class ShoulderFlexionNode(Node):
    def __init__(self):
        side_param = 'left'  # Temporarily hold the default 'side' value
        super().__init__(f'{side_param}_shoulder_flexion')  # Initialize the base class first
        self.declare_parameter('side', side_param)  # Now declare the parameter
        side = self.get_parameter('side').get_parameter_value().string_value  # Retrieve the parameter value
        self.side = side
        self.subscription = self.create_subscription(PoseLandmark, 'pose_landmarks', self.listener_callback, 10)
        self.publisher = self.create_publisher(Float64, f'{side}_shoulder_flexion', 10)

    def listener_callback(self, msg):
        side = self.side
        opposite_side = 'left' if side == 'right' else 'right'
        labels, points = msg.label, msg.point
        idx = {label: labels.index(label) for label in [f'{side}_shoulder', f'{opposite_side}_shoulder', f'{side}_elbow', f'{opposite_side}_elbow', f'{side}_hip', f'{opposite_side}_hip']}

        upper_arm = vector_from_points(points[idx[f'{side}_shoulder']], points[idx[f'{side}_elbow']])
        shoulder_to_hip = vector_from_points(points[idx[f'{side}_shoulder']], points[idx[f'{side}_hip']])
        shoulder_to_shoulder = vector_from_points(points[idx[f'{side}_shoulder']], points[idx[f'{opposite_side}_shoulder']])

        projected = {
            'upper_arm': project_vector_onto_plane(upper_arm, shoulder_to_shoulder),
            'shoulder_to_hip': project_vector_onto_plane(shoulder_to_hip, shoulder_to_shoulder)
        }

        flexion_angle = calculate_angle(upper_arm, shoulder_to_hip)
        # if calculate_angle(np.cross(projected['upper_arm'], projected['shoulder_to_hip']), shoulder_to_shoulder) > np.pi/2:
        #     flexion_angle = -flexion_angle

        flexion_msg = Float64()
        flexion_msg.data = flexion_angle
        self.publisher.publish(flexion_msg)

def main():
    rclpy.init()
    node = ShoulderFlexionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()