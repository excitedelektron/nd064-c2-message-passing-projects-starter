import os
from kafka import KafkaProducer
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask import request, g

db = SQLAlchemy()


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="UdaConnect API", version="0.1.0")

    CORS(app)  # Set CORS for development

    @app.before_request
    def before_request():
        if request.endpoint == "UdaConnect_location_resource_2":
            KAFKA_SERVER = os.getenv("KAFKA_PRODUCER_SERVER", "localhost:9092")
            print("kafka producer connected to: ", KAFKA_SERVER)
            producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
            g.kafka_producer = producer

    register_routes(api, app)
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
