#!/bin/sh

echo "Running grpc service"
(cd grpc && ./run-grpc-service.sh&)

echo "Running kafka consumer"
(export PYTHONPATH=/workspace/rest/ && cd kafka_consumer && python consumer.py&)

echo "Running flask application"
(cd rest && flask run --host 0.0.0.0 --port 5001)