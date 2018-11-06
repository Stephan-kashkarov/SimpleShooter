import time
import random

import pygame as pg

# recycled from last assignement

def generateMap(size):
	map = []  # makes boundries
	map.append([])
	for j in range(size[1] + 1):
		map[0].append("#")
	for i in range(1, size[0]):
		map.append(["#"])
		for j in range(1, size[1]):
			map[i].append("0")  # appends local val
		map[i].append("#")
	map.append([])
	for j in range(size[1] + 1):
		map[-1].append("#")

	for i in range(int(size[0]/2)):
			while True:
				# brute forces empty time
				x = random.randint(1, len(map) - 1)
				y = random.randint(1, len(map) - 1)
				if map[y][x] == " ":
					break
			shape = random.randint(0, 2)  # choses shape
			if shape == 0:  # if box
				for i in range(y, y + int(size[1]/8)):
					for j in range(x, x + int(size[0]/8)):
						try:
							if map[i][j] != "#":
								map[i][j] = "O"
						except:
							pass
			elif shape == 1:  # if ver line
				for i in range(y, y + int(size[1]/4)):
					try:
						if map[i][x] != "#":
							map[i][x] = "O"
					except:
						pass
			else:  # if hoz line
				for i in range(x, x + int(size[0]/4)):
					try:
						if map[y][i] != "#":
							map[y][i] = "O"
					except:
						pass
