import struct
import serial
import os
import socket 
import netifaces
import time
from adafruit_servokit import ServoKit
import board
import adafruit_pca9685
from adafruit_motor import servo
import busio
# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=8)

i2c=busio.I2C(board.SCL, board.SDA)
while not i2c.try_lock():
    pass
devices = i2c.scan()
print("Devices Found: ", devices)
i2c.unlock()

pca1 = adafruit_pca9685.PCA9685(i2c, address=0x40) 

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
        while (len(buf) < 12):
            buf = client.recv(12)
            if (time.time()-start) > 1:
                return socket.timeout

        rb, rf, lb, lf, lb_button, rb_button, dpad_value_1, dpad_value_2, lt_trigger, rt_trigger, a, y = struct.unpack('!BBBBBBBBBB', buf)
        if(dpad_value_1 == 1):
            kit.continuous_servo[1].throttle = 1
            kit.continuous_servo[0].throttle = -1
        elif(dpad_value_1 == -1):
            kit.continuous_servo[1].throttle = -1
            kit.continuous_servo[0].throttle = 1
        else:
            kit.continuous_servo[1].throttle = 0
            kit.continuous_servo[0].throttle = 0

        if(dpad_value_2 == 1):     
            kit.servo[2].angle = 180
        elif(dpad_value_2 == -1):
            kit.servo[2].angle = 0
        if(y == 1):
            kit.servo[3].angle = 180
        else:
            kit.servo[3].angle = 0
        if(a == 1):
            kit.servo[4].angle = 180
        else:
            kit.servo[4].angle = 0
                
        ser.write(struct.pack('!BBBB', lf, lb, rf, rb))


if __name__ == "__main__":
    while(True):
        try:
            main()
        except socket.timeout:
            time.sleep(0.1)
