import time
import json
import math
import random
import requests

import pygame as pg


import app.game.clients.client as client
import app.game.sprites.soldier as soldier

class AI(client.Client):
	def __init__(self, ip, map):
		super().__init__(ip, map)
		self.turns = 0
		self.clock = pg.time.Clock()

	def actions(self):
		try:
			ygrad = (self.pos[1] - self.unitPoses['players']['0'][0][1])
			xgrad = (self.pos[0] - self.unitPoses['players']['0'][0][0])
		except:
			ygrad = 0
			xgrad = 0
		self.rot = (0 - math.degrees(math.atan2(ygrad, xgrad)) + 90)
		pos1 = self.pos
		pos2 = self.unitPoses['players']['0'][0]

		distance = math.sqrt(((pos2[1] - pos1[1])**2) +
		                     ((pos2[0] - pos1[0])**2)) - 25
		if distance == 0:
			self.posChange = [0, 0]
		elif distance < 0:
			xchange = 2*(math.cos(math.radians(0 - self.rot - 90)))
			ychange = 2*(math.sin(math.radians(0 - self.rot - 90)))
			self.posChange = [int(xchange), int(ychange)]
			if self.ammo > 0:
				self.timer = 1000
				requests.post(self.ip + '/bullet/send',
				              json=json.dumps([self.pos, self.rot, self.id]))
				self.ammo -= 1
			else:
				if self.timer <= 0:
					self.ammo = 1000
				self.timer -= 1
		else:
			xchange = 2*(math.cos(math.radians(0 - self.rot + 90)))
			ychange = 2*(math.sin(math.radians(0 - self.rot + 90)))
			self.posChange = [int(xchange), int(ychange)]
		self.clock.tick(30)

	def run(self):
		while True:
			self.getUnits()
			self.actions()
			self.updatePos()
			self.sendUnits()
