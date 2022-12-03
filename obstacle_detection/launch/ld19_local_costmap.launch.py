# Copyright 2022 Walter Lucetti
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###########################################################################

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction)
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
    TextSubstitution)
from launch_ros.actions import Node

def launch_setup(context, *args, **kwargs):
    use_lifecycle_mgr = LaunchConfiguration("use_lifecycle_mgr")
    namespace = LaunchConfiguration("namespace")

    lifecycle_mgr_config = PathJoinSubstitution(
        [
            get_package_share_directory("ld19_obstacle_detection"),
            "params",
            "lifecycle_mgr.yaml",
        ]
    )

    local_costmap_config = PathJoinSubstitution(
        [
            get_package_share_directory("ld19_obstacle_detection"),
            "params",
            "local_costmap.yaml",
        ]
    )

    lifecycle_mgr_node = Node(
        condition=IfCondition(use_lifecycle_mgr),
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager",
        namespace=namespace,
        arguments=[],
        parameters=[
            # YAML file
            lifecycle_mgr_config
        ],
        output="screen",
    )

    local_costmap_node = Node(
        package="nav2_costmap_2d",
        executable="nav2_costmap_2d",
        name="local_costmap",
        namespace=namespace,
        arguments=[],
        parameters=[
            # YAML file
            local_costmap_config
        ],
        output="screen",
    )

    return [
        lifecycle_mgr_node,
        local_costmap_node
    ]


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_lifecycle_mgr",
                default_value="true",
                description=(
                    "Set to 'false' to use an external lifecycle manager or to trigger node status "
                    "manually."
                ),
            ),
            DeclareLaunchArgument(
                "namespace",
                default_value=TextSubstitution(text=""),
                description=(
                    "Namespace of the local cost map configuration."
                ),
            ),
            OpaqueFunction(function=launch_setup),
        ]
    )
