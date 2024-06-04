# from zero.xoServer import xoClient

# from expando import Expando

from zeroless import Client, Server
# from xo.zmq import xoServer
import killport
# from xo_zmq import xoClient
from .xoServer import xoClient

from threading import Thread
import traceback
import time, os
import json
import dill as pk


from .xo import xoBenedict# Server, Client, FreshRedis,
xo = xoBenedict()

public:xoBenedict = xo.public

class FreshZero(xoBenedict):
	_reqServer = None
	_reqPort = None
	__root = None
	# value = None
	request_port=1970
	publish_port=19701
	inc = 0
	def __init__(self, request_port=1970, publish_port=19701, inc=0, *a, **kw):
		request_port += inc
		publish_port += inc
		if FreshZero.__root == None:
			FreshZero.__root = self
			print("------------ ONLY ONCE ------------")
			super().__init__(*a,**{**kw,**{"_id":"FreshZeroServer"}} )
			self._isRoot = True
		if self._isRoot:
			super().__init__(*a, **kw)
			self._reqPort = reqPort = request_port
			pubPort = publish_port
			killport.kill_ports(ports=[reqPort, pubPort])
			time.sleep(.2)
			print("@@@@@@@@@@@@@@@@@@@@@@@@@@",reqPort,self._reqPort)
			self._reqServer = Server(reqPort)
			print("@@@@@@@@@@@@@@@@@@@@@@@@@@x",reqPort,self._reqPort)
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
						# payload = json.loads(payload)
						payload = pk.loads(payload)
						target = payload["target"] if "target" in payload else None
						# print("TTTTTTTTTTT:",target)
						if target in public or target in self:
							if target in self: owner = self
							else: owner = public
							print(" ::: TARGET FOUND ! :::", target, owner[target])
							# print("##########")
							res = None
							try:
								# res = self.index[target](*payload["args"],**payload["kwargs"])
								res = owner[target].value
								if "function" in str(type(res)):
									res = res(*payload["args"],**payload["kwargs"])

								print("@@@@@@@@@@@")
								# res = json.dumps(res)
								res = pk.dumps(res)
								print("@@@@@@@@@@@")
								# res = res.encode()
							except:
								traceback.print_exc()
							print(" ::: OUTGOING REPLY :::\n",res,"\n\n\n")
							if res is None:
								# reply(bytes(True))
								reply(pk.dumps(True))
							else:
								# reply(bytes(json.dumps(res)))
								# print("##########")
								# reply(json.dumps(res).encode())
								# if res
								# reply(pk.dumps(res))
								reply(res)
								# print("##########")
						else:
							print(f"{target} not found in public")
							reply(pk.dumps(f"ECHO! {target} was not found in index ({payload['args'],payload['kwargs']})".encode()))
							if True and len(payload["args"])>0:#Change to Auth
								public[target] = payload["args"][0]
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
		# print(self._id+"!!!!!", self._rootName,)
			requests = Thread(target=listen, args=["new", ])
			requests.start()
			# print(" ::: Requests Server Started {"+f" {namespace}"+" }"+f" port {self._reqPort}")
			print(" ::: Requests Server Started {"+f" xxxxxx "+" }"+f" port {reqPort}")
			# time.sleep(1)
			# pub = Thread(target=pushToSubs, args=[self._id, ])
			# pub.start()

	def __call__(self,funcOrValue, *args, **kwargs):
		print("CALLING FRESH SERVER",funcOrValue, args, kwargs)
		self.__setitem__("value",funcOrValue)
		return funcOrValue


if __name__ == '__main__':
	freshServer = FreshZero()
	freshServer.public = public

	def pnr(v,*a,**kw): print(v,a,kw); return v if a==[] and kw == {} else (v,a,kw)

	@freshServer.nice
	def nice(*a, **kw):
		'''a nice description'''
		return pnr("NICE",a,kw)

	@public.very.nice
	def very_nice(*a, **kw):
		'''a very nice description'''
		return pnr("VERY NICE",a,kw)

	hi = lambda *args, **kwargs: ("hi",args,kwargs)
	get_index_keys = lambda *a,**k: list(public.flatten().keys()) if len(a) == 0 else list(public[a[0]].flatten().keys())
	get_funcs = lambda *a, **kw: [[k, public[k].value.__doc__] for k in get_index_keys(*a, **kw)]

	def hi(*a, **kw):
		'''hi aaaaaaaaa nice description'''
		return pnr("hi",a,kw)

	public.foo.hi = hi
	public.index = get_funcs
	public.new_func = lambda _id, func: public[_id].value.set(func)


	print(xo)
	if __name__ == "__main__":
		while(True):
			time.sleep(1)
