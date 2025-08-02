// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from sensor:msg/DeviceStatus.idl
// generated code does not contain a copyright notice

#ifndef SENSOR__MSG__DETAIL__DEVICE_STATUS__BUILDER_HPP_
#define SENSOR__MSG__DETAIL__DEVICE_STATUS__BUILDER_HPP_

#include "sensor/msg/detail/device_status__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace sensor
{

namespace msg
{

namespace builder
{

class Init_DeviceStatus_val
{
public:
  explicit Init_DeviceStatus_val(::sensor::msg::DeviceStatus & msg)
  : msg_(msg)
  {}
  ::sensor::msg::DeviceStatus val(::sensor::msg::DeviceStatus::_val_type arg)
  {
    msg_.val = std::move(arg);
    return std::move(msg_);
  }

private:
  ::sensor::msg::DeviceStatus msg_;
};

class Init_DeviceStatus_mq2
{
public:
  explicit Init_DeviceStatus_mq2(::sensor::msg::DeviceStatus & msg)
  : msg_(msg)
  {}
  Init_DeviceStatus_val mq2(::sensor::msg::DeviceStatus::_mq2_type arg)
  {
    msg_.mq2 = std::move(arg);
    return Init_DeviceStatus_val(msg_);
  }

private:
  ::sensor::msg::DeviceStatus msg_;
};

class Init_DeviceStatus_presence
{
public:
  explicit Init_DeviceStatus_presence(::sensor::msg::DeviceStatus & msg)
  : msg_(msg)
  {}
  Init_DeviceStatus_mq2 presence(::sensor::msg::DeviceStatus::_presence_type arg)
  {
    msg_.presence = std::move(arg);
    return Init_DeviceStatus_mq2(msg_);
  }

private:
  ::sensor::msg::DeviceStatus msg_;
};

class Init_DeviceStatus_humidity
{
public:
  explicit Init_DeviceStatus_humidity(::sensor::msg::DeviceStatus & msg)
  : msg_(msg)
  {}
  Init_DeviceStatus_presence humidity(::sensor::msg::DeviceStatus::_humidity_type arg)
  {
    msg_.humidity = std::move(arg);
    return Init_DeviceStatus_presence(msg_);
  }

private:
  ::sensor::msg::DeviceStatus msg_;
};

class Init_DeviceStatus_temperature
{
public:
  Init_DeviceStatus_temperature()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DeviceStatus_humidity temperature(::sensor::msg::DeviceStatus::_temperature_type arg)
  {
    msg_.temperature = std::move(arg);
    return Init_DeviceStatus_humidity(msg_);
  }

private:
  ::sensor::msg::DeviceStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::sensor::msg::DeviceStatus>()
{
  return sensor::msg::builder::Init_DeviceStatus_temperature();
}

}  // namespace sensor

#endif  // SENSOR__MSG__DETAIL__DEVICE_STATUS__BUILDER_HPP_
