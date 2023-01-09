import os
import grpc
import person_pb2
import person_pb2_grpc


def getPersons():
    endpoint = os.getenv("PERSONS_SERVICE_ENDPOINT", "localhost:31000")
    channel = grpc.insecure_channel(endpoint)
    stub = person_pb2_grpc.PersonServiceStub(channel)

    response = stub.GetPersons(request=person_pb2.NoRequest())
    print(response)

    return response
