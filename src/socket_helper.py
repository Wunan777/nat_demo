def recvall(socket, length=-1):
    """
    Receive specified amount of data from the socket.

    :param length: Number of bytes to receive.
    :return: Received data.
    """
    received_data = b""
    if length == -1:
        while True:
            received_chunk = socket.recv(1024)
            print("received_chunk: {}".format(received_chunk))
            if not received_chunk:
                # Connection closed or no more data
                break
            received_data += received_chunk

            if len(received_chunk) < 1024:
                break

    else:

        while len(received_data) < length:
            remaining_length = length - len(received_data)
            received_chunk = socket.recv(remaining_length)
            if not received_chunk:
                # Connection closed or no more data
                break
            received_data += received_chunk

    return received_data
