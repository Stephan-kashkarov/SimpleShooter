import math
import random

import pygame as pg

import app.game.sprites.sprite as sprite


class Bullet(sprite.Sprite):
	def __init__(self, map, pos, id, rot):
		super().__init__(map, id)
		self.pos = pos
		self.rot = 0-rot-90
		self.velX = 1 * math.cos(math.radians(self.rot))
		self.velY = 1 * math.sin(math.radians(self.rot))
		self.dead = False

	def update(self):
		if self.map[int(self.pos[1])][int(self.pos[0])] != "0":
			self.dead = True
		else:
			self.pos[0] += self.velX
			self.pos[1] += self.velY

