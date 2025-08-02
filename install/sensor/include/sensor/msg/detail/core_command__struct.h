// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from sensor:msg/CoreCommand.idl
// generated code does not contain a copyright notice

#ifndef SENSOR__MSG__DETAIL__CORE_COMMAND__STRUCT_H_
#define SENSOR__MSG__DETAIL__CORE_COMMAND__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in msg/CoreCommand in the package sensor.
typedef struct sensor__msg__CoreCommand
{
  int32_t led;
  int32_t pwm;
} sensor__msg__CoreCommand;

// Struct for a sequence of sensor__msg__CoreCommand.
typedef struct sensor__msg__CoreCommand__Sequence
{
  sensor__msg__CoreCommand * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} sensor__msg__CoreCommand__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SENSOR__MSG__DETAIL__CORE_COMMAND__STRUCT_H_
