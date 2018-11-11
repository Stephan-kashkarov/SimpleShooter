import time
import json
import math
import random
import requests

import pygame as pg


import app.game.sprites.soldier as soldier

class Client(object):
	"""Client class
	to be inherited"""
	def __init__(self, ip, map):
		"""IP is a string and the IP of the server
		map is the game map"""
		self.ip = "http://" + ip
		self.map = map
		self.rot = 0
		self.id = 0
		# for timing with treads
		time.sleep(1)
		self.getMap()
		self.pos = self.genXY()
		self.posChange = [0, 0]
		self.unitPoses = {}
		self.getUnits()
		self.ammo = 100
		self.timer = 0
		self.health = 100

	def getMap(self):
		"""Get map method
		gets map and id of player from server"""
		data = requests.get(str(self.ip + '/map/get')).json()
		self.map = data['map']
		self.id = data['id']

	def getUnits(self):
		"""get Units method
		sends a get request to server for units"""
		self.unitPoses = requests.get(str(self.ip + '/units/get')).json()

	def sendUnits(self):
		"""Send units method
		sends clients unit to server to be updated
		"""
		data = {
			'id': self.id,
			'unitPos': self.unitPoses['players'][str(self.id)]
		}
		requests.post(str(self.ip + '/unit/send'), json=json.dumps(data))

	def genXY(self):
		"""genXY method
		to randomly find place to spawn on the map
		"""
		x = random.randint(1, len(self.map[0]) - 1)
		y = random.randint(1, len(self.map) - 1)
		while not self.map[y][x] == "0":
			x = random.randint(1, len(self.map[0]) - 1)
			y = random.randint(1, len(self.map) - 1)
		return [x, y]

	def updatePos(self):
		"""Update pos method
		updates pos in the unit pos list by pos of client
		"""
		self.unitPoses['players'][str(self.id)][0] = self.pos
		self.unitPoses['players'][str(self.id)][1] = self.rot
		self.unitPoses['players'][str(self.id)][2] = self.posChange
		self.posChange = [0, 0]
