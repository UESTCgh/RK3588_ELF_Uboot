# generated from rosidl_generator_py/resource/_idl.py.em
# with input from sensor:msg/DeviceStatus.idl
# generated code does not contain a copyright notice


# Import statements for member types

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_DeviceStatus(type):
    """Metaclass of message 'DeviceStatus'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('sensor')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'sensor.msg.DeviceStatus')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__device_status
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__device_status
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__device_status
            cls._TYPE_SUPPORT = module.type_support_msg__msg__device_status
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__device_status

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class DeviceStatus(metaclass=Metaclass_DeviceStatus):
    """Message class 'DeviceStatus'."""

    __slots__ = [
        '_temperature',
        '_humidity',
        '_presence',
        '_mq2',
        '_val',
    ]

    _fields_and_field_types = {
        'temperature': 'float',
        'humidity': 'float',
        'presence': 'int32',
        'mq2': 'int32',
        'val': 'int32',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.temperature = kwargs.get('temperature', float())
        self.humidity = kwargs.get('humidity', float())
        self.presence = kwargs.get('presence', int())
        self.mq2 = kwargs.get('mq2', int())
        self.val = kwargs.get('val', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.temperature != other.temperature:
            return False
        if self.humidity != other.humidity:
            return False
        if self.presence != other.presence:
            return False
        if self.mq2 != other.mq2:
            return False
        if self.val != other.val:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @property
    def temperature(self):
        """Message field 'temperature'."""
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'temperature' field must be of type 'float'"
        self._temperature = value

    @property
    def humidity(self):
        """Message field 'humidity'."""
        return self._humidity

    @humidity.setter
    def humidity(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'humidity' field must be of type 'float'"
        self._humidity = value

    @property
    def presence(self):
        """Message field 'presence'."""
        return self._presence

    @presence.setter
    def presence(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'presence' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'presence' field must be an integer in [-2147483648, 2147483647]"
        self._presence = value

    @property
    def mq2(self):
        """Message field 'mq2'."""
        return self._mq2

    @mq2.setter
    def mq2(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'mq2' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'mq2' field must be an integer in [-2147483648, 2147483647]"
        self._mq2 = value

    @property
    def val(self):
        """Message field 'val'."""
        return self._val

    @val.setter
    def val(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'val' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'val' field must be an integer in [-2147483648, 2147483647]"
        self._val = value
