# Instructions

`pip install grpcio-tools grpcio`

`python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=../messages Person.proto`