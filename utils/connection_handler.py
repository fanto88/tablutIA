import socket
import json


class ConnectionHandler:
    def __init__(self, port=80, host="localhost"):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__port = port
        self.__host = host

    def socket(self):
        return self.__socket

    def port(self, port=None):
        if port is None:
            return self.__port
        self.__port = port
        return self

    def host(self, host=None):
        if host is None:
            return self.__host
        self.__host = host
        return self

    def connect(self):
        try:
            self.__socket.connect((self.__host, self.__port))
            return self
        except Exception as exception:
            print("Can't connect to localhost %s at port %d. Exception is %s" % (self.__host, self.__port, exception))

    def disconnect(self):
        self.__socket.close()
        return self

    # Send int to the server
    def send_int(self, integer):
        bytes_to_send = integer.to_bytes(4, byteorder='big')
        return self.__socket.send(bytes_to_send)  # Send the integer, converted in bytes, to the server

    # Send string to the server
    def send_string(self, message):
        message = json.dumps(message)  # Convert message to JSON
        self.send_int(len(message))  # Send message length to the server
        self.__socket.sendall(message.encode())  # Send the string to the server
        return self

    # Read string from server
    def read_string(self):
        string_length = self.read_int()  # Read the length of the string from an integer sent by the server itself
        message = self.__socket.recv(string_length, socket.MSG_WAITALL)  # Read the actual string
        message = message.decode('utf-8')  # Decode the message
        return json.loads(message)  # Convert object to JSON

    # Read integer 4Bytes from the server
    def read_int(self):
        read_bytes = b''  # Create empty bytes
        while len(read_bytes) < 4:  # Wait for all the bytes
            data = self.__socket.recv(4 - len(read_bytes))
            if not data:
                break
            read_bytes += data
        return int.from_bytes(read_bytes, byteorder='big')  # Converts bytes to int
