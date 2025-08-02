// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from sensor:msg/DeviceStatus.idl
// generated code does not contain a copyright notice
#include "sensor/msg/detail/device_status__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
sensor__msg__DeviceStatus__init(sensor__msg__DeviceStatus * msg)
{
  if (!msg) {
    return false;
  }
  // temperature
  // humidity
  // presence
  // mq2
  // val
  return true;
}

void
sensor__msg__DeviceStatus__fini(sensor__msg__DeviceStatus * msg)
{
  if (!msg) {
    return;
  }
  // temperature
  // humidity
  // presence
  // mq2
  // val
}

bool
sensor__msg__DeviceStatus__are_equal(const sensor__msg__DeviceStatus * lhs, const sensor__msg__DeviceStatus * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // temperature
  if (lhs->temperature != rhs->temperature) {
    return false;
  }
  // humidity
  if (lhs->humidity != rhs->humidity) {
    return false;
  }
  // presence
  if (lhs->presence != rhs->presence) {
    return false;
  }
  // mq2
  if (lhs->mq2 != rhs->mq2) {
    return false;
  }
  // val
  if (lhs->val != rhs->val) {
    return false;
  }
  return true;
}

bool
sensor__msg__DeviceStatus__copy(
  const sensor__msg__DeviceStatus * input,
  sensor__msg__DeviceStatus * output)
{
  if (!input || !output) {
    return false;
  }
  // temperature
  output->temperature = input->temperature;
  // humidity
  output->humidity = input->humidity;
  // presence
  output->presence = input->presence;
  // mq2
  output->mq2 = input->mq2;
  // val
  output->val = input->val;
  return true;
}

sensor__msg__DeviceStatus *
sensor__msg__DeviceStatus__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  sensor__msg__DeviceStatus * msg = (sensor__msg__DeviceStatus *)allocator.allocate(sizeof(sensor__msg__DeviceStatus), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(sensor__msg__DeviceStatus));
  bool success = sensor__msg__DeviceStatus__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
sensor__msg__DeviceStatus__destroy(sensor__msg__DeviceStatus * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    sensor__msg__DeviceStatus__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
sensor__msg__DeviceStatus__Sequence__init(sensor__msg__DeviceStatus__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  sensor__msg__DeviceStatus * data = NULL;

  if (size) {
    data = (sensor__msg__DeviceStatus *)allocator.zero_allocate(size, sizeof(sensor__msg__DeviceStatus), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = sensor__msg__DeviceStatus__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        sensor__msg__DeviceStatus__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
sensor__msg__DeviceStatus__Sequence__fini(sensor__msg__DeviceStatus__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      sensor__msg__DeviceStatus__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

sensor__msg__DeviceStatus__Sequence *
sensor__msg__DeviceStatus__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  sensor__msg__DeviceStatus__Sequence * array = (sensor__msg__DeviceStatus__Sequence *)allocator.allocate(sizeof(sensor__msg__DeviceStatus__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = sensor__msg__DeviceStatus__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
sensor__msg__DeviceStatus__Sequence__destroy(sensor__msg__DeviceStatus__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    sensor__msg__DeviceStatus__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
sensor__msg__DeviceStatus__Sequence__are_equal(const sensor__msg__DeviceStatus__Sequence * lhs, const sensor__msg__DeviceStatus__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!sensor__msg__DeviceStatus__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
sensor__msg__DeviceStatus__Sequence__copy(
  const sensor__msg__DeviceStatus__Sequence * input,
  sensor__msg__DeviceStatus__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(sensor__msg__DeviceStatus);
    sensor__msg__DeviceStatus * data =
      (sensor__msg__DeviceStatus *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!sensor__msg__DeviceStatus__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          sensor__msg__DeviceStatus__fini(&data[i]);
        }
        free(data);
        return false;
      }
    }
    output->data = data;
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!sensor__msg__DeviceStatus__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
