import time
from Misc import helloClient


#This serves as a test function to run on the helloClient
#Will utlize connection2 and transmit via TCP
def hello1():
    message ='The sky is the limit'
    helloClient.connection(message)
    message2 = 'The sky is the limit'
    repeat = 8

    while repeat >0:
        time.sleep(2)
        helloClient.connection(message2)
        repeat-=1

if __name__=='__main__':
    hello1()


        
