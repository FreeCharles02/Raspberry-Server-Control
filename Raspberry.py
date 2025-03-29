import struct
import serial
import os
import socket 
import netifaces
import time

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


# All available interfaces
host = get_non_loopback_ip()
# host = '127.0.0.1'
port = 9999

# TCP internet connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", port))
server.listen(1)

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.write(struct.pack('!BBBB', 0, 0, 0, 0))


def main():
    print("gettin connection...")
    client, addr = server.accept()
    print("got a connection")

    # Checks constantly for client data
    while True:
        # client.send("Hello from RaspberryPi".encode())

        buf = ''
        start = time.time()
        while (len(buf) < 4):
            buf = client.recv(4)
            if (time.time()-start) > 1:
                return socket.timeout

        lf, lb, rf, rb = struct.unpack('!BBBB', buf)
        print(f"\t{lf:3d}\t{rf:3d}\n\t{lb:3d}\t{rb:3d}\n\n")

        ser.write(struct.pack('!BBBB', lf, lb, rf, rb))


if __name__ == "__main__":
    while(True):
        try:
            main()
        except socket.timeout:
            time.sleep(0.1)
