import tqdm
import os
import socket
import tkinter as tk
from tkinter import filedialog
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
def send_file(filename, host, port):
    filesize = os.path.getsize(filename)
    s = socket.socket()
    print(f"Connecting to {host}:{port}")
    s.connect((host,int(port)))
    print(f"Connection to {host} was completed successfully.")
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit = "B", unit_scale = True, unit_divisor = 1024)
    with open(filename, "rb") as file:
        ok = True
        while ok:
            bytes_read = file.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
    s.close()
    import time
    time.sleep(1.2)
    print(f"{filename} has been successfully sent to {host} through {port}")

host = input("Host IP: ")
port = 5001
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
file = str(file_path)
send_file(file,host,port)