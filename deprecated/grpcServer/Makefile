#
# Generate gRPC 
#

grpc:
	protoc --python_out=. audioID.proto
	python3 -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ audioID.proto

# tools:
# 	pip install grpcio grpcio_tools

clean::
	-rm -f audioID_pb2.py audioID_pb2_grpc.py