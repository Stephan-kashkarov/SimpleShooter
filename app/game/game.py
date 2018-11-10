import time
import random
import multiprocessing

import pygame as pg

import app.game.match as match
import app.game.map.map as maps
import app.game.player as player
import app.game.server as server


def singlePlayer(screen):
	options = match.options(
		'127.0.0.1:5000',
		2000,
		random.randint(1000, 9999)
	)

	_map = maps.generateMap(options.mapSize)
	host = server.Server(_map, options.key)
	server_ = multiprocessing.Process(target=host.run)
	server_.start()
	# allow for the server to initializse
	time.sleep(1)
	player1 = player.Player(options.serverIP, _map, screen)
	player2 = player.AI(options.serverIP, _map)
	players = [player1, player2]
	game = match.Match(options, _map, players)

	# Making Threads
	gameThread = multiprocessing.Process(target=game.run)
	aiThread = multiprocessing.Process(target=player2.run)
	# Starting Threads
	gameThread.start()
	print("Running AI")
	aiThread.start()
	# Running clientside
	state = player1.run()
	# Joining of threads
	gameThread.terminate()
	gameThread.join()
	aiThread.terminate()
	aiThread.join()
	server_.terminate()
	server_.join(5)
	time.sleep(1)
	if state == 'quit':
		pg.quit()
		quit()
	return 0
