// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from sensor:msg/CoreCommand.idl
// generated code does not contain a copyright notice

#ifndef SENSOR__MSG__DETAIL__CORE_COMMAND__BUILDER_HPP_
#define SENSOR__MSG__DETAIL__CORE_COMMAND__BUILDER_HPP_

#include "sensor/msg/detail/core_command__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace sensor
{

namespace msg
{

namespace builder
{

class Init_CoreCommand_pwm
{
public:
  explicit Init_CoreCommand_pwm(::sensor::msg::CoreCommand & msg)
  : msg_(msg)
  {}
  ::sensor::msg::CoreCommand pwm(::sensor::msg::CoreCommand::_pwm_type arg)
  {
    msg_.pwm = std::move(arg);
    return std::move(msg_);
  }

private:
  ::sensor::msg::CoreCommand msg_;
};

class Init_CoreCommand_led
{
public:
  Init_CoreCommand_led()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CoreCommand_pwm led(::sensor::msg::CoreCommand::_led_type arg)
  {
    msg_.led = std::move(arg);
    return Init_CoreCommand_pwm(msg_);
  }

private:
  ::sensor::msg::CoreCommand msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::sensor::msg::CoreCommand>()
{
  return sensor::msg::builder::Init_CoreCommand_led();
}

}  // namespace sensor

#endif  // SENSOR__MSG__DETAIL__CORE_COMMAND__BUILDER_HPP_
