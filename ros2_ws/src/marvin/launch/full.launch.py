from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    ld = LaunchDescription()

    # Declare parameters for the package name, model path, and RViz config
    ld.add_action(DeclareLaunchArgument('marvin', default_value='marvin',
                                        description='The package where the robot description is located'))
    
    default_model_path = 'urdf/open_manipulator.urdf.xacro'
    ld.add_action(DeclareLaunchArgument('model', default_value=default_model_path,
                                        description='The path to the robot description relative to the package root'))
    
    marvin_path = FindPackageShare(LaunchConfiguration('marvin'))
    default_rviz_config_path = PathJoinSubstitution([marvin_path, 'rviz', 'urdf.rviz'])
    ld.add_action(DeclareLaunchArgument(name='rviz_config', default_value=default_rviz_config_path,
                                        description='Absolute path to RViz config file'))

    # Setup for robot description
    model = PathJoinSubstitution([marvin_path, LaunchConfiguration('model')])
    robot_description_content = ParameterValue(Command(['xacro ', model]), value_type=str)

    robot_state_publisher_node = Node(package='robot_state_publisher',
                                      executable='robot_state_publisher',
                                      parameters=[{
                                          'robot_description': robot_description_content,
                                      }])
    ld.add_action(robot_state_publisher_node)

    pose_detection_node = Node(
        package='marvin',
        executable='poseDetection',
        output='screen',
    )
    ld.add_action(pose_detection_node)

    left_shoulder_flexion = Node(
        package='marvin',
        executable='shoulderFlexion',
        name='left_shoulder_flexion',
        # parameters=[{'side': 'left'}],
        output='screen'
    )
    ld.add_action(left_shoulder_flexion)

    # right_shoulder_flexion = Node(
    #     package='marvin',
    #     executable='shoulderFlexion',
    #     name='right_shoulder_flexion',
    #     parameters=[{'side': 'right'}],
    #     output='screen'
    # )
    # ld.add_action(right_shoulder_flexion)

    left_shoulder_adduction = Node(
        package='marvin',
        executable='shoulderAdduction',
        name='left_shoulder_adduction',
        # parameters=[{'side': 'left'}],
        output='screen'
    )
    ld.add_action(left_shoulder_adduction)

    # right_shoulder_adduction = Node(
    #     package='marvin',
    #     executable='shoulderAdduction',
    #     name='right_shoulder_adduction',
    #     parameters=[{'side': 'right'}],
    #     output='screen'
    # )
    # ld.add_action(right_shoulder_adduction)

    elbow_joint_node = Node(
        package='marvin',
        executable='elbowJoint',
        output='screen',
    )
    ld.add_action(elbow_joint_node)

    wrist_joint_node = Node(
        package='marvin',
        executable='wristJoint',
        output='screen',
        emulate_tty=True
    )
    ld.add_action(wrist_joint_node)

    joint_state_publisher_node = Node(
        package='marvin',
        executable='jointStatePublisher',
        output='screen',
    )
    ld.add_action(joint_state_publisher_node)

    display_joint_states = Node(
        package='marvin',
        executable='displayJointStates',
        output='screen',
    )
    ld.add_action(display_joint_states)

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rviz_config')],
    )
    ld.add_action(rviz_node)

    return ld