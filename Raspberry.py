import struct
import serial
import os
import socket 
import netifaces

def get_non_loopback_ip():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface == 'lo' or interface.startswith('docker'):
            continue
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for ip_data in addresses[netifaces.AF_INET]:
                ip_address = ip_data['addr']
                if ip_address != '127.0.0.1':
                    return ip_address
    return None

host = get_non_loopback_ip() # All available interfaces
port = 9999 # Non privledged port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP internet connection
server.bind(("", port)) # Establishes connection between IP and port

server.listen(1)
ser = serial.Serial('/dev/ttyACM0', 9600)
#ser.write(struct.pack('!bbbb', 0, 0, 0, 0))

print("gettin connection...")
client, addr = server.accept()
print("got a connection")


#Checks constantly for client data
while True: 
#  client.send("Hello from RaspberryPi".encode())

    buf = '';
    while len(buf) < 16:
        buf = client.recv(16)
    lf, lb, rf, rb = struct.unpack('!iiii', buf[:16])

    print(f"\tA: {lf}\n" +
          f"\tB: {lb}\n" +
          f"\tC: {rf}\n" +
          f"\tD: {rb}\n")


    ser.write(struct.pack('!iiii', lf, lb, rf, rb))
