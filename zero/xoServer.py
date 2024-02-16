

import threading
from pickle import FALSE
import time
import zmq
import json
import traceback
from ast import arg
# from xo import *
# # from xo.expando import 
# from expando import Expando

from zeroless import Client, Server
from threading import Thread
import dill as pk
import killport



class xoServer():
	_pubPort = 1980
	_reqPort = 19801
	_id = "_root_"

	def __init__(self) -> None:
		killport.kill_ports(ports=[xoServer._pubPort, xoServer._reqPort])
		time.sleep(1)
		self._pubserver = Server(xoServer._pubPort)
		self._reqserver = Server(xoServer._reqPort)

		def pushToSubs(topic: str):
			listen_for_push = self._pubserver.pull()
			for msg in listen_for_push:
				try:
					print(msg)
					topic, data = "updates", msg
					self._pubserver.pub()(topic, data)
				except:
					traceback.print_exc()
				finally:
					pass

		def listen(data, *args, **kwargs):
			reply, listen_for_request = self._reqserver.reply()
			c = 0
			for msg in listen_for_request:
				c += 1
				try:
					print(c, "::: INCOMING:", msg)
					# f"ECHO! {msg}".encode()
					# reply(bytes("ECHO! "+str(msg)))
					reply(f"ECHO! {msg}".encode())
					# MERGE WITH MICROXO
					# reply(msg)
				except:
					traceback.print_exc()
				finally:
					pass
			# topic = topic[0] if isinstance(topic, list) else topic

			# # Initiate a subscriber client
			# # Assigns an iterable to wait for incoming messages with the topic 'sh'
			# listen_for_pub = self._hook.sub(topics=[topic.encode()])

			# for topic, msg in listen_for_pub:
			#     print(topic, ' - ', msg)
			#     self._setValue(msg)

		requests = Thread(target=listen, args=[self._id, ])
		requests.start()
		time.sleep(1)
		pub = Thread(target=pushToSubs, args=[self._id, ])
		pub.start()



class xoClient():
	_reqPort = 1970
	_pubPort = 19701
	_rootName = "xo.zmq"

	@staticmethod
	def connect(client, port, ip="127.0.0.1"):
		try:
			client.disconnect(ip=ip, port=port)
		except:
			pass
		client.connect(ip=ip, port=port)
		return client

	def _isNameSpace(self):
		return True if self._parent is not None and self._parent.isRoot else False

	def _getNameSpace(self):
		if self._namespace != None:
			return self
		return None if self._parent is None else self._parent._getNameSpace()
		# return True if self._parent is not None and self._parent.isRoot else False

	def subNamespace(self):
		# ask master server for known namespace port
		# subscribe to port changes for namespace
		pass

	def __init__(self, _pubPort=None, _reqPort=None, _val=None, _id=None, _parent=None, _behaviors=..., _xoT_=None, *vars, **entries):
		# super().__init__(_val, _id = _id, _parent = _parent, _behaviors=_behaviors, _xoT_=_xoT_, *vars, **entries)
		# self._rootName = xoClient._rootName
		self._namespace = None
		if _parent is None:
			pass
			# connect to defaultserver, or launch it
			# self._pubPort = _pubPort if _pubPort is not None else xoClient._pubPort
			self._reqPort = _reqPort if _reqPort is not None else xoClient._reqPort
			# reqPort = reqPort if reqPort is not None else xoZMQ._reqPort
			self._pubclient = Client()
			self._reqclient = Client()
			if _reqPort is None:
				_reqPort = self._reqPort
			# only root does clients ?
			try:
				# xoClient.connect(self._pubclient, self._pubPort)
				xoClient.connect(self._reqclient,_reqPort)
				# print(f"{_reqPort} TTTTTTTTTTTTTTTTTT111 connected to {self._reqclient} {_reqPort}")

			except:
				traceback.print_exc()
			try:
				# print("TTTTTTTTTTTTTTTTTT0")
				xoClient.connect(self._reqclient, _reqPort)
				# print("TTTTTTTTTTTTTTTTTT01")
				self._clientRequest, self._listenReply = self._reqclient.request()
				# print(f"TTTTTTTTTTTTTTTTTT111 connected to  {_reqPort}")
				# request, listen_for_reply = client.request()
				# request, listen_for_reply = client

				# c = 0
				# t = time.time()
				# while time.time()-t < 0.01:
				#     c+=1
				# print(f"Elapsed for {c} {time.time()-t}")

			except:
				traceback.print_exc()

			# self._pubclient.connect_local(port=self._pubPort)
		# elif _parent._isRoot:
		elif self._isNameSpace():
			self._namespace = self.subNamespace()
			self._reqclient = self._getRoot()._reqclient
		else:
			self._namespace = self._getNameSpace()
			self._reqclient = self._getRoot()._reqclient

		def subscribeToZMQ(topic: str):
			topic = topic[0] if isinstance(topic, list) else topic

			# Initiate a subscriber client
			# Assigns an iterable to wait for incoming messages with the topic 'sh'
			listen_for_pub = self._pubclient.sub(topics=[topic.encode()])

			for topic, msg in listen_for_pub:
				print(topic, ' - ', msg)
				self._setValue(msg)

		# th = Thread(target=subscribeToZMQ, args=[self._id, ])
		# th.start()

	def request(self, target="microxo/foo", *args, **kwargs):
		# print("RRRRRRRRRRRRR",target,args,kwargs)
		# request, listen_for_reply = self.clientRequest, self.listenReply
		try:
			# self._clientRequest(f"sara is amazing X {c}".encode())
			# self._clientRequest(payload.encode()) #jsonify(payload).encode())
			payload = {"target": target, "args": args, "kwargs": kwargs}
			self._clientRequest(json.dumps(payload).encode())
			response = next(self._listenReply)
			pk.loads(response)
			print("RRRRRRxxxxxxxxRRR",response)
			return response
		except:
			traceback.print_exc()
			print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",self._reqPort)
			xoClient.connect(self._reqclient, self._reqPort)
			self._clientRequest, self._listenReply = self._reqclient.request()
			if "retry" not in kwargs or kwargs["retry"]:
				kwargs["retry"] = False
				self.request(target=target,retry=False,*args,**kwargs)
			# request, listen_for_reply = client.request()
		finally:
			pass

	def call(self, *args, **kwargs):
		pass
		# check namespace, if exists, request value or func(args,kwargs)
		return self._value

	def set(self, value, *args, **kwargs):
		if value is not None:
			# val = pk.dumps(value)
			val = str(value).encode()
			# print("PUB:", self._id, val)
			# self._pubclient.pub()(self._id.encode(), val)
			self._pubclient.pub()(str(id(self)).encode(), val)
			# self._hook
			# r = self._getRoot()._redis
			# res = r.set(self._id, val)
			# r.publish(self._id, val)
			return True  # To continue with super() set
		return False

	# def get(self, *args, **kwargs):
	#     r = self._getRoot()._redis
	#     res = r.get(self._id)
	#     try:
	#         res = pk.loads(res)
	#     except:
	#         print(" - - - COULD NOT UNPICKLE", self._id, ":::", res)
	#     self._setValue(res)
	#     return res

		# subscribeToZMQ(self._id)

		'''
		request, listen_for_reply = client.request()

		c = 0
		t = time.time()
		while time.time()-t < 1:
			c += 1
			request(f"sara is amazing X {c}".encode())
			response = next(listen_for_reply)
			print(response)

		print(f"Elapsed for {c} {time.time()-t}")
		'''

		if _defaultServer is None:
			self._pubPort = xoClient._pubPort
		else:
			self._pubPort = _defaultServer





