// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from sensor:msg/DeviceStatus.idl
// generated code does not contain a copyright notice
#include "sensor/msg/detail/device_status__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "sensor/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "sensor/msg/detail/device_status__struct.h"
#include "sensor/msg/detail/device_status__functions.h"
#include "fastcdr/Cdr.h"

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

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _DeviceStatus__ros_msg_type = sensor__msg__DeviceStatus;

static bool _DeviceStatus__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _DeviceStatus__ros_msg_type * ros_message = static_cast<const _DeviceStatus__ros_msg_type *>(untyped_ros_message);
  // Field name: temperature
  {
    cdr << ros_message->temperature;
  }

  // Field name: humidity
  {
    cdr << ros_message->humidity;
  }

  // Field name: presence
  {
    cdr << ros_message->presence;
  }

  // Field name: mq2
  {
    cdr << ros_message->mq2;
  }

  // Field name: val
  {
    cdr << ros_message->val;
  }

  return true;
}

static bool _DeviceStatus__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _DeviceStatus__ros_msg_type * ros_message = static_cast<_DeviceStatus__ros_msg_type *>(untyped_ros_message);
  // Field name: temperature
  {
    cdr >> ros_message->temperature;
  }

  // Field name: humidity
  {
    cdr >> ros_message->humidity;
  }

  // Field name: presence
  {
    cdr >> ros_message->presence;
  }

  // Field name: mq2
  {
    cdr >> ros_message->mq2;
  }

  // Field name: val
  {
    cdr >> ros_message->val;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_sensor
size_t get_serialized_size_sensor__msg__DeviceStatus(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _DeviceStatus__ros_msg_type * ros_message = static_cast<const _DeviceStatus__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name temperature
  {
    size_t item_size = sizeof(ros_message->temperature);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name humidity
  {
    size_t item_size = sizeof(ros_message->humidity);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name presence
  {
    size_t item_size = sizeof(ros_message->presence);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name mq2
  {
    size_t item_size = sizeof(ros_message->mq2);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name val
  {
    size_t item_size = sizeof(ros_message->val);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _DeviceStatus__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_sensor__msg__DeviceStatus(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_sensor
size_t max_serialized_size_sensor__msg__DeviceStatus(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;

  // member: temperature
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: humidity
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: presence
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: mq2
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: val
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  return current_alignment - initial_alignment;
}

static size_t _DeviceStatus__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_sensor__msg__DeviceStatus(
    full_bounded, 0);
}


static message_type_support_callbacks_t __callbacks_DeviceStatus = {
  "sensor::msg",
  "DeviceStatus",
  _DeviceStatus__cdr_serialize,
  _DeviceStatus__cdr_deserialize,
  _DeviceStatus__get_serialized_size,
  _DeviceStatus__max_serialized_size
};

static rosidl_message_type_support_t _DeviceStatus__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_DeviceStatus,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, sensor, msg, DeviceStatus)() {
  return &_DeviceStatus__type_support;
}

#if defined(__cplusplus)
}
#endif
