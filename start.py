#!/usr/bin/python
# -*- coding: UTF-8 -*-

from bot import Bot
from mqtt import MqttClient
from emoji import emojize
import time

def emoji (which):
	return emojize(":" + which + ":", use_aliases=True)

def onSubscribe(xbot, update):
	if str(update.message.chat_id) not in bot.getSubscribedUsers():
		message = update.message.from_user.first_name + ", Du hast Dich angemeldet " + emoji("heavy_check_mark") + "."
		bot.addSubscribedUser(str(update.message.chat_id))
	else:
		message = emoji("no_entry") + " Du bist bereits angemeldet."
	bot.sendText(chatId = update.message.chat_id, text = message)

def onUnsubscribe(xbot, update):
	if str(update.message.chat_id) in bot.getSubscribedUsers():
		message = "Erfolgreich abgemeldet " + emoji("x") + "."
		bot.removeSubscribedUser(str(update.message.chat_id))
	else:
		message = emoji("no_mobile_phones") + " Du warst nicht angemeldet."
	bot.sendText(chatId = update.message.chat_id, text = message)

def onMessage(xbot, update):
	bot.sendText(chatId = update.message.chat_id, text = "Du hast geschrieben:\n" + update.message.text, replyTo = update.message.message_id)

def onStatus(xbot, update):
	global mqtt
	message = time.strftime("%H:%M:%S") + "\nBot bereit"
	if(mqtt.isConnected()):
		message += "\nMQTT verbunden"
	else:
		message += "\nMQTT getrennt"
	if(str(update.message.chat_id) in bot.getSubscribedUsers()):
		message += "\nFeuerwehrservice abonniert"
	else:
		message += "\nFeuerwehrservice nicht abonniert"
	bot.sendText(chatId = update.message.chat_id, text = message, replyTo = update.message.message_id)

def onUnknown(xbot, update):
	bot.sendText(chatId = update.message.chat_id, text = "Entschuldige, das kann ich leider noch nicht.", replyTo = update.message.message_id)

def onMqttMessage(client, userdata, msg):
	global bot
	if(msg.topic == "/feuerwehr/alarm"):
		setSilent = False
		message = time.strftime("%H:%M:%S") + "\n"
		if(msg.payload == "0"):
			#message += "Melder erfolgreich zurückgesetzt"
			setSilent = True
		elif(msg.payload == "1"):
			message += emoji("fire") + " Einsatz " + emoji("fire_engine") + emoji("dash")
		else:
			message += "Komische Nachricht vom Melder erhalten. Melder prüfen!"
		for chatId in bot.getSubscribedUsers():
			bot.sendText(chatId = chatId, text = message, simulatesTyping=False, silent = setSilent)



mqtt = MqttClient(onMqttMessage)
mqtt.addTopic("/feuerwehr/alarm")
mqttIsConnected = False

bot = Bot(token = "123456789:sampleToken", onMessage = onMessage, onSubscribe = onSubscribe, onUnsubscribe = onUnsubscribe, onStatus = onStatus, onUnknown = onUnknown)


while 1:
	try:
		if(mqtt.isConnected() == False and mqttIsConnected == True): # war verbunden, jetzt nicht mehr
			print(time.strftime("%H:%M:%S") + ": MQTT getrennt")
		elif (mqtt.isConnected() == True and mqttIsConnected == False): # war getrennt, jetzt verbunden
			print(time.strftime("%H:%M:%S") + ": MQTT verbunden")
		mqtt.loop()
	except KeyboardInterrupt:
		bot.shutdown()
