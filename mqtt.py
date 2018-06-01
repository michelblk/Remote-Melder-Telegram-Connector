#!/usr/bin/python
# -*- coding: UTF-8 -*-
import paho.mqtt.client as paho

class MqttClient:
	def __init__ (self, onMessage):
		self.__client = paho.Client("TelegramBot", clean_session=False, transport="tcp")
		self.__client.username_pw_set("admin", password="admin")
		self.__client.on_connect = self.__on_connect
		self.__client.on_disconnect = self.__on_disconnect
		self.__client.on_message = onMessage
		self.__client.connect("127.0.0.1", port=1883, keepalive=60)
		self.__isConnected = False

	def __on_connect(self, client, userdata, flags, rc):
		print("MQTT Verbunden mit Code: " + str(rc))
		if(rc == 0):
			self.__isConnected = True
		else:
			self.__isConnected = False

	def __on_disconnect(self, client, userdata, rc):
		self.__isConnected = False

	def __subscribe (self, path):
		self.__client.subscribe(path)

	def sendMessage (self, topic, payload):
		print topic + "->" + payload
		self.__client.publish(topic, payload=str(payload), qos=1, retain=True)

	def addTopic (self, topicPath):
		self.__subscribe(topicPath)

	def isConnected (self):
			return self.__isConnected

	def loop (self):
		self.__client.loop_forever()
