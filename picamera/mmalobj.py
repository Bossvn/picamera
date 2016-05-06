# vim: set et sw=4 sts=4 fileencoding=utf-8:
#
# Python header conversion
# Copyright (c) 2013-2015 Dave Jones <dave@waveform.org.uk>
#
# Original headers
# Copyright (c) 2012, Broadcom Europe Ltd
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import (
    unicode_literals,
    print_function,
    division,
    absolute_import,
    )

# Make Py2's str equivalent to Py3's
str = type('')

import ctypes as ct
from fractions import Fraction

from . import mmal
from .exc import (
    mmal_check,
    PiCameraValueError,
    PiCameraRuntimeError,
    PiCameraMMALError,
    PiCameraDeprecated,
    )


PARAM_TYPES = {
    mmal.MMAL_PARAMETER_ALGORITHM_CONTROL:           mmal.MMAL_PARAMETER_ALGORITHM_CONTROL_T,
    mmal.MMAL_PARAMETER_ANNOTATE:                    mmal.MMAL_PARAMETER_CAMERA_ANNOTATE_V3_T, # XXX adjust for firmware
    mmal.MMAL_PARAMETER_AUDIO_LATENCY_TARGET:        mmal.MMAL_PARAMETER_AUDIO_LATENCY_TARGET_T,
    mmal.MMAL_PARAMETER_AWB_MODE:                    mmal.MMAL_PARAMETER_AWBMODE_T,
    mmal.MMAL_PARAMETER_BRIGHTNESS:                  mmal.MMAL_RATIONAL_T,
    mmal.MMAL_PARAMETER_BUFFER_REQUIREMENTS:         mmal.MMAL_PARAMETER_BUFFER_REQUIREMENTS_T,
    mmal.MMAL_PARAMETER_CAMERA_BURST_CAPTURE:        mmal.MMAL_BOOL_T,
    mmal.MMAL_PARAMETER_CAMERA_CONFIG:               mmal.MMAL_PARAMETER_CAMERA_CONFIG_T,
    mmal.MMAL_PARAMETER_CAMERA_CUSTOM_SENSOR_CONFIG: ct.c_uint32,
    mmal.MMAL_PARAMETER_CAMERA_INFO:                 mmal.MMAL_PARAMETER_CAMERA_INFO_T,
    mmal.MMAL_PARAMETER_CAMERA_NUM:                  mmal.MMAL_PARAMETER_INT32_T,
    mmal.MMAL_PARAMETER_CAMERA_SETTINGS:             mmal.MMAL_PARAMETER_CAMERA_SETTINGS_T,
    mmal.MMAL_PARAMETER_CAPTURE:                     mmal.MMAL_BOOL_T,
    mmal.MMAL_PARAMETER_CAPTURE_MODE:                mmal.MMAL_PARAMETER_CAPTUREMODE_T,
    mmal.MMAL_PARAMETER_CAPTURE_STATS_PASS:          mmal.MMAL_BOOL_T,
    mmal.MMAL_PARAMETER_CHANGE_EVENT_REQUEST:        mmal.MMAL_PARAMETER_CHANGE_EVENT_REQUEST_T,
    mmal.MMAL_PARAMETER_CLOCK_DISCONT_THRESHOLD:     mmal.MMAL_PARAMETER_CLOCK_DISCONT_THRESHOLD_T,
    mmal.MMAL_PARAMETER_CLOCK_LATENCY:               mmal.MMAL_PARAMETER_CLOCK_LATENCY_T,
    mmal.MMAL_PARAMETER_CLOCK_REQUEST_THRESHOLD:     mmal.MMAL_PARAMETER_CLOCK_REQUEST_THRESHOLD_T,
    mmal.MMAL_PARAMETER_CLOCK_UPDATE_THRESHOLD:      mmal.MMAL_PARAMETER_CLOCK_UPDATE_THRESHOLD_T,
    mmal.MMAL_PARAMETER_COLOUR_EFFECT:               mmal.MMAL_PARAMETER_COLOURFX_T,
    mmal.MMAL_PARAMETER_CONTRAST:                    mmal.MMAL_RATIONAL_T,
    mmal.MMAL_PARAMETER_CORE_STATISTICS:             mmal.MMAL_PARAMETER_CORE_STATISTICS_T,
    mmal.MMAL_PARAMETER_CUSTOM_AWB_GAINS:            mmal.MMAL_PARAMETER_AWB_GAINS_T,
    mmal.MMAL_PARAMETER_DISPLAYREGION:               mmal.MMAL_DISPLAYREGION_T,
    mmal.MMAL_PARAMETER_DYNAMIC_RANGE_COMPRESSION:   mmal.MMAL_PARAMETER_DRC_T,
    mmal.MMAL_PARAMETER_ENABLE_RAW_CAPTURE:          mmal.MMAL_BOOL_T,
    mmal.MMAL_PARAMETER_EXIF:                        mmal.MMAL_PARAMETER_EXIF_T,
    mmal.MMAL_PARAMETER_EXP_METERING_MODE:           mmal.MMAL_PARAMETER_EXPOSUREMETERINGMODE_T,
    mmal.MMAL_PARAMETER_EXPOSURE_COMP:               ct.c_int32,
    mmal.MMAL_PARAMETER_EXPOSURE_MODE:               mmal.MMAL_PARAMETER_EXPOSUREMODE_T,
    mmal.MMAL_PARAMETER_FIELD_OF_VIEW:               mmal.MMAL_PARAMETER_FIELD_OF_VIEW_T,
    mmal.MMAL_PARAMETER_FLASH:                       mmal.MMAL_PARAMETER_FLASH_T,
    mmal.MMAL_PARAMETER_FLASH_SELECT:                mmal.MMAL_PARAMETER_FLASH_SELECT_T,
    mmal.MMAL_PARAMETER_FLICKER_AVOID:               mmal.MMAL_PARAMETER_FLICKERAVOID_T,
    mmal.MMAL_PARAMETER_FOCUS:                       mmal.MMAL_PARAMETER_FOCUS_T,
    mmal.MMAL_PARAMETER_FOCUS_REGIONS:               mmal.MMAL_PARAMETER_FOCUS_REGIONS_T,
    mmal.MMAL_PARAMETER_FOCUS_STATUS:                mmal.MMAL_PARAMETER_FOCUS_STATUS_T,
    mmal.MMAL_PARAMETER_FPS_RANGE:                   mmal.MMAL_PARAMETER_FPS_RANGE_T,
    mmal.MMAL_PARAMETER_IMAGE_EFFECT:                mmal.MMAL_PARAMETER_IMAGEFX_T,
    mmal.MMAL_PARAMETER_IMAGE_EFFECT_PARAMETERS:     mmal.MMAL_PARAMETER_IMAGEFX_PARAMETERS_T,
    mmal.MMAL_PARAMETER_INPUT_CROP:                  mmal.MMAL_PARAMETER_INPUT_CROP_T,
    mmal.MMAL_PARAMETER_INTRAPERIOD:                 mmal.MMAL_PARAMETER_UINT32_T,
    mmal.MMAL_PARAMETER_ISO:                         ct.c_uint32,
    mmal.MMAL_PARAMETER_JPEG_Q_FACTOR:               ct.c_uint32,
    mmal.MMAL_PARAMETER_LOGGING:                     mmal.MMAL_PARAMETER_LOGGING_T,
    mmal.MMAL_PARAMETER_MEM_USAGE:                   mmal.MMAL_PARAMETER_MEM_USAGE_T,
    mmal.MMAL_PARAMETER_MIRROR:                      mmal.MMAL_PARAMETER_MIRROR_T,
    mmal.MMAL_PARAMETER_PRIVACY_INDICATOR:           mmal.MMAL_PARAMETER_PRIVACY_INDICATOR_T,
    mmal.MMAL_PARAMETER_PROFILE:                     mmal.MMAL_PARAMETER_VIDEO_PROFILE_T,
    mmal.MMAL_PARAMETER_REDEYE:                      mmal.MMAL_PARAMETER_REDEYE_T,
    mmal.MMAL_PARAMETER_ROTATION:                    ct.c_int32,
    mmal.MMAL_PARAMETER_SATURATION:                  mmal.MMAL_RATIONAL_T,
    mmal.MMAL_PARAMETER_SEEK:                        mmal.MMAL_PARAMETER_SEEK_T,
    mmal.MMAL_PARAMETER_SENSOR_INFORMATION:          mmal.MMAL_PARAMETER_SENSOR_INFORMATION_T,
    mmal.MMAL_PARAMETER_SHARPNESS:                   mmal.MMAL_RATIONAL_T,
    mmal.MMAL_PARAMETER_SHUTTER_SPEED:               ct.c_uint32,
    mmal.MMAL_PARAMETER_STATISTICS:                  mmal.MMAL_PARAMETER_STATISTICS_T,
    mmal.MMAL_PARAMETER_STEREOSCOPIC_MODE:           mmal.MMAL_PARAMETER_STEREOSCOPIC_MODE_T,
    mmal.MMAL_PARAMETER_STILLS_DENOISE:              mmal.MMAL_BOOL_T,
    mmal.MMAL_PARAMETER_THUMBNAIL_CONFIGURATION:     mmal.MMAL_PARAMETER_THUMBNAIL_CONFIG_T,
    mmal.MMAL_PARAMETER_VIDEO_DENOISE:               mmal.MMAL_BOOL_T,
    mmal.MMAL_PARAMETER_VIDEO_ENCODE_INITIAL_QUANT:  mmal.MMAL_PARAMETER_UINT32_T,
    mmal.MMAL_PARAMETER_VIDEO_ENCODE_INLINE_HEADER:  mmal.MMAL_BOOL_T,
    mmal.MMAL_PARAMETER_VIDEO_ENCODE_INLINE_VECTORS: mmal.MMAL_BOOL_T,
    mmal.MMAL_PARAMETER_VIDEO_ENCODE_MAX_QUANT:      mmal.MMAL_PARAMETER_UINT32_T,
    mmal.MMAL_PARAMETER_VIDEO_ENCODE_MIN_QUANT:      mmal.MMAL_PARAMETER_UINT32_T,
    mmal.MMAL_PARAMETER_VIDEO_ENCODE_SEI_ENABLE:     mmal.MMAL_BOOL_T,
    mmal.MMAL_PARAMETER_VIDEO_IMMUTABLE_INPUT:       mmal.MMAL_BOOL_T,
    mmal.MMAL_PARAMETER_VIDEO_INTRA_REFRESH:         mmal.MMAL_PARAMETER_VIDEO_INTRA_REFRESH_T,
    mmal.MMAL_PARAMETER_VIDEO_STABILISATION:         mmal.MMAL_BOOL_T,
    mmal.MMAL_PARAMETER_ZERO_SHUTTER_LAG:            mmal.MMAL_PARAMETER_ZEROSHUTTERLAG_T,
    }


class PiCameraFraction(Fraction):
    """
    Extends :class:`~fractions.Fraction` to act as a (numerator, denominator)
    tuple when required.
    """
    def __len__(self):
        warnings.warn(
            PiCameraDeprecated(
                'Accessing framerate as a tuple is deprecated; this value is '
                'now a Fraction, so you can query the numerator and '
                'denominator properties directly, convert to an int or float, '
                'or perform arithmetic operations and comparisons directly'))
        return 2

    def __getitem__(self, index):
        warnings.warn(
            PiCameraDeprecated(
                'Accessing framerate as a tuple is deprecated; this value is '
                'now a Fraction, so you can query the numerator and '
                'denominator properties directly, convert to an int or float, '
                'or perform arithmetic operations and comparisons directly'))
        if index == 0:
            return self.numerator
        elif index == 1:
            return self.denominator
        else:
            raise IndexError('invalid index %d' % index)

    def __contains__(self, value):
        return value in (self.numerator, self.denominator)


def to_rational(value):
    """
    Converts a value to a numerator, denominator tuple.

    Given a :class:`int`, :class:`float`, or :class:`~fractions.Fraction`
    instance, returns the value as a `(numerator, denominator)` tuple where the
    numerator and denominator are integer values.
    """
    try:
        # int, long, or fraction
        n, d = value.numerator, value.denominator
    except AttributeError:
        try:
            # float
            n, d = value.as_integer_ratio()
        except AttributeError:
            try:
                # tuple
                n, d = value
                warnings.warn(
                    PiCameraDeprecated(
                        "Setting framerate or gains as a tuple is deprecated; "
                        "please use one of Python's many numeric classes like "
                        "int, float, Decimal, or Fraction instead"))
            except (TypeError, ValueError):
                # try and convert anything else (e.g. Decimal) to a Fraction
                value = Fraction(value)
                n, d = value.numerator, value.denominator
    # Ensure denominator is reasonable
    if d == 0:
        raise PiCameraValueError("Denominator cannot be 0")
    elif d > 65536:
        f = Fraction(n, d).limit_denominator(65536)
        n, d = f.numerator, f.denominator
    return n, d


def to_fraction(rational):
    """
    Converts an MMAL_RATIONAL_T to a Fraction instance.
    """
    return Fraction(rational.num, rational.den)


class MMALComponent(object):
    """
    Represents a generic MMAL component. The component type is specified as a
    string to the constructor along with the opaque sub-formats to apply to the
    input and output ports respectively (the length of these sequences are also
    checked against the number of inputs and outputs defined by the component).
    """
    def __init__(
            self, component_type, input_count, output_count):
        super(MMALComponent, self).__init__()
        self._component = ct.POINTER(mmal.MMAL_COMPONENT_T)()
        mmal_check(
            mmal.mmal_component_create(component_type, self._component),
            prefix="Failed to create MMAL component %s" % component_type)
        if self._component[0].input_num != input_count:
            raise PiCameraRuntimeError(
                'Expected %d inputs but found %d on component %s' % (
                    input_count,
                    self._components[0].input_num,
                    component_type))
        if self._component[0].output_num != output_count:
            raise PiCameraRuntimeError(
                'Expected %d inputs but found %d on component %s' % (
                    output_count,
                    self._components[0].input_num,
                    component_type))
        self._control = MMALControlPort(self._component[0].control)
        port_class = {
            mmal.MMAL_ES_TYPE_UNKNOWN:    MMALPort,
            mmal.MMAL_ES_TYPE_CONTROL:    MMALControlPort,
            mmal.MMAL_ES_TYPE_VIDEO:      MMALVideoPort,
            mmal.MMAL_ES_TYPE_AUDIO:      MMALAudioPort,
            mmal.MMAL_ES_TYPE_SUBPICTURE: MMALSubPicturePort,
            }
        self._inputs = tuple(
            port_class[self._component[0].input[n][0].format[0].type](
                self._component[0].input[n])
            for n in range(input_count))
        self._outputs = tuple(
            port_class[self._component[0].output[n][0].format[0].type](
                self._component[0].output[n])
            for n in range(output_count))

    def close(self):
        """
        Close the component and release all its resources. After this is
        called, most methods will raise exceptions if called.
        """
        if self._component:
            # ensure we free any pools associated with input/output ports
            for output in self.outputs:
                output.disable()
            for input in self.inputs:
                input.disable()
            mmal.mmal_component_destroy(self._component)
            self._component = None
            self._inputs = ()
            self._outputs = ()
            self._control = None

    @property
    def name(self):
        return self._component[0].name

    @property
    def control(self):
        """
        The :class:`MMALControlPort` control port of the component which can be
        used to configure most aspects of the component's behaviour.
        """
        return self._control

    @property
    def inputs(self):
        """
        A sequence of :class:`MMALPort` objects representing the inputs
        of the component.
        """
        return self._inputs

    @property
    def outputs(self):
        """
        A sequence of :class:`MMALPort` objects representing the outputs
        of the component.
        """
        return self._outputs

    def _get_enabled(self):
        return bool(self._component[0].is_enabled)
    def _set_enabled(self, value):
        if value:
            mmal_check(
                mmal.mmal_component_enable(self._component),
                prefix="Failed to enable component")
        else:
            mmal_check(
                mmal.mmal_component_disable(self._component),
                prefix="Failed to disable component")
    enabled = property(
        # use lambda trick to enable overriding _get_enabled, _set_enabled
        lambda self: self._get_enabled(),
        lambda self, value: self._set_enabled(value),
        doc="""\
        Retrieves or sets whether the component is currently enabled. When a
        component is disabled it does not produce or consume data. Components
        may be implicitly enabled by downstream components.
        """)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def __repr__(self):
        if self._component:
            return '<MMALComponent "%s": %d inputs %d outputs>' % (
                self.name, len(self.inputs), len(self.outputs))
        else:
            return '<MMALComponent closed>'


def _control_callback(port, buf):
    port = ct.cast(port[0].userdata, ct.POINTER(ct.py_object))[0]
    buf = MMALBuffer(buf)
    try:
        if port._callback:
            port._callback(port, buf)
    finally:
        buf.release()


def _data_callback(port, buf):
    port = ct.cast(port[0].userdata, ct.POINTER(ct.py_object))[0]
    buf = MMALBuffer(buf)
    try:
        if port._callback:
            if port._callback(port, buf):
                port._callback = None
    finally:
        buf.release()
        if port._callback:
            port._pool.send_buffer(port)


class MMALControlPort(object):
    """
    Represents an MMAL port with properties to configure the port's parameters.
    """
    def __init__(self, port):
        super(MMALControlPort, self).__init__()
        self._port = port
        self._params = MMALPortParams(port)
        self._callback = None

    @property
    def enabled(self):
        """
        Returns a :class:`bool` indicating whether the port is currently
        enabled. Unlike other classes, this is a read-only property. Use
        :meth:`enable` and :meth:`disable` to modify the value.
        """
        return bool(self._port[0].is_enabled)

    def enable(self, callback=None):
        """
        Enable the port with the specified callback function (this must be
        ``None`` for connected ports, and a callable for disconnected ports).

        The callback function must accept two parameters which will be this
        :class:`MMALControlPort` (or descendent) and an :class:`MMALBuffer`
        instance. Any return value will be ignored.
        """
        if not self.enabled:
            if callback:
                self._callback = callback
                self._port[0].userdata = ct.cast(
                    ct.pointer(ct.py_object(self)),
                    ct.c_void_p)
                wrapper = mmal.MMAL_PORT_BH_CB_T(_control_callback)
            else:
                wrapper = None
            mmal_check(
                mmal.mmal_port_enable(self._port, wrapper),
                prefix="Unable to enable port %s" % self.name)

    def disable(self):
        """
        Disable the port.
        """
        self._callback = None
        if self.enabled:
            mmal_check(
                mmal.mmal_port_disable(self._port),
                prefix="Unable to disable port %s" % self.name)

    def send_buffer(self, buf):
        """
        Send the *buf* :class:`MMALBuffer` to the port.
        """
        mmal_check(
            mmal.mmal_port_send_buffer(self._port, buf._buf),
            prefix="unable to send the buffer to port %s" % self.name)

    def flush(self):
        """
        Flush the port.
        """
        mmal_check(
            mmal.mmal_port_flush(self._port),
            prefix="Unable to flush port %s" % self.name)

    @property
    def name(self):
        return self._port[0].name

    @property
    def params(self):
        """
        The configurable parameters for the port. This is presented as a
        mutable mapping of parameter numbers to values, implemented by the
        :class:`MMALPortParams` class.
        """
        return self._params

    def __repr__(self):
        if self._port:
            return '<MMALControlPort "%s">' % self.name
        else:
            return '<MMALControlPort closed>'


class MMALPort(MMALControlPort):
    """
    Represents an MMAL port with properties to configure and update the port's
    format. This is the base class of :class:`MMALVideoPort`,
    :class:`MMALAudioPort`, and :class:`MMALSubPicturePort`.
    """
    def __init__(self, port, opaque_subformat='OPQV'):
        super(MMALPort, self).__init__(port)
        self.opaque_subformat = opaque_subformat
        self._pool = None
        self._callback = None

    def _get_opaque_subformat(self):
        return self._opaque_subformat
    def _set_opaque_subformat(self, value):
        self._opaque_subformat = value
    opaque_subformat = property(
        _get_opaque_subformat, _set_opaque_subformat, doc="""\
        Retrieves or sets the opaque sub-format that the port speaks. While
        most formats (I420, RGBA, etc.) mean one thing, the opaque format is
        special; different ports produce different sorts of data when
        configured for OPQV format. This property stores a string which
        uniquely identifies what the associated port means for OPQV format.

        If the port does not support opaque format at all, set this property to
        ``None``.

        :class:`MMALConnection` uses this information when negotiating formats
        for a connection between two ports.
        """)

    def _get_format(self):
        # Workaround: swap RGB3 and BGR3 formats (the firmware has them
        # backwards)
        result = self._port[0].format[0].encoding
        return {
            mmal.MMAL_ENCODING_RGB24: mmal.MMAL_ENCODING_BGR24,
            mmal.MMAL_ENCODING_BGR24: mmal.MMAL_ENCODING_RGB24,
            }.get(result, result)
    def _set_format(self, value):
        value = {
            mmal.MMAL_ENCODING_RGB24: mmal.MMAL_ENCODING_BGR24,
            mmal.MMAL_ENCODING_BGR24: mmal.MMAL_ENCODING_RGB24,
            }.get(value, value)
        self._port[0].format[0].encoding = value
        if value == mmal.MMAL_ENCODING_OPAQUE:
            self._port[0].format[0].encoding_variant = mmal.MMAL_ENCODING_I420
        else:
            self._port[0].format[0].encoding_variant = value
    format = property(_get_format, _set_format, doc="""\
        Retrieves or sets the encoding format of the port. Setting this
        attribute implicitly sets the encoding variant to a sensible value
        (I420 in the case of OPAQUE).

        After setting this attribute, call :meth:`commit` to make the changes
        effective.
        """)

    def _get_bitrate(self):
        return self._port[0].format[0].bitrate
    def _set_bitrate(self, value):
        self._port[0].format[0].bitrate = value
    bitrate = property(_get_bitrate, _set_bitrate, doc="""\
        Retrieves or sets the bitrate limit for the port's format.
        """)

    def copy_from(self, source):
        """
        Copies the port's :attr:`format` from the *source*
        :class:`MMALControlPort`.
        """
        mmal.mmal_format_copy(self._port[0].format, source._port[0].format)

    def commit(self):
        """
        Commits the port's configuration and automatically updates the number
        and size of associated buffers. This is typically called after
        adjusting the port's format and/or associated settings (like width and
        height for video ports).
        """
        mmal_check(
            mmal.mmal_port_format_commit(self._port),
            prefix="Format couldn't be set on port %s" % self.name)
        # Workaround: Unfortunately, there is an upstream issue with the
        # buffer_num_recommended which means it can't currently be used (see
        # discussion in raspberrypi/userland#167). There's another upstream
        # issue with buffer_num_min which means we need to guard against 0
        # values...
        self._port[0].buffer_num = max(1, self._port[0].buffer_num_min)
        # Workaround: There is a bug in the MJPEG encoder that causes a
        # deadlock if the FIFO is full on shutdown. Increasing the encoder
        # buffer size makes this less likely to happen. See
        # raspberrypi/userland#208
        if self._port[0].format[0].encoding == mmal.MMAL_ENCODING_MJPEG:
            self._port[0].buffer_size = max(512 * 1024, self._port[0].buffer_size_recommended)
        else:
            self._port[0].buffer_size = self._port[0].buffer_size_recommended

    @property
    def pool(self):
        """
        Returns the :class:`MMALPool` associated with the buffer, if any.
        """
        return self._pool

    @property
    def buffer_count(self):
        return self._port[0].buffer_num

    @property
    def buffer_size(self):
        return self._port[0].buffer_size

    def enable(self, callback=None):
        """
        Enable the port with the specified callback function (this must be
        ``None`` for connected ports, and a callable for disconnected ports).

        The callback function must accept two parameters which will be this
        :class:`MMALControlPort` (or descendent) and an :class:`MMALBuffer`
        instance. The callback should return ``True`` when its processing is
        complete, and ``False`` otherwise.
        """
        if not self.enabled:
            if callback:
                assert self._pool is None
                try:
                    self._callback = callback
                    self._pool = MMALPool.for_port(self)
                    self._port[0].userdata = ct.cast(
                        ct.pointer(ct.py_object(self)),
                        ct.c_void_p)
                    wrapper = mmal.MMAL_PORT_BH_CB_T(_data_callback)
                    mmal_check(
                        mmal.mmal_port_enable(self._port, wrapper),
                        prefix="Unable to enable port %s" % self.name)
                    self._pool.send_all_buffers(self)
                except:
                    self._pool.close()
                    self._pool = None
            else:
                super(MMALPort, self).enable()

    def disable(self):
        """
        Disable the port.
        """
        super(MMALPort, self).disable()
        if self._pool:
            self._pool.close()
            self._pool = None

    def __repr__(self):
        if self._port:
            return '<MMALPort "%s": format=%r buffers=%dx%d>' % (
                self.name, self.format, self.buffer_count, self.buffer_size)
        else:
            return '<MMALPort closed>'


class MMALVideoPort(MMALPort):
    """
    Represents an MMAL port used to pass video data.
    """

    def _get_width(self):
        return self._port[0].format[0].es[0].video.crop.width
    def _set_width(self, value):
        video = self._port[0].format[0].es[0].video
        video.width = mmal.VCOS_ALIGN_UP(value, 32)
        video.crop.width = value
    width = property(_get_width, _set_width, doc="""\
        Retrieves or sets the width of the port's video frames in pixels.

        After setting this attribute, call :meth:`commit` to make the changes
        effective.
        """)

    def _get_height(self):
        return self._port[0].format[0].es[0].video.crop.height
    def _set_height(self, value):
        video = self._port[0].format[0].es[0].video
        video.height = mmal.VCOS_ALIGN_UP(value, 16)
        video.crop.height = value
    height = property(_get_height, _set_height, doc="""\
        Retrieves or sets the height of the port's video frames in pixels.

        After setting this attribute, call :meth:`commit` to make the changes
        effective.
        """)

    def _get_framerate(self):
        video = self._port[0].format[0].es[0].video
        try:
            return Fraction(
                video.frame_rate.num,
                video.frame_rate.den)
        except ZeroDivisionError:
            return Fraction(0, 1)
    def _set_framerate(self, value):
        n, d = to_rational(value)
        video = self._port[0].format[0].es[0].video
        video.frame_rate.num = n
        video.frame_rate.den = d
    framerate = property(_get_framerate, _set_framerate, doc="""\
        Retrieves or sets the framerate of the port's video frames in fps.

        After setting this attribute, call :meth:`commit` to make the changes
        effective.
        """)

    def __repr__(self):
        if self._port:
            return '<MMALVideoPort "%s": format=%r buffers=%dx%d frames=%dx%d@%sfps>' % (
                self.name, self.format, self._port[0].buffer_num,
                self._port[0].buffer_size, self.width, self.height,
                self.framerate)
        else:
            return '<MMALVideoPort closed>'


class MMALAudioPort(MMALPort):
    """
    Represents an MMAL port used to pass audio data.
    """

    def __repr__(self):
        if self._port:
            return '<MMALAudioPort "%s": format=%r buffers=%dx%d>' % (
                self.name, self.format, self._port[0].buffer_num,
                self._port[0].buffer_size)
        else:
            return '<MMALAudioPort closed>'


class MMALSubPicturePort(MMALPort):
    """
    Represents an MMAL port used to pass sub-picture (caption) data.
    """

    def __repr__(self):
        if self._port:
            return '<MMALSubPicturePort "%s": format=%r buffers=%dx%d>' % (
                self.name, self.format, self._port[0].buffer_num,
                self._port[0].buffer_size)
        else:
            return '<MMALSubPicturePort closed>'


class MMALPortParams(object):
    """
    Represents the parameters of an MMAL port. This class implements the
    :attr:`MMALControlPort.params` attribute.

    Internally, the class understands how to convert certain structures to more
    common Python data-types. For example, parameters that expect an
    MMAL_RATIONAL_T type will return and accept Python's
    :class:`~fractions.Fraction` class (or any other numeric types), while
    parameters that expect an MMAL_BOOL_T type will treat anything as a truthy
    value. Parameters that expect the MMAL_PARAMETER_STRING_T structure will be
    treated as plain strings, and likewise MMAL_PARAMETER_INT32_T and similar
    structures will be treated as plain ints.

    Parameters that expect more complex structures will return and expect
    those structures verbatim.
    """
    def __init__(self, port):
        self._port = port

    def __getitem__(self, key):
        dtype = PARAM_TYPES[key]
        func = {
            mmal.MMAL_RATIONAL_T: mmal.mmal_port_parameter_get_rational,
            mmal.MMAL_BOOL_T:     mmal.mmal_port_parameter_get_boolean,
            ct.c_uint64:          mmal.mmal_port_parameter_get_uint64,
            ct.c_int64:           mmal.mmal_port_parameter_get_int64,
            ct.c_uint32:          mmal.mmal_port_parameter_get_uint32,
            ct.c_int32:           mmal.mmal_port_parameter_get_int32,
            }.get(dtype, mmal.mmal_port_parameter_get)
        conv = {
            mmal.MMAL_RATIONAL_T:           lambda v: Fraction(v.num, v.den),
            mmal.MMAL_PARAMETER_RATIONAL_T: lambda v: Fraction(v.value.num, v.value.den),
            mmal.MMAL_BOOL_T:               lambda v: v.value != mmal.MMAL_FALSE,
            mmal.MMAL_PARAMETER_BOOLEAN_T:  lambda v: v.enable != mmal.MMAL_FALSE,
            mmal.MMAL_PARAMETER_INT32_T:    lambda v: v.value,
            mmal.MMAL_PARAMETER_INT64_T:    lambda v: v.value,
            mmal.MMAL_PARAMETER_UINT32_T:   lambda v: v.value,
            mmal.MMAL_PARAMETER_UINT64_T:   lambda v: v.value,
            mmal.MMAL_PARAMETER_STRING_T:   lambda v: v.str.decode('ascii'),
            ct.c_uint64:                    lambda v: v.value,
            ct.c_int64:                     lambda v: v.value,
            ct.c_uint32:                    lambda v: v.value,
            ct.c_int32:                     lambda v: v.value,
            }.get(dtype, lambda v: v)
        if func == mmal.mmal_port_parameter_get:
            result = dtype(
                mmal.MMAL_PARAMETER_HEADER_T(key, ct.sizeof(dtype))
                )
            mmal_check(
                func(self._port, result.hdr),
                prefix="Failed to get parameter %d" % key)
        else:
            result = dtype()
            mmal_check(
                func(self._port, key, result),
                prefix="Failed to get parameter %d" % key)
        return conv(result)

    def __setitem__(self, key, value):
        dtype = PARAM_TYPES[key]
        func = {
            mmal.MMAL_RATIONAL_T: mmal.mmal_port_parameter_set_rational,
            mmal.MMAL_BOOL_T:     mmal.mmal_port_parameter_set_boolean,
            ct.c_uint64:          mmal.mmal_port_parameter_set_uint64,
            ct.c_int64:           mmal.mmal_port_parameter_set_int64,
            ct.c_uint32:          mmal.mmal_port_parameter_set_uint32,
            ct.c_int32:           mmal.mmal_port_parameter_set_int32,
            }.get(dtype, mmal.mmal_port_parameter_set)
        conv = {
            mmal.MMAL_RATIONAL_T:           lambda v: mmal.MMAL_RATIONAL_T(*to_rational(v)),
            mmal.MMAL_PARAMETER_RATIONAL_T: lambda v: mmal.MMAL_PARAMETER_RATIONAL_T(
                mmal.MMAL_PARAMETER_HEADER_T(
                    key, ct.sizeof(mmal.MMAL_PARAMETER_RATIONAL_T)),
                mmal.MMAL_RATIONAL_T(*to_rational(v))),
            mmal.MMAL_PARAMETER_BOOLEAN_T:  lambda v: mmal.MMAL_PARAMETER_BOOLEAN_T(
                mmal.MMAL_PARAMETER_HEADER_T(
                    key, ct.sizeof(mmal.MMAL_PARAMETER_BOOLEAN_T)),
                bool(value)),
            mmal.MMAL_BOOL_T:               lambda v: mmal.MMAL_TRUE if v else mmal.MMAL_FALSE,
            mmal.MMAL_PARAMETER_INT32_T:    lambda v: mmal.MMAL_PARAMETER_INT32_T(
                mmal.MMAL_PARAMETER_HEADER_T(
                    key, ct.sizeof(mmal.MMAL_PARAMETER_INT32_T)),
                v),
            mmal.MMAL_PARAMETER_INT64_T:    lambda v: mmal.MMAL_PARAMETER_INT64_T(
                mmal.MMAL_PARAMETER_HEADER_T(
                    key, ct.sizeof(mmal.MMAL_PARAMETER_INT64_T)),
                v),
            mmal.MMAL_PARAMETER_UINT32_T:   lambda v: mmal.MMAL_PARAMETER_UINT32_T(
                mmal.MMAL_PARAMETER_HEADER_T(
                    key, ct.sizeof(mmal.MMAL_PARAMETER_UINT32_T)),
                v),
            mmal.MMAL_PARAMETER_UINT64_T:   lambda v: mmal.MMAL_PARAMETER_UINT64_T(
                mmal.MMAL_PARAMETER_HEADER_T(
                    key, ct.sizeof(mmal.MMAL_PARAMETER_UINT64_T)),
                v),
            mmal.MMAL_PARAMETER_STRING_T:   lambda v: mmal.MMAL_PARAMETER_STRING_T(
                mmal.MMAL_PARAMETER_HEADER_T(
                    key, ct.sizeof(mmal.MMAL_PARAMETER_STRING_T)),
                v.encode('ascii')),
            }.get(dtype, lambda v: v)
        if func == mmal.mmal_port_parameter_set:
            mp = conv(value)
            assert mp.hdr.id == key
            assert mp.hdr.size >= ct.sizeof(dtype)
            mmal_check(
                func(self._port, mp.hdr),
                prefix="Failed to set parameter %d to %r" % (key, value))
        else:
            mmal_check(
                func(self._port, key, conv(value)),
                prefix="Failed to set parameter %d to %r" % (key, value))


class MMALBuffer(object):
    """
    Represents an MMAL buffer header. This is usually constructed from the
    buffer header pointer and is largely supplied simply to make working with
    the buffer's data a bit simpler; accessing the :attr:`data` attribute
    implicitly locks the buffer's memory and returns the data as a bytes
    string.
    """
    def __init__(self, buf):
        self._buf = buf

    @property
    def flags(self):
        return self._buf[0].flags

    @property
    def pts(self):
        return self._buf[0].pts

    @property
    def dts(self):
        return self._buf[0].dts

    @property
    def size(self):
        """
        Returns the length of the buffer's data area in bytes. This will be
        greater than or equal to :attr:`length` and is fixed in value.
        """
        return self._buf[0].alloc_size

    @property
    def length(self):
        """
        Returns the length of data held in the buffer. This is equal to calling
        :func:`len` on :attr:`data` but faster (as retrieving the buffer's data
        requires memory locks in certain cases).
        """
        return self._buf[0].length

    @property
    def data(self):
        # dirty hack; we could do pointer arithmetic with offset but it's
        # rather long-winded in Python and this method needs to be *fast*
        assert self._buf[0].offset == 0
        mmal_check(
            mmal.mmal_buffer_header_mem_lock(self._buf),
            prefix='unable to lock buffer header memory')
        try:
            return ct.string_at(self._buf[0].data, self._buf[0].length)
        finally:
            mmal.mmal_buffer_header_mem_unlock(self._buf)

    def update(self, data):
        """
        Overwrites the :attr:`data` in the buffer. The *data* parameter is an
        object supporting the buffer protocol which contains up to
        :attr:`alloc_size` bytes.
        """
        bp = ct.c_uint8 * len(data)
        try:
            sp = bp.from_buffer(data)
        except TypeError:
            sp = bp.from_buffer_copy(data)
        ct.memmove(self._buf[0].data, sp, len(data))
        self._buf[0].length = len(data)

    def copy(self, data=None):
        """
        Return a copy of this buffer header, optionally replacing the
        :attr:`data` attribute with *data* which must be an object supporting
        the buffer protocol.
        """
        result = MMALBuffer(ct.pointer(mmal.MMAL_BUFFER_HEADER_T.from_buffer_copy(self._buf[0])))
        if data is not None:
            bp = ct.c_uint8 * len(data)
            try:
                sp = bp.from_buffer(data)
            except TypeError:
                sp = bp.from_buffer_copy(data)
            result._buf[0].length = len(data)
            result._buf[0].data = ct.cast(ct.pointer(sp), ct.POINTER(ct.c_uint8))
        return result

    def acquire(self):
        mmal.mmal_buffer_header_acquire(self._buf)

    def release(self):
        mmal.mmal_buffer_header_release(self._buf)

    def reset(self):
        mmal.mmal_buffer_header_reset(self._buf)

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.release()

    def __repr__(self):
        if self._buf:
            return '<MMALBuffer object: size=%d length=%d flags=%d>' % (
                self.size, self.length, self.flags)
        else:
            return '<MMALBuffer object: ???>'


class MMALPool(object):
    """
    Represents an MMAL pool of buffer headers. This can be constructed from an
    existing MMAL pool pointer, or via a couple of class methods
    :meth:`for_port` and :meth:`for_buffers`.
    """
    def __init__(self, pool, port=None):
        self._pool = pool
        self._port = port

    def close(self):
        if self._pool is not None:
            if self._port is None:
                mmal.mmal_pool_destroy(self._pool)
            else:
                mmal.mmal_port_pool_destroy(self._port._port, self._pool)
                self._port = None
            self._pool = None

    @classmethod
    def for_port(cls, port):
        """
        Construct an MMAL pool for the number and size of buffers required by
        the :class:`MMALPort` *port*.
        """
        pool = mmal.mmal_port_pool_create(
            port._port, port._port[0].buffer_num, port._port[0].buffer_size)
        if not pool:
            raise PiCameraRuntimeError(
                'failed to create buffer header pool for port %s' % port.name)
        return MMALPool(pool, port)

    @classmethod
    def for_buffers(cls, num, size):
        """
        Construct an MMAL pool containing *num* buffer headers of *size* bytes.
        """
        pool = mmal.mmal_pool_create(num, size)
        if not pool:
            raise PiCameraRuntimeError(
                'failed to create buffer header pool of size %dx%d' % (num, size))
        return MMALPool(pool)

    def get_buffer(self):
        """
        Get the next buffer from the pool.
        """
        buf = mmal.mmal_queue_get(self._pool[0].queue)
        if not buf:
            raise PiCameraRuntimeError('failed to get a buffer from the pool')
        return MMALBuffer(buf)

    def send_buffer(self, port=None):
        """
        Get a buffer from the pool and send it to *port*. If *port* is
        ``None``, send it to the port the pool was created for.
        """
        if port is None:
            port = self._port
        port.send_buffer(self.get_buffer())

    def send_all_buffers(self, port=None):
        """
        Send all buffers from the pool to *port*. If *port* is ``None``, send
        them to the port the pool was created for.
        """
        if port is None:
            port = self._port
        for i in range(mmal.mmal_queue_length(self._pool[0].queue)):
            port.send_buffer(self.get_buffer())


class MMALConnection(object):
    """
    Represents an MMAL internal connection between two components. The
    constructor accepts arguments providing the source and target components,
    along with the index numbers of the output and input to connect.
    """

    # Format encoding negotiation. Some things to be aware of:
    #
    # 1. OPAQUE is always the most efficient format as it simply passes
    #    around pointers under the covers
    # 2. Not all OPAQUE formats are equivalent.
    # 3. The camera's video port's OPAQUE format outputs two
    #    pictures ("OPQV-dual")
    # 4. The camera's image port's OPAQUE format outputs strips of
    #    pictures ("OPQV-strips")
    # 5. The camera's preview port's OPAQUE format, and the splitter's
    #    OPAQUE format is a single image ("OPQV-single")
    # 6. The image encoder's input port, if configured for OPAQUE, expects
    #    the strips of pictures output by the camera's image port
    #    ("OPQV-strips")
    # 7. The video encoder's input port, if configured for OPAQUE, expects
    #    the dual-frames outputs by the camera's video port ("OPQV-dual")
    # 8. Ergo, the splitter *will* break the use of OPAQUE in the above
    #    cases. However, it's still worth using OPAQUE on the splitter
    #    input as it improves efficiency.
    # 9. I420 is the next most efficient format; RGB should be avoided
    #    wherever possible
    compatible_formats = {
        (f, f) for f in (
            'OPQV-single',
            'OPQV-dual',
            'OPQV-strips',
            'I420')
        } | {
        ('OPQV-dual', 'OPQV-single'),
        }

    def __init__(self, source, target):
        self._connection = ct.POINTER(mmal.MMAL_CONNECTION_T)()
        if (source.opaque_subformat, target.opaque_subformat) in self.compatible_formats:
            source.format = mmal.MMAL_ENCODING_OPAQUE
        else:
            source.format = mmal.MMAL_ENCODING_I420
        source.commit()
        target.copy_from(source)
        target.commit()
        mmal_check(
            mmal.mmal_connection_create(
                self._connection, source._port, target._port,
                mmal.MMAL_CONNECTION_FLAG_TUNNELLING |
                mmal.MMAL_CONNECTION_FLAG_ALLOCATION_ON_INPUT),
            prefix="Failed to create connection")
        mmal_check(
            mmal.mmal_connection_enable(self._connection),
            prefix="Failed to enable connection")

    def close(self):
        if self._connection is not None:
            mmal.mmal_connection_destroy(self._connection)
            self._connection = None

    def _get_enabled(self):
        return bool(self._connection[0].is_enabled)
    def _set_enabled(self, value):
        if value:
            mmal_check(
                mmal.mmal_connection_enable(self._connection),
                prefix="Failed to enable connection")
        else:
            mmal_check(
                mmal.mmal_connection_disable(self._connection),
                prefix="Failed to disable connection")
    enabled = property(_get_enabled, _set_enabled)

    @property
    def name(self):
        return self._connection[0].name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def __repr__(self):
        if self._connection:
            return '<MMALConnection "%s">' % self._connection[0].name
        else:
            return '<MMALConnection closed>'


class MMALCamera(MMALComponent):
    """
    Represents the MMAL camera component.
    """
    def __init__(self):
        super(MMALCamera, self).__init__(
            mmal.MMAL_COMPONENT_DEFAULT_CAMERA, 0, 3)
        formats = (
            'OPQV-single', # preview
            'OPQV-dual',   # video
            'OPQV-strips', # stills
            )
        for port, opaque_subformat in zip(self.outputs, formats):
            port.opaque_subformat = opaque_subformat


class MMALDownstreamComponent(MMALComponent):
    """
    Represents an MMAL component that acts as a filter of some sort, with a
    single input that connects to an upstream source port.
    """
    def __init__(self, component_type, output_count):
        super(MMALDownstreamComponent, self).__init__(
                component_type, 1, output_count)
        self._connection = None

    def connect(self, source):
        if self.connection:
            self.disconnect()
        self._connection = MMALConnection(source, self.inputs[0])

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self._connection = None

    def close(self):
        self.disconnect()
        super(MMALDownstreamComponent, self).close()

    def _set_enabled(self, value):
        if value:
            super(MMALDownstreamComponent, self)._set_enabled(True)
            if self.connection:
                self.connection.enabled = True
        else:
            if self.connection:
                self.connection.enabled = False
            super(MMALDownstreamComponent, self)._set_enabled(False)

    @property
    def connection(self):
        return self._connection


class MMALSplitter(MMALDownstreamComponent):
    """
    Represents the MMAL splitter component.
    """
    def __init__(self):
        super(MMALSplitter, self).__init__(mmal.MMAL_COMPONENT_DEFAULT_VIDEO_SPLITTER, 4)
        self.inputs[0].opaque_subformat = 'OPQV-single'
        for output in self.outputs:
            output.opaque_subformat = 'OPQV-single'


class MMALResizer(MMALDownstreamComponent):
    """
    Represents the MMAL resizer component.
    """
    def __init__(self):
        super(MMALResizer, self).__init__(mmal.MMAL_COMPONENT_DEFAULT_RESIZER, 1)
        self.inputs[0].opaque_subformat = None
        self.outputs[0].opaque_subformat = None


class MMALVideoEncoder(MMALDownstreamComponent):
    """
    Represents the MMAL video encoder component.
    """
    def __init__(self):
        super(MMALVideoEncoder, self).__init__(mmal.MMAL_COMPONENT_DEFAULT_VIDEO_ENCODER, 1)
        self.inputs[0].opaque_subformat = 'OPQV-dual'
        self.outputs[0].opaque_subformat = None


class MMALImageEncoder(MMALDownstreamComponent):
    """
    Represents the MMAL image encoder component.
    """
    def __init__(self):
        super(MMALImageEncoder, self).__init__(mmal.MMAL_COMPONENT_DEFAULT_IMAGE_ENCODER, 1)
        self.inputs[0].opaque_subformat = 'OPQV-strips'
        self.outputs[0].opaque_subformat = None


class MMALRenderer(MMALDownstreamComponent):
    """
    Represents the MMAL preview renderer component.
    """
    def __init__(self):
        super(MMALRenderer, self).__init__(mmal.MMAL_COMPONENT_DEFAULT_VIDEO_RENDERER, 0)
        self.inputs[0].opaque_subformat = 'OPQV-single'


class MMALNullSink(MMALDownstreamComponent):
    """
    Represents the MMAL null-sink component.
    """
    def __init__(self):
        super(MMALNullSink, self).__init__(mmal.MMAL_COMPONENT_DEFAULT_NULL_SINK, 0)
        self.inputs[0].opaque_subformat = 'OPQV-single'
