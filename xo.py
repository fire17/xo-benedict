import ast
from benedict.dicts.io import IODict
from benedict.dicts.keyattr import KeyattrDict
# from benedict.dicts.keylist import KeylistDict
from benedict.dicts.keypath import KeypathDict
from benedict.dicts.parse import ParseDict
from benedict import benedict#, KeyattrDict, KeypathDict, IODict, ParseDict
# b = benedict()
import dill as pk


counter =0

class xoBenedict(benedict):#KeyattrDict, KeypathDict, IODict, ParseDict):
	# _benedict = benedict()
	_root = None
	_isRoot = False
	_id:str = "yyy"
	
	ignore_keys = ['_override','keyattr_dynamic', 'keyattr_enabled','keypath_separator','check_keys']
	def __init__(self,*args, **kwargs):
		"""
		Constructs a new instance.
		"""
		if xoBenedict._root is None:
			xoBenedict._root = self
			self._isRoot = True
		else:
			self._root = xoBenedict._root
		
		nid = None
		print("iiiiiiiiiiiiiiii",args,kwargs)
		if "_id" in kwargs:
			nid = kwargs.pop("_id")
		print("_IDIDIDID", nid, "param")
		# print("_IDIDIDID", nid, "param",_id)
		if nid:
			self._id = nid
		else:
			# self._id = str(_id)
			self._id = "ROOT"
		print(":::",self._id)
		

		global counter
		my_c = counter
		counter += 1
		# print("iiiiiiiiiiiiiiiiiiiiiiiiiiiii",":::",my_c,":::",len(args))
		kwargs["keyattr_dynamic"] = True
		setRoot = False
		# if "_parent" not in kwargs:
			# print("RRRRRRRRRRRRRRRRRRRRRRRRooooooooooot")
		# 	pass
			# kwargs["_isRoot"] = True
			# kwargs["_parent"] = None
			# kwargs["_root"] = self
			# self.set("_root",[self])
			# setRoot = True
		# else:
		# 	self.set("_root",kwargs["_parent"]["_root"])

		# 	kwargs["_isRoot"] = False
		# 	kwargs["_root"] = kwargs["_parent"]["_root"]

			
		# args = list(args)
		
		# no args other than self
		# print("aaaaaaaaaaaaaa",args,kwargs)#, args[0] == self)
		if len(args) == 1 and isinstance(args[0], xoBenedict):
			# print("zZZZZZZZZ")
			obj = args[0]
			kwargs.setdefault("keyattr_enabled", obj.keyattr_enabled)
			kwargs.setdefault("keyattr_dynamic", obj.keyattr_dynamic)
			# kwargs.setdefault("keyattr_dynamic", True)
			kwargs.setdefault("keypath_separator", obj.keypath_separator)
			# print("OOOOOOOOOOOOOOOOxxxxOOOOOOOOOOOOO",len(args),args,kwargs)
			print("@ @ @ @ @ @ @ @ @ @ B", args, kwargs)
			super().__init__(obj.dict(), **kwargs)
			# self.update(kwargs)
			# print("OOOOOOOOO o o ")
			# if setRoot:
				# self.set("_root",kwargs["_parent"]["_root"])
				# self.set("_root",[self])
			return
		# super().__init__(*args, **kwargs)
		# if "_skip" not in kwargs or not kwargs["_skip"]:  
		#     super().__init__(*args, **kwargs)
		extras = []
		if len(args)>=1:
			if isinstance(args[0],str):
				# try:
				if True:
					#TODO: more general string to dict parser
					# print("JJJJJJJJSSSSSSSSSSSSSSSSSS")
					# print("JJJJJJJJSSSSSSSSSSSSSSSSSS",type(args[0]),args[0])
					# args[0] = self.from_json(args[0])
					args = [ast.literal_eval(args[0].strip("'<>() ")) ]
					# args = [json.loads(repr(args[0]).strip("'<>() ").replace("\\\'","\\\\'"))]#..replace('\'', '\"'))]
					# print("JJJJJJJJSSSSSSSSSSSSSSSSSS",type(args[0]),args[0])
					# print("JJJJJJJJSSSSSSSSSSSSSSSSSS")
				# except:
				# 	print("XXXXXXXXXXXXXXXXXXXXXXXXXX Could not load from string",)
				# 	pass
			if isinstance(args[0], dict):
				for k in args[0]:
					if k not in self.ignore_keys:
						kwargs[k] = args[0][k]
					else:
						extras.append(args[0][k])
				if len(extras) > 0:
					args = [extras]
			else:
				extras.append(args[0])
				args = [extras]
		if len(args)>1:
			final = {}
			for a in args:
				if isinstance(a,dict) and not isinstance(a,type(self)):
					for k in a:
						final[k] = a[k]
						kwargs[k] = a[k]
				else:
					extras.append(a)
			if len(final) > 0:
				args = [final]
		# print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOO",len(args),args)
		# print("OOOOOOOOOOOOOOOOvvvvOOOOOOOOOOOOO",len(args),args,kwargs)

		# print("@ @ @ @ @ @ @ @ @ @ ", args, kwargs)
		super().__init__(*args[::], **kwargs)
		#{"AAA": {"b": {"c": "yooooooooooooooo'\""}}, "a": {"b": {"c": {"d": "DDDDDDDDDDDDDDDDDDDDDDDDDDD"}}}, "aa": 1111111}
		# extras = []

		if "_parent" not in kwargs:
			pass
			# kwargs["_isRoot"] = True
			# kwargs["_parent"] = None
			# kwargs["__root"] = self
		# else:
		# 	kwargs["_isRoot"] = False
		# 	kwargs["_root"] = kwargs["_parent"]["_root"]
		extra_keys = {k:v for k,v in kwargs.items() if k not in self.ignore_keys}
		
		# if setRoot:
			# extra_keys["_root"] = kwargs["_parent"]["_root"]
			# extra_keys["_root"] = self
			# self.set("_root",)
		# if len(args)==1 and args[0] == self:
		#         return self.__init__(**{**{"_skip":True}, **args[0]})

		if len(args)>1:
			print("AAAaaaaaaaaaaaaaa",args, args[0] == self)
			for a in args:
				if a != self:
					print("AAA")
					if isinstance(a,dict):
						for k in a:
							# kwargs[k] = a[k]
							
							extra_keys[k] = a[k]
					else:
						extras.append(a)
						print("OOOOOOOOOOOOOOOO")
						print("OOOOOOOOOOOOOOOO")
						print("OOOOOOOOOOOOOOOO")
						print("OOOOOOOOOOOOOOOO",a)
				# print("BBB")
				else:
					pass
					# return
		# print("eeeeeeeeeeee",extras)
		# print("yo yo yo ", kwargs == self)
		
		if "value" not in extra_keys and len(extras) > 0:
			extra_keys["value"] = extras[0] if len(extras)==1 else extras
		
		update_incoming = True # Set to False to work leaner (checking for self[key] doubles the calls)
		# update_incoming = False # Set to False to work leaner (checking for self[key] doubles the calls)
		if update_incoming:
			for key, value in extra_keys.items():
				# print("mmm",key,value, key in self)
				# print("WWWWWWWW",type(value))
				if key != "value" and key in self and type(self[key]) != type(self):
				# if key != "value" and key in self:# and type(self[key]) != type(self):
					# print("kkk",key,type(self[key]) != type(self))
					# print("MMMMMMMMMMMMM",key,value, key in self)
					self[key] = value
					# print(".x.",key)
				elif key not in self:
					# print("!!!!!!!!!!!!!!!!!!",key)
					if key == "value":
						self[key] = value
					else:
						self[key] = value
						pass
				else:
					pass
					# print("...")

		if False and "_override" in kwargs and kwargs["_override"]:
			if len(args) == 1 and isinstance(args[0], dict):
				obj = args[0]
				# for key, value in {**obj,**extra_keys}.items():
				# for key, value in {**obj}.items():
				for key, value in {**obj,**extra_keys}.items():
					print("vvv",key, value, key in obj,":::",my_c,":::")
					#TODO: check missing key
					if key not in self:
						print("~~~~~~~~R0",key,":::",my_c,":::")
						self[key] = type(self)()
					else:
						pass
						if not isinstance(self[key], dict):
							print("~~~~~~~~R1",key,":::",my_c,":::")
							self[key] = type(self)()
							self[key].value = self[key]
							pass
					# print("TTTTTTTT",key, type(self[key]),self[key])
					# if False:
					if isinstance(value, dict):
						print("DDDDDDDD")
						self[key] = value
					else:
						if key == "value":
							print(" V V V V")
							
							print("~~~~~~~~R2",key,":::",my_c,":::")
							self[key] = value
							pass
							# self[key] = value
						else:
							print("vVVVVVVV",key)
							print("~~~~~~~~R3",key)
							self[key]["value"] = value
							print("VVV", self)
		# self.update(kwargs)


	def __call__(self,*args, **kwargs):
		# print("ccccccccccccccCCCCCCCALLLLLLLLLLLLLLLLLL")
		if "value" in self and "function" in str(type(self["value"])):
			return self["value"](*args, **kwargs)
		else:
			entries = type(self)(kwargs,_override=True, keyattr_dynamic=True)

			self.update(entries)
			if len(args) == 1:
				if isinstance(args[0], dict):
					for key, value in args[0].items():
						self[key] = value
				else:
					self["value"] = args[0]
			elif len(args) > 1:
				
				self["value"] = list(args)
			return self
			# return self["value"] if "value" in self else self


	#TODO update and constructor of dicts, final value as obj


	
	def __getitem__(self, key):
		
		# if key not in self.__dict__:
		# getKeys = True
		# if key == "keys":
		# 	print("XXXXXXXXXXXX")
		# if key not in self.keys():
		if key not in self.__dict__:
			res = self._cast(super().__getitem__(key), key = self._id+"."+key)
			# print("WORKING !!!!!!!!!!!!")
			self.__dict__[key] = res
			return res
		if key in self.__dict__ and isinstance(self[key],type(self)):
			print("skip!")
			return dict(self).__getitem__(key)
		return super().__getitem__(key)


    # def __getitem__(self, key):
    #     return self._cast(super().__getitem__(key), key = self._id+key)

    # def __setitem__(self, key, value):
    #     return super().__setitem__(key, self._cast(value))

	def set(self,*args, **kwargs):
		# print("SSSSSSSSSSSSSSSSS",)
		# print("SSSSSSSSSSSSSSSSS")
		# print("SSSSSSSSSSSSSSSSS")
		# print("SSSSSSSSSSSSSSSSS",args,kwargs,)
		# print("CCCCCCCCCCCCCCCCC",self)
		for k in kwargs:
			self.set(k,kwargs[k])
		kwargs = {}
		#TODO: goto parent, set by name
		if len(args) == 1:
			target = args[0]
			if isinstance(target, dict) or isinstance(target, type(self)):
				for k in target:
					self[k] = target[k]
				return self
			# elif isinstance(target, obj_type):
			# 	for k in target:
			# 		self[k] = target[k]
			# 	return self
			# else:
			# 	self["value"] = target
			# 	return self
			self["value"] = target
			return self
		# print("######################")
		# print("######################")
		# print("######################")
		# print("######################")
		# print("######################",args, kwargs)
		if len(args) > 1:
			res = super().set(*args, **kwargs)
		# if res: return res;
		return self

	def __setitem__(self, key, value, skip = False, **kw):
		
		obj_type = type(self)
		# obj_type()
		print("set KKKKKKKK",key)
		if key != "value" and not isinstance(value, dict) and not isinstance(value, obj_type) and not skip:
			print("111111111111", value)
			
			# value = obj_type({"value":value}, keyattr_dynamic=True, _parent = self)
			print("NEXT:",self._id+"."+key)
			value = xoBenedict({"value":value}, _id = self._id+"."+key, keyattr_dynamic=True)
			print("set 22222222222", value)
			# value.__setitem__(,value, skip = True)
			# print("value", value)
			# print("key", key)
			if key in self and key != "value":
				if not isinstance(self[key],dict):
					self[key] = value
					# self.__dict__[key] = value
					self.__dict__[key] = self[key]
				else:
					self[key].update(value)
					for k in value:
						# self[key].__dict__.update(value)
						# self[key].__dict__[k]=value[k]
						# self[key].__dict__[k]=self[key][k]
						# self.__dict__[key].__dict__[k]=self[key][k]
						pass
					# self[key].__dict__.update(value)
					# self[key].__dict__.update(value)
				return self[key]
			else:
				print("key",key,"type",type(value),"value",value)
				# self.__dict__[key] = value
				# self[key] = value
				# res = super().__setitem__(key, value)
				print("222222222222222@@@@@@@@@@@@@@@@@22")
				# res = self.__setitem__(key, value, skip = True)
				# res = self.__setitem__(key, value, skip = True)
				# self.__dict__[key] = self[key]
				# return res
				# return self[key]
		if True:
			print("set 3333333", value, key, )
			print(key in self,"!!!!!!!!!!!!", type(value))
			if isinstance(value, dict) and not isinstance(value, type(self)):
				value = self._cast(value, key = self._id+"."+key)
			# self.__dict__[key]=f
			# return f
			# res = super().__setitem__(key, f)
			# if key in self.__dict__ and isinstance(self[key],type(self)):
			# 	print("skip!")
			# 	return super().__getitem__(key)
			res = super().__setitem__(key, value)
			self.__dict__[key]=value
			print(key in self,"!!!!!!!!!!!!")#, type(self.__dict__[key]))
		# if isinstance(value, dict):
		# 	for k in value:
		# 		# self[key].__dict__[k] = self[key][k]
		# 		# self[key].__dict__[k] =
				 
		# 		print("@@@@@@@@@@@@",key)
		# 		if key in self.__dict__:
		# 			self.__dict__[key].__dict__[k] = self[key][k]
		# 			print("@@@@@@xxx@@@@@@",key)
		# self.__dict__[key] = self[key]
		# # self.__dict__[key] = f
		if isinstance(value, dict):
			for k in value:
				# self.__dict__[key].__dict__[k] = self[key][k]
				# self.__dict__[key].__dict__[k] = value[k]
				# res.__dict__[k] = self[key][k]
				# self.__dict__[k] = self[key][k]
				# self.__dict__[key][k]=self[key][k]
				# self.__dict__[key].__dict__[k]=value[k]
				# self.__dict__[key].__dict__[k]=self[key][k]
				pass #messup
		# return self[key]
		return res


	# def items(self):
	#     for key, value in super().items():
	#         # yield (key, self._cast(value))
	#         yield (key, value)

	def _cast(self, value, key = None):
		"""
		Cast a dict instance to a benedict instance
		keeping the pointer to the original dict.
		"""
		# print("Cast", self)
		obj_type = type(self)
		print("oooooooo",obj_type,key)
		if isinstance(value, dict) and not isinstance(value, obj_type):
			data = {"keyattr_enabled":self._keyattr_enabled,
				"keyattr_dynamic":self._keyattr_dynamic,
				"keypath_separator":self._keypath_separator,
				"check_keys":False,}
			# if key:
			# 	data["_id"] = key
			
			# return obj_type(
			return xoBenedict(
				value,_id = key,
				**data
				# _parent = self,
			)
		elif isinstance(value, list):
			for index, item in enumerate(value):
				value[index] = self._cast(item)
		# final = obj_type(
		#         {"value":value},
		#         keyattr_enabled=self._keyattr_enabled,
		#         keyattr_dynamic=self._keyattr_dynamic,
		#         keypath_separator=self._keypath_separator,
		#         check_keys=False,
		#     )
		# return final
		return value




	#TODO print cleanup
	#TODO add _id
	#TODO add subscribe
	#TODO add getHook
	#TODO add setHook
	#TODO flat expando - get _ids from _root_
	def __imatmul__(self, other):
		''' Special Subscribe function '''
		print("SUBSCRIBING TO ",self)
		if "value" in self:
			self["value"] @= other
		else:
			super().__imatmul__(other)
		return self


	def append(self, other):
		if "value" in self:
			if isinstance(self["value"],list): 
				for item in other:
					self["value"].append(item)
			else:
				if isinstance(other,list): 
					self["value"] = [self["value"]]
					for item in other:
						self["value"].append(item)
				else:
					self["value"] = [self["value"], other]
		else:
			self["value"] = [other]
		return self

	def __add__(self, other):
		otherT = type(other)
		if otherT == dict:
			pass
		if "value" in self:
			if isinstance(other, str) and not isinstance(self["value"], str) \
				or isinstance(self["value"], str) and not isinstance(other, str) :
				return str(self["value"]) + str(other)
			if otherT == list:
				if isinstance(self["value"],list):
					return list(self["value"]).append(other)
				return [self["value"]].append(other)

			return self["value"] + other
		if otherT == list:
			return otherT
		return self._cast(super().__add__(other))

	def __iadd__(self, other):
		otherT = type(other)
		if isinstance(other,dict):
			for k in other:
				self[k] = other[k]			
			return self
		if otherT == list:			
			return self.append(other)
		
		if "value" in self:
			if isinstance(self["value"],list) and not isinstance(other,list):
				return self.append([other])
			self["value"] += other
		else:
			if otherT == list:
				return otherT
			super().__iadd__(other)
		return self

	def __sub__(self, other):
		if "value" in self:
			return self["value"] - other
		return self._cast(super().__sub__(other))
	
	def __isub__(self, other):
		if "value" in self:
			self["value"] -= other
		else:
			super().__isub__(other)
		return self

	def __mul__(self, other):
		if "value" in self:
			return self["value"] * other
		return self._cast(super().__mul__(other))

	def __imul__(self, other):
		if "value" in self:
			self["value"] *= other
		else:
			super().__imul__(other)
		return self

	def __truediv__(self, other):
		if "value" in self:
			return self["value"] / other
		return self._cast(super().__truediv__(other))
	
	def __itruediv__(self, other):
		if "value" in self:
			self["value"] /= other
		else:
			super().__itruediv__(other)
		return self
	
	def __floordiv__(self, other):
		if "value" in self:
			return self["value"] // other
		return self._cast(super().__floordiv__(other))

	def __ifloordiv__(self, other):
		if "value" in self:
			self["value"] //= other
		else:
			super().__ifloordiv__(other)
		return self

	def __mod__(self, other):
		if "value" in self:
			return self["value"] % other
		return self._cast(super().__mod__(other))

	def __imod__(self, other):
		if "value" in self:
			self["value"] %= other
		else:
			super().__imod__(other)
		return self

	def __pow__(self, other):
		if "value" in self:
			return self["value"] ** other
		return self._cast(super().__pow__(other))

	def __ipow__(self, other):
		if "value" in self:
			self["value"] **= other
		else:
			super().__ipow__(other)
		return self
	
	def __radd__(self, other):
		if "value" in self:
			if isinstance(other, str) and not isinstance(self["value"], str) \
				or isinstance(self["value"], str) and not isinstance(other, str) :
				return  str(other)+str(self["value"])
			return other + self["value"]
		return self._cast(super().__radd__(other))

	def __rsub__(self, other):
		if "value" in self:
			return other - self["value"]
		return self._cast(super().__rsub__(other))

	def __rmul__(self, other):
		if "value" in self:
			return other * self["value"]
		return self._cast(super().__rmul__(other))

	def __rtruediv__(self, other):
		if "value" in self:
			return other / self["value"]
		return self._cast(super().__rtruediv__(other))

	def __rfloordiv__(self, other):
		if "value" in self:
			return other // self["value"]
		return self._cast(super().__rfloordiv__(other))
	
	def __rmod__(self, other):
		if "value" in self:
			return other % self["value"]
		return self._cast(super().__rmod__(other))

	def __rpow__(self, other):
		if "value" in self:
			return other ** self["value"]
		return self._cast(super().__rpow__(other))
	
	'''
	def __lshift__(self, other):
		if "value" in self:
			return self["value"] << other
		return self._cast(super().__lshift__(other))

	def __ilshift__(self, other):
		if "value" in self:
			self["value"] <<= other
		else:
			super().__ilshift__(other)
		return self

	def __rshift__(self, other):
		if "value" in self:
			return self["value"] >> other
		return self._cast(super().__rshift__(other))

	def __irshift__(self, other):
		if "value" in self:
			self["value"] >>= other
		else:
			super().__irshift__(other)
		return self
	'''
	def __and__(self, other):
		if "value" in self:
			return self["value"] & other
		return self._cast(super().__and__(other))

	def __iand__(self, other):
		if "value" in self:
			self["value"] &= other
		else:
			super().__iand__(other)
		return self
	
	def __or__(self, other):
		if "value" in self:
			return self["value"] | other
		return self._cast(super().__or__(other))

	def __ior__(self, other):
		if "value" in self:
			self["value"] |= other
		else:
			super().__ior__(other)
		return self
	
	def __xor__(self, other):
		if "value" in self:
			return self["value"] ^ other
		return self._cast(super().__xor__(other))
		
	def __ixor__(self, other):
		if "value" in self:
			self["value"] ^= other
		else:
			super().__ixor__(other)
		return self
	
	'''
	def __rlshift__(self, other):
		if "value" in self:
			return other << self["value"]
		return self._cast(super().__rlshift__(other))
	
	def __rrshift__(self, other):
		if "value" in self:
			return other >> self["value"]
		return self._cast(super().__rrshift__(other))
	'''
	def __rand__(self, other):
		if "value" in self:
			return other & self["value"]
		return self._cast(super().__rand__(other))

	def __ror__(self, other):
		if "value" in self:
			return other | self["value"]
		return self._cast(super().__ror__(other))

	def __rxor__(self, other):
		if "value" in self:
			return other ^ self["value"]
		return self._cast(super().__rxor__(other))

	def __neg__(self):
		if "value" in self:
			return -self["value"]
		return super().__neg__()

	def __pos__(self):
		if "value" in self:
			return +self["value"]
		return super().__pos__()

	def __abs__(self):
		if "value" in self:
			return abs(self["value"])
		return super().__abs__()

	def __invert__(self):
		if "value" in self:
			return ~self["value"]
		return super().__invert__()
		
	def __complex__(self):
		if "value" in self:
			return complex(self["value"])
		return super().__complex__()
	
	def __int__(self):
		if "value" in self:
			return int(self["value"])
		return super().__int__()
	
	def __float__(self):
		if "value" in self:
			return float(self["value"])
		return super().__float__()
	
	def __round__(self, n=None):
		if "value" in self:
			return round(self["value"], n)
		return super().__round__()

	def __trunc__(self):
		if "value" in self:
			return math.trunc(self["value"])
		return super().__trunc__()
	
	# def __floor__(self):
	# 	if "value" in self:
	# 		return math.floor(self["value"])
	# 	return self._cast(super().__floor__(other))

	# def __ceil__(self):
	# 	if "value" in self:
	# 		return math.ceil(self["value"])
	# 	return self._cast(super().__ceil__(other))

	def __bool__(self):
		if "value" in self:
			return bool(self["value"])
		return super().__bool__()
	
	

	def __eq__(self, other):
		if "value" in self:
			return self["value"] == other
		return self._cast(super().__eq__(other))

	def __ne__(self, other):
		if "value" in self:
			return self["value"]!= other
		return self._cast(super().__ne__(other))

	def __lt__(self, other):
		if "value" in self:
			return self["value"] < other
		return self._cast(super().__lt__(other))

	def __le__(self, other):
		if "value" in self:
			return self["value"] <= other
		return self._cast(super().__le__(other))
	
	def __gt__(self, other):
		if "value" in self:
			return self["value"] > other
		return self._cast(super().__gt__(other))

	def __ge__(self, other):
		if "value" in self:
			return self["value"] >= other
		return self._cast(super().__ge__(other))

	# def __hash__(self):
	# 	if "value" in self:
	# 		return hash(self["value"])
	# 	return self._cast(super().__hash__(other))

	# def __len__(self):
	# 	''' Check if the item is in the dictionary or the value. '''
	# 	if "value" in self:
	# 		return len(self["value"])
	# 	return self._cast(super().__len__(other))

	def __matmul__(self, other):
		if "value" in self:
			return self["value"] @ other
		return self._cast(super().__matmul__(other))
	
	def __rmatmul__(self, other):
		if "value" in self:
			return other @ self["value"]
		return self._cast(super().__rmatmul__(other))
	
	


	
	def xxx(self, *args, **kwargs):
		print("XXXXXXXXXXXXXXXXXXX")

	def search(self, query, *args, **kwargs):
		''' Search for a key in the dictionary. '''
		#TODO: currently choosing defult, add params to get more/all results from super()

		return list(super().search(query)[0])[0][query]

	def __repr__(self):
		return self.__str__()
		print("rrrrrrrrrrr",len(self.keys()),self.keys())
		if self._pointer:
			return repr(self._dict)
		return super().__repr__()
	
	# def __str__(self):
	#     print("ssssssssss",len(self.keys()),self.keys())
	#     if self._pointer:
	#         return str(self._dict)
	#     return super().__str__()

	def __str__(self):
		# print("S S S",len(self.keys()), self.keys())
		if "value" in self and len(self.keys()) == 1:
			# print(" VLAST ",str(self.value))
			x,y = '\"','\\"'
			if isinstance(self.value, str) and ("'" in self.value or '"' in self.value):
				# print("EEEEEEEEEEEEEEEEEE",self.value,)
				# print("EEEEEEEEEEEEEEEEEe",self.value.replace(x,y),)
				return f'"{self.value.replace(x,y)}"'
			elif isinstance(self.value, str):
				# print("eeeeeeeeee",self.value,)
				return f'"{self.value}"'
			 
			# # print(" VLAST ")
			# # if isinstance(self.value, str):
			# if type(self.value)== str:
			#     # f,r = "'",'\''
			#     # return f"\'{self.value.replace(f,r)}\'"
			#     print("vvvvvvvvvvvvvvvvvvvvvvv",self.value,":::",str(self.value))
			#     # return f"'{self.value}'"
			#     if "'" in self.value or '"' in self.value:
			#         print("AAAAAAAAAAAAAAAAAAAAAAAA")
			#         r,p,e= "\'","\\'",""
			#         r2,p2,e= "\"",'\\"',""
			#         f,pf = """\\"""+"""\\""","""\\"""
			#         res = f"""\"{(e+self.value).replace(r,p).replace(r2,p2).replace(f,p)}\""""
			#         print("RRRR:",res)
			#         return res
			#     print("BBBBBBBBBBBBBBBBBBBBBBBB")
			#     return f'"{self.value}"'
			#     # return str(f"""'''{self.value}'''""")
			# print("CCCCCCCCCCCCCCCCCCCCCCC")
			return str(self.value)
			return str(self.value)
		# return super().__str__()
		# print("DDDDDDDDDDDDDDDDDDD")
		# return "{"+""", """.join((f"""{repr(key)}: {type(self)(val) if type(val) == dict else val}""") for key, val in self.items())+"}"
		# return "{"+", ".join((f"\'{key}\': {val}") for key, val in self.items())+"}"
		return "{"+", ".join((f"\"{key}\": {val}") for key, val in self.items() if len(key)>0 and key[0]!="_")+"}"

	def to_csv(self, key="values", columns=None, columns_row=True, **kwargs):
		#TODO: MAKE SURE NESTING WORKS -> check og benedict to see behavior
		
		"""
		Encode a list of dicts in the current dict instance in CSV format.
		Encoder specific options can be passed using kwargs:
		https://docs.python.org/3/library/csv.html
		Return the encoded string and optionally save it at 'filepath'.
		A ValueError is raised in case of failure.
		"""
		kwargs["columns"] = columns
		kwargs["columns_row"] = columns_row
		if key == "values":
			return self._encode([kv for kv in self.dict().items()], "csv", **kwargs)
		else:
			return to_csv(self.dict()[key], **kwargs)

	@classmethod
	def from_json(cls, s, **kwargs):
		"""
		Load and decode JSON data from url, filepath or data-string.
		Decoder specific options can be passed using kwargs:
		https://docs.python.org/3/library/json.html
		Return a new dict instance. A ValueError is raised in case of failure.
		"""
		return cls(s, **kwargs)
	def json(self, **kwargs):
		return self.to_json(**kwargs)
	def _json(self, **kwargs):
		return self.to_json(**kwargs)
	def to_json(self, **kwargs):
		"""
		Encode the current dict instance in JSON format.
		Encoder specific options can be passed using kwargs:
		https://docs.python.org/3/library/json.html
		Return the encoded string and optionally save it at 'filepath'.
		A ValueError is raised in case of failure.
		"""
		D = self.dict()
		# print("jjjjjjjjjjjjjj",self)
		# print("dddddddddddddd",D)
		def dictOrValue(D):
			if isinstance(D,dict):
				if len(D) == 1 and "value" in D:
					# print("TTTTTTTTTTT",)
					# print("TTTTTTTTTTT",)
					# print("TTTTTTTTTTT",)
					# print("TTTTTTTTTTT",D,D["value"])
					return D["value"]
				for k in D:
					# print("kkkkkk",k)
					target = D[k]
					if isinstance(target, dict):
						# print("kkkkkkD",target)
						if len(target) == 1 and "value" in target:
							# print("TTTTTTTTTTT",)
							# print("TTTTTTTTTTT",)
							# print("TTTTTTTTTTT",)
							# print("TTTTTTTTTTT",D,target["value"])
							# return target["value"]
							D[k] = target["value"]
						else:
							for kk in target:
								# print("kkkkkkDDDDkkkk",kk)
								target[kk] = dictOrValue(target[kk])
			return D
		D = dictOrValue(D)
		# print("DDDDDDDDDDDDDDDDDDDDDDDDDD",D)
		if len(D) == 1 and "value" in D:
			return self._encode(D["value"], "json", **kwargs)
		return self._encode(D, "json", **kwargs)
	
	def _getRoot(self):
		if self._parent is not None:
			return self._parent._getRoot()
		return self


class xoEvents(xoBenedict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		ignore = ["append","clean","clear","clone","copy","deepcopy","deepupdate","dict","dump","filter","find","flatten","from_base64","from_cli","from_csv","from_html","from_ini","from_json","from_pickle","from_plist","from_query_string","from_toml","from_xls","set","setdefault","standardize","subset","swap","to_base64","to_cli","to_csv","to_html","to_ini","to_json","to_pickle","to_plist","to_query_string","to_toml","to_xls","to_xml","to_yaml","traverse","unflatten","unique","update","values","xxx","get_str_list","get_uuid","get_uuid_list","groupby","ignore_key","invert","items","items_sorted_by_keys","items_sorted_by_values","json","keyattr_dynami","keyattr_enable","keypath_separato","keypaths","keys","match","merge","move","nest","pop","popitem","remove","rename","search","from_xml","from_yaml","fromkeys","get","get_bool","get_bool_list","get_date","get_date_list","get_datetime","get_datetime_list","get_decimal","get_decimal_list","get_dict","get_email","get_float","get_float_list","get_int","get_int_list","get_list","get_list_item","get_phonenumber","get_slug","get_slug_list","get_str",]
		# self.__class__.__dir__ = lambda self, *a, **kw: list(set(dir(self)) - set(ignore))
		# self.__dir__ = self.keys
		# self.__dir__ = self.keys
	def __getitem__(self, key, *args, **kwargs):
		res = super().__getitem__(key, *args, **kwargs)
		# if key == '__dir__':
		# 	# return res without keys ['ignore','_pointer','_dict']
		# 	return {k:v for k,v in res.items() if k not in ['ignore','_pointer','_dict']}
		print("Getting", key)
		return res
	def __setitem__(self, key, value, *args, **kwargs):
		if "_id" in kwargs:
			print("XIDX - Setting", key, "to", value, kwargs["_id"])
		print("Setting", key, "to", value)

		res = super().__setitem__(key, value, *args, **kwargs)
		return res


	# @classmethod
	def xdir(self, *a, **kw):
		print("ssssssssssss",type(self),self, a, kw)
		ignore = ["append","clean","clear","clone","copy","deepcopy","deepupdate","dict","dump","filter","find","flatten","from_base64","from_cli","from_csv","from_html","from_ini","from_json","from_pickle","from_plist","from_query_string","from_toml","from_xls","set","setdefault","standardize","subset","swap","to_base64","to_cli","to_csv","to_html","to_ini","to_json","to_pickle","to_plist","to_query_string","to_toml","to_xls","to_xml","to_yaml","traverse","unflatten","unique","update","values","xxx","get_str_list","get_uuid","get_uuid_list","groupby","ignore_key","invert","items","items_sorted_by_keys","items_sorted_by_values","json","keyattr_dynami","keyattr_enable","keypath_separato","keypaths","keys","match","merge","move","nest","pop","popitem","remove","rename","search","from_xml","from_yaml","fromkeys","get","get_bool","get_bool_list","get_date","get_date_list","get_datetime","get_datetime_list","get_decimal","get_decimal_list","get_dict","get_email","get_float","get_float_list","get_int","get_int_list","get_list","get_list_item","get_phonenumber","get_slug","get_slug_list","get_str",]
		return list(set(dir(self)) - set(ignore))
		print("XXX", self.keys())
		return list(self.keys())

	# def __dir__(self):
	# 	print("XXX", self.keys())
	# 	return list(self.keys())
		ignore = ["append","clean","clear","clone","copy","deepcopy","deepupdate","dict","dump","filter","find","flatten","from_base64","from_cli","from_csv","from_html","from_ini","from_json","from_pickle","from_plist","from_query_string","from_toml","from_xls","set","setdefault","standardize","subset","swap","to_base64","to_cli","to_csv","to_html","to_ini","to_json","to_pickle","to_plist","to_query_string","to_toml","to_xls","to_xml","to_yaml","traverse","unflatten","unique","update","values","xxx","get_str_list","get_uuid","get_uuid_list","groupby","ignore_key","invert","items","items_sorted_by_keys","items_sorted_by_values","json","keyattr_dynami","keyattr_enable","keypath_separato","keypaths","keys","match","merge","move","nest","pop","popitem","remove","rename","search","from_xml","from_yaml","fromkeys","get","get_bool","get_bool_list","get_date","get_date_list","get_datetime","get_datetime_list","get_decimal","get_decimal_list","get_dict","get_email","get_float","get_float_list","get_int","get_int_list","get_list","get_list_item","get_phonenumber","get_slug","get_slug_list","get_str",]
		print(list(super().__dir__()))
		print("DDDDDDDD",type(super().__dir__()),super().__dir__()[2])
		print("XXXXXXXX",[x for x in super().__dir__() if x in self.keys()])
		return [x for x in super().__dir__() if x in self.keys()]
		return list(set(super().__dir__()) - set(ignore))
	



defaultRedisConfig = {
	# "host" : "0.0.0.0",
	"host" : "localhost",
	# "port" : 6379,
	"port" : 6379,
}
def getArgs():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--host", help="Redis host",
						default=defaultRedisConfig["host"])
	parser.add_argument("--port", help="Redis port",
						default=defaultRedisConfig["port"])
	args = parser.parse_args()
	return args

host = getArgs().host
port = getArgs().port

def getArgsFromEnv(defaultHost = host, defaultPort = port):
	import os
	host = os.getenv("REDIS_HOST", defaultHost)
	port = os.getenv("REDIS_PORT", defaultPort)
	return host, port	
host, port = getArgsFromEnv(host, port)
from redis import Redis as RedisClient

class xoRedis(xoEvents):
	_host = host
	_port = port
	_db = 0
	_rootName = "root"
	_namespace = "namespace"
	# _parent = None
	_redis = None
	_pubsub = None
	_binded = None
	_live = None
	def __init__(self, *args, **kwargs):
		self._host = kwargs["host"] if "host" in kwargs else host
		self._port = kwargs["port"] if "port" in kwargs else port
		
		self._rootName = "xoRedis"
		self._namespace = self._rootName
		# if self._isRoot: # should work the same
		
		super().__init__(*args, **kwargs)
		# if self._getRoot()._redis:
		# 	pass
		# 	print("!!!!!!!!!!!!!")
		# time.sleep(1)
		if self._isRoot:
			print("RRRRRRRRRRRRRRRRRRRRRRRRooooooooooot")
			if "host" not in kwargs:
				kwargs["host"] = self._host
			if "port" not in kwargs:
				kwargs["port"] = self._port
			if "db" not in kwargs:
				kwargs["db"] = self._db
			# self._redis = RedisClient(host=self._host, port=self._port, db=self._db)
			# self._redis = RedisClient(**kwargs)
			try:
				print("CONNECTING")
				self._redis = RedisClient(**kwargs)
				success = self._redis.ping()
				if not success:
					print(f"Failed to connect to Redis at {self._host}:{self._port}")
			except Exception as e:
				# print(f"Failed to connect to Redis at {self._host}:{self._port} with error: {e.}")
				print(f"Failed to connect to Redis at {self._host}:{self._port} with error")
			
		
		self._binded = False
		self._live = False
			# self._pubsub = self._getRoot()._redis.pubsub()


	
	def _checkIfExist_(self, *args,**kwargs):
		# print(" WILL CHECK IF EXISTS ", self._id, args, kwargs, " ON REDIS")
		# Check if key exits on redis
		try:
			# print("ccccccccccccccccccheckifexist...............")
			res = self._getRoot()._redis.exists(self._id)
			return res
		except Exception as e:
			# print(f"Failed to connect to Redis at {self._host}:{self._port} with error: {e.}")
			print(f"Redis is not connected")
			return False
		
	def __getitem__(self, key, *args, **kwargs):
		res = super().__getitem__(key, *args, **kwargs)
		# if key == '__dir__':
		# 	# return res without keys ['ignore','_pointer','_dict']
		# 	return {k:v for k,v in res.items() if k not in ['ignore','_pointer','_dict']}
		if "value" == key:
			print("XGetting", key)
			gotRes = False
			try:
				r = self._root._redis
				res = r.get(self._id)
				res = pk.loads(res)
				gotRes = True
			except:
				print(" - - - COULD NOT UNPICKLE", self._id, ":::", res)
			if gotRes and res != None:
				print("SHOULD SET",key, "TO", res)
				self.value = res
			# self._setValue(res, skipUpdate = True)
		print("ffffffffffff")
		return res	
		return res
	def __setitem__(self, key, value, *args, **kwargs):
		if key == "value" and value != self:
			if value is not None:
				print("XSetting", key, "to", value)
				val = pk.dumps(value)
				r = self._root._redis
				res = r.set(self._id, val)
				r.publish(self._id, val)
		# if isinstance(value, type(self)):
		# 	value._id = str(self._id)+str(key)

		res = super().__setitem__(key, value, *args, **kwargs)
		return res



import time
def testing():
	# bi = xoBenedict()
	if False:		
		bi = xoEvents()
		t = time.time()
		bi.a.b.c = "yooooooooooooooo'\""
		bi.a.b.c.d = 444444444
		# bi.awesome.nice.abc.a.b.c.d.e.f.g
		# print(bi)
		bi.awesome.nice = "cool"
		# t = time.time()
		bi.awesome.nice.set("COOL!!!").abc("ABC@@@@@@@@").a.b.c({"d":{"e":{"f":"FFFFFFFF"}}}).d.e.f.g("FANASTIC!!!!")
		
		# print(bi)
		print(":::",time.time()-t)
		t = time.time()
		bi.awesome.nice.set("COOL!!!").abc("ABC@@@@@@@@").a.b.c({"d":{"e":{"f":"FFFFFFFF"}}}).d.e.f.g("FANASTIC!!!!")
		print(":::",time.time()-t)
		t = time.time()
		bi.awesome.nice.set("COOL!!!").abc("ABC@@@@@@@@").a.b.c({"d":{"e":{"f":"FFFFFFFF"}}}).d.e.f.g("FANASTIC!!!!")
		print(":::",time.time()-t)
		# print(bi)
		t = time.time()
		print(xoBenedict.from_json(bi.json()))
		print(type(dict(bi)))
		print(":::",time.time()-t)


xo = xoBenedict()
print("......................")
xo.a.b.c = 3
# xo.a.b = 2
	# print(bx)
	# bi2 = xoBenedict(bi.json().replace("\"a\"","\"AAA\""), bi({"aa":1111111,"a":{"b":{"c":"cccccccc"}}}), **{**bi,**{"a":{"b":{"c":{"d":"DDDDDDDDDDDDDDDDDDDDDDDDDDD"}}}}})
	# print(bi2)
	
	# bi.a.b.c.set(3).d.set(4).e(5).f.set(6).g("777").set("h",888).set(7777, HH = "1000000000000000").HH.awesome.set(11111)

if __name__ == '__main__':
	testing()


	