import socket
import tqdm
import os
hostname = socket.gethostname()
SERVER_HOST = socket.gethostbyname(hostname)
SERVER_PORT = 8000

BUFFER_SIZE = 1024 * 4

SEPARATOR = "<SEPARATOR>"

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
client_socket, address = s.accept()
print(f"{address} is connected.")
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)
filesize = int(filesize)
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            break
        f.write(bytes_read)
        progress.update(len(bytes_read))

client_socket.close()
current_folder = os.getcwd()
file_location = str(current_folder) + "/" + str(filename)
s.close()
import time
time.sleep(1.2)
print(" ")
print(" ")
print(f"Your file has been received from {address} to {SERVER_HOST} through port {SERVER_PORT}.\nFile location: " + str(file_location) + "\n")
