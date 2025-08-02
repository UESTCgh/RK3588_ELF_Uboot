// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from fishbot_interfaces:srv/FishBotConfig.idl
// generated code does not contain a copyright notice

#ifndef FISHBOT_INTERFACES__SRV__DETAIL__FISH_BOT_CONFIG__TRAITS_HPP_
#define FISHBOT_INTERFACES__SRV__DETAIL__FISH_BOT_CONFIG__TRAITS_HPP_

#include "fishbot_interfaces/srv/detail/fish_bot_config__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<fishbot_interfaces::srv::FishBotConfig_Request>()
{
  return "fishbot_interfaces::srv::FishBotConfig_Request";
}

template<>
inline const char * name<fishbot_interfaces::srv::FishBotConfig_Request>()
{
  return "fishbot_interfaces/srv/FishBotConfig_Request";
}

template<>
struct has_fixed_size<fishbot_interfaces::srv::FishBotConfig_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<fishbot_interfaces::srv::FishBotConfig_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<fishbot_interfaces::srv::FishBotConfig_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<fishbot_interfaces::srv::FishBotConfig_Response>()
{
  return "fishbot_interfaces::srv::FishBotConfig_Response";
}

template<>
inline const char * name<fishbot_interfaces::srv::FishBotConfig_Response>()
{
  return "fishbot_interfaces/srv/FishBotConfig_Response";
}

template<>
struct has_fixed_size<fishbot_interfaces::srv::FishBotConfig_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<fishbot_interfaces::srv::FishBotConfig_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<fishbot_interfaces::srv::FishBotConfig_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<fishbot_interfaces::srv::FishBotConfig>()
{
  return "fishbot_interfaces::srv::FishBotConfig";
}

template<>
inline const char * name<fishbot_interfaces::srv::FishBotConfig>()
{
  return "fishbot_interfaces/srv/FishBotConfig";
}

template<>
struct has_fixed_size<fishbot_interfaces::srv::FishBotConfig>
  : std::integral_constant<
    bool,
    has_fixed_size<fishbot_interfaces::srv::FishBotConfig_Request>::value &&
    has_fixed_size<fishbot_interfaces::srv::FishBotConfig_Response>::value
  >
{
};

template<>
struct has_bounded_size<fishbot_interfaces::srv::FishBotConfig>
  : std::integral_constant<
    bool,
    has_bounded_size<fishbot_interfaces::srv::FishBotConfig_Request>::value &&
    has_bounded_size<fishbot_interfaces::srv::FishBotConfig_Response>::value
  >
{
};

template<>
struct is_service<fishbot_interfaces::srv::FishBotConfig>
  : std::true_type
{
};

template<>
struct is_service_request<fishbot_interfaces::srv::FishBotConfig_Request>
  : std::true_type
{
};

template<>
struct is_service_response<fishbot_interfaces::srv::FishBotConfig_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // FISHBOT_INTERFACES__SRV__DETAIL__FISH_BOT_CONFIG__TRAITS_HPP_
