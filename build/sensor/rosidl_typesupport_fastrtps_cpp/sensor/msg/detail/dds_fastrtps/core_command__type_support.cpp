// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from sensor:msg/CoreCommand.idl
// generated code does not contain a copyright notice
#include "sensor/msg/detail/core_command__rosidl_typesupport_fastrtps_cpp.hpp"
#include "sensor/msg/detail/core_command__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

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
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: led
  cdr << ros_message.led;
  // Member: pwm
  cdr << ros_message.pwm;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_sensor
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  sensor::msg::CoreCommand & ros_message)
{
  // Member: led
  cdr >> ros_message.led;

  // Member: pwm
  cdr >> ros_message.pwm;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_sensor
get_serialized_size(
  const sensor::msg::CoreCommand & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: led
  {
    size_t item_size = sizeof(ros_message.led);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: pwm
  {
    size_t item_size = sizeof(ros_message.pwm);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_sensor
max_serialized_size_CoreCommand(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;


  // Member: led
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: pwm
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  return current_alignment - initial_alignment;
}

static bool _CoreCommand__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const sensor::msg::CoreCommand *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _CoreCommand__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<sensor::msg::CoreCommand *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _CoreCommand__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const sensor::msg::CoreCommand *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _CoreCommand__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_CoreCommand(full_bounded, 0);
}

static message_type_support_callbacks_t _CoreCommand__callbacks = {
  "sensor::msg",
  "CoreCommand",
  _CoreCommand__cdr_serialize,
  _CoreCommand__cdr_deserialize,
  _CoreCommand__get_serialized_size,
  _CoreCommand__max_serialized_size
};

static rosidl_message_type_support_t _CoreCommand__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_CoreCommand__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace sensor

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_sensor
const rosidl_message_type_support_t *
get_message_type_support_handle<sensor::msg::CoreCommand>()
{
  return &sensor::msg::typesupport_fastrtps_cpp::_CoreCommand__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, sensor, msg, CoreCommand)() {
  return &sensor::msg::typesupport_fastrtps_cpp::_CoreCommand__handle;
}

#ifdef __cplusplus
}
#endif
