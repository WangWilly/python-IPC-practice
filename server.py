"""
client1 => OK.
client2 => OK.
client3 => a little BUG
call subprocess => a little BUG
"""
import os
import time
import socket
import sysv_ipc
import subprocess


# Configuration of the socket
HOST = '127.0.0.1'
PORT = 2502
socket_server = None

# Configuration of the named pipe
write_path = "/tmp/server_out.pipe"
read_path = "/tmp/server_in.pipe"

# Configuration of the shared memory object
ipc_key     = 20220239
n_bytes     = 256
sysv_shm   = None


def socket_sent(inp_str: str):
    # Wait for an incoming connection
    conn, addr = socket_server.accept()
    try:
        msg = str(conn.recv(1024), encoding='utf-8')
        # print(msg)
        if msg == "ready":
            conn.sendall(inp_str.encode())
    finally:
        conn.close()


def pipe_sent(inp_str: str):
    with open(write_path, "w") as f:
        f.write(inp_str)
    conti = True
    while conti:
        with open(read_path, "r") as rf:
            data = rf.read()
            if len(data) != 0 and data == "ack": conti = False
            else: time.sleep(0.25)


def shm_sent(inp_str: str):
    # Make sure the client get datas before next proc.
    deliver_data = (inp_str + "\0").encode()
    sysv_shm.write(deliver_data, offset=0)
    # TODO: workaround ``
    while True and inp_str != "shut":
        flag = str(sysv_shm.read(byte_count=1, offset=0), encoding='utf-8')
        if flag == "\0":
            break


# TODO: Use the multithread to manage three processes status.
def proc(inp_str: str) -> bool:
    socket_sent(inp_str)
    pipe_sent(inp_str)
    shm_sent(inp_str)

    if inp_str == "shut": return False
    return True


if __name__ == "__main__":
    subprocess.Popen("python client1.py & python client2.py & python client3.py", shell=True)

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((HOST, PORT))
    socket_server.listen()

    # Create named pipe to communicate with subprocess.
    try:
        os.mkfifo(write_path)
        os.mkfifo(read_path)
    except OSError as oe:
        print (f"mkfifo error: {oe}")

    # Create shared memory object
    sysv_shm = sysv_ipc.SharedMemory(ipc_key, sysv_ipc.IPC_CREAT | sysv_ipc.IPC_EXCL, 0o666, n_bytes, "\0".encode())

    try:
        while True:
            time.sleep(0.03)
            inp_str = str(input("Server is ready. You can type intergers and then click [ENTER]. Clients will show the mean, median, and mode of the input values.\n"))
            inp_str = inp_str.strip("\n")
            if inp_str == "shut":
                break
            proc(inp_str)
    finally:
        proc("shut")
        os.remove(write_path)
        os.remove(read_path)
        sysv_shm.remove()