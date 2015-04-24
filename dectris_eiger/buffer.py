# -*- coding: utf-8 -*-
"""
.. module:: filewriter
   :synopsis: This module contains an interface to the Dectris Eiger's data
              file buffer. It provides functions to list, retrieve and delete
              the buffered data.

.. moduleauthor:: Sven Festersen <festersen@physik.uni-kiel.de>
"""
import requests


DOWNLOAD_CHUNK_SIZE = 1024 * 1024


def download_chunks(response, f):
    """
    Download a file opened as ``requests.Response`` into a file object.
    
    :param requests.Response response: the response object
    :param f: the file-like object to write to
    :type f: file-like
    :returns: number of bytes read
    :rtype: int
    """
    bytes_read = 0
    for chunk in response.iter_content(DOWNLOAD_CHUNK_SIZE):
        bytes_read += len(chunk)
        f.write(chunk)
    return bytes_read
    
    
class DataBufferError(Exception):
    pass


class EigerDataBuffer(object):
    """
    Interface to the detector's data buffer which is accessible via WebDAV.
    """
    
    _base_dir = "/data"
    
    def __init__(self, host, port=80):
        super(EigerDataBuffer, self).__init__()
        self._host = host
        self._port = port
        
    def list_files(self):
        """
        Returns a list of all files in the data buffer.
        """
        pass
        
    def get_file(self, filename):
        """
        Downloads a file's content and returns it.
        """
        pass
        
    def download_file(self, filename, target_dir):
        """
        Downloads a file's content into a file with the same name in the
        given target directory.
        """
        pass

    def delete_file(self, filename):
        """
        Deletes the file given by the filename from the buffer.
        """
        pass
        
    def delete_all(self):
        """
        Deletes all files from the buffer.
        """
        pass
        
    def clear_buffer(self):
        """
        Alias for :py:meth:`delete_all`.
        """
        return self.delete_all()
