import time
import gevent
import logging
import h5py

self._target_dir = None
self.keep_polling = False
self.buffer = None

def spawn(self):
    self.keep_polling = True
    # write files to local buffer storage first, then backed up to the bulky_storage
    logging.info("Start data backup from Eiger DCU %s to Storage %s" % (self._host, self._target_dir))
    self.polling = gevent.spawn(self._polling, self._target_dir)
    gevent.sleep(0)

def backup_dcu(self, target_dir):
    """
    Backup all files currently in DCU to target_dir and remove them in DCU.

    Args:
        target_dir: Directory, where to store the files
    """
    dcu_files = self.buffer.list_files(name_pattern=None)
    num_files = len(dcu_files)

    start = time.time()

    for filename in dcu_files:
        self.buffer.download_file(filename, target_dir)
        if "master.h5" in filename:
            #generate XDS.INP !? do it in mxCuBE
            self.add_header(os.path.join(target_dir,filename))
        logging.info("%s has been copied from DCU to  %s" % (filename, target_dir))
        #self.buffer.delete_file(filename)
        logging.info("%s is removed from DCU" % filename)

    end = time.time()
    elapsed_time = end - start

    logging.info("Elapsed time for backing up %d files is %d s." % (num_files, elapsed_time))

def _polling(self, target_dir, interval=2):
    while self.keep_polling:
        try:
            self.backup_dcu(target_dir)
        except:
            time.sleep(interval)
            continue
        time.sleep(interval)

def add_header(self, filename):
    h5file = h5py.File (filename)
    beamline = h5file.require_group("/entry/instrument")
    beamline.attrs['name'] = 'BioMAX@MAXIV'
    omega = h5file.require_group("/entry/sample/transformations/omega")
    omega.attrs['vector'] = (0.0, -1.0, 0.0)
    h5file.close()
    logging.info("%s has been updated with rotation axis" % (filename))
