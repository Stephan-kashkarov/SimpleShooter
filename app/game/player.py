import time
import requests

import pygame as pg

import app.game.sprites.bullet as bullet
import app.game.sprites.soldier as soldier


class Client(object):
	def __init__(self, ip):
		self.ip = "http://" + ip
		self.map = ""
		self.pos = (0,0)
		self.getMap()
		# self.sprite = soldier.Soldier()

	def getMap(self):
		self.map = requests.get(str(self.ip + '/map/get')).json()

	def getUnits(self):
		pass
		
	def sendUnits(self):
		pass

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
		self.pos = (0,0)
		self.controls = {
			'up': pg.K_w,
			'down': pg.K_s,
			'left': pg.K_a,
			'right': pg.K_d
		}

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

		xranges = range((self.pos[0] - int(self.numTiles[0] / 2)) - offsetX, (self.pos[0] + int(self.numTiles[0] / 2)) - offsetX)
		print(xranges)
		yranges = range(
			(self.pos[1] - int(self.numTiles[1] / 2)) - offsetY,
			(self.pos[1] + int(self.numTiles[1] / 2)) - offsetY)
		print(yranges)
		#paint screen
		for mapY in yranges:
			for mapX in xranges:
				point = self.map[mapY][mapX]
				# print("Point (x: {}, y: {}) is {}".format(mapX, mapY, point))
				# print("Screen (x: {}, y: {})".format(screenX, screenY))
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
				if screenX > self.numTiles[0]:
					break
			screenY += self.tileSize
			if screenY > self.numTiles[1]:
				break
		pg.display.flip()

	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return False
		pressed = pg.key.get_pressed()
		if pressed[self.controls['up']]:
			self.pos -= (0, 1)
		elif pressed[self.controls['down']]:
			self.pos += (0, 1)
		elif pressed[self.controls['left']]:
			self.pos -= (1, 0)
		elif pressed[self.controls['right']]:
			self.pos += (1, 0)

		pg.event.pump()
	
	def run(self):
		while True:
			self.gui()
			self.events()
