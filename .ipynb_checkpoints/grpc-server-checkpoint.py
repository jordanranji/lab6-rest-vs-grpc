#!/usr/bin/env python3
import argparse
import base64
import io
from concurrent import futures

import grpc
from PIL import Image

import lab6_pb2
import lab6_pb2_grpc

MAX_MSG = 50 * 1024 * 1024  # default limit is 4MB


def dims(data):
    try:
        img = Image.open(io.BytesIO(data))
        return lab6_pb2.ImageReply(width=img.size[0], height=img.size[1])
    except Exception as e:
        print("image error:", repr(e))
        return lab6_pb2.ImageReply(width=0, height=0)


class Lab6Servicer(lab6_pb2_grpc.Lab6Servicer):
    def Add(self, request, context):
        return lab6_pb2.AddReply(sum=request.a + request.b)

    def RawImage(self, request, context):
        return dims(request.img)

    def DotProduct(self, request, context):
        total = sum(x * y for x, y in zip(request.a, request.b))
        return lab6_pb2.DotProductReply(dotproduct=total)

    def JsonImage(self, request, context):
        try:
            return dims(base64.b64decode(request.image))
        except Exception as e:
            print("jsonimage error:", repr(e))
            return lab6_pb2.ImageReply(width=0, height=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gRPC server')
    parser.add_argument('-p', '--port', type=int, default=50051)
    args = parser.parse_args()

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[('grpc.max_receive_message_length', MAX_MSG),
                 ('grpc.max_send_message_length', MAX_MSG)])
    lab6_pb2_grpc.add_Lab6Servicer_to_server(Lab6Servicer(), server)
    server.add_insecure_port(f'[::]:{args.port}')
    server.start()
    print(f"gRPC server listening on port {args.port}")
    server.wait_for_termination()