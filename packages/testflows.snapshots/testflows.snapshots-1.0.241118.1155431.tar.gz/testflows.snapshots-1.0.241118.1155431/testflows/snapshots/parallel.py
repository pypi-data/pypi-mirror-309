from contextlib import contextmanager
from threading import Lock


class RWLock(object):
    """Read-Write lock that allows multiple readers but only single writer."""

    def __init__(self):
        self.writer_lock = Lock()
        self.reader_lock = Lock()
        self.readers = 0

    def reader_acquire(self):
        with self.reader_lock:
            self.readers += 1
            if self.readers == 1:
                self.writer_lock.acquire()

    def reader_release(self):
        assert self.readers > 0, "no readers to release"
        with self.reader_lock:
            self.readers -= 1
            if self.readers == 0:
                self.writer_lock.release()

    def writer_acquire(self):
        self.writer_lock.acquire()

    def writer_release(self):
        self.writer_lock.release()

    @contextmanager
    def read(self):
        try:
            self.reader_acquire()
            yield
        finally:
            self.reader_release()

    @contextmanager
    def write(self):
        try:
            self.writer_acquire()
            yield
        finally:
            self.writer_release()
