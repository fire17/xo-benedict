#xoDecorator.py

from xo import xoBenedict, FreshRedis, xoMetric, Fresh, color, figlet, pnr


class xoDecorator(xoBenedict):
	# def __init__(self,*args, **kwargs):
	# 	return super().__init__(*args, **kwargs)
	args, kwargs, first, =  None, True, None
	xo = None
	func = None
	def __init__(self, *args, **kwargs):
		print("DECORATOR INIT",args,kwargs)
		self.args = args
		self.kwargs = kwargs
		self.first = True
		if len(args)>=1 and isinstance(args[0],xoBenedict):
			self.xo = args[0]
			args = list(args)
			args.pop(0)
			print("Got xo!", self.xo._id)
			
		sup = super().__init__(*args, **kwargs)
		print("AFTER INIT")
		return sup
	
	def __call__(self, *args, **kwargs):
		print("DECORATOR CALL",args,kwargs)
		print("ALL ARGS",self._id, self.args,self.kwargs)
		if self.first and "func" in str(type(args[0])): #TODO: check for better way to check type is function
			self.first = False
			func = args[0]
			if self.xo:
				self.xo.value = func

			def wrapper(*args, **kwargs):
				print(f"ON CALL -> ", args, kwargs)
				print("ALL ARGS",self._id, self.args,self.kwargs)
				res = func(*args, **kwargs)
				print("AFTER CALL")
				self.result = res
				return res
			if self.xo:
				self.xo.value = wrapper
				self.xo @= wrapper
			self.func = wrapper
			self.value = wrapper
			return wrapper
		return super().__call__(*args, **kwargs)
	
	def __onchange__(self, fullkey, value, *args, **kwargs):
		key = fullkey[len(self._id+"."):]
		print("DECORATOR CHANGED",self._id,fullkey,value, args, kwargs)
		# if self[key].value == value:
		# 	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
		# 	return value
		
		print("$ $ $ $ $ Decorator changed $ $ $ $ $", fullkey, value, args, kwargs)
		# if "sender" not in kwargs: #kwargs include __setitem__ kwargs
		# 	yourID = hash(self._root._redis)
		# 	print("$ $ $ $ $ SYNCING METRICS! $ $ $ $ $", fullkey, value, args, kwargs)
		# else: # Got metric from another xooMetric (redis) client
		# 	print(f"$ $ $ $ $ Got METRICS from {kwargs['sender']}! $ $ $ $ $", fullkey, value, args, kwargs)
		# if "skip_publish" in kwargs:
		# 	return value
		return value # make sure to call redis
		# return super().__onchange__(fullkey, value, *args, **kwargs) # make sure to call redis


class expose(xoDecorator):
	pass

class Host(xoDecorator):
	pass

xo = xoBenedict()
host = Host()

# @expose(xo.foo)
# def foo(*a,**kw):
# 	return pnr("Does Something Cool!",*a,**kw)

@host.a.b.c
def bar(*a,**kw):
	return pnr("Does Something AWESOME!",*a,**kw)

