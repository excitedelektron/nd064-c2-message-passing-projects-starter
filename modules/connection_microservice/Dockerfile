FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5002 50002

COPY . .

RUN (cd app/grpc && ./generate-messages.sh)
ENV PYTHONPATH /app/grpc/messages
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5002"]