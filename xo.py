import ast
from benedict.dicts.io import IODict
from benedict.dicts.keyattr import KeyattrDict
# from benedict.dicts.keylist import KeylistDict
from benedict.dicts.keypath import KeypathDict
from benedict.dicts.parse import ParseDict
from benedict import benedict#, KeyattrDict, KeypathDict, IODict, ParseDict
b = benedict()


counter =0

class xoBenedict(benedict):#KeyattrDict, KeypathDict, IODict, ParseDict):
	# _benedict = benedict()
	ignore_keys = ['_override','keyattr_dynamic', 'keyattr_enabled','keypath_separator','check_keys']
	def __init__(self, *args, **kwargs):
		"""
		Constructs a new instance.
		"""
		global counter
		my_c = counter
		counter += 1
		# print("iiiiiiiiiiiiiiiiiiiiiiiiiiiii",":::",my_c,":::",len(args))
		kwargs["keyattr_dynamic"] = True
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

			super().__init__(obj.dict(), **kwargs)
			# self.update(kwargs)
			# print("OOOOOOOOO o o ")
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
					print("JJJJJJJJSSSSSSSSSSSSSSSSSS")
					print("JJJJJJJJSSSSSSSSSSSSSSSSSS",type(args[0]),args[0])
					# args[0] = self.from_json(args[0])
					args = [ast.literal_eval(args[0].strip("'<>() ")) ]
					# args = [json.loads(repr(args[0]).strip("'<>() ").replace("\\\'","\\\\'"))]#..replace('\'', '\"'))]
					print("JJJJJJJJSSSSSSSSSSSSSSSSSS",type(args[0]),args[0])
					print("JJJJJJJJSSSSSSSSSSSSSSSSSS")
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

		super().__init__(*args[::], **kwargs)
		#{"AAA": {"b": {"c": "yooooooooooooooo'\""}}, "a": {"b": {"c": {"d": "DDDDDDDDDDDDDDDDDDDDDDDDDDD"}}}, "aa": 1111111}
		# extras = []
		extra_keys = {k:v for k,v in kwargs.items() if k not in self.ignore_keys}
		
		
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
		res = self._cast(super().__getitem__(key))
		if key not in self.__dict__:
			# print("WORKING !!!!!!!!!!!!")
			self.__dict__[key] = res
		return res

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

	def __setitem__(self, key, value, skip = False):
		obj_type = type(self)
		# obj_type()
		# print("set KKKKKKKK",key)
		if key != "value" and not isinstance(value, dict) and not isinstance(value, obj_type) and not skip:
			# print("111111111111", value)
			
			value = obj_type({"value":value}, keyattr_dynamic=True)
			# print("set 22222222222", value)
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
				# self.__dict__[key] = value
				res = self.__setitem__(key, value, skip = True)
				self.__dict__[key] = self[key]
				
				return res
		# print("set 3333333", value)
		f = self._cast(value)
		res = super().__setitem__(key, f)
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
		return res

	def _cast(self, value):
		"""
		Cast a dict instance to a benedict instance
		keeping the pointer to the original dict.
		"""
		obj_type = type(self)
		if isinstance(value, dict) and not isinstance(value, obj_type):
			return obj_type(
				value,
				keyattr_enabled=self._keyattr_enabled,
				keyattr_dynamic=self._keyattr_dynamic,
				keypath_separator=self._keypath_separator,
				check_keys=False,
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
		return "{"+", ".join((f"\"{key}\": {val}") for key, val in self.items())+"}"

import time
def testing():
	bi = xoBenedict()
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
	bx = xoBenedict()
	bx.a.b = 3
	# print(bx)
	# bi2 = xoBenedict(bi.json().replace("\"a\"","\"AAA\""), bi({"aa":1111111,"a":{"b":{"c":"cccccccc"}}}), **{**bi,**{"a":{"b":{"c":{"d":"DDDDDDDDDDDDDDDDDDDDDDDDDDD"}}}}})
	# print(bi2)
	
	# bi.a.b.c.set(3).d.set(4).e(5).f.set(6).g("777").set("h",888).set(7777, HH = "1000000000000000").HH.awesome.set(11111)
	print(bi)

if __name__ == '__main__':
	testing()


	