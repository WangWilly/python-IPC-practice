import socket
import numpy as np


# Configuration of the socket
HOST = '127.0.0.1'
PORT = 2502


if __name__ == "__main__":
    while True:
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_client.connect((HOST, PORT))
        try:
            # print("wait")
            socket_client.sendall(b"ready")
            data = str(socket_client.recv(1024), encoding='utf-8')
            if data == "shut": break
            nums = np.array([int(n) for n in data.split()])
            print(nums.mean())
        finally:
            socket_client.close()