import time
import json
import math
import random
import requests

import pygame as pg


import app.game.clients.client as client
import app.game.sprites.soldier as soldier


class Player(client.Client):
	"""Player class
	inherets client
	
	this class contains all logic for printing
	and event handling in the encoutner
	"""
	def __init__(self, ip, map, screen, controls):
		"""
		IP is the ip of the server
		map is the game map
		screen is the pg surface of the screen
		controls is the controls obj
		"""
		super().__init__(ip, map) # inits the client obj
		self.screen = screen
		self.resX, self.resY = self.screen.get_rect().size
		self.tileSize = 8
		self.numTiles = (self.resX / self.tileSize, self.resY / self.tileSize)
		self.controls = controls
		self.sprites = { # loads sprites
			'green': pg.image.load('app/game/sprites/imgs/player1.png'),
			'red': pg.image.load('app/game/sprites/imgs/player2.png'),
			'bullet': pg.image.load('app/game/sprites/imgs/bullet.png')
		}

	def gui(self):
		"""runs gui"""
		state = self.paintGame()
		pg.display.flip()
		return state

	def paintGame(self):
		"""Draws map and sprites"""
		# checks for death
		state = 0
		if len(self.unitPoses['players']) < 2:
			return True
		
		# locals init
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

		# calculates what portion of the map to print
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
		
		# prints player sprites
		for id, player in self.unitPoses['players'].items(): 
			# kills player if health is 0
			if player[3] == 0:
				del self.unitPoses['players'][id]
				continue
			# checks if player is on screen
			if player[0][1] in yranges and player[0][0] in xranges:
				# if its the player's player then 
				if str(id) == str(self.id):
					sprite = self.sprites['green']
				else:
					sprite = self.sprites['red']

				# finds sprites coord on the screen
				screenCoord = [
					(player[0][0] - (self.pos[0] - int(self.numTiles[0] / 2)) + offsetX)*self.tileSize,
					(player[0][1] - (self.pos[1] - int(self.numTiles[1] / 2)) + offsetY)*self.tileSize
				]
				# finds rot if sprite is player's sprite
				if id == str(self.id):
					mousePos = pg.mouse.get_pos()
					try:
						ygrad = (mousePos[1] - screenCoord[1])
						xgrad = (mousePos[0] - screenCoord[0])
					except: # Zero div error
						ygrad = 0
						xgrad = 0
					# applys rotation
					player[1] = (0 - math.degrees(math.atan2(ygrad, xgrad)) - 90)
					self.rot = player[1] # finalises rotaiton
				sprite = pg.transform.rotate(sprite, player[1]) # transforms sprite
				self.screen.blit(sprite, screenCoord) # prints sprite
		# draws bullets
		for pos, rot, ownerid, id in self.unitPoses['bullets']: 
			# finds screen coords
			screenCoord = [
					(pos[0] - (self.pos[0] - int(self.numTiles[0] / 2)) + offsetX)*self.tileSize,
					(pos[1] - (self.pos[1] - int(self.numTiles[1] / 2)) + offsetY)*self.tileSize
				]
			# rotates sprite
			sprite = pg.transform.rotate(self.sprites['bullet'], (rot))
			self.screen.blit(sprite, screenCoord) # prints
		return state # exit cond

	def events(self):
		"""Events method tracks keyboard events"""
		# exit cond
		if len(self.unitPoses['players']) < 2:
			return True

		# quit loop
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return False

		# gets pressed keys
		pressed = pg.key.get_pressed()

		if pressed[self.controls['up']]: # up
			self.posChange = [0, -1]
		elif pressed[self.controls['down']]: # down
			self.posChange = [0, 1]
		elif pressed[self.controls['left']]: # left
			self.posChange = [-1, 0]
		elif pressed[self.controls['right']]: # right
			self.posChange = [1, 0]
		elif pressed[self.controls['reload']]: # reload
			self.ammo = 10000

		if pg.mouse.get_pressed()[0]:
			# shoots
			if self.ammo > 0:
				requests.post(self.ip + '/bullet/send', json=json.dumps([self.pos, self.rot, self.id]))
				# self.ammo -= 1


		pg.event.pump()
		return 0

	def run(self):
		"""Runs the event loop for this client"""
		while True:
			self.getUnits()
			state = self.gui()
			if state != 0:
				return state
			state = self.events()
			if state != 0:
				return state
			self.updatePos()
			self.sendUnits()
