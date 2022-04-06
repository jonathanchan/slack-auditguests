FROM python:3.9-alpine

WORKDIR /build

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "./guest_channels.py"]
