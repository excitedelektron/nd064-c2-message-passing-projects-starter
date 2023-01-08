FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000 50000

RUN mkdir -p /workspace
WORKDIR /workspace
COPY . .

ENV BASEPATH /workspace

CMD ["./run.sh"]