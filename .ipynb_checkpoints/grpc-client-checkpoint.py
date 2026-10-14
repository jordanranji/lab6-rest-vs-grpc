#!/usr/bin/env python3
import argparse
import base64
import random
import time

import grpc

import lab6_pb2
import lab6_pb2_grpc

IMG_FILE = 'Flatirons_Winter_Sunrise_edit_2.jpg'
MAX_MSG = 50 * 1024 * 1024


def doAdd(stub, debug=False):
    reply = stub.Add(lab6_pb2.AddMsg(a=5, b=10))
    if debug:
        print(reply)


def doRawImage(stub, debug=False):
    img = open(IMG_FILE, 'rb').read()
    reply = stub.RawImage(lab6_pb2.ImageMsg(img=img))
    if debug:
        print(reply)


def doDotProduct(stub, debug=False):
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]
    reply = stub.DotProduct(lab6_pb2.DotProductMsg(a=a, b=b))
    if debug:
        print(reply)


def doJsonImage(stub, debug=False):
    img = open(IMG_FILE, 'rb').read()
    encoded = base64.b64encode(img).decode('utf-8')
    reply = stub.JsonImage(lab6_pb2.JsonImageMsg(image=encoded))
    if debug:
        print(reply)


parser = argparse.ArgumentParser(description='gRPC client for measuring server operations')
parser.add_argument('host')
parser.add_argument('cmd', choices=['add', 'rawImage', 'dotProduct', 'jsonImage'])
parser.add_argument('reps', type=int)
parser.add_argument('-p', '--port', type=int, default=50051)
parser.add_argument('-d', '--debug', action='store_true')
args = parser.parse_args()

funcs = {'add': doAdd, 'rawImage': doRawImage,
         'dotProduct': doDotProduct, 'jsonImage': doJsonImage}
fn = funcs[args.cmd]

channel = grpc.insecure_channel(
    f"{args.host}:{args.port}",
    options=[('grpc.max_receive_message_length', MAX_MSG),
             ('grpc.max_send_message_length', MAX_MSG)])
stub = lab6_pb2_grpc.Lab6Stub(channel)

print(f"Running {args.reps} reps against {args.host}:{args.port}")
start = time.perf_counter()
for _ in range(args.reps):
    fn(stub, debug=args.debug)
delta = ((time.perf_counter() - start) / args.reps) * 1000
print("Took", delta, "ms per operation")