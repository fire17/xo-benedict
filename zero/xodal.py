# from argparse import Namespace
# from dataclasses import dataclass, field, asdict
# from xo.expando import Expando
from expando import Expando

from zeroless import Client, Server
# from xo.zmq import xoServer
import killport
# from xo_zmq import xoClient
from xoServer import xoClient

from threading import Thread
import traceback
import time, os
import json


class xodal(Expando):
	_rootName = "xodal"
	index = {}
	_auth = None
	# _id = xo

	def __init__(self, func=None,_rootName=None, _xoT_=None, *args, **kwargs):
		print("########0000000Xodal", func, args, kwargs)
		if _rootName is not None:
			self._rootName = _rootName
			kwargs["_id"] = _rootName
			print("5555555555555",_rootName,  kwargs["_id"],"::::::", kwargs)

		if "_id" in kwargs:
			_id = kwargs.pop("_id")
			super().__init__(_id=_id, _rootName=_rootName, _xoT_=_xoT_ if _xoT_ is not None else xodal, *args, **kwargs)
		else:
			super().__init__(_rootName=_rootName, _xoT_=_xoT_ if _xoT_ is not None else xodal, *args, **kwargs)
		# if func is None:
		# 	super().__init__(*args, **kwargs)
		# else:
		# 	super().__init__(self, *args, **kwargs)

		self._func = func
		if func is not None:
			print(self._id, "!!!!!!!", func.__name__, type(func))
			xodal.index[self._id+"/"+func.__name__] = func

	
	@staticmethod
	def _checkAuth(payload):
		return True
		
	# Override the call method
	def __call__(self, *args, **kwargs):
		print("CALLING", self._id, args, kwargs)
		# if "args" not in kwargs:
		# 	print("args",type(args))
		# 	if isinstance(args,tuple):
		# 		kwargs["args"] = list(args)
				
		if "value" not in kwargs and self.value is not None:
			kwargs["value"] = self.value
		if "id" not in kwargs:
			kwargs["id"] = self._id
			
		
		return self.CallFunc(
			payload = {
						"pointer":self._id,
						"kwargs": kwargs,
						"args": list(args),
						"auth": self._auth
					})

	def DefaultFunc(self, payload):
		''' OVERLOAD THIS FUNCTION TO CHANGE DEFAULT BEHAVIOR '''
		print("DEFAULT", self._id, payload)
		return "NICE"

	def CallFunc(self, payload):
		# print("GGGGGGGGGGGGGGGGGetXO", self._id, get, getValue)
		# if "None" not in str(type(self._parent)):
		# if not self._isRoot:
		# 	# get = ".".join(self._id.replace("/",".").split(".")[1:] + get.split("."))
		# 	return self._getRoot().CallFunc(payload)

		final = self
		if not isinstance(payload, dict) or not xodal._checkAuth(payload):
			return False
		
		# data should be kwargs {}
		data = payload["kwargs"] if "kwargs" in payload else None
		args = payload["args"] if "args" in payload else None
		auth = payload["auth"] if "auth" in payload else None
		pointer = payload["pointer"] if "pointer" in payload else None
		if pointer is not None and pointer in xodal.index:
			print(" CALLING EXISTING FUNC IN INDEX",
				  pointer, ":::", type(xodal.index[pointer]), ":", xodal.index[pointer])
			return xodal.index[pointer](*args, **data)
		else:
			print(" RUNNING DEFAULT FUNCTION ",self._id, payload)
			return self.DefaultFunc(payload)

	

	# def default(self, o):
	# 	return super().default(o)


class MicroXO(xodal):
	_rootName = "microxo"
	_reqPort = 1970
	_pubPort = 19701
	_services = {}

	def __init__(self, funcOrNamespace=None, reqPort=None, _xoT_=None, *args, **kwargs):
		# print("########00000M", funcOrNamespace, args, kwargs)
		runServer = False
		func = None
		# namespace = self._rootName
		namespace = None
		_rootName = None
		_id = None
		if isinstance(funcOrNamespace,str):
			# print("1111111")
			namespace = funcOrNamespace
			kwargs["_id"]=namespace
			_rootName = namespace
			runServer = True
		elif "_id" not in kwargs:
			func = funcOrNamespace
			# get namespace from running filename
			# print("##########22222222", type(self))
			# namespace = ".".join(str(type(self)).split(".")[1:]).split("'")[0]
			namespace = str(type(self)).split(".")[-1].split("'")[0]
			# print("##########22222222", namespace)
			_rootName = namespace
			_id = namespace
			if "_id" in kwargs:
				kwargs.pop("_id")
		if '_func' in kwargs:
			func = kwargs['_func']
			
			
		if _id is not None:
			super().__init__(_id = _id, func=func,_rootName=_rootName, _xoT_=_xoT_ if _xoT_ is not None else MicroXO, *args, **kwargs)
		else:
			super().__init__(func=func,_rootName=_rootName, _xoT_=_xoT_ if _xoT_ is not None else MicroXO, *args, **kwargs)
		# self._id = namespace
		if _rootName is not None:
			self._rootName = _rootName

		if "_services" in kwargs and len(self._services) == 0:
			self._services = kwargs["_services"]
			for service in kwargs["_services"]:
				# print(" ::: SERVICE1 :::", service)
				self._services[service] = {"client": None,
                                    "port": kwargs["_services"][service]}
			# for service in self._services:
			# 	print(" ::: SERVICE0 :::", service)

		if type(self)._services is not None and len(self._services) == 0:
			self._services = type(self)._services

		if self._services is not None:
			type(self)._services = self._services
			if namespace is not None and runServer:
				if namespace in self._services:
					print(" !!! FOUND SERVER NAMESPACE ",
					      namespace, self._services[namespace])
					reqPort = self._services[namespace]["port"]
					self._reqPort = reqPort
					# print("999999999999999999999", reqPort)
				else:
					pass
					# print("XXXXXXXXXXXXXXXXXXXXXXXXXX11111",
					#       runServer, namespace, kwargs["_services"])
			# for service in self._services:
			# 	print(" ::: SERVICE0 :::", service)
		else:
			# print("XXXXXXXXXXXXXXXXXXXXXXXXXX2222", func, namespace, kwargs)
			pass

		if runServer:
			pubPort = MicroXO._pubPort
			if reqPort is None:
				pass
				print(" ::: WTF0 ::: ",namespace,self._reqPort,self._services)
			if reqPort is None:
				# Get port
				reqPort = self._reqPort
				# print("NICEEEEEEEEEEEEE")
			if reqPort is None:
				# Get port
				reqPort = MicroXO._reqPort
			else:
				pubPort = int(str(reqPort)+"1")
			

			# self._reqServer = xoServer(port = int(str(port)+"1")) 
			killport.kill_ports(ports=[reqPort, pubPort])
			time.sleep(.2)
			# self._pubserver = Server(xoServer._pubPort)
			self._reqPort = reqPort
			print("@@@@@@@@@@@@@@@@@@@@@@@@@@",reqPort,self._reqPort)
			self._reqServer = Server(reqPort)
			self._pubPort = pubPort

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
				reply, listen_for_request = self._reqServer.reply()
				c = 0
				for payload in listen_for_request:
					c += 1
					try:
						print()
						print(c, "::: INCOMING:", payload, "type:",type(payload))
						# print()
						# print("INDEX:",MicroXO.index)
						# print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
						# f"ECHO! {msg}".encode()
						# reply(bytes("ECHO! "+str(msg)))
						payload = json.loads(payload)
						# payload = pk.loads(payload)
						target = payload["target"] if "target" in payload else None
						if target in MicroXO.index:
							print(" ::: TARGET FOUND ! :::", target, MicroXO.index[target])
							# print("##########")
							res = None
							try:
								res = self.index[target](*payload["args"],**payload["kwargs"])
								# print("@@@@@@@@@@@")
								res = json.dumps(res)
								# print("@@@@@@@@@@@")
								res = res.encode()
							except:
								traceback.print_exc()

							print(" ::: OUTGOING REPLY :::\n",res,"\n\n\n")
							if res is None:
								reply(bytes(True))
							else:
								# reply(bytes(json.dumps(res)))
								# print("##########")
								# reply(json.dumps(res).encode())
								reply(res)
								# print("##########")
						else:
							reply(f"ECHO! {target} was not found in index".encode())
		
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
			print(self._id+"!!!!!", self._rootName,)
			requests = Thread(target=listen, args=[self._id, ])
			requests.start()
			# print(" ::: Requests Server Started {"+f" {namespace}"+" }"+f" port {self._reqPort}")
			print(" ::: Requests Server Started {"+f" {namespace}"+" }"+f" port {reqPort}")
			# time.sleep(1)
			# pub = Thread(target=pushToSubs, args=[self._id, ])
			# pub.start()
			

	@staticmethod
	def register(namespace=None, port=None,*args,**kwargs):
		if namespace is None:
			namespace = MicroXO.getNamespace()
		return MicroXO(funcOrNamespace=namespace, reqPort = port, *args, **kwargs)

	@staticmethod
	def getNamespace():
		return "microxo"

	@staticmethod
	def getPorts():
		return {""}
		
	# _services = {"microxo": 1993,} # OVERLOAD THIS
	# _current_namespace = MicroXO.getNamespace()
	# _servers = getPorts()

	def DefaultFunc(self, payload):
		# print("PPPPPPP", payload)
		id = payload["kwargs"]["id"] if "kwargs" in payload and "id" in payload["kwargs"] else None
		namespace, target = None, None
		if id is not None:
			if len(id.split("/")) > 2:
				namespace = id.split("/")[1]
				target = "/".join(id.split("/")[2:])
				
				# print(" $$$$$$$ NAMESPACE $$$$$$$ ", namespace)
				# print(" $$$$$$$ TARGET $$$$$$$ ", target)

				# if MicroXO._current_namespace == namespace:
				# 	pass
				# 	BROADCAST PUSH 
				# else:
				# 	# REQUEST FROM SERVER
				# 	print(" $$$$$$$ REQUESTING FROM SERVER $$$$$$$ ", namespace)
				# 	SEND REQUEST TO SERVER
				# xoClient().request(namespace+"/"+target, * payload["args"], ** payload["kwargs"])
				if namespace in self._services:
					# print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
					# print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
					# print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
					if self._services[namespace]["client"] is None:
						print(f" ::: Found Port for namespace {namespace} ",self._services[namespace])
						print(f" ::: OPENING CLIENT TO {namespace} {self._services[namespace]['port']}")
						self._services[namespace]["client"] = xoClient(_reqPort=self._services[namespace]["port"])
						
					resp = self._services[namespace]["client"].request(namespace+"/"+target, *payload["args"], ** payload["kwargs"])
					print(" ::: GOT REPLY FROM {namespace} / {target} :::")
					# print(resp)
					return resp


				else:
					print(f" ::: COULD NOT FIND Port for namespace {namespace} !  Available Services:\n",self._services,"\n\n")
					# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",self._services)
					# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
					# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
					# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",namespace)

					# xoClient().request(namespace+"/"+target, * payload["args"], ** payload["kwargs"])



				
		# print(":::::::::::::::::::::::::::", self._id, payload)
		# if target is not None:
		# 	print(f" ::: Sending Request to Server {namespace} ::: {target}")
		# 	print(" $$$$$$$ TARGET $$$$$$$ ", target)
		# 	# return self._getRoot().CallFunc(payload)
		# return "NICE!!!!!!"
		return False



class service(MicroXO):
	pass

class gps(MicroXO):
	pass


@service
def foo(*args, **kwargs):
	print("FOO", args, kwargs)


@service
def bar(*args, **kwargs):
	print("BAR", args, kwargs)


@service
def Sara(*args, **kwargs):
	print("SARA IS AWESOME <3", args, kwargs)
	# fin = json.dumps({"SARA IS AWESOME <3", args, kwargs})
	fin = {"res":"SARA IS AWESOME <3", "args": args, "kwargs":kwargs}
	print("$$$$$$$$$$")
	return fin
	# return "SARA IS AWESOME <3"


@gps
def location(*args, **kwargs):
	fin = {"location": {"lat": 37.422, "lng": -122.084}, "args": args, "kwargs":kwargs}
	return fin

# bar()
# m = MicroXO()

# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
# print(m.index)
# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
# print(type(d.index["xo/bar"]))
# d.index["xo/bar"]("NICEEEEEEEE!!!!!!!!!!!!!!")


# import MicRobee
# MicRobee = MicRobee.register("Webapi", 1970)


# def getLocation():
# 	return MicRobee.gps.location()


# m.Sara(" And very loved by me :-*")
# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

		# print(args, kwargs)
		# self._func = lambda : 1

	# def __call__(self, *args, **kwargs):
	# 	self._id
	# 	print("DECORATOR", self._id, self._func, args, kwargs)
	# 	if self._func is not None:
	# 		return self._func(*args, **kwargs)
	# 	# if isinstance(self.value, function):
	# 	if "function" in str(type(self.value)):
	# 		return self.value(*args, **kwargs)
	# 	return self.value

