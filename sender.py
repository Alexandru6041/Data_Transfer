import tqdm
import os
import socket
import argparse

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 4
def send_file(filename, host, port):
    filesize = os.path.getsize(filename)
    s = socket.socket()
    print(f"Connecting to {host}:{port}")
    s.connect((host,int(port)))
    print("Connection to host {host} was completed successfully.")
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

host = input("Host IP: ")
port = input("Port: ")
file = input("Filename: ")
send_file(file,host,port)