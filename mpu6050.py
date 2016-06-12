#!/usr/bin/python
import smbus
import math
import time

# Power management registers

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

bus = smbus.SMBus(1)
address = 0x68

topLocate=False
decide=False

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

def get_value():
    x_queue = []
    y_queue = []
    z_queue = []   

    while 1:
        bus.write_byte_data(address, power_mgmt_1, 0)        
        gyro_xout = read_word_2c(0x43)
        gyro_yout = read_word_2c(0x45)
        gyro_zout = read_word_2c(0x47)
        
        if(len(x_queue)<20):
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
            for i in range(20):
                x_sum += x_queue[i]
                y_sum += y_queue[i]
                z_sum += z_queue[i]
            global topLocate
            print(y_sum)
            if(y_sum<-500):
                print("unlock")
                topLocate=True
                x_queue.clear()
                y_queue.clear()
                z_queue.clear()
            if(topLocate==True):
                if( x_sum > -500 and x_sum < 2000):
                    if( y_sum > 700 and y_sum < 7000):
                        if( z_sum > -500 and z_sum < 2000):
                            print("!!!!!!!!!!!!!!!!decide!!!!!!!!!!!!!!")
                            global decide
                            decide = True                        
                            break            
        time.sleep(0.08)

def set_decide(tf):
    global decide
    decide=tf

def is_decide():
    return decide
