./generate-messages.sh

echo  'running server...'
export PYTHONPATH=$BASEPATH/location_microservice/grpc/messages:$BASEPATH/location_microservice/rest/
python services/main.py