import socket



def connection(message):
    print('Begin')
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #208.103.44.151 is the router address that will forward 10000
    # to the computer running the server
    server_address = ('208.103.44.151', 10000)
    print('connecting to %s port %s' % server_address)
    sock.connect(server_address)

    try:
        # Encode data
        message_as_bytes = str.encode(message)
        type(message_as_bytes)  # ensure it is byte representation

        # Decode data, not needed for now
        my_decoded_str = message_as_bytes.decode()
        type(my_decoded_str)

        # Print and send all data
        print('Transmitting From Client Transport"%s"' % message)
        sock.sendall(message_as_bytes)

        # Look for server response
        data_received = 0
        data_expected = len(message)

        while data_received < data_expected:
            data = sock.recv(16)
            data_received += len(data)
            print('received "%s"' % data)

    finally:
        print('closing socket')
        sock.close()
