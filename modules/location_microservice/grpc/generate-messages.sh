echo "generating messages..."
python -m grpc_tools.protoc -I./proto --python_out=./messages --grpc_python_out=./messages location.proto