import grpc
import location_pb2
import location_pb2_grpc

channel = grpc.insecure_channel("localhost:50001")
stub = location_pb2_grpc.LocationServiceStub(channel)

response = stub.GetLocations(
    request=location_pb2.LocationRequest(
        person_id=1, start_date="2020-07-01 10:37:06", end_date="2020-08-15 10:37:06"
    )
)

print(response)
