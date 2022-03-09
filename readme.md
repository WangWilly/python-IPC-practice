# Python3 IPC Practice📝 - Socket, Pipe and SysV-SHM

A simple project aims to utilize IPC. A server would get the number series from user and pass to three clients. Consequently, each of clients counts the output. `client1` counts the mean of series. `client2` counts the median of series. `client3` counts the mode of series. In addition, socket, pipe and sysV-shm as IPC methods are applied in these three clients, respectively.

## 🧩Installation
Here are my environment settings for this project:
- Ubuntu 18.04.3 LTS (You can use Windows with cygwin support.)
- miniconda 4.9.2
- Python 3.7.7

🚩 The instructions for installing Python package
```bash
conda create --name ipc_practice python=3.7.7
conda activate ipc_practice
pip install -r requirements.txt
```

## 🧩Execution
You can just simply execute `python server.py` to raise all four processes. Afterward, type some number series to check the functionality. Last, you either type `shut` or press `ctrl + c` to shut down these four programs.
