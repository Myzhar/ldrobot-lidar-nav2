cmake_minimum_required(VERSION 3.5)
project(ld19_obstacle_detection)

################################################
# Check the ROS2 version

set(ROS2_FOUND FALSE)
if(DEFINED ENV{ROS_DISTRO})
  set(FOUND_ROS2_DISTRO $ENV{ROS_DISTRO})
  set(ROS2_FOUND TRUE)
  message(STATUS "* Found ROS2 ${FOUND_ROS2_DISTRO}")
else()
  message(WARNING "* ROS2 distro variable not set. Trying to figure it out...")
  set(ROS2_DISTROS "ardent;crystal;dashing;eloquent;foxy;galactic;humble;rolling")
  set(ROS2_FOUND FALSE)
  foreach(distro ${ROS2_DISTROS})
    if(NOT ROS2_FOUND)
      find_path(RCLCPP_H rclcpp.hpp PATHS /opt/ros/${distro}/include/rclcpp)
      if(RCLCPP_H)
        message(STATUS "* Found ROS2 ${distro}")
        set(FOUND_ROS2_DISTRO ${distro})
        set(ROS2_FOUND TRUE)
      endif()
    endif()
  endforeach()
endif()

if(ROS2_FOUND)
  if(${FOUND_ROS2_DISTRO} STREQUAL "humble")
    message(STATUS "* ROS2 ${FOUND_ROS2_DISTRO} is officially supported by this package.")
    add_definitions(-DFOUND_HUMBLE)
  else()
    message(FATAL_ERROR "ROS2 ${FOUND_ROS2_DISTRO} is not officially supported by this package. Correct working is not guarantee.")
  endif()
else()
  message(FATAL_ERROR "*** WARNING *** ROS2 distro is unknown. This package could not work correctly.")
endif()
################################################

find_package(ament_cmake REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

###############################################################################
#Add all files in subdirectories of the project in
# a dummy_target so qtcreator have access to all files
file(GLOB_RECURSE all_files ${CMAKE_SOURCE_DIR}/*)
add_custom_target(all_${PROJECT_NAME}_files SOURCES ${all_files})

###############################################################################
# INSTALL

# Install LAUNCH files
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

# Install PARAMS files
install(DIRECTORY
  params
  DESTINATION share/${PROJECT_NAME}
)

# Testing
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
