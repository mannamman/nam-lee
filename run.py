import RPi.GPIO as GPIO
import time
import spidev
import paho.mqtt.publish as publish

GPIO.setmode(GPIO.BCM)
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 50000

brokerIP = '192.168.43.20'
D = 240
gap = 80
MAX = 30
#30
MIN = 10
COUNT = 30
#30
SIZE = 2
#base v1

class sensor:
    def __init__(self):
        self.arr = list()
    def append(self, x):
        self.arr.append(x)
    def get_avg(self):
        return sum(self.arr)/SIZE
    def pop(self):
        self.arr.pop(0)

def read_spi_adc(adcChannel):
    adcValue = 0
    buff = spi.xfer2([1,(8+adcChannel)<<4,0])
    adcValue = ((buff[1]&3)<<8)+buff[2]
    return adcValue

def determin(v1,v2,v3):
    global status
    if(v1>abs(v3-gap) and v1>abs(v2-gap) and hasPeople == True):#down
        status = -1
    if(abs(v1-v3)<gap and abs(v1-v2)<gap and hasPeople == True):#stop
        status = 0
    elif(hasPeople == False):#up
        status = 1
    send_msg()
    
def send_msg():
    #payload = str(v1)+" "+str(v2)+" "+str(v3)+" "+str(status)
    global COUNT
    global status
    msgs = [
        {
            'topic' : '/order',
            'payload' : status,
            'qos' : 0
    }
    ]
    if((COUNT+status)<=MAX-1 and (COUNT+status)>=MIN+1):
        publish.multiple(msgs,hostname=brokerIP)
        COUNT = COUNT+status
    if((COUNT == MAX-1 and status ==1)and(COUNT == MIN+1 and status ==-1)):
        publish.multiple(msgs,hostname=brokerIP)
        COUNT = COUNT+status
        
sensor1 = sensor()
sensor2 = sensor()
sensor3 = sensor()
try:
    hasPeople = False
    status = 0 #1 up 0 stop -1 down
    while True:
        v1 = read_spi_adc(0)
        v2 = read_spi_adc(1)
        v3 = read_spi_adc(2)
        print(v1,v2,v3,end=" ")
        if(len(sensor1.arr)==SIZE):
            if(sensor1.get_avg()>D):
                hasPeople = True
            else:
                hasPeople = False
            determin(sensor1.get_avg(),sensor2.get_avg(),sensor3.get_avg())
            print("v1 : {}, v2 : {}, v3 : {}, haspeople : {}, status : {}, count : {}".
                  format(sensor1.get_avg(),sensor2.get_avg(),sensor3.get_avg(),hasPeople,status,COUNT))
            sensor1.pop()
            sensor2.pop()
            sensor3.pop()
        else:
            sensor1.append(v1)
            sensor2.append(v2)
            sensor3.append(v3)
        time.sleep(0.5)
finally:
    GPIO.cleanup()
    spi.close()
