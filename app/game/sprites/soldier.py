import random

import pygame as pg

import app.game.sprites.sprite as sprite
import app.game.sprites.bullet as bullet


class Soldier(sprite.Sprite):
	def __init__(self, map, pos):
		super().__init__(map)
		self.pos = pos

	def shoot(self):
		pass
