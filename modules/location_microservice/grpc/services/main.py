import time
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc

from app.udaconnect.models import Location
from app.config import config_by_name

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_db_session():
    SQLALCHEMY_DATABASE_URI = config_by_name["test"].SQLALCHEMY_DATABASE_URI

    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    Base = declarative_base()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()

    return session


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def GetLocations(self, request, context):
        session = get_db_session()
        response = location_pb2.LocationsMessage()

        locations: List = (
            session.query(Location)
            .filter(Location.person_id == request.person_id)
            .filter(Location.creation_time < request.end_date)
            .filter(Location.creation_time >= request.start_date)
            .all()
        )

        for location in locations:
            pretty_location = {
                "longitude": location.longitude,
                "latitude": location.latitude,
                "creation_time": location.creation_time.strftime("%m/%d/%Y"),
                "id": location.id,
                "person_id": location.person_id,
            }
            response.locations.append(location_pb2.LocationMessage(**pretty_location))

        print(response)

        return response


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

port = 31001
print("Server starting on port", port)
server.add_insecure_port("[::]:" + str(port))
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
