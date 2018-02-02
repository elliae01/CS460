import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Establish IP and port for incoming connections
server_address = ('192.168.1.11', 10000)
print ( 'starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for client connection')
    connection, client_address = sock.accept()

    try:
        print('connection from client:  ', client_address)

        # Receive and transmit data
        while True:
            data = connection.recv(15)
            print ('received "%s"' % data)
            if data:
                print('Transmitting data to client')
                message = 'Received Data'
                # Encode message
                message_as_bytes = str.encode(message)
                type(message_as_bytes)
                # Transmit all data back to client
                connection.sendall(message_as_bytes)
            else:
                print >> sys.stderr, 'finished received data from client: ', client_address
                break

    finally:
        # close client connection
        connection.close()