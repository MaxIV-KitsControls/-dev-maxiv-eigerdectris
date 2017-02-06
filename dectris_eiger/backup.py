import time
import threading
import logging
import h5py


class BackupThread(threading.Thread):
    def __init__(self, name='BackupThread'):
        """Constructor, setting initial variables."""
        self._stopevent = threading.Event()
        self._sleepperiod = 2.0
        self.target_dir = '/data'
        self.buffer = None
        threading.Thread.__init__(self, name=name)

    def start(self):
        """Main loop."""
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
        logging.info("checking files....")
        print 'check files'
        dcu_files = self.buffer.list_files(name_pattern=None)
        num_files = len(dcu_files)
        print 'in back up...'
        start = time.time()

        for filename in dcu_files:
            self.buffer.download_file(filename, target_dir)
            if "master.h5" in filename:
            #    #generate XDS.INP !? do it in mxCuBE
                self.add_header(os.path.join(target_dir, filename))
            logging.info("%s has been copied from DCU to  %s" % (filename, target_dir))
            self.buffer.delete_file(filename)
            logging.info("%s is removed from DCU" % filename)

        end = time.time()
        elapsed_time = end - start

        logging.info("Elapsed time for backing up %d files is %d s." % (num_files, elapsed_time))

    def add_header(self, filename):
        h5file = h5py.File(filename)
        beamline = h5file.require_group("/entry/instrument")
        beamline.attrs['name'] = 'BioMAX@MAXIV'
        omega = h5file.require_group("/entry/sample/transformations/omega")
        omega.attrs['vector'] = (0.0, -1.0, 0.0)
        h5file.close()
        logging.info("%s has been updated with rotation axis" % (filename))
