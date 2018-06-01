#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import BadRequest
import csv
from settings import Settings
from emoji import emojize
import time
from random import randint

# set UTF-8 Charset
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

class Bot:
	def __init__ (self, token, onMessage, onSubscribe, onUnsubscribe, onStatus, onUnknown):
		self.__bot = telegram.Bot(token=token)
		self.__updater = Updater(token=token)
		self.__dispatcher = self.__updater.dispatcher
		self.__subscribedUsers = []
		self.__onMessage = onMessage
		self.__onSubscribe = onSubscribe
		self.__onUnsubscribe = onUnsubscribe
		self.__onStatus = onStatus
		self.__onUnknown = onUnknown
		self.__start()

	def __start(self):
		self.__readSaveFile()

		# welcome user
		for chat in self.getSubscribedUsers():
			try:
				self.sendText(chatId=chat, text = self.emoji("heart_eyes") + " ich stehe Dir wieder zur Verfügung.", silent = True)
			except BadRequest:
				print("UserID " + chat + " konnte nicht gefunden werden")

		# Event-Handlers
		self.__dispatcher.add_handler(CommandHandler('subscribe', self.__onSubscribe))
		self.__dispatcher.add_handler(CommandHandler('unsubscribe', self.__onUnsubscribe))
		self.__dispatcher.add_handler(CommandHandler('status', self.__onStatus))
		self.__dispatcher.add_handler(MessageHandler(Filters.text, self.__onMessage))
		self.__dispatcher.add_handler(MessageHandler(Filters.command, self.__onUnknown))
		# Start Listening
		self.__updater.start_polling()

	def shutdown(self):
		print("Bot wird heruntergefahren, bitte warten...")
		# Save IDs
		self.__writeToSaveFile()
		# Farewell user
		print("Nachrichten werden an aktive Nutzer gesendet.")
		for chat in self.getSubscribedUsers():
			self.sendText(chatId=chat, text = self.emoji("confused") + " ich lege mich schlafen. Bis später... " + self.emoji("sleeping"), silent = True)
		self.__updater.stop()
		print("bye.")
		sys.exit()

	def __readSaveFile(self):
		try:
			with open(Settings.getSaveFileName(), "r") as userfile:
				userreader = csv.reader(userfile)
				for row in userreader:
					self.__subscribedUsers.append(str(row[0]))
		except IOError:
			print("Speicherdatei " + Settings.getSaveFileName() + " nicht gefunden oder nicht lesbar")

	def __writeToSaveFile(self):
		with open(Settings.getSaveFileName(), "w") as userfile: #overwrite old file
			userwriter = csv.writer(userfile)
			for row in self.getSubscribedUsers():
				userwriter.writerow([str(row)])

	def getSubscribedUsers(self):
		return self.__subscribedUsers

	def addSubscribedUser(self, userid):
		self.__subscribedUsers.append(str(userid))

	def removeSubscribedUser(self, userid):
		self.__subscribedUsers.remove(str(userid))

	def sendText(self, chatId, text, simulatesTyping=True, replyTo=None, silent = False, parse = telegram.ParseMode.HTML):
		self.__bot.send_chat_action(chat_id = chatId, action = telegram.ChatAction.TYPING)
		if (simulatesTyping == True):
			time.sleep(randint(1,4)) #TODO async
		self.__bot.send_message(chat_id = chatId, text = text, reply_to_message_id=replyTo, disable_web_page_preview = False, disable_notification = silent, parse_mode = parse)

	def emoji (self, which):
		return emojize(":" + which + ":", use_aliases=True)
