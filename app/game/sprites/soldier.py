import random

import pygame as pg

import app.game.sprites.sprite as sprite


class Soldier(sprite.Sprite):
	def __init__(self, map, pos, id):
		super().__init__(map, id)
		self.health = 1000
		self.pos = pos
		self.rect = pg.Rect(self.pos[0], self.pos[1], 32, 32)

	def move(self, pos):
		self.pos = pos
		self.rect.move(pos[0], pos[1])