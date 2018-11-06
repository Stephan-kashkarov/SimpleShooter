from flask import Flask, Response, request, make_response
from flask_socketio import send, emit
import json
import time

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

		#Game stuff
		self.gameState = False
		self.map = _map
		self.units = {
			'keys': [0, 1, 2, 3],
			0: {
				'start': [],
				'resouces': {},
				'alive': False,
				'units': ()
			},
			1: {
				'start': [],
				'resouces': {},
				'alive': False,
				'units': ()
			},
			2: {
				'start': [],
				'resouces': {},
				'alive': False,
				'units': ()
			},
			3: {
				'start': [],
				'resouces': {},
				'alive': False,
				'units': ()
			}
		}
		self.events = []
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
			endpoint='/units/add',
			endpoint_name='addUnits',
			handler=self.addUnits,
			_methods=['POST']
		)
		self.add_endpoint(
			endpoint='/events/get',
			endpoint_name='getEvents',
			handler=self.getEvents
		)
		self.add_endpoint(
			endpoint='/events/add',
			endpoint_name='addEvents',
			handler=self.addEvents,
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

	def addUnits(self):
		data = json.loads(request.json)
		if data['key'] == self.key:
			for i in self.units['keys']:
				self.units[str(i)]['units'].append(
					set(data[str(i)]['units']) - set(self.units[str(i)]['units']))
			return 'True'
		return 'False'

	def setUnits(self):
		data = json.loads(request.json)
		if data['key'] == self.key:
			self.units = data['units']
			return 'True'
		return 'False'

	def addEvents(self):
		data = json.loads(request.json)
		if data['key'] == self.key:
			self.events.append(data['events'])
			return 'True'
		return 'False'

	# get routes
	def getMap(self):
		return json.dumps(self.map)

	def getUnits(self):
		return json.dumps(self.units)

	def getEvents(self):
		return json.dumps(list(self.events))

	# Misc routes

	def run(self):
		self.app.run()

	def gameOver(self):
		return str(self.gameOver)

	def test(self):
		return "<title>Hell0!</title>"

	def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, _methods=None):
		self.app.add_url_rule(endpoint, endpoint_name,
		                      EndpointAction(handler), methods=_methods)


# Testing
if __name__ == '__main__':
	s = Server(None, None)
	s.run()
