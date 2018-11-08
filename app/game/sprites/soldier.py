import random

import pygame as pg

import app.game.sprites.sprite as sprite


class Soldier(sprite.Sprite):
	def __init__(self, screen, map, img):
		super().__init__(screen, map, img)
		self.pos = [random.randint(1, len(self.map[1]) - 1), random.randint(1, len(self.map) - 1)]

	def move(self, x, y):
		pass

	def shoot(self):
		pass
