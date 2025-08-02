// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from sensor:msg/DeviceStatus.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "sensor/msg/detail/device_status__struct.h"
#include "sensor/msg/detail/device_status__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool sensor__msg__device_status__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[39];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("sensor.msg._device_status.DeviceStatus", full_classname_dest, 38) == 0);
  }
  sensor__msg__DeviceStatus * ros_message = _ros_message;
  {  // temperature
    PyObject * field = PyObject_GetAttrString(_pymsg, "temperature");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->temperature = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // humidity
    PyObject * field = PyObject_GetAttrString(_pymsg, "humidity");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->humidity = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // presence
    PyObject * field = PyObject_GetAttrString(_pymsg, "presence");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->presence = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // mq2
    PyObject * field = PyObject_GetAttrString(_pymsg, "mq2");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->mq2 = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // val
    PyObject * field = PyObject_GetAttrString(_pymsg, "val");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->val = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * sensor__msg__device_status__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of DeviceStatus */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("sensor.msg._device_status");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "DeviceStatus");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  sensor__msg__DeviceStatus * ros_message = (sensor__msg__DeviceStatus *)raw_ros_message;
  {  // temperature
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->temperature);
    {
      int rc = PyObject_SetAttrString(_pymessage, "temperature", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // humidity
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->humidity);
    {
      int rc = PyObject_SetAttrString(_pymessage, "humidity", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // presence
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->presence);
    {
      int rc = PyObject_SetAttrString(_pymessage, "presence", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // mq2
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->mq2);
    {
      int rc = PyObject_SetAttrString(_pymessage, "mq2", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // val
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->val);
    {
      int rc = PyObject_SetAttrString(_pymessage, "val", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
