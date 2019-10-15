#!/usr/bin/env python3

import cherrypy
import paho.mqtt.client as mqtt
import configparser

action2payload = {
        '1': 'single',
        '2': 'double',
        '3': 'long'
        }

topic = "TBD"

class MYSTROM2MQTT(object):
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client

    @cherrypy.expose
    def index(self):
        return "OK"

    @cherrypy.expose
    def mystrom2mqtt(self, mac=None, action=None, battery=None):
        
        payload = action2payload[action]

        self.mqtt_client.publish(topic, payload=payload)

        return "OK"

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("/config/config.ini")

    username  = config['mqtt-server']['username']
    password  = config['mqtt-server']['password']
    mqtt_host = config['mqtt-server']['host']
    mqtt_port = int(config['mqtt-server']['port'])
    client_id = config['mqtt-server']['client_id']
    ca_certs  = config['mqtt-server']['ca_certs']

    listen_addr = config['http']['listen_addr']
    listen_port = int(config['http']['listen_port'])

    mqtt_client = mqtt.Client(client_id=client_id)
    mqtt_client.username_pw_set(username, password=password)
    mqtt_client.tls_set(ca_certs=ca_certs)
    mqtt_client.connect(mqtt_host, mqtt_port, 60)

    cherrypy.config.update({'server.socket_host': listen_addr})
    cherrypy.config.update({'server.socket_port': listen_port})

    cherrypy.quickstart(
            MYSTROM2MQTT(
                mqtt_client
                )
            )

    mqtt_client.disconnect()
