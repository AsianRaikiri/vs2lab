"""
Client and server using classes
"""

import logging
import socket

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))

    def serve(self):
        """ Serve echo """
        self.sock.listen(1)
        while self._serving:  # as long as _serving (checked after connections or socket timeouts)
            try:
                # pylint: disable=unused-variable
                (connection, address) = self.sock.accept()  # returns new socket and address of client
                while True:  # forever
                    data = connection.recv(1024)  # receive data from client
                    if not data:
                        break  # stop if client stopped
                    connection.send(data + "*".encode('ascii'))  # return sent data plus an "*"
                connection.close()  # close the connection
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")

    def telephoneBook(self,telephoneDatabase={"Adam": "125654", "Steve": "6504033"}):
        self._logger.info("Telephone Database initialized and server online.")
        self.sock.listen(1)
        while self._serving:
            try:
                (connection, address) = self.sock.accept()
                self._logger.info("Creating server...")
                while True:  
                    request = connection.recv(1024)
                    if not request:
                        break
                    requestString = request.decode("ascii")
                    if(requestString in telephoneDatabase):    
                        self._logger.info("Received a name and send response.")
                        connection.send(telephoneDatabase[requestString].encode("ascii"))
                    elif(requestString == "requestAll"):
                        self._logger.info("Send all telephone Data to Client.")
                        telephoneValues = ""  
                        for (telName, telNumber) in telephoneDatabase.items():
                            telephoneValues +=telName + ": " + telNumber + ", "
                        telephoneValues = telephoneValues[:-2]
                        connection.send(telephoneValues.encode("ascii"))
                    else:
                        self._logger.info("Invalid name received.")
                        connection.send("No Person in Database with that name".encode("ascii"))
                connection.close()
            except socket.timeout:
                pass
        self.sock.close()
        self._logger.info("Server down")



class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def call(self, msg_in="Hello, world"):
        """ Call server """
        self.sock.send(msg_in.encode('ascii'))  # send encoded string as data
        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('ascii')
        print(msg_out)  # print the result
        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return msg_out

    def close(self):
        """ Close socket """
        self.sock.close()

    def get(self,msg="Steve"):
        self.logger.info("Getting telephone Number of " + msg + ".")
        self.sock.send(msg.encode('ascii'))
        data = self.sock.recv(1024)
        result = data.decode("ascii")
        print(result)
        self.sock.close() 
        self.logger.info("Client down.")
        return result
    
    def getAll(self):
        self.logger.info("Getting all available telephone number.")        
        msg = "requestAll"
        self.sock.send(msg.encode('ascii'))
        data = self.sock.recv(1024)
        result = data.decode("ascii")
        print(result)
        self.sock.close() 
        self.logger.info("Client down.")
        return result