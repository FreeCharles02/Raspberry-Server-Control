import struct
import serial
import os
import socket 


host = '192.168.1.253' # All available interfaces
port = 9999 # Non privledged port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP internet connection
server.bind((host, port)) # Establishes connection between IP and port

server.listen(1)
ser = serial.Serial('/dev/ttyACM0', 9600)

#Checks constantly for client data
while True: 
    client, addr = server.accept()
    client.send("Hello from RaspberryPi".encode())
    lf = client.recv(1)
    lb = client.recv(1)
    rf = client.recv(1)
    rb = client.recv(1)

    

    ser.write(struct.pack('!bbbb', lf, lb, rf, rb))

