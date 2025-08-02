// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from sensor:msg/CoreCommand.idl
// generated code does not contain a copyright notice

#ifndef SENSOR__MSG__DETAIL__CORE_COMMAND__FUNCTIONS_H_
#define SENSOR__MSG__DETAIL__CORE_COMMAND__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "sensor/msg/rosidl_generator_c__visibility_control.h"

#include "sensor/msg/detail/core_command__struct.h"

/// Initialize msg/CoreCommand message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * sensor__msg__CoreCommand
 * )) before or use
 * sensor__msg__CoreCommand__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_sensor
bool
sensor__msg__CoreCommand__init(sensor__msg__CoreCommand * msg);

/// Finalize msg/CoreCommand message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_sensor
void
sensor__msg__CoreCommand__fini(sensor__msg__CoreCommand * msg);

/// Create msg/CoreCommand message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * sensor__msg__CoreCommand__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_sensor
sensor__msg__CoreCommand *
sensor__msg__CoreCommand__create();

/// Destroy msg/CoreCommand message.
/**
 * It calls
 * sensor__msg__CoreCommand__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_sensor
void
sensor__msg__CoreCommand__destroy(sensor__msg__CoreCommand * msg);

/// Check for msg/CoreCommand message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_sensor
bool
sensor__msg__CoreCommand__are_equal(const sensor__msg__CoreCommand * lhs, const sensor__msg__CoreCommand * rhs);

/// Copy a msg/CoreCommand message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_sensor
bool
sensor__msg__CoreCommand__copy(
  const sensor__msg__CoreCommand * input,
  sensor__msg__CoreCommand * output);

/// Initialize array of msg/CoreCommand messages.
/**
 * It allocates the memory for the number of elements and calls
 * sensor__msg__CoreCommand__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_sensor
bool
sensor__msg__CoreCommand__Sequence__init(sensor__msg__CoreCommand__Sequence * array, size_t size);

/// Finalize array of msg/CoreCommand messages.
/**
 * It calls
 * sensor__msg__CoreCommand__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_sensor
void
sensor__msg__CoreCommand__Sequence__fini(sensor__msg__CoreCommand__Sequence * array);

/// Create array of msg/CoreCommand messages.
/**
 * It allocates the memory for the array and calls
 * sensor__msg__CoreCommand__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_sensor
sensor__msg__CoreCommand__Sequence *
sensor__msg__CoreCommand__Sequence__create(size_t size);

/// Destroy array of msg/CoreCommand messages.
/**
 * It calls
 * sensor__msg__CoreCommand__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_sensor
void
sensor__msg__CoreCommand__Sequence__destroy(sensor__msg__CoreCommand__Sequence * array);

/// Check for msg/CoreCommand message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_sensor
bool
sensor__msg__CoreCommand__Sequence__are_equal(const sensor__msg__CoreCommand__Sequence * lhs, const sensor__msg__CoreCommand__Sequence * rhs);

/// Copy an array of msg/CoreCommand messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_sensor
bool
sensor__msg__CoreCommand__Sequence__copy(
  const sensor__msg__CoreCommand__Sequence * input,
  sensor__msg__CoreCommand__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // SENSOR__MSG__DETAIL__CORE_COMMAND__FUNCTIONS_H_
