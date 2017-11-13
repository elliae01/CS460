import time
import threading

import ClientTransport

# This serves as a test function to run on the helloClient
# Will utlize connection2 and transmit via TCP


def hello():
    message = 'The sky is the limit'
    ClientTransport.connection(message)
    #3 more times
    message2 = 'The sky is the limit'
    repeat = 3

    while repeat > 0:
        time.sleep(2)
        ClientTransport.connection(message2)
        repeat -= 1


if __name__ == '__main__':
    hello()
