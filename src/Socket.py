import socket
import math


class Socket(socket.socket):

    def recvall(self, length=math.inf):
        """
        Receive specified amount of data from the socket.

        :param length: Number of bytes to receive.
        :return: Received data.
        """
        received_data = b""

        while len(received_data) < length:
            remaining_length = length - len(received_data)
            received_chunk = self.recv(remaining_length)
            if not received_chunk:
                # Connection closed or no more data
                break
            received_data += received_chunk
        return received_data
