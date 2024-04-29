# Ein Mapper kriegt einen Satz und zerlegt diese in Wörter
# Gibt die Wörter nach einem Schema genau einem Reducer als Nachricht
import pickle
import sys
import time
import zmq
import constPipe

me = "Mapper " + str(sys.argv[1])
address1 = "tcp://" + constPipe.SRC1 + ":" + constPipe.PORT1  
address2 = "tcp://" + constPipe.SRC2 + ":" + constPipe.PORT2  
address3 = "tcp://" + constPipe.SRC3 + ":" + constPipe.PORT3

context = zmq.Context()
pull_socket = context.socket(zmq.PULL)  # create a pull socket
push_socket_1 = context.socket(zmq.PUSH)
push_socket_2 = context.socket(zmq.PUSH)
pull_socket.connect(address1) 
push_socket_1.connect(address2) 
push_socket_2.connect(address3)


print("{} started".format(me))

while True: 
    work = pickle.loads(pull_socket.recv())
    sentence = str(work[1])
    sentence = sentence.replace(".", "")
    listOfWords = sentence.split()
    print("Sentence: {}".format(str(listOfWords)))
    for word in listOfWords:
        if(len(word) < 6):
            push_socket_1.send(pickle.dumps((me, word)))
            print("Sent word {} to Reducer 1".format(word))
        else:
            push_socket_2.send(pickle.dumps((me, word)))
            print("Sent word {} to Reducer 2".format(word))