import time
from concurrent import futures

import grpc
import person_pb2
import person_pb2_grpc

from app.udaconnect.models import Person
from app.config import config_by_name

from sqlalchemy import Column, Integer, String
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


class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    def GetPersons(self, request, context):
        session = get_db_session()
        response = person_pb2.PersonsMessage()

        for person in session.query(Person).all():
            person_props = vars(person)
            del person_props["_sa_instance_state"]
            response.persons.append(person_pb2.PersonMessage(**vars(person)))

        print(response)

        return response


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
person_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)

port = 50000
print("Server starting on port", port)
server.add_insecure_port("[::]:" + str(port))
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
