import time
import sysv_ipc
import numpy as np
from scipy import stats


# Configuration of the shared memory object
ipc_key = 20220239


if __name__ == "__main__":
    sysv_shm = sysv_ipc.SharedMemory(ipc_key)
    conti = True
    try:
        while conti:
            flag = sysv_shm.read(byte_count=1, offset=0).decode()
            if flag == "\0":
                time.sleep(0.5)
                continue
            
            data = str(sysv_shm.read(byte_count=0, offset=0), encoding='utf-8')
            data = data.strip("\0")
            
            sysv_shm.write("\0".encode(), offset=0)
            time.sleep(0.25)
            # TODO: data == 'shut\x00'?? Here use workaround to solve it.
            if "shut" in data:
                conti = False
            else:
                nums = np.array([int(n) for n in data.split()])
                print(stats.mode(nums)[0][0])
    finally:
        sysv_shm.detach()