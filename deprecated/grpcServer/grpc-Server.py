#!/usr/bin/env python3
from concurrent import futures
from PIL import Image
import io,base64
import grpc
import audioID_pb2
import audioID_pb2_grpc

uploadDir = '/Users/ayu/Study/Courses/CSCI5253/TermProject/storage/'

class Server(audioID_pb2_grpc.audioIDgrpcServicer):
    def __init__(self):
        pass

    def addNewSong(self,request,context):
        print(f"Receive addNewSong")
        with open(uploadDir+request.name,'wb') as f:
            f.write(io.BytesIO(request.audio).getbuffer())
        return audioID_pb2.addNewSongReply('Request received!')

        
    # def doAdd(self, request, context):
    #     print(f"Receive doAdd({request.a},{request.b})")
    #     return lab6_pb2.addReply(c = request.a+request.b )
    
    # def doDotproduct(self, request, context):
    #     print(f"Receive doDotproduct")
    #     c = 0
    #     for a,b in zip(request.a,request.b):
    #         c += a*b
    #     return lab6_pb2.dotproductReply(c = c)
    
    # def doRawimage(self,request,context):
    #     print(f"Receive raw image")
    #     img = Image.open(io.BytesIO(request.img))
    #     return lab6_pb2.imageReply(width=img.size[0],height=img.size[1])
    
    # def doJsonimage(self,request,context):
    #     print(f"Receive json image")
    #     img  = Image.open(io.BytesIO(base64.b64decode(request.img.encode())))
    #     return lab6_pb2.imageReply(width=img.size[0],height=img.size[1])

def serve():    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    audioID_pb2_grpc.add_audioIDgrpcServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:9999')
    server.start()
    server.wait_for_termination()

serve()