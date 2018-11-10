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


	def getMap(self):
		data = requests.get(str(self.ip + '/map/get')).json()
		self.map = data['map']
		self.id = data['id']

	def getUnits(self):
		self.unitPoses = requests.get(str(self.ip + '/units/get')).json()
		self.posChange = [0, 0]
		
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
		self.unitPoses['players'][str(self.id)][2] = self.posChange

class AI(Client):
	def __init__(self, ip, map):
		super().__init__(ip, map)

	def actions(self):
		if self.pos[0] < 220:
			self.posChange = [1, 0]
		elif self.pos[1] < 150:
			self.posChange = [0, -1]
		else:
			self.pos = 50


	def run(self):
		while True:
			self.getUnits()
			self.actions()
			self.updatePos()
			self.sendUnits()

class Player(Client):
	def __init__(self, ip, map, screen):
		super().__init__(ip, map)
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
		self.sprites = {
			'green': pg.image.load('app/game/sprites/imgs/player.png'),
			'red': pg.image.load('app/game/sprites/imgs/player.png')
		}

	def gui(self):
		self.paintGame()
		pg.display.flip()

	def paintGame(self):
		self.pos = self.unitPoses['players'][str(self.id)][0]
		screenX = 0
		screenY = 0

		#calculate offset
		offsetX = 0
		offsetY = 0

		#X offset
		if (self.pos[0] - int(self.numTiles[0] / 2)) < 0:
			offsetX = (self.pos[0] - int(self.numTiles[0] / 2))
		elif (self.pos[0] + int(self.numTiles[0] / 2)) > len(self.map):
			offsetX = (self.pos[0] + int(self.numTiles[0] / 2)) - len(self.map[0])

		#Y offset
		if (self.pos[1] - int(self.numTiles[1] / 2)) < 0:
			offsetY = (self.pos[1] - int(self.numTiles[1] / 2))
		elif (self.pos[1] + int(self.numTiles[1] / 2)) > len(self.map[0]):
			offsetY = (self.pos[1] + int(self.numTiles[1] / 2)) - len(self.map)

		#fill screen
		self.screen.fill((0, 0, 0))

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
					color = (0, 200, 0)
				elif point == "1":
					color = (200, 200, 200)
				elif point == "#":
					color = (255, 255, 255)
				pg.draw.rect(
					self.screen,
					color,
					pg.Rect(screenX, screenY, self.tileSize, self.tileSize)
				)
				screenX += self.tileSize
			screenX = 0
			screenY += self.tileSize
		
		for id, player in self.unitPoses['players'].items():
			print(id, player)
			if player[0][1] in yranges and player[0][0] in xranges:
				if id == self.id:
					sprite = self.sprites['green']
				else:
					sprite = self.sprites['red']
				screenCoord = [
					(player[0][0] - (self.pos[0] - int(self.numTiles[0] / 2)) + offsetX)*16,
					(player[0][1] - (self.pos[1] - int(self.numTiles[1] / 2)) + offsetY)*16
				]
				if id == self.id:
					mousePos = pg.mouse.get_pos()
					try:
						ygrad = (mousePos[1] - screenCoord[1])
						xgrad = (mousePos[0] - screenCoord[0])
					except:
						ygrad = 0
						xgrad = 0
					player[1] = (0 - math.degrees(math.atan2(ygrad, xgrad)) - 90)
				sprite = pg.transform.rotate(sprite, player[1])
				self.screen.blit(sprite, screenCoord)
		# for pos, rot, types in self.unitPoses['bullets']:
		# 	pass

	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return False
		pressed = pg.key.get_pressed()
		
		if pressed[self.controls['up']]:
			self.posChange = [0, -1]
		elif pressed[self.controls['down']]:
			self.posChange = [0, 1]
		elif pressed[self.controls['left']]:
			self.posChange = [-1, 0]
		elif pressed[self.controls['right']]:
			self.posChange = [1, 0]




		
		
		pg.event.pump()
	
	def run(self):
		while True:
			self.getUnits()
			self.gui()
			self.events()
			self.updatePos()
			self.sendUnits()
