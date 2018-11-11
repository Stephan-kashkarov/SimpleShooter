import pygame as pg


class Sprite(pg.sprite.Sprite):
	"""Sprite class
	to be inherited
	"""
	def __init__(self, map, id):
		super().__init__()
		self.rotation = 0
		self.map = map
		self.pos = [0, 0]
		self.id = id
