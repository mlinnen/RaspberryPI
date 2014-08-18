#!/usr/bin/python
import paho.mqtt.publish as publish

def menu():
    print "1 - Ring Front Doorbell"
    print "2 - Ring Back Doorbell"
    print "Enter - Exit"
    result = 0
    while True:
        char = raw_input("Select an option from the menu:")
        if char == '1':
            result = 1
            break
        if char == '2':
            result = 2
            break
        else:
            result = 0
            break
    return result

while True:
    menuOption = menu()
    if menuOption == 1:
        publish.single("protosystemdemo/doorbell/ring", "1", hostname="test.mosquitto.org")
        print "message sent to ring the front doorbell"
    elif menuOption == 2:
        publish.single("protosystemdemo/doorbell/ring", "2", hostname="test.mosquitto.org")
        print "message sent to ring the back doorbell"
    else:
        break

