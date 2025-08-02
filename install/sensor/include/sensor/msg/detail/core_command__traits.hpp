// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from sensor:msg/CoreCommand.idl
// generated code does not contain a copyright notice

#ifndef SENSOR__MSG__DETAIL__CORE_COMMAND__TRAITS_HPP_
#define SENSOR__MSG__DETAIL__CORE_COMMAND__TRAITS_HPP_

#include "sensor/msg/detail/core_command__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<sensor::msg::CoreCommand>()
{
  return "sensor::msg::CoreCommand";
}

template<>
inline const char * name<sensor::msg::CoreCommand>()
{
  return "sensor/msg/CoreCommand";
}

template<>
struct has_fixed_size<sensor::msg::CoreCommand>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<sensor::msg::CoreCommand>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<sensor::msg::CoreCommand>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SENSOR__MSG__DETAIL__CORE_COMMAND__TRAITS_HPP_
