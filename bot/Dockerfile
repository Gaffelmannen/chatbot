FROM python:3.13.2
ENV IN_DOCKER_CONTAINER=True
ADD . /app
WORKDIR /app
RUN pip install --upgrade pip && \ 
    pip install -r requirements.txt
