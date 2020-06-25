import paho.mqtt.publish as publish
import time
brokerIP = '192.168.43.20'
x = int(input("nums : "))
status = int(input("status : "))
#arr = []
determin = 29
for i in range(x):
    print(i+1," ",status)
    #arr.append(status)
    #determin = sum(arr)
    #if(determin>=23 and determin<=-23):
        #continue
    msgs = [
    {
        'topic' : '/order',
        'payload' : status,
        'qos' : 0
    }
    ]
    publish.multiple(msgs,hostname=brokerIP)
    time.sleep(2)
