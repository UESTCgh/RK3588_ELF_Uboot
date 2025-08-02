// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from sensor:msg/CoreCommand.idl
// generated code does not contain a copyright notice

#ifndef SENSOR__MSG__DETAIL__CORE_COMMAND__STRUCT_HPP_
#define SENSOR__MSG__DETAIL__CORE_COMMAND__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__sensor__msg__CoreCommand __attribute__((deprecated))
#else
# define DEPRECATED__sensor__msg__CoreCommand __declspec(deprecated)
#endif

namespace sensor
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CoreCommand_
{
  using Type = CoreCommand_<ContainerAllocator>;

  explicit CoreCommand_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->led = 0l;
      this->pwm = 0l;
    }
  }

  explicit CoreCommand_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->led = 0l;
      this->pwm = 0l;
    }
  }

  // field types and members
  using _led_type =
    int32_t;
  _led_type led;
  using _pwm_type =
    int32_t;
  _pwm_type pwm;

  // setters for named parameter idiom
  Type & set__led(
    const int32_t & _arg)
  {
    this->led = _arg;
    return *this;
  }
  Type & set__pwm(
    const int32_t & _arg)
  {
    this->pwm = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    sensor::msg::CoreCommand_<ContainerAllocator> *;
  using ConstRawPtr =
    const sensor::msg::CoreCommand_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<sensor::msg::CoreCommand_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<sensor::msg::CoreCommand_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      sensor::msg::CoreCommand_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<sensor::msg::CoreCommand_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      sensor::msg::CoreCommand_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<sensor::msg::CoreCommand_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<sensor::msg::CoreCommand_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<sensor::msg::CoreCommand_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__sensor__msg__CoreCommand
    std::shared_ptr<sensor::msg::CoreCommand_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__sensor__msg__CoreCommand
    std::shared_ptr<sensor::msg::CoreCommand_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CoreCommand_ & other) const
  {
    if (this->led != other.led) {
      return false;
    }
    if (this->pwm != other.pwm) {
      return false;
    }
    return true;
  }
  bool operator!=(const CoreCommand_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CoreCommand_

// alias to use template instance with default allocator
using CoreCommand =
  sensor::msg::CoreCommand_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace sensor

#endif  // SENSOR__MSG__DETAIL__CORE_COMMAND__STRUCT_HPP_
