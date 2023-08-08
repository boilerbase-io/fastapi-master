# Pull base image
FROM python:3.10

# Install dependencies
COPY requirements.txt requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN alembic upgrade head

COPY . /vision_image
WORKDIR /vision_image

EXPOSE 8000
