// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from sensor:msg/CoreCommand.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "sensor/msg/detail/core_command__rosidl_typesupport_introspection_c.h"
#include "sensor/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "sensor/msg/detail/core_command__functions.h"
#include "sensor/msg/detail/core_command__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void CoreCommand__rosidl_typesupport_introspection_c__CoreCommand_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  sensor__msg__CoreCommand__init(message_memory);
}

void CoreCommand__rosidl_typesupport_introspection_c__CoreCommand_fini_function(void * message_memory)
{
  sensor__msg__CoreCommand__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember CoreCommand__rosidl_typesupport_introspection_c__CoreCommand_message_member_array[2] = {
  {
    "led",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sensor__msg__CoreCommand, led),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "pwm",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(sensor__msg__CoreCommand, pwm),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers CoreCommand__rosidl_typesupport_introspection_c__CoreCommand_message_members = {
  "sensor__msg",  // message namespace
  "CoreCommand",  // message name
  2,  // number of fields
  sizeof(sensor__msg__CoreCommand),
  CoreCommand__rosidl_typesupport_introspection_c__CoreCommand_message_member_array,  // message members
  CoreCommand__rosidl_typesupport_introspection_c__CoreCommand_init_function,  // function to initialize message memory (memory has to be allocated)
  CoreCommand__rosidl_typesupport_introspection_c__CoreCommand_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t CoreCommand__rosidl_typesupport_introspection_c__CoreCommand_message_type_support_handle = {
  0,
  &CoreCommand__rosidl_typesupport_introspection_c__CoreCommand_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_sensor
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sensor, msg, CoreCommand)() {
  if (!CoreCommand__rosidl_typesupport_introspection_c__CoreCommand_message_type_support_handle.typesupport_identifier) {
    CoreCommand__rosidl_typesupport_introspection_c__CoreCommand_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &CoreCommand__rosidl_typesupport_introspection_c__CoreCommand_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
