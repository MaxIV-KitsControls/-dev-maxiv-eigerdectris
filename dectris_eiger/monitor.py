# -*- coding: utf-8 -*-
"""
.. module:: monitor
   :synopsis: This module contains an interface to the Dectris Eiger's monitor subsystem.

.. moduleauthor:: Teresa Nunez <tnunez@mail.desy.de>
"""
from .communication import get_value, set_value


class EigerMonitorCtrl(object):
    """
    Interface to the Dectris Eiger detector's file writer subsystem. This
    interface can be used to configure filename patterns and storage details.
    """

    def __init__(self, host, port=80, api_version="1.0.0"):
        super(EigerMonitorCtrl, self).__init__()
        self._host = host
        self._port = port
        self._api_v = api_version

    # initialize
    def initialize(self, timeout=100.0):
        """
        Resets the monitor o its original state.

        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "monitor",
                  "command", "initialize", "initialize", timeout=timeout,
                  no_data=True) 
    # clear
    def clear(self, timeout=100.0):
        """
        Drops all buffered images and resets status/dropped to zero.

        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "monitor",
                  "command", "clear", "clear", timeout=timeout,
                  no_data=True)

    # status
    def get_status(self, timeout=2.0, return_full=False):
        """
        Returns the monitor's status. The status can be one "normal" or
        "overflow".

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: subsystem status
        :rytpe: str
        """
        return get_value(self._host, self._port, self._api_v, "monitor",
                         "status", "state", timeout=timeout,
                         return_full=return_full)
    status = property(get_status)

    # error
    def get_error(self, timeout=2.0, return_full=False):
        """
        Returns list of status parameters causing error condition.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: subsystem status
        :rytpe: str
        """
        return get_value(self._host, self._port, self._api_v, "monitor",
                         "status", "error", timeout=timeout,
                         return_full=return_full)
    error = property(get_error)

    # mode
    def get_mode(self, timeout=2.0, return_full=False):
        """
        Returns the operation mode.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: the operation mode
        :rytpe: str
        """
        return get_value(self._host, self._port, self._api_v, "monitor",
                         "config", "mode", timeout=timeout,
                         return_full=return_full)

    def set_mode(self, mode, timeout=2.0):
        """
        Set the monitor's operation mode.

        :param str mode: operation mode
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "monitor",
                  "config", "mode", mode, timeout=timeout, no_data=True)
    mode = property(get_mode, set_mode)

    # number of images that can be buffered by the monitor interface
    def get_buffer_size(self, timeout=2.0, return_full=False):
        """
        Returns the number of images that can be buffered.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: number of images that can be buffered
        :rytpe: int
        """
        return int(get_value(self._host, self._port, self._api_v, "monitor",
                             "config", "buffer_size", timeout=timeout,
                             return_full=return_full))

    def set_buffer_size(self, n, timeout=2.0):
        """
        Set the number of images that can be buffered.

        :param int n: number of images that can be buffered
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "monitor",
                  "config", "buffer_size", n, timeout=timeout,
                  no_data=True)
    buffer_size = property(get_buffer_size, set_buffer_size)

