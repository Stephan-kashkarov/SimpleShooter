import time
import json
import random
import requests

import pygame as pg


import app.game.sprites.soldier as soldier


class Client(object):
	def __init__(self, ip):
		self.ip = "http://" + ip
		self.id = 0
		self.map = ""
		self.getMap()
		self.pos = self.genXY()
		self.unitPoses = {}
		self.getUnits()


	def getMap(self):
		data = requests.get(str(self.ip + '/map/get')).json()
		self.map = data['map']
		self.id = data['id']

	def getUnits(self):
		self.unitPoses = requests.get(str(self.ip + '/units/get')).json()
		
	def sendUnits(self):
		data = {
			'id': self.id,
			'unitPos': self.unitPoses[self.id]
		}
		requests.post(str(self.ip + '/units/send'), json=json.dumps(data))

	def genXY(self):
		x = random.randint(1, len(self.map[0]) - 1)
		y = random.randint(1, len(self.map) - 1)
		while not self.map[y][x] == "0":
			x = random.randint(1, len(self.map[0]) - 1)
			y = random.randint(1, len(self.map) - 1)
		return [x, y]

class AI(Client):
	def __init__(self, ip):
		super().__init__(ip)

	def actions(self):
		pass

	def run(self):
		self.getUnits()
		self.actions()
		self.sendUnits()

class Player(Client):
	def __init__(self, ip, screen):
		super().__init__(ip)
		self.screen = screen
		self.resX, self.resY = self.screen.get_rect().size
		self.tileSize = 16
		self.numTiles = (self.resX / self.tileSize, self.resY / self.tileSize)
		self.controls = {
			'up': pg.K_w,
			'down': pg.K_s,
			'left': pg.K_a,
			'right': pg.K_d
		}
		self.units = {}
		self.getUnits()

	def gui(self):
		screenX = 0
		screenY = 0

		#calculate offset
		offsetX = 0
		offsetY = 0

		#X offset
		if (self.pos[0] - int(self.numTiles[0] / 2)) < 0:
			offsetX = (self.pos[0] - int(self.numTiles[0] / 2))
		elif (self.pos[0] - int(self.numTiles[0] / 2)) > len(self.map):
			offsetX = len(self.map) - (self.pos[0] - int(self.numTiles[0] / 2))

		#Y offset
		if (self.pos[1] - int(self.numTiles[1] / 2)) < 0:
			offsetY = (self.pos[1] - int(self.numTiles[1] / 2))
		elif (self.pos[1] - int(self.numTiles[1] / 2)) > len(self.map[0]):
			offsetY = len(self.map[0]) - (self.pos[1] - int(self.numTiles[1] / 2))

		#fill screen
		self.screen.fill((0,0,0))

		xranges = range(
			(self.pos[0] - int(self.numTiles[0] / 2)) - offsetX,
			(self.pos[0] + int(self.numTiles[0] / 2)) - offsetX)
		yranges = range(
			(self.pos[1] - int(self.numTiles[1] / 2)) - offsetY,
			(self.pos[1] + int(self.numTiles[1] / 2)) - offsetY)
		#paint screen
		for mapY in yranges:
			for mapX in xranges:
				point = self.map[mapY][mapX]
				if point == "0":
					color = (0,200,0)
				elif point == "1":
					color = (200, 200, 200)
				elif point == "#":
					color = (255,255,255)
				pg.draw.rect(
					self.screen,
					color,
					pg.Rect(screenX, screenY, self.tileSize, self.tileSize)
				)
				screenX += self.tileSize
			screenX = 0
			screenY += self.tileSize
		pg.display.flip()

	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return False
		pressed = pg.key.get_pressed()
		if pressed[self.controls['up']]:
			self.pos[1] -= 1
		elif pressed[self.controls['down']]:
			self.pos[1] += 1
		elif pressed[self.controls['left']]:
			self.pos[0] -= 1
		elif pressed[self.controls['right']]:
			self.pos[0] += 1

		pg.event.pump()
	
	def run(self):
		while True:
			self.gui()
			self.events()
