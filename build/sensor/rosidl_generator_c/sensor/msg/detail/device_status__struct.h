// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from sensor:msg/DeviceStatus.idl
// generated code does not contain a copyright notice

#ifndef SENSOR__MSG__DETAIL__DEVICE_STATUS__STRUCT_H_
#define SENSOR__MSG__DETAIL__DEVICE_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in msg/DeviceStatus in the package sensor.
typedef struct sensor__msg__DeviceStatus
{
  float temperature;
  float humidity;
  int32_t presence;
  int32_t mq2;
  int32_t val;
} sensor__msg__DeviceStatus;

// Struct for a sequence of sensor__msg__DeviceStatus.
typedef struct sensor__msg__DeviceStatus__Sequence
{
  sensor__msg__DeviceStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} sensor__msg__DeviceStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SENSOR__MSG__DETAIL__DEVICE_STATUS__STRUCT_H_
