import random

import pygame as pg

import app.game.sprites.sprite as sprite
import app.game.sprites.bullet as bullet


class Soldier(sprite.Sprite):
	def __init__(self, screen, map, img, x, y):
		super().__init__(screen, map, img)
		self.pos = [x, y]

	def shoot(self):
		pass
