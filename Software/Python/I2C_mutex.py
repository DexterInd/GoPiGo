import fcntl
import time

class Mutex(object):

    DexterLockI2C_handle = None

    def __init__(self, debug = False):
        self.mutex_debug = debug

    def acquire(self):
        if self.mutex_debug:
            print("I2C mutex acquire")
        while self.DexterLockI2C_handle is not None:
            time.sleep(0.001)
        DexterLockI2C_handle = True

        try:
            DexterLockI2C_handle = open('/run/lock/DexterLockI2C')
        except:
            pass

        acquired = False
        while not acquired:
            try:
                # lock
                fcntl.lockf(DexterLockI2C_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
            except IOError: # already locked by a different process
                time.sleep(0.001)
            except Exception as e:
                print(e)

    def release(self):
        if self.mutex_debug:
            print("I2C mutex release")
        if self.DexterLockI2C_handle is not None and self.DexterLockI2C_handle is not True:
            self.DexterLockI2C_handle.close()
            self.DexterLockI2C_handle = None
            time.sleep(0.001)

    def enableDebug(self):
        self.mutex_debug = True

    def disableDebug(self):
        self.mutex_debug = False

    def __enter__(self):
        if self.mutex_debug:
            print("I2C mutex enter")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.release()
        if self.mutex_debug:
            print("I2C mutex exit")
