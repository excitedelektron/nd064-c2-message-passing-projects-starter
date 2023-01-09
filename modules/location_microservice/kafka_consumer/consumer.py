import json
import os
import time
import logging
from typing import Dict
from kafka import KafkaConsumer

from app.config import config_by_name
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

KAFKA_SERVER = os.getenv("KAFKA_CONSUMER_SERVER", "localhost:9092")
print("Running consumer, kafka server:", KAFKA_SERVER)
consumer = KafkaConsumer("Locations", bootstrap_servers=[KAFKA_SERVER])

print("Consumer created...")


def get_db_session():
    SQLALCHEMY_DATABASE_URI = config_by_name["test"].SQLALCHEMY_DATABASE_URI

    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    Base = declarative_base()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()

    return session


def save(location: Dict, session: sessionmaker):
    validation_results: Dict = LocationSchema().validate(location)
    if validation_results:
        logger.warning(f"Unexpected data format in payload: {validation_results}")
        raise Exception(f"Invalid payload: {validation_results}")

    new_location = Location()
    new_location.person_id = location["person_id"]
    new_location.creation_time = location["creation_time"]
    new_location.coordinate = ST_Point(location["latitude"], location["longitude"])

    session.add(new_location)
    session.commit()


while True:
    records = consumer.poll(10000, 500)
    if records:
        for message in records.values():
            for msg in message:
                print(msg.value)
                value = msg.value.decode("utf-8")
                json_val = json.loads(value)

                print(json_val)
                session = get_db_session()

                print("saving to database")
                save(json_val, session)
    else:
        print("waiting for data...")
        time.sleep(5)
