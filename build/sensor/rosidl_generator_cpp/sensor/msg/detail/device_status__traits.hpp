// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from sensor:msg/DeviceStatus.idl
// generated code does not contain a copyright notice

#ifndef SENSOR__MSG__DETAIL__DEVICE_STATUS__TRAITS_HPP_
#define SENSOR__MSG__DETAIL__DEVICE_STATUS__TRAITS_HPP_

#include "sensor/msg/detail/device_status__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<sensor::msg::DeviceStatus>()
{
  return "sensor::msg::DeviceStatus";
}

template<>
inline const char * name<sensor::msg::DeviceStatus>()
{
  return "sensor/msg/DeviceStatus";
}

template<>
struct has_fixed_size<sensor::msg::DeviceStatus>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<sensor::msg::DeviceStatus>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<sensor::msg::DeviceStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SENSOR__MSG__DETAIL__DEVICE_STATUS__TRAITS_HPP_
