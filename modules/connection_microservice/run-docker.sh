docker run --rm -ti \
  --network host \
  -e DB_USERNAME="ct_admin" \
  -e DB_NAME="geoconnections" \
  -e DB_HOST="localhost" \
  -e DB_PORT="5432" \
  -e DB_PASSWORD="wowimsosecure" \
  excitedelektron/uda-connect-connection-microservice