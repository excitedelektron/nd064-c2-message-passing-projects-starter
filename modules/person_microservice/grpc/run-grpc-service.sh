./generate-messages.sh

echo  'running server...'
export PYTHONPATH=$BASEPATH/grpc/messages:$BASEPATH/rest/
python ./services/main.py