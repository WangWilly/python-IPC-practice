import os
import posix_ipc
import numpy as np


# Configuration of the shared memory object
ipc_key     = "20220225"

if __name__ == "__main__":
    # With flags set to the default of 0, the module attempts to 
    #   open an existing shared memory segment identified by key 
    #   and raises a ExistentialError if it doesn't exist.
    posix_shm = posix_ipc.SharedMemory(ipc_key)

    # while True:
    #     with os.fdopen(posix_shm.fd, "r+", encoding="ascii", closefd=True) as f:
    #         data = f.readline()

    #     if len(data) == 0:
    #         continue
    #     # print(data)
    #     nums = np.array([int(n) for n in data.split()])
    #     print(np.median(nums))

    try:
        with os.fdopen(posix_shm.fd, "r+", encoding="ascii") as f:
            while True:
                f.seek(0)
                data = f.readline()
                if len(data) == 0:
                    continue
                
                nums = np.array([int(n) for n in data.split()])
                print(np.median(nums))
                f.truncate(0)
    finally:
        # posix_shm.close_fd()
        pass