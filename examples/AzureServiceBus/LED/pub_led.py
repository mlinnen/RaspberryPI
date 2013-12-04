# uncomment the following lines to enable visual studio remote debugging
#import ptvsd
#ptvsd.enable_attach(secret = 'vs2013')

from azure.servicebus import *
import azconfig

# Read any configuration
config = azconfig.AzureConfig()
config.read()

def menu():
    print "1 - Turn LED on"
    print "2 - Turn LED off"
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

bus_service = ServiceBusService(service_namespace=config.AZURE_SERVICEBUS_NAMESPACE, account_key=config.AZURE_SERVICEBUS_ACCESS_KEY, issuer=config.AZURE_SERVICEBUS_ISSUER)
count = 1
while True:
    menuOption = menu()
    if menuOption == 2:
        msg = Message('Msg ' + str(count), custom_properties={'led':0})
        bus_service.send_topic_message('blinky', msg)
        print "message sent to turn off LED"
    elif menuOption == 1:
        msg = Message('Msg ' + str(count), custom_properties={'led':1})
        bus_service.send_topic_message('blinky', msg)
        print "message sent to turn on LED"
    else:
        break
    count = count +1



