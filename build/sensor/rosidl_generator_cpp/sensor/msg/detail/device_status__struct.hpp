// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from sensor:msg/DeviceStatus.idl
// generated code does not contain a copyright notice

#ifndef SENSOR__MSG__DETAIL__DEVICE_STATUS__STRUCT_HPP_
#define SENSOR__MSG__DETAIL__DEVICE_STATUS__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__sensor__msg__DeviceStatus __attribute__((deprecated))
#else
# define DEPRECATED__sensor__msg__DeviceStatus __declspec(deprecated)
#endif

namespace sensor
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct DeviceStatus_
{
  using Type = DeviceStatus_<ContainerAllocator>;

  explicit DeviceStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->temperature = 0.0f;
      this->humidity = 0.0f;
      this->presence = 0l;
      this->mq2 = 0l;
      this->val = 0l;
    }
  }

  explicit DeviceStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->temperature = 0.0f;
      this->humidity = 0.0f;
      this->presence = 0l;
      this->mq2 = 0l;
      this->val = 0l;
    }
  }

  // field types and members
  using _temperature_type =
    float;
  _temperature_type temperature;
  using _humidity_type =
    float;
  _humidity_type humidity;
  using _presence_type =
    int32_t;
  _presence_type presence;
  using _mq2_type =
    int32_t;
  _mq2_type mq2;
  using _val_type =
    int32_t;
  _val_type val;

  // setters for named parameter idiom
  Type & set__temperature(
    const float & _arg)
  {
    this->temperature = _arg;
    return *this;
  }
  Type & set__humidity(
    const float & _arg)
  {
    this->humidity = _arg;
    return *this;
  }
  Type & set__presence(
    const int32_t & _arg)
  {
    this->presence = _arg;
    return *this;
  }
  Type & set__mq2(
    const int32_t & _arg)
  {
    this->mq2 = _arg;
    return *this;
  }
  Type & set__val(
    const int32_t & _arg)
  {
    this->val = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    sensor::msg::DeviceStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const sensor::msg::DeviceStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<sensor::msg::DeviceStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<sensor::msg::DeviceStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      sensor::msg::DeviceStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<sensor::msg::DeviceStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      sensor::msg::DeviceStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<sensor::msg::DeviceStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<sensor::msg::DeviceStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<sensor::msg::DeviceStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__sensor__msg__DeviceStatus
    std::shared_ptr<sensor::msg::DeviceStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__sensor__msg__DeviceStatus
    std::shared_ptr<sensor::msg::DeviceStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DeviceStatus_ & other) const
  {
    if (this->temperature != other.temperature) {
      return false;
    }
    if (this->humidity != other.humidity) {
      return false;
    }
    if (this->presence != other.presence) {
      return false;
    }
    if (this->mq2 != other.mq2) {
      return false;
    }
    if (this->val != other.val) {
      return false;
    }
    return true;
  }
  bool operator!=(const DeviceStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DeviceStatus_

// alias to use template instance with default allocator
using DeviceStatus =
  sensor::msg::DeviceStatus_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace sensor

#endif  // SENSOR__MSG__DETAIL__DEVICE_STATUS__STRUCT_HPP_
