from collections.abc import Callable, Iterable, Mapping
from typing import Any
import constRPC
import time
import threading
from context import lab_channel


class DBList:
    def __init__(self, basic_list):
        self.value = list(basic_list)

    def append(self, data):
        self.value = self.value + [data]
        return self
    
class AsyncDBCall(threading.Thread):
    def __init__(self,channel, server, message):
        threading.Thread.__init__(self)
        self.channel = channel
        self.server = server
        self.msglst = message
        self.returnValue = None
    def run(self):
        self.channel.send_to(self.server, self.msglst)  # send msg to server
        msgrcv = self.channel.receive_from(self.server)  # wait for response
        self.returnValue = msgrcv[1]
        print("This is the return Value: " + self.returnValue)


class Client:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.client = self.chan.join('client')
        self.server = None

    def run(self):
        self.chan.bind(self.client)
        self.server = self.chan.subgroup('server')

    def stop(self):
        self.chan.leave('client')

    async def append(self, data, db_list):
        assert isinstance(db_list, DBList)
        msglst = (constRPC.APPEND, data, db_list)  # message payload
        newThread = AsyncDBCall(self.chan, self.server, msglst)
        newThread.start()
        newThread.join()
        return newThread.returnValue # pass it to caller


class Server:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.server = self.chan.join('server')
        self.timeout = 3

    @staticmethod
    def append(data, db_list):
        assert isinstance(db_list, DBList)  # - Make sure we have a list
        return db_list.append(data)

    def run(self):
        self.chan.bind(self.server)
        while True:
            msgreq = self.chan.receive_from_any(self.timeout)  # wait for any request
            if msgreq is not None:
                client = msgreq[0]  # see who is the caller
                msgrpc = msgreq[1]  # fetch call & parameters
                if constRPC.APPEND == msgrpc[0]:  # check what is being requested
                    result = self.append(msgrpc[1], msgrpc[2])  # do local call
                    self.chan.send_to({client}, result)  # return response
                else:
                    pass  # unsupported request, simply ignore


import logging
from context import lab_logging
lab_logging.setup(stream_level=logging.INFO)

cl = Client()
cl.run()

base_list = DBList({'foo'})
result_list = cl.append('bar', base_list)

print("Result: {}".format(result_list.value))

cl.stop()