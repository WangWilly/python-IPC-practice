import os
import posix_ipc
from mmap import mmap

# Configuration of the shared memory object
ipc_key     = "20220225"
n_bytes     = 256
posix_shm   = None

# Configuration of the named pipe
write_path = "/tmp/server_out.pipe"


def shm_sent(inp_str: str):
    # Make sure all client proc get datas before next proc.
    with os.fdopen(posix_shm.fd, "r+") as f:
        f.seek(0)
        f.write(inp_str + "\n")
        while True:
            f.seek(0)
            if len(f.read()) == 0:
                break
    posix_shm.close_fd()


def pipe_sent(inp_str: str):
    with open(write_path, "w") as f:
        f.write(inp_str)


def proc(inp_str: str) -> bool:
    if inp_str == "shut":
        return False

    # TODO: check shm first
    # pipe_sent(inp_str)
    shm_sent(inp_str)
    return True


# TODO: threading
if __name__ == "__main__":
    # Create shared memory object
    posix_shm = posix_ipc.SharedMemory(ipc_key, posix_ipc.O_CREAT | posix_ipc.O_EXCL, 0o666, n_bytes)

    # Create named pipe to communicate with subprocess.
    try:
        os.mkfifo(write_path)
    except OSError as oe:
        print (f"mkfifo error: {oe}")

    try:
        while True:
            inp_str = str(input("Server is ready. You can type intergers and then click [ENTER].  Clients will show the mean, median, and mode of the input values.\n"))
            proc(inp_str)
    finally:
        # posix_shm.close_fd()
        posix_shm.unlink()