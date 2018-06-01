#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Settings(object):
	__LOG_FILE = ""
	__SAVE_FILE = "subscribedUsers.csv"

	@staticmethod
	def getLogFileName():
		return Settings.__LOG_FILE

	@staticmethod
	def getSaveFileName():
		return Settings.__SAVE_FILE
