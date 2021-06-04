FROM python:3.7

# RUN apt-get update -y && \
#     apt-get install -y python-pip python-dev && \
#     pip install --upgrade pip

WORKDIR /app
COPY requirements.txt requirements.txt
RUN --mount=type=ssh pip install -r requirements.txt
