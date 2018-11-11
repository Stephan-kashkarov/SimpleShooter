import random

import pygame as pg

import app.game.sprites.sprite as sprite


class Soldier(sprite.Sprite):
	"""Soldier class
	inherits sprite class
	"""
	def __init__(self, map, pos, id):
		super().__init__(map, id)
		self.health = 10000
		self.pos = pos
		self.rect = pg.Rect(self.pos[0], self.pos[1], 1, 1)

	def move(self, pos):
		"""moves sprite and rect together"""
		self.pos = pos
		self.rect.move(pos[0], pos[1])