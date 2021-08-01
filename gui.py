import time
import socket
import os
import tkinter as tk
from tkinter import Entry, filedialog
import tqdm
from tkinter import *
window = tk.Tk()
window.title("Data Transfer Software")
window.geometry("800x400")
title = tk.Label(
    window,
    text = "Data Trasnfer Software",
    bg = "white",
    fg = "black",
    font = ("Arial Bold", 18)
)
title.pack()
Label(window, text="Host IP: ").pack()
host_tf = Entry(window, width=100)
host_1 = host_tf.pack()
def send_file():
    try:
        host = host_tf.get() 
        def send_file_function(filename, host, port):
            SEPARATOR = "<SEPARATOR>"
            BUFFER_SIZE = 4096
            filesize = os.path.getsize(filename)
            s = socket.socket()
            print(f"Connecting to {host}:{port}")
            connecting_1 = tk.Label(
                window,
                text = f"Connecting to {host}:{port}"
            )
            connecting_1.pack()
            s.connect((host, int(port)))
            tk.Label(window, text = f"Connection to {host} was completed successfully").pack()
            s.send(f"{filename}{SEPARATOR}{filesize}".encode())
            with open(filename, "rb") as file:
                ok = True
                while ok:
                    bytes_read = file.read(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    s.sendall(bytes_read)
            s.close()
            import time
            time.sleep(1.2)
            print("")
            print("")
            print(f"Your file has been successfully sent to {host} through port {port}")
            tk.Label(window, text = f"Your file has been successfully sent to {host} through port {port}").pack()
            print("")
        import time
        port = 5001
        root = tk.Tk()
        root.title("File")
        root.withdraw()
        file_path = filedialog.askopenfilename()
        file = str(file_path)
        send_file_function(file, str(host), int(port))
    except Exception as e:
        print(e)
        Label(window, text = str(e)).pack()


def receive_file():
    try:
        hostname = socket.gethostname()
        SERVER_HOST = socket.gethostbyname(hostname)
        SERVER_PORT = 5001

        BUFFER_SIZE = 1024 * 4

        SEPARATOR = "<SEPARATOR>"

        s = socket.socket()
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(5)
        Label(window, text = f"Listening as {SERVER_HOST}:{SERVER_PORT}").pack()
        client_socket, address = s.accept()
        Label(window, text = f"{address} is connected.").pack()
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        with open(filename, "wb") as f:
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)

        client_socket.close()
        current_folder = os.getcwd()
        file_location = str(current_folder) + "/" + str(filename)
        s.close()
        time.sleep(1.2)
        print(" ")
        print(" ")
        print(f"Your file has been received from {address} to {SERVER_HOST} through port {SERVER_PORT}.\nFile location: " + str(file_location) + "\n")
        Label(window, text= f"Your file has been received from {address} to {SERVER_HOST} through port {SERVER_PORT}.\nFile location: " + str(file_location) + "\n").pack()
    except Exception as e:
        print(e)
        Label(window, text = str(e)).pack()
send_file = tk.Button(
    window,
    text = "Send a File",
    command = send_file
)
send_file.pack()
receive_file = tk.Button(
    window,
    text = "Receive a File",
    command = receive_file  
)
receive_file.pack()

window.mainloop()
