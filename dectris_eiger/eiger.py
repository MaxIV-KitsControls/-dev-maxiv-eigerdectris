# -*- coding: utf-8 -*-
"""
.. module:: eiger
   :synopsis: This module contains an interface to the Dectris Eiger's data
              acquisition system/controller. Originally written for the 1M
              version at P08 (PETRA III/DESY), should also work with larger
              detector versions.

.. moduleauthor:: Sven Festersen <festersen@physik.uni-kiel.de>
"""
from .buffer import EigerDataBuffer
from .communication import get_value, set_value
from .filewriter import EigerFileWriter


class EigerDetector(object):
    """
    Interface to the Dectris Eiger detector's data acquisition and control
    server. All API functions are mapped to methods and properties.

    ``EigerDectector`` instances have a *filewriter* attribute which points
    to an instance of :py:class:`dectris_eiger.filewrite.EigerFileWriter``.
    This can be used to configure the temporary data storage.
    """

    def __init__(self, host, port=80, api_version="1.0.0"):
        super(EigerDetector, self).__init__()
        self.filewriter = EigerFileWriter(host, port, api_version)
        self.buffer = EigerDataBuffer(host, port, api_version)
        self._host = host
        self._port = port
        self._api_v = api_version

    # detector state
    def get_state(self, timeout=2.0, return_full=False):
        """
        Returns the detector state. This can be one of "na", "initialize",
        "configure", "acquire", "test", "ready", and "idle".

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: The detector state.
        :rytpe: str or dict
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "status", "state", timeout=timeout,
                         return_full=return_full)
    state = property(get_state)

    # board temperature
    def get_temperature(self, timeout=2.0, return_full=False,
                        board="board_000"):
        """
        Returns the temperature reading (in Celsius) for a specific detector
        board.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :param str board: board name (default board_000 - first board)
        :returns: board temperature
        :rtype: float
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "status", "{0}/th0_temp".format(board),
                         timeout=timeout, return_full=return_full)
    temperature = property(get_temperature)

    # board humidity
    def get_humidity(self, timeout=2.0, return_full=False, board="board_000"):
        """
        Returns the relative humidity reading (in percent) for a specific
        detector board.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :param str board: board name (default board_000 - first board)
        :returns: board humidity
        :rtype: float
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "status", "{0}/th0_humidity".format(board),
                         timeout=timeout, return_full=return_full)
    humidity = property(get_humidity)

    # detector error
    def get_error(self, timeout=2.0, return_full=False):
        """
        Returns the list of staus parameters causing an error condition. 

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: error
        :rytpe: str or dict
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "status", "error", timeout=timeout,
                         return_full=return_full)
    error = property(get_error)

    # detector time
    def get_detector_time(self, timeout=2.0, return_full=False):
        """
        Returns the actual system time. 

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: error
        :rytpe: str or dict
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "status", "time", timeout=timeout,
                         return_full=return_full)
    detector_time = property(get_detector_time)

    # count time
    def get_count_time(self, timeout=2.0, return_full=False):
        """
        Returns the currently set count time per image in seconds.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: count time in seconds
        :rtype: float
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "count_time", timeout=timeout,
                         return_full=return_full)

    def set_count_time(self, t, timeout=2.0):
        """
        Set the count time per image in seconds.

        :param float t: count time in seconds
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "detector",
                  "config", "count_time", t, timeout=timeout)
    count_time = property(get_count_time, set_count_time)



    
    # frame time
    def get_frame_time(self, timeout=2.0, return_full=False):
        """
        Returns the currently set frame time (count time plus read out time)
        per image in seconds.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: frame time in seconds
        :rtype: float
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "frame_time", timeout=timeout,
                         return_full=return_full)

    def set_frame_time(self, t, timeout=2.0):
        """
        Set the frame time per image in seconds.

        :param float t: frame time in seconds
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "detector",
                  "config", "frame_time", t, timeout=timeout)
    frame_time = property(get_frame_time, set_frame_time)

    # number of images
    def get_nimages(self, timeout=2.0, return_full=False):
        """
        Returns the number of images per series.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: number of images
        :rtype: int
        """
        return int(get_value(self._host, self._port, self._api_v, "detector",
                             "config", "nimages", timeout=timeout,
                             return_full=return_full))

    def set_nimages(self, n, timeout=2.0):
        """
        Set the number of images per series.

        :param int n: number of images
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "detector",
                  "config", "nimages", n, timeout=timeout)
    nimages = property(get_nimages, set_nimages)

    # number of triggers
    def get_ntrigger(self, timeout=2.0, return_full=False):
        """
        Returns the allowed number of trigger per arm/disarm sequence.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: number of images
        :rtype: int
        """
        return int(get_value(self._host, self._port, self._api_v, "detector",
                             "config", "ntrigger", timeout=timeout,
                             return_full=return_full))

    def set_ntrigger(self, n, timeout=2.0):
        """
        Set the allowed number of triggers per arm/disarm sequence.

        :param int n: number of triggers
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "detector",
                  "config", "ntrigger", n, timeout=timeout)
    ntrigger = property(get_ntrigger, set_ntrigger)

    # photon energy
    def get_energy(self, timeout=2.0, return_full=False):
        """
        Returns the currently set photon energy in electron volts.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: photon energy in electron volts
        :rtype: float
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "photon_energy", timeout=timeout,
                         return_full=return_full)

    def set_energy(self, energy, timeout=2.0):
        """
        Set the photon energy in electron volts. This will also affect the
        wavelength property and the threshold.

        :param float timeout: communication timeout in seconds
        :param float energy: the new photon energy in electron volts
        """
        set_value(self._host, self._port, self._api_v, "detector",
                  "config", "photon_energy", energy, timeout=timeout)
    energy = property(get_energy, set_energy)

    # photon wavelength
    def get_wavelength(self, timeout=2.0, return_full=False):
        """
        Returns the currently set photon wavelength in Angstrom.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: photon wavelength in Angstrom
        :rtype: float
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "wavelength", timeout=timeout,
                         return_full=return_full)

    def set_wavelength(self, wavelength, timeout=2.0):
        """
        Set the photon energy in Angstrom. This will also affect the energy
        and threshold properties.

        :param float timeout: communication timeout in seconds
        :param float wavelength: photon wavelength in Angstrom
        """
        set_value(self._host, self._port, self._api_v, "detector",
                  "config", "wavelength", wavelength, timeout=timeout)
    wavelength = property(get_wavelength, set_wavelength)

    # energy threshold
    def get_threshold(self, timeout=2.0, return_full=False):
        """
        Returns the currently set energy threshold in electron volts.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: energy threshold in electron volts
        :rtype: float
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "threshold_energy", timeout=timeout,
                         return_full=return_full)

    def set_threshold(self, energy, timeout=2.0):
        """
        Set the energy threshold in electron volts.

        :param float timeout: communication timeout in seconds
        :param float energy: threshold energy
        """
        set_value(self._host, self._port, self._api_v, "detector",
                  "config", "threshold_energy", energy, timeout=timeout)
    threshold = property(get_threshold, set_threshold)

    # flatfield
    def get_flatfield_enabled(self, timeout=2.0, return_full=False):
        """
        Returns True if the flatfield correction is enabled.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: True if the flatfield correction is enabled, False otherwise
        :rtype: boolean
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "flatfield_correction_applied",
                         timeout=timeout, return_full=return_full)

    def set_flatfield_enabled(self, enabled, timeout=2.0):
        """
        Enable or disable the flatfield correction.

        :param boolean enabled: set the flatfield correction status
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "detector",
                  "config", "flatfield_correction_applied", enabled,
                  timeout=timeout)
    flatfield_enabled = property(get_flatfield_enabled, set_flatfield_enabled)

    # auto summation
    def get_auto_summation_enabled(self, timeout=2.0, return_full=False):
        """
        Returns True if the auto summation feature (to increase the dynamic
        range) is enabled.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: True if auto summation is enabled, False otherwise
        :rtype: boolean
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "auto_summation", timeout=timeout,
                         return_full=return_full)

    def set_auto_summation_enabled(self, enabled, timeout=2.0):
        """
        Enable or disable the auto summation feature.

        :param boolean enabled: set the auto summation status
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "detector",
                  "config", "auto_summation", enabled, timeout=timeout)
    auto_summation_enabled = property(get_auto_summation_enabled,
                                      set_auto_summation_enabled)

    # trigger mode
    def get_trigger_mode(self, timeout=2.0, return_full=False):
        """
        Returns the current trigger mode. Following trigger modes are
        supported:

         * expo
         * extt
         * extm
         * exte
         * exts
         * ints
         * inte

        This is likely to change with future API versions.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: the current trigger mode
        :rtype: string
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "trigger_mode", timeout=timeout,
                         return_full=return_full)

    def set_trigger_mode(self, mode, timeout=2.0):
        """
        Set the trigger mode. Raises ``ValueError`` if *mode* is an invalid
        mode string. See :py:meth:`get_trigger_mode` for supported modes.

        :param string mode: trigger mode
        :param float timeout: communication timeout in seconds
        """
        if mode not in ["expo", "extt", "extm", "exte", "exts", "ints", "inte"]:
            raise ValueError("Invalid trigger mode.")
        set_value(self._host, self._port, self._api_v, "detector",
                  "config", "trigger_mode", mode, timeout=timeout)
    trigger_mode = property(get_trigger_mode, set_trigger_mode)

    # rate correction
    def get_rate_correction_enabled(self, timeout=2.0, return_full=False):
        """
        Returns True if the rate correction is enabled, False otherwise.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: True if rate correction is enabled, False otherwise
        :rtype: boolean
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "countrate_correction_applied",
                         timeout=timeout, return_full=return_full)

    def set_rate_correction_enabled(self, enabled, timeout=2.0):
        """
        Enable or disable the rate correction.

        :param boolean enabled: set the rate correction status
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "detector",
                  "config", "countrate_correction_applied", enabled,
                  timeout=timeout)
    rate_correction_enabled = property(get_rate_correction_enabled,
                                       set_rate_correction_enabled)

    # bit depth
    def get_bit_depth(self, timeout=2.0, return_full=False):
        """
        Returns the detector's bit depth, i.e. the dynamic range.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: bit depth
        :rtype: int
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "bit_depth_readout", timeout=timeout,
                         return_full=return_full)
    bit_depth = property(get_bit_depth)

    # readout time
    def get_readout_time(self, timeout=2.0, return_full=False):
        """
        Return the detector's readout time per image.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: readout time in seconds
        :rtype: float
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "detector_readout_time", timeout=timeout,
                         return_full=return_full)
    readout_time = property(get_readout_time)

    # description
    def get_description(self, timeout=2.0, return_full=False):
        """
        Returns the detector description, i.e. the model.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: detector description
        :rtype: string
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "description", timeout=timeout,
                         return_full=return_full)
    description = property(get_description)

    # serial number
    def get_serial_number(self, timeout=2.0, return_full=False):
        """
        Returns the detector's serial number.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: detector serial number
        :rtype: string
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "detector_number", timeout=timeout,
                         return_full=return_full)
    serial_number = property(get_serial_number)

    # firmware version
    def get_firmware_version(self, timeout=2.0, return_full=False):
        """
        Returns the detector's firmware version.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: detector firmware version
        :rtype: string
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "software_version", timeout=timeout,
                         return_full=return_full)
    firmware_version = property(get_firmware_version)

    # sensor material
    def get_sensor_material(self, timeout=2.0, return_full=False):
        """
        Returns the detector sensor's material.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: material
        :rtype: string
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "sensor_material", timeout=timeout,
                         return_full=return_full)
    sensor_material = property(get_sensor_material)

    # sensor thickness
    def get_sensor_thickness(self, timeout=2.0, return_full=False):
        """
        Returns the thickness of the sensor material in meters.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: sensor thickness in meters
        :rtype: float
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "sensor_thickness", timeout=timeout,
                         return_full=return_full)
    sensor_thickness = property(get_sensor_thickness)

    # initialize
    def initialize(self, timeout=100.0):
        """
        Initialize the detector.

        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "detector",
                  "command", "initialize", "initialize", timeout=timeout,
                  no_data=True)

    # arm
    def arm(self, timeout=100.0, return_full=False):
        """
        Arm the detector.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: next series id
        :rtype: int
        """
        data = set_value(self._host, self._port, self._api_v, "detector",
                         "command", "arm", "arm", timeout=timeout)
        if return_full:
            return data
        else:
            return data["sequence id"]

    # disarm
    def disarm(self, timeout=100.0):
        """
        Disarm the detector.

        :param float timeout: communication timeout in seconds
        """
        data = set_value(self._host, self._port, self._api_v, "detector",
                         "command", "disarm", "disarm", timeout=timeout,
                         no_data=True)

    # trigger
    def trigger(self, timeout=100.0, input_value=-1):
        """
        Trigger the detector.

        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "detector",
                  "command", "trigger", input_value, timeout=timeout,
                  no_data=True)

    # cancel
    def cancel(self, timeout=2.0, return_full=False):
        """
        Stop data acquisition after the current image.

        .. note::

           The cancel() command is not available in firmware version 0.9 and
           below.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: current series id
        :rtype: int
        """
        data = set_value(self._host, self._port, self._api_v, "detector",
                         "command", "cancel", "cancel", timeout=timeout)
        if return_full:
            return data
        else:
            return data["sequence id"]

    # abort
    def abort(self, timeout=2.0, return_full=False):
        """
        Abort all operations and reset the detector system.

        .. note::

           The abort() command is not available in firmware version 0.9 and
           below.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: current series id
        :rtype: int
        """
        data = set_value(self._host, self._port, self._api_v, "detector",
                         "command", "abort", "abort", timeout=timeout)
        if return_full:
            return data
        else:
            return data["sequence id"]

    def get_param_lim(self, parameter, limit, timeout=2.0, return_full = True):
        """
        Returns the limit max or min of the given parameter

        :param string parameter: parameter name
        :param string limit: max or min
        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: max count time in seconds
        :rtype: float
        """
        response = get_value(self._host, self._port, self._api_v, "detector",
                             "config", parameter, timeout=timeout,
                             return_full=return_full)

        return response[limit]

    # beam center
    def get_beam_center_x(self, timeout=2.0, return_full=False):
        """
        Returns the currently set beam center horizontal position.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: beam center horizontal position
        :rtype: float
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "beam_center_x", timeout=timeout,
                         return_full=return_full)

    def set_beam_center_x(self, beam_center_x, timeout=2.0):
        """
        Set the beam center horizontal position.

        :param float timeout: communication timeout in seconds
        :param float beam_center_x: the new beam center horizontal position
        """
        set_value(self._host, self._port, self._api_v, "detector",
                  "config", "beam_center_x", beam_center_x, timeout=timeout)
    beam_center_x = property(get_beam_center_x, set_beam_center_x)

    def get_beam_center_y(self, timeout=2.0, return_full=False):
        """
        Returns the currently set beam center vertical position.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: beam center vertical position
        :rtype: float
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "beam_center_y", timeout=timeout,
                         return_full=return_full)

    def set_beam_center_y(self, beam_center_y, timeout=2.0):
        """
        Set the beam center horizontal position.

        :param float timeout: communication timeout in seconds
        :param float beam_center_y: the new beam center vertical position
        """
        set_value(self._host, self._port, self._api_v, "detector",
                  "config", "beam_center_y", beam_center_y, timeout=timeout)
    beam_center_y = property(get_beam_center_y, set_beam_center_y)

    def get_detector_distance(self, timeout=2.0, return_full=False):
        """
        Returns the currently set detector distance.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: detector distance
        :rtype: float
        """
        return get_value(self._host, self._port, self._api_v, "detector",
                         "config", "detector_distance", timeout=timeout,
                         return_full=return_full)

    def set_detector_distance(self, detector_distance, timeout=2.0):
        """
        Set the detector distance.

        :param float timeout: communication timeout in seconds
        :param float detector_distance: the new detector distance
        """
        set_value(self._host, self._port, self._api_v, "detector",
                  "config", "detector_distance", detector_distance, timeout=timeout)
    detector_distance = property(get_detector_distance, set_detector_distance)
