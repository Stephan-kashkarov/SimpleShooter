import os
import json
import requests

import pygame as pg


class options(object):
	def __init__(self, serverIP, mapSize, key):
		self.serverIP = serverIP
		self.mapSize = mapSize
		self.key = key


class Match(object):
	def __init__(self, options, _map):
		self.serverIP = 'http://' + options.serverIP
		self.map = _map
		self.key = options.key
		self.units = []
		self.setUnits()
		self.sendMap()

	# Unit Processing

	def getUnits(self):
		self.units = requests.get(str(self.serverIP + '/units/get')).json()

	def setUnits(self):
		requests.post(
			str(self.serverIP + '/units/set'),
			json=json.dumps({
				'key': self.key,
				'payload': self.units
			})
		)
	
	def updateUnits(self):
		pass

	# Map Processing
	def sendMap(self):
		requests.post(str(self.serverIP + '/map/set'),
		json=json.dumps({
			'key': self.key,
			'map': self.map
		}))

	def checkWin(self):
		return False if not bool(requests.get(self.serverIP + '/game/over')) else True

	def run(self):
		while True:
			print('Game: tick')
			self.getUnits()
			self.updateUnits()
			self.setUnits()
			if self.checkWin() == True:
				break
