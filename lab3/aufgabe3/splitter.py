#kriegt Sätze aus einer Datei und lädt Zeileweise Sätze raus
import pickle
import random
import sys
import time
import zmq
import constPipe

me = "Splitter"

src = constPipe.SRC1
prt = constPipe.PORT1

context = zmq.Context()
push_socket = context.socket(zmq.PUSH)  # create a push socket

address = "tcp://" + src + ":" + prt  # how and where to connect
push_socket.bind(address)  # bind socket to address

time.sleep(1)
with open("text.txt", "r") as text:
  lines = text.readlines()
  for line in lines:
    line = line.strip()
    if (len(line) == 0):
      continue
    else:
      push_socket.send(pickle.dumps((me, line)))