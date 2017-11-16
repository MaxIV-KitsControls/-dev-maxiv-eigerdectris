import time
import threading
import logging
import h5py
import os

class BackupThread(threading.Thread):
    def __init__(self, name='BackupThread'):
        """Constructor, setting initial variables."""
        self._stopevent = threading.Event()
        self._sleepperiod = 2.0
        self.target_dir = '/data'
        self.buffer = None
        self.data_threads = 1
        self.MAX_THREADS = 4  # To be fine tunned

        threading.Thread.__init__(self, name=name)

    def convert_bytes(self, size):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return size, x
            size /= 1024.0

    def set_number_of_data_threads(self, value):
        if 1 <= value <= self.MAX_THREADS:
            self.data_threads = value
        else:
            self.data_threads = self.MAX_THREADS

    def save_and_remove(self, filename, target_dir, regex=False):
        start = time.time()
        logging.info("start to copy %s from DCU to  %s" % (filename, target_dir))
        self.buffer.download_file(filename, target_dir)
        file_path = os.path.join(target_dir,filename)
        if "master.h5" in filename:
           #generate XDS.INP !? do it in mxCuBE
            self.add_header(file_path)
        logging.info("%s has been copied from DCU to  %s" % (filename, target_dir))
        self.buffer.delete_file(filename)
        logging.info("%s is removed from DCU" % filename)

        end = time.time()
        elapsed_time = end - start
        file_size, unit = self.convert_bytes(os.path.getsize(file_path))
        logging.info("Elapsed time for backing up file %s is %d s, and speed is %.2f %s/s" % (filename, elapsed_time, file_size/elapsed_time, unit))

    def run(self):
        """Main loop for downloading data from the dcu."""
        print "%s starts" % (self.getName(),)

        while not self._stopevent.isSet():
            try:
                self.backup_dcu(self.target_dir)
            except:
                self._stopevent.wait(self._sleepperiod)
                continue
            self._stopevent.wait(self._sleepperiod)

    def stop(self, timeout=None):
        """Stop the thread and wait for it to end."""
        self._stopevent.set()
        threading.Thread.join(self, timeout)

    def backup_dcu(self, target_dir):
        """
        Backup all files currently in DCU to target_dir and remove them in DCU.

        Args:
            target_dir: Directory, where to store the files
        """
        dcu_files = self.buffer.list_files()
        dcu_files.reverse()

        threads = [threading.Thread(target=self.save_and_remove,
                                    args=(filename, target_dir)) for filename in dcu_files[0:self.data_threads]]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def add_header(self, filename):
        h5file = h5py.File(filename)
        beamline = h5file.require_group("/entry/instrument")
        beamline.attrs['name'] = 'BioMAX@MAXIV'
        omega = h5file.require_group("/entry/sample/transformations/omega")
        omega.attrs['vector'] = (0.0, -1.0, 0.0)
        h5file.close()
        logging.info("%s has been updated with rotation axis" % (filename))


class DataTransferThread(threading.Thread):
    def __init__(self, name='DataTransferThread'):
        self._stopevent_data_transfer = threading.Event()
        self._sleepperiod_data_transfer = 30.0
        self.target_dir = '/data'
        self.local_dir = '/localdata'

        threading.Thread.__init__(self, name=name)

    def run(self):
        """Main loop for hte data transfer to final storage."""
        print "%s data transfer starts" % (self.getName(),)

        while not self._stopevent_data_transfer.isSet():
            try:
                self.transfer_data(self.local_dir, self.target_dir)
            except:
                self._stopevent_data_transfer.wait(self._sleepperiod_data_transfer)
                continue
            self._stopevent_data_transfer.wait(self._sleepperiod_data_transfer)

    def stop(self, timeout=None):
        """Stop the thread and wait for it to end."""
        self._stopevent_data_transfer.set()
        threading.Thread.join(self, timeout)

    def rsync(self, local_dir, target_dir):
        os.system("rsync -aqz %s/* %s/." % (local_dir, target_dir))

    def transfer_data(self, local_dir, target_dir):
        """
        Copy all files in localfolder (e.g. /localdata) to final storage (e.g. /data.

        Args:
            local_dir: Directory, where to pick the files from
            target_dir: Directory, where to store the files
        """

        thread = threading.Thread(target=self.rsync,
                                  args=(local_dir, target_dir))

        thread.start()
        thread.join()
