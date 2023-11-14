import rpc
import logging
import time

from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)

def printCallback(result):
    print("Result: {}".format(result.value))

cl = rpc.Client()
cl.run()

base_list = rpc.DBList({'foo'})
cl.append(data='bar',db_list= base_list,printCallback= printCallback)
for i in range(15):
    print(i)
    time.sleep(1)

cl.stop()
