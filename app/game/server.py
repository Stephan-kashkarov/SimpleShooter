from flask import Flask, Response, request, make_response
from flask_socketio import send, emit
import json
import time
import logging

# parts of this code where found
# on stackoverflow:
# "https://stackoverflow.com/questions/40460846/using-flask-inside-class


class EndpointAction(object):

	def __init__(self, action):
		self.action = action
		self.response = ""

	def __call__(self, *args):
		self.response = make_response(self.action())
		return self.response


class Server(object):
	def __init__(self, _map, key):
		#server stuff
		self.name = "Game Server"
		self.app = Flask(self.name)
		log = logging.getLogger('werkzeug')
		log.setLevel(logging.ERROR)
		del log
		self.id = 0

		#Game stuff
		self.gameState = False
		self.map = _map
		self.units = {
			'bullets': [],
			'players': {}
		}
		self.key = key

		# Endpoints
		self.add_endpoint(
			endpoint='/test',
			endpoint_name='test',
			handler=self.test
		)
		self.add_endpoint(
			endpoint='/map/get',
			endpoint_name='getMap',
			handler=self.getMap
		)
		self.add_endpoint(
			endpoint='/map/set',
			endpoint_name='setMap',
			handler=self.setMap,
			_methods=['POST']
		)
		self.add_endpoint(
			endpoint='/units/set',
			endpoint_name='setUnits',
			handler=self.setUnits,
			_methods=['POST']
		)
		self.add_endpoint(
			endpoint='/units/get',
			endpoint_name='getUnits',
			handler=self.getUnits
		)
		self.add_endpoint(
			endpoint='/unit/send',
			endpoint_name='sendUnit',
			handler=self.sendUnit,
			_methods=['POST']
		)
		self.add_endpoint(
			endpoint='/bullet/send',
			endpoint_name='sendBullet',
			handler=self.sendBullet,
			_methods=['POST']
		)
		self.add_endpoint(
			endpoint='/game/over',
			endpoint_name='gameOver',
			handler=self.gameOver
		)

	# Game Routes

	# set routes
	def setMap(self):
		data = json.loads(request.json)
		if data['key'] == self.key:
			self.map = data['map']
			return 'True'
		return 'False'

	def sendUnit(self):
		data = json.loads(request.json)
		id = data['id']
		unitPos = data['unitPos']
		self.units['players'][str(id)] = unitPos
		return 'True'

	def setUnits(self):
		data = json.loads(request.json)
		if data['key'] == self.key:
			self.units = data['payload']
			return 'True'
		return 'False'

	def sendBullet(self):
		data = json.loads(request.json)
		data.append(self.id)
		self.id += 1
		self.units['bullets'].append(data)
		return 'True'


	# get routes
	def getMap(self):
		id = self.id
		self.id += 1
		return json.dumps({'map':self.map, 'id':id})

	def getUnits(self):
		return json.dumps(self.units)


	# Misc routes

	def run(self):
		self.app.run()

	def gameOver(self):
		return str(self.gameOver)

	def test(self):
		return "<head><title>Hell0!</title></head><body>Server is ONLINE!</body>"

	def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, _methods=None):
		self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=_methods)


# Testing
if __name__ == '__main__':
	s = Server(None, None)
	s.run()
