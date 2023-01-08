import grpc
import location_pb2
import location_pb2_grpc


def getLocations(person_id, start_date, end_date):
    channel = grpc.insecure_channel("localhost:50001")
    stub = location_pb2_grpc.LocationServiceStub(channel)

    response = stub.GetLocations(
        request=location_pb2.LocationRequest(
            person_id=int(person_id),
            start_date=start_date.strftime("%Y-%m-%d %H:%M:%S"),
            end_date=end_date.strftime("%Y-%m-%d %H:%M:%S"),
        )
    )

    print(response)

    return response
