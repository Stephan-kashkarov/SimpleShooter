import os
import time
import json
import requests

import pygame as pg

import app.game.sprites.bullet as bullet
import app.game.sprites.soldier as soldier


class options(object):
	def __init__(self, serverIP, mapSize, key):
		self.serverIP = serverIP
		self.mapSize = mapSize
		self.key = key


class Match(object):
	def __init__(self, options, _map, players):
		self.serverIP = 'http://' + options.serverIP
		self.map = _map
		self.key = options.key
		self.sendMap()
		time.sleep(2)
		self.players = players
		self.playerGroup = pg.sprite.Group()
		self.bulletGroup = pg.sprite.Group()
		self.unitPoses = {'players':{}, 'bullets':[]}
		for player in self.players:
			self.playerGroup.add(soldier.Soldier(self.map, player.pos))
			self.unitPoses['players'][player.id] = [player.pos, player.rot]
		self.setUnits()

	# Unit Processing

	def getUnits(self):
		self.unitPoses = requests.get(str(self.serverIP + '/units/get')).json()

	def setUnits(self):
		requests.post(
			str(self.serverIP + '/units/set'),
			json=json.dumps({
				'key': self.key,
				'payload': self.unitPoses
			})
		)
	
	def updateUnits(self):
		pass

	# Map Processing
	def sendMap(self):
		requests.post(
			str(self.serverIP + '/map/set'),
			json=json.dumps({
				'key': self.key,
				'map': self.map
			})
		)

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
