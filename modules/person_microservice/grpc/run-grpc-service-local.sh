./generate-messages.sh

echo  'running server...'
export PYTHONPATH=$BASEPATH/person_microservice/grpc/messages:$BASEPATH/person_microservice/rest/
python ./services/main.py