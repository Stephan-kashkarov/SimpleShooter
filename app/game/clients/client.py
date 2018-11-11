import time
import json
import math
import random
import requests

import pygame as pg


import app.game.sprites.soldier as soldier

class Client(object):
	def __init__(self, ip, map):
		self.ip = "http://" + ip
		self.map = map
		self.rot = 0
		self.id = 0
		time.sleep(1)
		self.getMap()
		self.pos = self.genXY()
		self.posChange = [0, 0]
		self.unitPoses = {}
		self.getUnits()
		self.ammo = 100
		self.timer = 0
		self.health = 1000

	def getMap(self):
		data = requests.get(str(self.ip + '/map/get')).json()
		self.map = data['map']
		self.id = data['id']

	def getUnits(self):
		self.unitPoses = requests.get(str(self.ip + '/units/get')).json()

	def sendUnits(self):
		data = {
			'id': self.id,
			'unitPos': self.unitPoses['players'][str(self.id)]
		}
		requests.post(str(self.ip + '/unit/send'), json=json.dumps(data))

	def genXY(self):
		x = random.randint(1, len(self.map[0]) - 1)
		y = random.randint(1, len(self.map) - 1)
		while not self.map[y][x] == "0":
			x = random.randint(1, len(self.map[0]) - 1)
			y = random.randint(1, len(self.map) - 1)
		return [x, y]

	def updatePos(self):
		self.unitPoses['players'][str(self.id)][0] = self.pos
		self.unitPoses['players'][str(self.id)][1] = self.rot
		self.unitPoses['players'][str(self.id)][2] = self.posChange
		self.posChange = [0, 0]
