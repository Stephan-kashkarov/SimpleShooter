import time
import random

import pygame as pg

# recycled from last assignement

def generateMap(size):
	map = []  # makes boundries
	map.append([])
	for j in range(0, size + 1):
		map[0].append("#")
	for i in range(1, size):
		map.append(["#"])
		for j in range(1, size):
			map[i].append("0")  # appends local val
		map[i].append("#")
	map.append([])
	for j in range(size + 1):
		map[-1].append("#")

	for i in range(int(size/4)):
			while True:
				# brute forces empty time
				x = random.randint(1, len(map) - 1)
				y = random.randint(1, len(map) - 1)
				if map[y][x] == "0":
					break
			shape = random.randint(0, 2)  # choses shape
			if shape == 0:  # if box
				for i in range(y, y + int(size/32)):
					for j in range(x, x + int(size/32)):
						try:
							if map[i][j] != "#":
								map[i][j] = "1"
						except:
							pass
			elif shape == 1:  # if ver line
				for i in range(y, y + int(size/16)):
					try:
						if map[i][x] != "#":
							map[i][x] = "1"
					except:
						pass
			else:  # if hoz line
				for i in range(x, x + int(size/16)):
					try:
						if map[y][i] != "#":
							map[y][i] = "1"
					except:
						pass
	return map

if __name__ == '__main__':
	map = generateMap(256)
	for line in map:
		print(line)
