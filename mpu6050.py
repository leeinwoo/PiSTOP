#!/usr/bin/python
import smbus
import math
import time

# Power management registers

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

x_queue = []
y_queue = []
z_queue = []

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1)
address = 0x68     

# Now wake the 6050 up as it starts in sleep mode
while 1:    
    bus.write_byte_data(address, power_mgmt_1, 0)
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)
    
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)
    
    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0

    if(len(x_queue)<10):
        x_queue.append(gyro_xout/131)
        y_queue.append(gyro_yout/131)
        z_queue.append(gyro_zout/131)
    else:
        x_queue.pop(0)
        y_queue.pop(0)
        z_queue.pop(0)
        x_queue.append(gyro_xout/131)
        y_queue.append(gyro_yout/131)
        z_queue.append(gyro_zout/131)
        x_sum=0
        y_sum=0
        z_sum=0
        for i in range(10):
            x_sum += x_queue[i]
            y_sum += y_queue[i]
            z_sum += z_queue[i]
        print(x_sum, y_sum, z_sum)
        if( x_sum > 50 and x_sum < 300):
            if( y_sum > 800 and y_sum < 1200):
                if( z_sum > 50 and z_sum < 300):
                    print("decide!!!")
                    break
    #print (accel_xout, accel_xout_scaled, accel_yout, accel_yout_scaled, accel_zout, accel_zout_scaled)
    #print ("x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
    #print ("y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
    time.sleep(0.1)
