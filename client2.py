import time
import numpy as np


read_path = "/tmp/server_out.pipe"
write_path = "/tmp/server_in.pipe"


if __name__ == "__main__":
    conti = True
    while conti:
        with open(read_path, "r") as rfifo:
            data = rfifo.read()
            if len(data) != 0:
                if data == "shut": conti = False
                else:
                    nums = np.array([int(n) for n in data.split()])
                    print(np.median(nums))

                with open(write_path, "w") as f:
                    f.write("ack")
            else:
                time.sleep(0.5)