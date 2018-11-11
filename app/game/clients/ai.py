# imports
import time
import json
import math
import random
import requests

import pygame as pg

import app.game.clients.client as client
import app.game.sprites.soldier as soldier

class AI(client.Client):
	"""AI class
	inherits client
	a bot for the encounter
	to be run on a thread"""
	def __init__(self, ip, map):
		"""param IP - str | ip of server w/o http://
		param map - [[]] | game map"""
		super().__init__(ip, map)
		self.turns = 0
		self.clock = pg.time.Clock()

	def actions(self):
		"""THe AI alogrithm itself
		"""
		# check dead
		if self.unitPoses['players'][str(self.id)][3] == 0:
			return 0
		# Sprite rotation
		try:
			ygrad = (self.pos[1] - self.unitPoses['players']['0'][0][1])
			xgrad = (self.pos[0] - self.unitPoses['players']['0'][0][0])
		except: # if devide by 0
			ygrad = 0
			xgrad = 0
		# calculates rotation
		self.rot = (0 - math.degrees(math.atan2(ygrad, xgrad)) + 90)
		
		# movement
		pos1 = self.pos
		pos2 = self.unitPoses['players']['0'][0]
		# calculates distance with offset of 100
		distance = math.sqrt(((pos2[1] - pos1[1])**2) +
		                     ((pos2[0] - pos1[0])**2)) - 100
		# if distance == 100 stay still
		if distance == 0:
			self.posChange = [0, 0]
			# if its more move closer
		elif distance < 0:
			# find what a step in rotation is
			xchange = 2*(math.cos(math.radians(0 - self.rot - 90)))
			ychange = 2*(math.sin(math.radians(0 - self.rot - 90)))
			#round and apply
			self.posChange = [int(xchange), int(ychange)]
			# shoot logic
			if self.ammo > 0:
				#simulates reload
				self.timer = 100
				# generates bullet
				requests.post(self.ip + '/bullet/send',
				              json=json.dumps([self.pos, self.rot, self.id]))
				self.ammo -= 1
			else:
				# reloaded
				if self.timer <= 0:
					self.ammo = 100
				# still reloading
				self.timer -= 1
		else:
			# calc step in rotation
			xchange = 2*(math.cos(math.radians(0 - self.rot + 90)))
			ychange = 2*(math.sin(math.radians(0 - self.rot + 90)))
			# round and apply
			self.posChange = [int(xchange), int(ychange)]
		# lower framerate to try control speed(dosent work well)
		self.clock.tick(30)

	def run(self):
		"""Run methods
		runs all methods in correct order
		to be run on thread"""
		while True:
			self.getUnits()
			a = self.actions()
			if a:
				break # exit cond
			self.updatePos()
			self.sendUnits()
