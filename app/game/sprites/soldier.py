import random

import pygame as pg

import app.game.sprites.sprite as sprite


class Soldier(sprite.Sprite):
	def __init__(self, map, pos, id):
		super().__init__(map, id)
		self.pos = pos