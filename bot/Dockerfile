##
## Step 1: Build
##
FROM python:3.13.2 AS builder
ENV IN_DOCKER_CONTAINER=True
ADD . /app
WORKDIR /app
RUN apt update && \
    apt upgrade -y && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

##
## Step 2: Production staging
##
FROM python:3.13.2
COPY --from=builder . .
WORKDIR /app
#CMD ["/bin/bash"]