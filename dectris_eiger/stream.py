# -*- coding: utf-8 -*-
"""
.. module:: stream
   :synopsis: This module contains an interface to the Dectris Eiger's stream interface.
              
.. moduleauthor:: Mikel Eguiraun <mikel.eguiraun@maxiv.lu.se>
"""

from .communication import get_value, set_value


class EigerStream(object):
    """
    Interface to the detector's stream interface.
    """

    def __init__(self, host, port=80, api_version="1.0.0"):
        super(EigerStream, self).__init__()
        self._host = host
        self._port = port
        self._api_v = api_version

    def get_header_detail(self, timeout=2.0, return_full=False):
        """
        Returns detail of header data to be sent:

        :returns: header detail
        :param bool return_full: whether to return the full response dict
        :rytpe: str
        :rtype: string
        """
        return get_value(self._host, self._port, self._api_v, "stream",
                         "config", "header_detail", timeout=timeout,
                         return_full=return_full)

    def set_header_detail(self, header_detail, timeout=2.0):
        """
        Set the  detail of header data to be sent.

        :param str header_detail: detail [all, basic, none]
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "stream",
                  "config", "header_detail", header_detail, timeout=timeout, no_data=True)

    header_detail = property(get_header_detail, set_header_detail)

    def get_header_appendix(self, timeout=2.0, return_full=False):
        """
        Returns header_appendix to be sent:

        :returns: header detail
        :param bool return_full: whether to return the full response dict
        :rytpe: str
        :rtype: string
        """
        return get_value(self._host, self._port, self._api_v, "stream",
                         "config", "header_appendix", timeout=timeout,
                         return_full=return_full)

    def set_header_appendix(self, header_appendix, timeout=2.0):
        """
        Set the  detail of header data to be sent.

        :param str header_appendix: detail [all, basic, none]
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "stream",
                  "config", "header_appendix", header_appendix, timeout=timeout, no_data=True)

    header_appendix = property(get_header_appendix, set_header_appendix)

    def get_image_appendix(self, timeout=2.0, return_full=False):
        """
        Returns image_appendix to be sent:

        :returns: image_appendix
        :param bool return_full: whether to return the full response dict
        :rytpe: str
        :rtype: string
        """
        return get_value(self._host, self._port, self._api_v, "stream",
                         "config", "image_appendix", timeout=timeout,
                         return_full=return_full)

    def set_image_appendix(self, image_appendix, timeout=2.0):
        """
        Set the image_appendix to be sent.

        :param str image_appendix: detail [all, basic, none]
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "stream",
                  "config", "image_appendix", image_appendix, timeout=timeout, no_data=True)

    image_appendix = property(get_image_appendix, set_image_appendix)
   
    def get_stream_mode(self, timeout=2.0, return_full=False):
        """
        Returns the stream operation mode.

        :param float timeout: communication timeout in seconds
        :param bool return_full: whether to return the full response dict
        :returns: the stream operation mode
        :rytpe: str
        """
        return get_value(self._host, self._port, self._api_v, "stream",
                         "config", "mode", timeout=timeout,
                         return_full=return_full)

    def set_stream_mode(self, stream_mode, timeout=2.0):
        """
        Set the stream operation mode.

        :param str stream_mode: operation mode
        :param float timeout: communication timeout in seconds
        """
        set_value(self._host, self._port, self._api_v, "stream",
                  "config", "mode", stream_mode, timeout=timeout, no_data=True)

    stream_mode = property(get_stream_mode, set_stream_mode)

