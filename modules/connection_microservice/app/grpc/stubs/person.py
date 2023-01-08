import grpc
import person_pb2
import person_pb2_grpc


def getPersons():
    channel = grpc.insecure_channel("localhost:50000")
    stub = person_pb2_grpc.PersonServiceStub(channel)

    response = stub.GetPersons(request=person_pb2.NoRequest())
    print(response)

    return response
