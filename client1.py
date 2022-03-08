import os
import numpy as np


read_path = "/tmp/server_out.pipe"

if __name__ == "__main__":
    try:
        os.mkfifo(read_path)
    except OSError as oe:
        print (f"mkfifo error: {oe}")

    while True:
        # print("Opening FIFO...")
        with open(read_path) as rfifo:
            # print("FIFO opened")
            while True:
                data = rfifo.read()
                if len(data) == 0:
                    break

                nums = np.array([int(n) for n in data.split()])
                print(nums.mean())