import os
import json
import requests

import pygame as pg


class options(object):
	def __init__(self, serverIP, mapType, mapSize, key):
		self.serverIP = serverIP
		self.mapType = mapType
		self.mapSize = mapSize
		self.key = key


class Match(object):
	def __init__(self, options, _map):
		self.serverIP = 'http://' + options.serverIP
		self.map = _map
		self.events = []
		self.key = options.key
		self.players = self.getUnits()
		self.sendUnits()
		self.sendMap()

	# Unit Processing

	def getUnits(self):
		return requests.get(str(self.serverIP + '/units/get')).json()

	def sendUnits(self):
		requests.post(
			str(self.serverIP + '/units/set'),
			json=json.dumps({
				'key': self.key,
				'units': self.units
			})
		)

	# Map Processing
	def sendMap(self):
		requests.post(str(self.serverIP + '/map/set'),
                    json=json.dumps({
			'key': self.key,
			'map': self.map
                    }))

	# Event processing
	def getEvents(self):
		request = requests.get(str(self.serverIP + '/events/get'))
		for event in list(set(request.json()) - set(self.events)):
			self.events.append(event)

	def executeEvents(self):
		events = []
		for event in [x for x in self.events[::-1]]:
			event = self.events.pop(event)
			event.step()
			if not event.complete:
				events.append(event)
		self.events = events

	def checkWin(self):
		win = bool(requests.post(self.serverIP + '/game/over'))
		for i in self.units['keys']:
			if not len(self.units[str(i)]['units']) or win:
				print("Match: Game Over!")
				return True
		return False

	def run(self):
		while True:
			print('Game: tick')
			self.units = self.getUnits()
			self.sendUnits()
			if self.checkWin() == True:
				break
