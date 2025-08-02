// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from sensor:msg/CoreCommand.idl
// generated code does not contain a copyright notice

#ifndef SENSOR__MSG__DETAIL__CORE_COMMAND__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define SENSOR__MSG__DETAIL__CORE_COMMAND__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "sensor/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "sensor/msg/detail/core_command__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace sensor
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_sensor
cdr_serialize(
  const sensor::msg::CoreCommand & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_sensor
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  sensor::msg::CoreCommand & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_sensor
get_serialized_size(
  const sensor::msg::CoreCommand & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_sensor
max_serialized_size_CoreCommand(
  bool & full_bounded,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace sensor

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_sensor
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, sensor, msg, CoreCommand)();

#ifdef __cplusplus
}
#endif

#endif  // SENSOR__MSG__DETAIL__CORE_COMMAND__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
