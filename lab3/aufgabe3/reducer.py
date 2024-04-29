# Ein Reducer sammelt die Wörter und zählt diese Wörter
import pickle
import sys
import time
import zmq
import constPipe

me = "Reducer " + str(sys.argv[1])
address1 = "tcp://" + constPipe.SRC2 + ":" + constPipe.PORT2 
address2 = "tcp://" + constPipe.SRC3 + ":" + constPipe.PORT3  

context = zmq.Context()
pull_socket = context.socket(zmq.PULL)  # create a pull socket
address = address1 if str(sys.argv[1]) == "1" else address2
pull_socket.bind(address)
print("{} started".format(me))
i = 0
while True:
    work = pickle.loads(pull_socket.recv())
    word = work[1]
    print("Received {} from {}".format(work[1], work[0]))
    i += 1
    print("{} words counted.".format(i))
