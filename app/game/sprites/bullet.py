import math
import random

import pygame as pg

import app.game.sprites.sprite as sprite


class Bullet(sprite.Sprite):
	def __init__(self, map, pos, id, rot, ownerid):
		super().__init__(map, id)
		self.pos = pos
		self.rot = 0-rot-90
		self.velX = 0.5 * math.cos(math.radians(self.rot))
		self.velY = 0.5 * math.sin(math.radians(self.rot))
		self.dead = False
		self.ownerid = ownerid
		self.rect = pg.Rect(self.pos[0], self.pos[1], 16, 16)

	def update(self):
		if self.map[int(self.pos[1])][int(self.pos[0])] != "0":
			self.dead = True
		else:
			self.pos[0] += self.velX
			self.pos[1] += self.velY
			self.rect.move(self.velX, self.velY)

