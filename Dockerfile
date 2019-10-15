FROM alpine:3.10

RUN mkdir -p /app /config
RUN apk --no-cache add \
    python3 \
    ca-certificates \
  && pip3 install \
    paho-mqtt \
    CherryPy

COPY mystrom2mqtt.py /app 
RUN chmod +x /app/mystrom2mqtt.py

CMD ["/app/mystrom2mqtt.py"]
