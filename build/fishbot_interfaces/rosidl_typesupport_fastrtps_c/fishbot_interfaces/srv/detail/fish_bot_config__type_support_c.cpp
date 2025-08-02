// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from fishbot_interfaces:srv/FishBotConfig.idl
// generated code does not contain a copyright notice
#include "fishbot_interfaces/srv/detail/fish_bot_config__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "fishbot_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "fishbot_interfaces/srv/detail/fish_bot_config__struct.h"
#include "fishbot_interfaces/srv/detail/fish_bot_config__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // key, value
#include "rosidl_runtime_c/string_functions.h"  // key, value

// forward declare type support functions


using _FishBotConfig_Request__ros_msg_type = fishbot_interfaces__srv__FishBotConfig_Request;

static bool _FishBotConfig_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _FishBotConfig_Request__ros_msg_type * ros_message = static_cast<const _FishBotConfig_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: key
  {
    const rosidl_runtime_c__String * str = &ros_message->key;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: value
  {
    const rosidl_runtime_c__String * str = &ros_message->value;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _FishBotConfig_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _FishBotConfig_Request__ros_msg_type * ros_message = static_cast<_FishBotConfig_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: key
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->key.data) {
      rosidl_runtime_c__String__init(&ros_message->key);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->key,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'key'\n");
      return false;
    }
  }

  // Field name: value
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->value.data) {
      rosidl_runtime_c__String__init(&ros_message->value);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->value,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'value'\n");
      return false;
    }
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_fishbot_interfaces
size_t get_serialized_size_fishbot_interfaces__srv__FishBotConfig_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _FishBotConfig_Request__ros_msg_type * ros_message = static_cast<const _FishBotConfig_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name key
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->key.size + 1);
  // field.name value
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->value.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _FishBotConfig_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_fishbot_interfaces__srv__FishBotConfig_Request(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_fishbot_interfaces
size_t max_serialized_size_fishbot_interfaces__srv__FishBotConfig_Request(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;

  // member: key
  {
    size_t array_size = 1;

    full_bounded = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: value
  {
    size_t array_size = 1;

    full_bounded = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  return current_alignment - initial_alignment;
}

static size_t _FishBotConfig_Request__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_fishbot_interfaces__srv__FishBotConfig_Request(
    full_bounded, 0);
}


static message_type_support_callbacks_t __callbacks_FishBotConfig_Request = {
  "fishbot_interfaces::srv",
  "FishBotConfig_Request",
  _FishBotConfig_Request__cdr_serialize,
  _FishBotConfig_Request__cdr_deserialize,
  _FishBotConfig_Request__get_serialized_size,
  _FishBotConfig_Request__max_serialized_size
};

static rosidl_message_type_support_t _FishBotConfig_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_FishBotConfig_Request,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, fishbot_interfaces, srv, FishBotConfig_Request)() {
  return &_FishBotConfig_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "fishbot_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "fishbot_interfaces/srv/detail/fish_bot_config__struct.h"
// already included above
// #include "fishbot_interfaces/srv/detail/fish_bot_config__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

// already included above
// #include "rosidl_runtime_c/string.h"  // key, value
// already included above
// #include "rosidl_runtime_c/string_functions.h"  // key, value

// forward declare type support functions


using _FishBotConfig_Response__ros_msg_type = fishbot_interfaces__srv__FishBotConfig_Response;

static bool _FishBotConfig_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _FishBotConfig_Response__ros_msg_type * ros_message = static_cast<const _FishBotConfig_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: key
  {
    const rosidl_runtime_c__String * str = &ros_message->key;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: value
  {
    const rosidl_runtime_c__String * str = &ros_message->value;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _FishBotConfig_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _FishBotConfig_Response__ros_msg_type * ros_message = static_cast<_FishBotConfig_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: key
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->key.data) {
      rosidl_runtime_c__String__init(&ros_message->key);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->key,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'key'\n");
      return false;
    }
  }

  // Field name: value
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->value.data) {
      rosidl_runtime_c__String__init(&ros_message->value);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->value,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'value'\n");
      return false;
    }
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_fishbot_interfaces
size_t get_serialized_size_fishbot_interfaces__srv__FishBotConfig_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _FishBotConfig_Response__ros_msg_type * ros_message = static_cast<const _FishBotConfig_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name key
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->key.size + 1);
  // field.name value
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->value.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _FishBotConfig_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_fishbot_interfaces__srv__FishBotConfig_Response(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_fishbot_interfaces
size_t max_serialized_size_fishbot_interfaces__srv__FishBotConfig_Response(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;

  // member: key
  {
    size_t array_size = 1;

    full_bounded = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: value
  {
    size_t array_size = 1;

    full_bounded = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  return current_alignment - initial_alignment;
}

static size_t _FishBotConfig_Response__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_fishbot_interfaces__srv__FishBotConfig_Response(
    full_bounded, 0);
}


static message_type_support_callbacks_t __callbacks_FishBotConfig_Response = {
  "fishbot_interfaces::srv",
  "FishBotConfig_Response",
  _FishBotConfig_Response__cdr_serialize,
  _FishBotConfig_Response__cdr_deserialize,
  _FishBotConfig_Response__get_serialized_size,
  _FishBotConfig_Response__max_serialized_size
};

static rosidl_message_type_support_t _FishBotConfig_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_FishBotConfig_Response,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, fishbot_interfaces, srv, FishBotConfig_Response)() {
  return &_FishBotConfig_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "fishbot_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "fishbot_interfaces/srv/fish_bot_config.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t FishBotConfig__callbacks = {
  "fishbot_interfaces::srv",
  "FishBotConfig",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, fishbot_interfaces, srv, FishBotConfig_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, fishbot_interfaces, srv, FishBotConfig_Response)(),
};

static rosidl_service_type_support_t FishBotConfig__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &FishBotConfig__callbacks,
  get_service_typesupport_handle_function,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, fishbot_interfaces, srv, FishBotConfig)() {
  return &FishBotConfig__handle;
}

#if defined(__cplusplus)
}
#endif
