cmake_minimum_required(VERSION 3.5)
project(sensor)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_srvs REQUIRED)

find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/CoreCommand.msg"
  "msg/DeviceStatus.msg"
  DEPENDENCIES std_msgs
)

# openamp
add_executable(openamp_core1 src/openamp_core1.cpp)
ament_target_dependencies(openamp_core1 rclcpp std_msgs)

rosidl_target_interfaces(openamp_core1
  ${PROJECT_NAME} "rosidl_typesupport_cpp"
)



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

# 添加包含路径
include_directories(include)

# 添加aht10_node
add_executable(sensor_node src/sensor_node.cpp)
ament_target_dependencies(sensor_node rclcpp std_msgs)

# 触摸
add_executable(human_detector_client src/human_detector_client.cpp)
add_executable(do_something_server src/do_something_server.cpp)

ament_target_dependencies(human_detector_client rclcpp std_srvs)
ament_target_dependencies(do_something_server rclcpp std_srvs)

# 安装
install(TARGETS
  sensor_node
  human_detector_client
  do_something_server
  openamp_core1
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
