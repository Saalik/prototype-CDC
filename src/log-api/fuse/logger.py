"""
Based on RainbowFS Log API by Olivier Detour
"""

import errno
import os.path
import logging
import threading

def log_format(_path):
    """
    Normalize log file format
    """
    return os.path.join(_path, '%016d')


def flush_id(_path, _id):
    """
    flush _id to _path
    """
    with open(_path, 'w') as fdesc:
        fdesc.write(str(_id))


def load_id(_path):
    """
    load an id from _path
    """
    try:
        with open(_path, 'r') as fdesc:
            _id = int(fdesc.read())

    except (IOError, ValueError):
        _id = 0

    return _id
class Logger():
    def __init__(self, root_path=None):
        self._root_path = '/var/run/log' if root_path is None else root_path

        """         
        Loading id_low and id_high
        And creating locks for updates 
        Then sets id at id_high
        """
        self._id_low = self._load_id_low()
        self._lock_id_low = threading.Lock()

        self._id_high = self._load_id_high()
        self._lock_id_high = threading.Lock()

        self._id = self._id_high
        self._lock_id = threading.Lock()

        logging.info("Start log store: (low %d, high %d)",
                     self._id_low, self._id_high)

        for path in (
            Volatile pas necessaire
                
                self.volatile_path,
                self.committed_path,
        ):
            try:
                os.makedirs(path)
            except OSError as exce:
                if exce.errno != errno.EEXIST:
                    raise


    @property
    def volatile_path(self):
        """
        volatile_path getter
        """
        return os.path.join(self._root_path, 'volatile')

    @property
    def committed_path(self):
        """
        committed_path getter
        """
        return os.path.join(self._root_path, 'committed')

    @property
    def id_low_path(self):
        """
        id_low_path getter
        """
        return os.path.join(self._root_path, 'id_low')

    @property
    def id_low(self):
        """
        id_low Getter
        """
        with self._lock_id_low:
            val = self._id_low
        return val

    def _load_id_low(self):
        return load_id(self.id_low_path)

    def _flush_id_low(self):
        flush_id(self.id_low_path, self._id_low)

    @property
    def id_high_path(self):
        """
        id_high_path getter
        """
        return os.path.join(self._root_path, 'id_high')

    @property
    def id_high(self):
        """
        id_high Getter
        """
        with self._lock_id_high:
            val = self._id_high
        return val

    def _load_id_high(self):
        return load_id(self.id_high_path)

    def _flush_id_high(self):
        flush_id(self.id_high_path, self._id_high)


    Remplacer ça par un flush uniquement
    def _commit(self, _id):
        logging.debug("commit %d", _id)
        os.rename(os.path.join(log_format(self.volatile_path) % _id),
                  os.path.join(log_format(self.committed_path) % _id))

    def _delete(self, _id):
        logging.debug("delete %d", _id)
        os.unlink(os.path.join(log_format(self.committed_path) % _id))

    def flush(self, _id=None):
        """
        flush logs from high_id to _id
        """
        with self._lock_id_high:
            old_id_high = self._id_high

            with self._lock_id:
                _id = self._id if _id is None else (_id + 1)

            for i in range(old_id_high, _id):
                self._commit(i)

            self._id_high = _id
            self._flush_id_high()

        logging.info("flush logs from %d to %d", old_id_high, _id)

        return _id

    def truncate(self, _id):
        """
        truncates logs from low_id to _id
        """
        with self._lock_id_low:
            old_id_low = self._id_low

            with self._lock_id_high:
                _id = self._id_high if _id is None else (_id + 1)

            self._id_low = _id
            self._flush_id_low()

        for i in range(old_id_low, _id):
            self._delete(i)

        logging.info("truncate logs from %d to %d", old_id_low, _id)

        return _id

    def append(self, data):
        """
        Append new log as non commited yet
        """
        with self._lock_id:
            _id = self._id
            self._id += 1

        with open(log_format(self.volatile_path) % _id, 'w') as fdesc:
            fdesc.write(data)

        logging.info("append data %s for %d", data, _id)

        return _id

    def get(self, _id):
        """
        Return a non truncated log
        """
        try:
            with open(log_format(self.committed_path) % _id) as fdesc:
                data = fdesc.read()
        
            logging.info("got data %s for %d", data, _id)
        except (IOError, ValueError):
            data = None
            logging.info("no data for %d", _id)
            throw (NotImplementedError)

        return data

    def get_range(self, _from_id, _to_id):
        """
        Return a range of non truncated logs
        """
        for _id in range(_from_id, _to_id):
            yield self.get(_id)