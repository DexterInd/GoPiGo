import fcntl
import time

DexterLockI2C_handle = None


def I2C_Mutex_Acquire():
    global DexterLockI2C_handle
    while DexterLockI2C_handle is not None:
        time.sleep(0.001)
    DexterLockI2C_handle = True # set to something other than None
    DexterLockI2C_handle = open('/run/lock/DexterLockI2C', 'w')
    acquired = False
    while not acquired:
        try:
            # lock
            fcntl.lockf(DexterLockI2C_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            acquired = True
        except IOError: # already locked by a different process
            time.sleep(0.001)

def I2C_Mutex_Release():
    global DexterLockI2C_handle
    if DexterLockI2C_handle is not None:
        DexterLockI2C_handle.close()
        DexterLockI2C_handle = None
        time.sleep(0.001)
