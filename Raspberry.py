import struct
import serial
import os
import socket 


host = '172.20.10.4' # All available interfaces
port = 9999 # Non privledged port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP internet connection
server.bind(("", port)) # Establishes connection between IP and port

server.listen(1)
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.write(struct.pack('!bbbb', 0, 0, 0, 0))

print("gettin connection...")
client, addr = server.accept()
print("got a connection")


#Checks constantly for client data
while True: 
#    client.send("Hello from RaspberryPi".encode())

    buf = '';
    while len(buf) < 4:
        buf = client.recv(4)
    lf, lb, rf, rb = struct.unpack('!bbbb', buf[:4])

    print(f"\tA: {lf}\n" +
          f"\tB: {lb}\n" +
          f"\tC: {rf}\n" +
          f"\tD: {rb}\n")


    ser.write(struct.pack('!bbbb', lf, lb, rf, rb))
