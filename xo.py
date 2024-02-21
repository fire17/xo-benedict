import ast
from pickle import NONE
from benedict.dicts.io import IODict
from benedict.dicts.keyattr import KeyattrDict
from benedict.dicts.base import BaseDict
# from benedict.dicts.keylist import KeylistDict
from benedict.dicts.keypath import KeypathDict
from benedict.dicts.parse import ParseDict
from benedict import benedict#, KeyattrDict, KeypathDict, IODict, ParseDict
# b = benedict()
import dill as pk
from pyfiglet import figlet_format as figlet
from colorama import Fore as color


debug = True
debug = False
funMode = True # send keys to others, even if they dont have them yet

counter =0

keypath_separator = "."




class xoBenedict(benedict):#KeyattrDict, KeypathDict, IODict, ParseDict):
	# _benedict = benedict()
	_root = None
	_isRoot = False
	_id:str = "yyy"
	_type:type = benedict

	_subscribers = []

	ignore_keys = ['_override','keyattr_dynamic', 'keyattr_enabled','keypath_separator','check_keys']
	_params = {}

	def __init__(self,*args, **kwargs):
		"""
		Constructs a new instance.
		"""
		self._type = type(self)
		if xoBenedict._root is None:
			xoBenedict._root = self

			self._isRoot = True
		else:
			self._root = xoBenedict._root

		# self.__dict__ = DictWrapper(self.__dict__, castFunc = self.__dict_wrap__)
		self._subscribers = []
		self._isRoot = True
		
		
		nid = None
		if "_id" in kwargs:
			nid = kwargs.pop("_id")
		# print("_IDIDIDID", nid, "param")
		# print("_IDIDIDID", nid, "param",_id)
		namespace = self._type.__name__
		if nid:
			self._id = nid
			self._isRoot = False
		else:
			# self._id = str(_id)
			# self._id = self._type.__name__
			self._id = namespace

		if self._isRoot and len(args) >= 1 and isinstance(args[0],str):
			namespace = args[0]
			newArgs = list(args);newArgs.remove(args[0])
			args = newArgs
		# else:
		# print("iiiiiiiiiiiiiiii",self._id,args,kwargs)
		# 	pass
		# 	print("XXXXX",self._isRoot, args )
		# print("iiiiiiiiiiiiiiii",self._id, ":::",args,":::",kwargs)
		new = "Root" if self._isRoot else "new" 
		
		if debug:
			print(f"::: Creating {new} {namespace} with ID:",self._id, ":::",args,":::",kwargs)
		# if len(args)==1:
		# 	print("TTTTTTTTTT",type(args[0]))
		# print(":::",self._id)
		
		if "skip_fetch" in kwargs:
			self._params["skip_fetch"] = kwargs.pop("skip_fetch")

		global counter
		my_c = counter
		counter += 1
		# print("iiiiiiiiiiiiiiiiiiiiiiiiiiiii",":::",my_c,":::",len(args))
		kwargs["keyattr_dynamic"] = True
		kwargs["keypath_separator"] = keypath_separator
		
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
					print("JJJJJJJJSSSSSSSSSSSSSSSSSS",type(args[0]),args[0])
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
		# print("ccccccccccccccCCCCCCCALLLLLLLLLLLLLLLLLL",args, kwargs)
		if "value" in self and "function" in str(type(self["value"])):
			# return self["value"](*args, **kwargs)
			f = self.value
			if debug: print("::: Calling inner function", f)
			# print(":::::::::::::::",self._id,type(f),f, args, kwargs)
			funcRes = f.__call__(*args, **kwargs)
			return funcRes
		else:
			# entries = type(self)(kwargs,_override=True, keyattr_dynamic=True)

			# self.update(entries)
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

	def __contains__(self, q, *args, **kwargs):
		# print("QQQQQQQQQQQQ",q)
		return super().__contains__(q,*args, **kwargs)
	
	def __getitem__(self, key, *args, **kwargs) -> benedict:
		try:
			return super().__getattribute__(key, *args, **kwargs)
			# return res
		except:
			pass
			res = super().__getitem__(key, *args, **kwargs)
			return res
			# res = super().__getitem__(key, *args, **kwargs)
		
		# if key not in self.__dict__:
		# getKeys = True
		# print("GGGGGGGGGG",self._id,key)
		if key == "keys":
			pass
			# print("XXXXXXXXXXXX")
		if key in self.keys():
			# print("YES")
			try:
				target = KeypathDict.__getitem__(self,key)
			except:
				target = super().__getitem__(key)

			# print("TARGET",type(target))
			if isinstance(target, type(self)):
				print("YES FASTTTTTTTTTTTT",)
				return target
			if False and isinstance(target,dict):
				print("FAST DICT")
				return target
			if isinstance(target, dict):
				print("YES SLOWWWWWWWWWWWWW",type(target), "_type" in target, target)
				return self._cast(target, key = key)
			return target
		# if key in self._dict:
		# 	print("YES2")
		# if key not in self.__dict__:
		if key not in self.keys() and key not in self.__dict__:
			# res = self._cast(super().__getitem__(key), key = self._id+"."+str(key))
			# res = self._cast(super().__getitem__(key), key = key)
			# print("again")
			try:
				# time.sleep(0.1)
				# target = KeypathDict.__getitem__(self,key)
				target = KeypathDict.__getitem__(self,key)
				# target = super().__getitem__(key)
				print("YOOOOOOOOOOOOOxxxxxx")
			except:
				print("YOOOOOOOOOOOOO",self._id,key)
				
				target = super().__getitem__(key)
				# try:
				# # target = super().__getitem__(key)
				# except:
				# 	# target = KeypathDict.__getitem__(self,key)
				# 	target = self.__getitem__(key)
			print("TARGET",type(target))
			res = self._cast(target, key = key)
			# print("againx2")
			# print("WORKING !!!!!!!!!!!!")
			self.__dict__[key] = res
			return res
		# if key in self.__dict__ and isinstance(self[key],type(self)):
		# 	print("skip!")
		# 	return dict(self).__getitem__(key)
		# print("again 3")
		# print("again 3")
		# print("again 3")
		target = KeypathDict.__getitem__(self,key)
		# if not isinstance(target, type(self)):
		if not isinstance(target, xoBenedict):
			print("CASTING TARGET",type(target))
			# return target
			f = self._cast(target, key = key)
			# KeypathDict.__setitem__(self, key, f)
			return f
		else:
			print("SKKKKKKKKKKKKK")
			print("SKKKKKKKKKKKKK")
			print("GOOD FIN SAME TYPE")#\nSKKKKKKKKKKKKK")
			print("SKKKKKKKKKKKKK")
			print("SKKKKKKKKKKKKK")
			return target
		return super().__getitem__(key)


	# def __dict_wrap__(self, *args, **kwargs):
	# 	print("!!!!!!!!!!")
	# 	legacy = False
	# 	if legacy:
	# 		return dict(super())
	# 	return self.flatten(*args, **kwargs)

	def flatten(self, sep=None,rep="/", fast=False, *a, **kw):
		if fast: return super().flatten(sep if sep else "/") if sep else super().flatten()
		def fix(key):
			key = key.replace(rep, sep if sep else keypath_separator)
			if len(key)>6 and key[-6:] == keypath_separator + "value":
				key = key[:-6]
			return key
		return {fix(k):v for k,v in super().flatten(rep).items()}
	
	def items(self, fast = False):
		# for key, value in BaseDict.items(self):
		for key, value in BaseDict.items(self):
			
			# print("i",key,type(value))
			if fast or True:
				# print("FAST")
				yield (key, value)
			else:
				print("SLOW", type(value),value,key)
				yield (key, self._cast(value, key = key))

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

	def __setitemx__(self, key, value, skip = False, **kw):
		# res = super().__setitem__(key, value)
		# print("SSSSSSSSS",key,value,skip,kw)
		if key != 'value' and value != {} and "__onchange__" in self.__dir__() and "skip_change" not in kw:
			#THIS IS NOT THE FUNCTION YOUR LOOKING FOR
			res = self.__onchange__(self._id+"."+str(key), value,*a,**kw)
			if res != None:
				value = res
			
			

		if key == "value":
			res = super().__setitem__(key, value)
		else:
			# if key inside self, set value
			# if key not in self, cast new value
			if key in self:
				child =  self.__getattr__(key)
				res = child.__setattr__("value",value)
			else:
				# res = super().__setitem__(key, self._cast(value, key = self._id+"."+str(key)))
				# res = super().__setitem__(key, self._cast(value, key = self._id+"."+str(key)))
				# res = super().__setitem__(key, self._cast(value, key = key))
				# child = self
				# child.value = value
				# res = None
				child = type(self)(_id = self._id+"."+str(key))
				print('xxx')
				child.value = value
				res = super().__setitem__(key,child)
		
		# print("SETTING",self._id,key)
		return res

	def __hash__(self):
		return hash(super())
		return hash(self._id)
	
	def __setitem__(self, key, value, skip = False,*a, **kw):
		if isinstance(value, ignore):
			# print("IIIIIIIIIIIIIIIIIIIIIII")
			# print("IIIIIIIIIIIIIIIIIIIIIII")
			# print("IIIIIIIIIIIIIIIIIIIIIII")
			return
		# print("IIIIIIIIIIIIIIIIIIIIIII",key, value, skip,a,kw)
		# print("IIIIIIIIIIIIIIIIIIIIIII",key in self)
		newKey = key not in self and key == value
		# print("ssssssss",key,value)
		if False and key != 'value' and value != {} and "__onchange__" in self.__dir__() and "skip_change" not in kw:
			print("SSSSSSSSSs")
			# res = self.__onchange__(self._id+"."+str(key), value, oorigin = "IIIIIII",*a,**kw)
			# res = self.__onchange__(self._id+"."+str(key), value, oorigin = "IIIIIII",*a,**kw)
			pass
			# self._updateSubscribersDeep_(res) this will update all children!
			# self._updateSubscribers_(res)

			# print("SSSSSSSSSsxxxxxxxx")
			# self._updateSubscribers_(res)
			
			# if res != None:
			# 	value = res
			pass
		if True:
			if key == "value":
				if (key == 'value' and value != {}):
					self._updateSubscribers_(value)

				if "__onchange__" in self.__dir__() and "skip_change" not in kw:
					res = self.__onchange__(self._id, value, origin2 = "setitem:value",*a,**kw)
					if res != None:
						if not isinstance(value, bool):
							# if results are bool continue as normally,
							# but if results are not bool, and onchange returned False
							# Then do not continue with setting the value
							if res == False: return self
						value = res

		# elif key == 'value' and value != {} and "__onchange__" not in self.__dir__() and "skip_change" not in kw:
		elif (newKey or key == 'value') and value != {}:
			# if newKey and key=="value" or key!=value and "origin" in kw: kw["skip_publish"] = True
			if newKey and key=="value" or key!=value and "origin" in kw: kw["skip_publish"] = True
			if (key == 'value' and value != {}):
				self._updateSubscribers_(value)
				
			if "origin" in kw: kw["skip_publish"] = True
			if "origin" in kw and "get_attr" in kw['origin']: kw["skip_change"] = True
			# print("!!!!!!!!",kw)
			if "__onchange__" in self.__dir__() and "skip_change" not in kw:
				res = self.__onchange__(self._id+"."+str(key), value, origin2 = "setitem:value",*a,**kw)
				if res != None:
					value = res

			# self._updateSubscribers_(value)
			pass
			# print("!!!!!!!!@@@")
		'''
		# if  "__onchange__" in self.__dir__():
		# if key == "value" and not skip:
		# if key == "value" or key.split(".")[-1] == "value":
		# 	# return super().__setitem__(key, self._cast(value))
		# 	return super().__setitem__(key, value)
		# else:
		# 	# return super().__setitem__(key+".value", self._cast(value))
		# 	return super().__setattr__(key+".value", value)
		'''
		# print("......................")
		obj_type = type(self)
		# obj_type()
		# print("set KKKKKKKK",key)
		if key != "value" and not isinstance(value, dict) and not isinstance(value, obj_type):# and not skip:
			# print("111111111111", self._id,key, value)
			
			# value = obj_type({"value":value}, keyattr_dynamic=True, _parent = self)
			# print("NEXT:",self._id+"."+str(key))
			# value = xoBenedict({"value":value}, _id = self._id+"."+str(key), keyattr_dynamic=True)
			# if key in self:
			# if key in self.keys():
			if key in super().keys():
				# print()
				# print(key in self,"$$$$$$$$$$$")
				# print("!!!!!!",super().__getattribute__(key)._type)
				# print("$$$$$$$$$$$$$$$$")
				# print()
				# if isinstance(self[key],type(self)):
				# if isinstance(self[key],type(self)):
				# print("$$$$$$$$$$$$$$$$")
				# child:xoBenedict =  self.__getattr__(key)
				# child:xoBenedict =  self.__getaFttr__(key)
				child =  self.__getitem__(key)
				# print("$$$$$$$$$$$$$$$$")
				if child._type == type(self):
				# if super().__getattribute__(key)._type == type(self):
					# print(isinstance(self[key],type(self)),"$$$$$$$$$$$")
					# print("%%%%%%%%%%%%%%%%%%%%")
					# if value != None and not skip:
					if not skip: # None Support
						# pass
						# print("HERERERERERE111111")
						# self[key].value = value
						
						# print("#########1111111111",key,value, kw)
						# child.__setattr__("value",value)
						child.__setitem__("value",value, **kw)
						#child.value = value
						# value = self[key]
						pass
						return value
					if skip:
						# print("#########121212",key)
						if super().__getattribute__(key)._type == type(self):
							print("BINGO!!!!!!!!!!!!!!!!!!!!!!!!")
							super().__getattribute__(key).value = value
							# super().__getattribute__(key).__setitem__("value",value, noPub=True)
							# super().__getattribute__(key).__setitem__("value",value, noPub=True)
						return super().__getattribute__(key)
				else:
					print("XXXXXXXXXXXX",type(self[key]))
					pass
					# value = type(self)({"value":value}, _id = self._id+"."+str(key), keyattr_dynamic=True)
					pass
					newobj = type(self)(_id = self._id+"."+str(key), keyattr_dynamic=True , keypath_separator = keypath_separator)
					# newobj.value = value
					# newobj.__setitem__("value",value,origin='setitem:new_value')
					newobj.__setitem__("value",value,**kw)
					value = newobj
			else:
				# print("KKKK",key,type(key), value)
				# value = type(self)({"value":value}, _id = self._id+"."+str(key), keyattr_dynamic=True)
				pass
				# value = type(self)({"value":value}, _id = str(self._id)+"."+key, keyattr_dynamic=True)
				pass
				newobj = type(self)(_id = self._id+"."+str(key), keyattr_dynamic=True, skip_fetch=True, keypath_separator = keypath_separator)
				# newobj.value = value
				# newobj.value = value
				newobj.__setitem__("value",value,origin='setitem:new_value2', *a, **kw)
				value = newobj
				
				# print("xxx finish quicker here")
			# print("set 22222222222", value)
			# value.__setitem__(,value, skip = True)
			if False and debug: print("value", value)
			if False and debug: print("key", key)
			if key in self and key != "value":
				if value is None:  #Added None support
					# if not hasattr(self,"value"):
					self[key].value = None
					# else:

				elif not isinstance(self[key],dict):
					print("#########22222",key)
					self[key] = value
					# self.__dict__[key] = value
					self.__dict__[key] = self[key]
				else:
					# print("##################",type(value))
					# print("#########22222.5",key)
					self[key].update(value)
					# for k in value:
					# 	print("##################",type(value[k]))
						# self[key].__dict__.update(value)
						# self[key].__dict__[k]=value[k]
						# self[key].__dict__[k]=self[key][k]
						# self.__dict__[key].__dict__[k]=self[key][k]
						# pass
					# self[key].__dict__.update(value)
					# self[key].__dict__.update(value)
				return self[key]
			else:
				# print("key",key,"type",type(value),"value",value)
				pass
				# self.__dict__[key] = value
				# self[key] = value
				# res = super().__setitem__(key, value)
				# print("222222222222222@@@@@@@@@@@@@@@@@22")
				# res = self.__setitem__(key, value, skip = True)
				# res = self.__setitem__(key, value, skip = True)
				# self.__dict__[key] = self[key]
				# return res
				# return self[key]
		if True:
			# print("set 3333333", value, key, )
			# print(key in self,"!!!!!!!!!!!!", type(value))
			if isinstance(value, dict) and not isinstance(value, type(self)):
				# value = self._cast(value, key = self._id+"."+str(key))
				# print("DOUBLE??????????")
				value = self._cast(value, key = key)
			# self.__dict__[key]=f
			# return f
			# res = super().__setitem__(key, f)
			# if key in self.__dict__ and isinstance(self[key],type(self)):
			# 	print("skip!")
			# 	return super().__getitem__(key)
			# print("#########3")
			res = super().__setitem__(key, value, )# origin="xoBenedict_setitem")
			self.__dict__[key]=value
			# print(key in self,"!!!!!!!!!!!!")#, type(self.__dict__[key]))
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

		if type(self) == type(value) or key == None:
			return value
		
		if debug: print(f"{self._id=}.{key} CASTING :",type(value))
		# print("Cast", self)
		obj_type = type(self)
		# print("oooooooo",obj_type,key, type(value),value)
		if isinstance(value, dict) and not isinstance(value, obj_type):
			data = {"keyattr_enabled":self._keyattr_enabled,
				"keyattr_dynamic":self._keyattr_dynamic,
				"keypath_separator":self._keypath_separator,
				"check_keys":False,}
			# if key:
			# 	data["_id"] = key
			
			# return obj_type(
			target = self._id if key is None or key == '' else self._id+"."+str(key)
			print("TTTTTTTT:",target)
			# return xoBenedict(
			return obj_type(
				# value,_id = self._id+"."+str(key),
				value=value, _id = target,
				# value, _id = target,
				**data
				# _parent = self,
			)
		elif isinstance(value, list):
			for index, item in enumerate(value):
				f = self._cast(item, )
				f._id = (self._id if key is None or key == '' else self._id+"."+str(key))+"."+str(index)
				value[index] = f
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
	# def __imatmul__(self, other):
	# 	''' Special Subscribe function '''
	# 	print("SUBSCRIBING TO ",self)
	# 	if "value" in self:
	# 		self["value"] @= other
	# 	else:
	# 		super().__imatmul__(other)
	# 	return self


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
		return self.__setitem__("value",other, skip_change=True)
		if "value" in self:
			self["value"] //= other
		else:
			super().__ifloordiv__(other)
		return self
	def unpickle(self):
		if "value" in self:
			return pk.loads(self.value)
	def pickle(self):
		return pk.dumps(self.value) if "value" in self else pk.dumps(self)
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
	def __len__(self):
		# print("S S S",len(self.keys()), self.keys())
		if "value" in self and len(self.keys()) == 1:
			if "__len__" in self.value.__dir__(): return len(self.value)
		return super().__len__()
		
	def __str__(self):
		# print("S S S",len(self.keys()), self.keys())
		if "value" in self and len(self.keys()) == 1:
			return f'{self.value!r}'
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
		# fastItems = {k:v for k,v in self.items(fast = True)}
		# def changeReq(d):
		# 	if type(d) == dict:
		# 		for k,v in d.items():
		# 			if type(v) == dict:
		# 				if len(v.keys()) == 1 and "value" in d:
		# 					return d["value"]
		# 				return {kk:changeReq(vv) for kk,vv in v}
		# 			return {k:v}
			# return {k:changeReq(v) for k,v in d.items()}
			# if type(d) == dict:
			# 	for k in d:
			# 		if len(d[k].keys()) == 1 and "value" in d:
			# 			return d[k]["value"]
			# 		yield {k:changeReq(v) for k,v in d.items()}
			# return d
		# fastItems = {k:v for k,v in changeReq(fastItems)}
		# print("FFFF",fastItems)
		# if len(fastItems.keys()) == 1:
		# 	if and "value" in fastItems:
		# 	return str(fastItems["value"])
		# return "{"+", ".join((f"\"{key}\": {val}") for key, val in fastItems if len(key)>0 and key[0]!="_")+"}"
		# return "{"+", ".join((f"\"{key}\": {val}") for key, val in self.items(fast = True) if len(key)>0 and key[0]!="_")+"}"
		result = {}  # Start with an empty dictionary to store the key-value pairs
		# Iterate over each key-value pair in self.items()
		for key, val in self.items(fast=True):
			# Check if the key is not empty and doesn't start with "_"
			if len(str(key)) > 0 and str(key)[0] != "_":
				# Add the key-value pair to the result dictionary
				if isinstance(val,dict) and "value" in val and len(val.keys())==1:
					# print("@@@@@@@@@@@@@@@@",val["value"])
					result[key] = f'{val["value"]!r}'
				else:
					# print(":::",val)
					# result[key] = val
					result[key] = f'{val!r}'

		if "value" in result:
			val = result.pop("value")
			result = {"value":val,**result}

		# Convert the dictionary to a JSON-like string
		output = "{" + ", ".join(f"\"{key}\": {val}" for key, val in result.items()) + "}"

		# Return the JSON-like string
		return output
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
	
		
	def show(self, t="    ", count=0, inLoop=False, ret=False):
		# print("ssssssssssssssss..............",self._id)
		s = ""
		#### print("///////////",self[Expando._valueArg],type(self[Expando._valueArg]))
		p = ""
		val = ""
		if "value" in self:
				# print("1111111")
				if "str" in str(type(self["value"])):
						# print("11111112")
						s = "\'"
				val = str(self["value"])
		# else:
				# print("00000000000000")
				# print("00000000000000",self._id)
				# print("00000000000000")
		finalval = " = " + s+str(val)+s if val is not None or True else ""
		p = self._id.split("/")[-1] + finalval
		tab = ""
		for i in range(count):
				tab += t

		retList = []
		res = []
		p = tab+p
		if ret:
				# print("22222221")
				retList.append(p)
		else:
				# print("22222222")
				print(p.replace("\t", "    "))
		for a in self:
				# print("33333", a, type(self[a]))
				# if "_" not in a:
				# print("st2", s)
				if not a.startswith("_"):
						if isinstance(self[a], type(self)) or "dict" in str(type(self[a])):
								# print("33334",a)
								if ret:
										# print("33335555",a)
										res = self[a].show(count=count+1, ret=ret)
								else:
										# print("3333466666",a)
										self[a].show(count=count+1, ret=ret)
						# else:
								# print("33337",a)
		if count == 0 and inLoop:
				print("\n\nPress Ctrl+C to stop whileShow()\n")

		if ret:
				# print("444444444")
				if count == 0:
						# print("4444444445")
						return str(retList + res)
				# print("55555555",count)
				return retList + ["\n"] + res
		# print("777777",ret,count,retList,res,)
		# return dict(self)

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
		print("jjjjjjjjjjjjjj",self)
		print("dddddddddddddd",D)
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

	def __getattr__(self, attr):
		# print("UUUUUUUUUUUUUUUUUUUUUUUUU")
		if attr == "value" and ("value" not in self or self["value"] == {}):
			return None
		attr_message = f"{self.__class__.__name__!r} object has no attribute {attr!r}"
		if not self._keyattr_enabled:
			raise AttributeError(attr_message)
		try:
			if attr not in self and "value" in self and isinstance(self.value,object) and attr in self.value.__dir__():
				return self.value.__getattribute__(attr)
			return self.__getitem__(attr)
		except KeyError:
			if attr.startswith("_"):
				raise AttributeError(attr_message) from None
			if not self._keyattr_dynamic:
				raise AttributeError(attr_message) from None
			# self.__setitem__(attr, {})
			# print("@@@@@@",self._id+"."+attr)
			self.__setitem__(attr, type(self)(_id = self._id+"."+attr), origin="get_attr")
			# self.__setitem__(attr, xoBenedict())
			return self.__getitem__(attr)

	def __imatmul__(self, other):
		# print("@= @@@@@@@@@@@@",other)
		if "tuple" in str(type(other)):
			print("X")
			res = None
			for func in other:
				# res = self.subscribe(func)
				res = self.subscribe(func)
				# self._subscribers.append(func)
			# return res
		else:
			# print("YYY",self._id)
			# self._subscribers.append(other)
			self.subscribe(other)
		# print(f"@@= @@@@@@@@@@@@{self._id}",other)
		return ignore()

	def subscribe(self, funcOrXo=None):
		# print(" ::: Subscribing to", self._name)
		print("::: Subscribing to", self._id)
		# print("SSSSSSSSSSSSSSS",self, funcOrXo)
		if funcOrXo is None:
			# print("XxxxxxX")
			funcOrXo = lambda a, *aa, **aaa: [a, aa, aaa]
			# withID = True
		# else:
		# print("ffffffffff", funcOrXo)
		if funcOrXo not in self._subscribers and funcOrXo not in self._subscribers:
			self._subscribers.append(funcOrXo)

	def _updateSubscribers_(self,value, *v, **kw):
		# for trigger in self._triggers:
		# 	#TODO: in new thread
		# 	trigger()
		# xo.a.<s>.a = 3
		# print("UUU",self._id,self._subscribers)
		for sub in self._subscribers:
			#TODO: in new thread
			# print(sub)
			# print("&&&",self[Expando._valueArg], sub)
			# print("***************",self._id, value, v, kw)
			# print(sub(*v, **kw))
			kw["_xo"] = self
			kw["_id"] = self._id
			# if "value" in self:
			# sub(value,*v, **kw)
			try:
				sub(value,*v, **kw)	
			except:
				traceback.print_exc()


class ignore():
	pass

class xoEvents(xoBenedict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		ignore = ["append","clean","clear","clone","copy","deepcopy","deepupdate","dict","dump","filter","find","flatten","from_base64","from_cli","from_csv","from_html","from_ini","from_json","from_pickle","from_plist","from_query_string","from_toml","from_xls","set","setdefault","standardize","subset","swap","to_base64","to_cli","to_csv","to_html","to_ini","to_json","to_pickle","to_plist","to_query_string","to_toml","to_xls","to_xml","to_yaml","traverse","unflatten","unique","update","values","xxx","get_str_list","get_uuid","get_uuid_list","groupby","ignore_key","invert","items","items_sorted_by_keys","items_sorted_by_values","json","keyattr_dynami","keyattr_enable","keypath_separato","keypaths","keys","match","merge","move","nest","pop","popitem","remove","rename","search","from_xml","from_yaml","fromkeys","get","get_bool","get_bool_list","get_date","get_date_list","get_datetime","get_datetime_list","get_decimal","get_decimal_list","get_dict","get_email","get_float","get_float_list","get_int","get_int_list","get_list","get_list_item","get_phonenumber","get_slug","get_slug_list","get_str",]
		# self.__class__.__dir__ = lambda self, *a, **kw: list(set(dir(self)) - set(ignore))
		# self.__dir__ = self.keys
		# self.__dir__ = self.keys
		
	def __getitem__(self, key, *args, **kwargs):
		print(f"Getting {self._id=}.+{key}", args, kwargs)
		res = super().__getitem__(key, *args, **kwargs)
		# if key == '__dir__':
		# 	# return res without keys ['ignore','_pointer','_dict']
		# 	return {k:v for k,v in res.items() if k not in ['ignore','_pointer','_dict']}
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
	

import traceback

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

# class xoRedis(xoEvents):
class xoRedis(xoBenedict):
	_host = host
	_port = port
	
	_db = 0
	_rootName = "root"
	_namespace = "namespace"
	# _parent = None
	_redis:RedisClient = None
	_pubsub = None
	_binded = None
	_live = None
	_clients = {}
	_root:xoBenedict

	def new(self,*args, **kwargs):
		#TODO: Clear memory of current instance
		return type(self)(*args,**kwargs)

	def _redisSubscribe(self, key="Redis*", handler=lambda msg: print('XXXXXXXXXXXXHandler', msg), *args, **kwargs):
		# print("UUUUUUUUUUUUUUUUUUUUUUUU", key, handler, args, kwargs)
		# print("UUUUUUUUUUUUUUUUUUUUUUUU")
		# print("UUUUUUUUUUUUUUUUUUUUUUUU")
		# print("UUUUUUUUUUUUUUUUUUUUUUUU")
		# print(" ::: SUBSCRIBING TO REDIS CHANNEL", key, ":::", )
		try:
			self._pubsub.psubscribe(**{key: handler})
		# pubsub.psubscribe(key = key, handler = handler)
		# pubsub.subscribe(subscribe_key)
		# pubsub.subscribe(key)
		# pubsub.subscribe(**{key: event_handler if handler is None else handler})
		# print("........00000")
			# self._pubsub.run_in_thread(sleep_time=.00001, daemon=True)
			self._pubsub.run_in_thread(sleep_time=.00001, daemon=True)
		except Exception as e:
			# print(f"Failed to connect to Redis at {self._host}:{self._port} with error: {e.}")
			print(f"Failed: Redis is not connected")
			return False
		# for item in pubsub.listen():
		#     print(item, type(item))
		#     if item['type'] == 'message':
		#         print(item['data'])
		# print("DONE")
	
	
	# TODO: Also, implement option to lazy load, (set _needsUpdate or something like so)
	def _directBind(self, msg, *args, **kwargs):
		# print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
		# print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
		print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu", msg, args, kwargs)
		# time.sleep(1)
		if isinstance(msg, dict) and "type" in msg:
			if "message" in msg["type"]:
				# do_something with the message
				channel = msg["channel"].decode() # .strip("Redis.")  # .split(".")[-1]
				# if channel.startswith(xoRedis._rootName+"."):
				# if channel.startswith(self._rootName+"/"):
				# print("ggggg", channel)
				if channel.startswith(self._id+"."):
					channel = ".".join(channel.split(".")[1:])  # .split(".")[-1]
				# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", msg, args, kwargs)
				# return message
				# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
				# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", str(msg["channel"]).replace("/", "."))
				# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
				# msg["channel"].decode().replace("/", "."))
				# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", msg["data"])

				# EDIT 1
				# f = xo._GetXO(channel, allow_creation=True)
				if True:
					# print("ggggg", channel)
					# f = self._GetXO(channel, allow_creation=False)
					# time.sleep(1)

					# f = self
					# print("PRE", self._id, "channel:", channel,"SELFID",self._id)
					
					# f = f[channel]
					# if channel.startswith(self._id):
					# 	channel = ".".join(channel.split(".")[1:])
					
					'''
					for c in channel.split("."):
						# print("c:",c)
						# if c not in f:
						# 	f[c] = xo()
						print("ccccccc",c)
						print("ffffffffff",f._id)
						f = f[c]
					'''
					# print("POST",f._id)
					
					# print("ggggg2")

					# f = xo[msg["channel"].decode().strip("xo/").replace("/", ".")]
					# f[channel] = msg["data"]
					# print("######  ", f)
					# sender, res = msg["data"]
					res = msg["data"]
					try:
						sender, res = final = pk.loads(res)
						# sender, res = final = pk.loads(res)
						if sender == hash(self._root._redis):
							# LEGACY
							# print("@@@@@@@@@@@@@@@ WORKING! SKIPPING SELF UPDATE", channel, "")
							return 
						# print("try res:",res)
					except:
						print(" - - - COULD NOT UNPICKLE", self._id, ":::", res)
					'''
					print("@@@@@@@@@@@ UPDATING ",channel,self._id)
					if len(channel.split(".")) > 1:
						target = self[".".join(channel.split(".")[1:])]
						key = channel.split(".")[-1]

					else:
						target = self
						key = channel
					print("@@@@@@@@@@@ UPDATING ",target._id,key)
					print("$$$$$$$$",self._id, self._isRoot)


					# target = 
					# print("@@@@@@@@@@@2 UPDATING ", target._id, target._type)
					if key == "value" or key not in target or target[key].value != res:
						print("\n:::UUUUUUUUUUUUUUUUUUU Updating ",target._id+"."+key)
						pass
					'''
					print('ZZZZZZZZ',channel, self._id)
					if channel not in self:
						# self[channel] = res
						# self[channel] = res
						if isinstance(res,dict):
							print("F I X I X I X I X")
							res = self._cast(res)
						getKeysYouDontHaveAlready = False
						if getKeysYouDontHaveAlready or funMode:
							if debug or funMode: print("::: Updating (xxx new)", channel, "=", str(res)[:40] + '...' if len(str(res)) > 40 else str(res))
							self.__setitem__(channel, res , skip_publish = True)
							pass
						# else:
						# 	print()
						return
					
					if channel in self:
						if channel not in self:
							print("Creating!!!!!!!!!!!! ",channel)
							done = False
							while not done:
								try:
									print(self[channel])
									done = True
								except:
									traceback.print_exc()
									print("Failed",channel,self._id,self)
									# time.sleep(1)
							print("Creating!!!!!!!!!!!! xxx")
						t = self
						l = len(channel.split("."))
						co = 0
						for c in channel.split("."):
							# print("cccccc",c)
							if l-co == 1: channel = c
							# else:t = t[c]
							else:t = t.__getitem__(c)
							co+=1
						if debug or funMode or True: print("ZZZ::: Updating",t._id+"."+channel,"=",res)
						t.__setitem__(channel, res, skip_publish = True)
					# self.__setitem__(channel, res)
					pass
						# xoRedis.__setitem__(target, key ,res)
					# print("@@@@@@@@@@@3 UPDATING ",channel)

					# f._setValue(res, skipUpdate=True)

				# f[self._valueArg] = res
				# f._updateSubscribers_(res)

				# print("######  ", f.value)
				# print("######  ", dict(f))
				# print(dict(f))
				# print("A@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",f)
				# print(">>>>>>>>>>>>>>>", msg["data"])
				# print(f._id, ":", dict(f))
				# print("<<<<<<<<<<<<<<<")
				# print()
			if msg["type"] == "subscribe":
				print(" ::: SUBSCRIBED TO CHANNEL", msg["pattern"])
				pass

	def __init__(self, *args, **kwargs):
		self._host = kwargs["host"] if "host" in kwargs else host
		self._port = kwargs["port"] if "port" in kwargs else port
		password = kwargs["password"] if "password" in kwargs else ""
		
		# if self._isRoot: # should work the same
		if "host" in kwargs: kwargs.pop("host")
		if "port" in kwargs: kwargs.pop("port")
		if "password" in kwargs: kwargs.pop("password")
		# kwargs.pop("pass")

		super().__init__(*args, **kwargs)
		# if self._isRoot:
			# print("Host",self._host)
			# print("Port",self._port)
			# if password != "":		
				# print("Pass","************")
		# self._rootName = "xoRedis"
		# self._namespace = self._rootName
		self._rootName = self._type.__name__
		self._namespace = self._id

		
		# if self._getRoot()._redis:
		# 	pass
		# 	print("!!!!!!!!!!!!!")
		# time.sleep(1)
		if self._isRoot:
			# print("RRRRRRRRRRRRRRRRRRRRRRRRooooooooooot")
			if "host" not in kwargs:
				kwargs["host"] = self._host
			if "port" not in kwargs:
				kwargs["port"] = self._port
			if "db" not in kwargs:
				kwargs["db"] = self._db
			if password != "":
				kwargs["password"] = password
			
			# self._redis = RedisClient(host=self._host, port=self._port, db=self._db)
			# self._redis = RedisClient(**kwargs)
			client_address = str(kwargs["host"])+":"+str(kwargs["port"])+"@"+str(kwargs["db"])
			if client_address not in xoRedis._clients:
				try:
					safekwargs = kwargs.copy()
					if "password" in safekwargs: safekwargs["password"] = "************"
					print(f"::: Connecting to {client_address}",safekwargs)
					self._redis = RedisClient(**kwargs)
					xoRedis._redis = self._redis
					success = self._redis.ping()
					if not success:
						print(f"Failed to connect to Redis at {self._host}:{self._port}")
					xoRedis._clients[client_address] = self._redis
				except Exception as e:
					# print(f"Failed to connect to Redis at {self._host}:{self._port} with error: {e.}")
					print(f"Failed to connect to Redis at {self._host}:{self._port} with error")
				self._pubsub = self._redis.pubsub()
				self._redisSubscribe(key=self._namespace+"*", handler=self._directBind)
			else:
				print(f"::: Already connected to {client_address}")
				self._redis = xoRedis._clients[client_address]

		else:
			# print("__FETCHING ON CREATION!!!!!",self._id)
			# self.__call__()
			found = None
			if len(args)>0 and isinstance(args[0], dict) and "value" in args[0]:
				found = args[0]["value"]
			elif "value" in kwargs:
				found = kwargs["value"]
			if found == None:
				# print("121212121212")
				# print("121212121212")
				# print("121212121212")
				res = self.fetchRedis()
				if res != None:
					# update instead set
					sender = yourID = hash(self._root._redis)
					super().__setitem__("value", res, skip_publish = True, sender=sender)
					# self.value = res
				else:
					pass
					# print("HANDLE NONE?")
			else:
				# print("SKIPPING FETCHING")
				print("@@@@@@@@@@")
				print("@@@@@@@@@@")
				print("@@@@@@@@@@")
				print("@@@@@@@@@@")
				self.value = found
				

			# print("__FETCHING DONE",self._id)
			# print("__PRINTING DONE_____________")
		
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


	def fetchRedis(self,*args, **kwargs):
		# print("::: Fetching ",self._id, res)
		# print("::: Fetching ",self._id)
		res = self._root._redis.get(self._id)
		if res:
			res = pk.loads(res)
			gotRes = True
			return res
		else:
			pass
			# print("::: No Matching:",self._id)
		return 
			# ex

	def __call__(self,*args, **kwargs):
		if 'value' in self:
			if 'function' in str(type(self.value)):
				# print(55555555)
				return self.value(*args, **kwargs)
		if len(args) == 0:
			# print("3434343434 call")
			# print("3434343434 call")
			# print("3434343434 call")
			res = self.fetchRedis()
			# print("MATCH:",res==self)
			if res and res != self:
				# print("Adding...",res)
				self(res, *args, **kwargs)
			# return res
			return self
		return super().__call__(*args,**kwargs)

	def __getitem__(self, key,  *args, **kwargs):
		# print("XGetting", key)
		# print("@@@@@@@@@@@@@@", key in self)
		if key == "value" or key not in self:
			
			res = super().__getitem__(key, *args, **kwargs)
		else:
			# res = super().__getitem__(key, *args, **kwargs)
			try:
				res = super().__getattribute__(key)
			except:
				res = super().__getitem__(key, *args, **kwargs)
			
		# print("2@@@@@@@@@@@@@@")
		if isinstance(res,type(self)) or isinstance(res,xoBenedict):
			# print("When New")
			# print("3@@@@@@@@@@@@@@")
			# print("XGetting got", res._id,key)
			return res
		else:
			# print("When Existing")
			# print("4@@@@@@@@@@@@@@")
			# print("GOT VALUE",type(res))
			return res
		# if key == '__dir__':
		# 	# return res without keys ['ignore','_pointer','_dict']
		# 	return {k:v for k,v in res.items() if k not in ['ignore','_pointer','_dict']}
		fkey = self._id+"."+str(key)
		if "value" == key:
			fkey = self._id
		if "value" == key or "value" in res:
			print("XFetching", fkey)
			gotRes = False
			# try:
			# try:
			if True:
				r = self._root._redis
				res = r.get(fkey)
				print("RRRRRRESSSSSSSSS",fkey, res)
				res = pk.loads(res)
				gotRes = True
			# except:
				# print(" - - - COULD NOT UNPICKLE", self._id, ":::", res)
			if gotRes and res != None:
				print("SHOULD SET",key, "TO", res)
				# self.value = res
			# self._setValue(res, skipUpdate = True)
		print("ffffffffffff",type(res))
		return res	
		return res
	
	_lastPub = {}

	def _safeUpdate(self, key, val, *args, **kwargs):
		pass
	
	def _normalPublish(self, fullkey, val, *args, **kwargs):
		r:RedisClient = self._root._redis
		sender = hash(self._root._redis)
		val = pk.dumps([sender,val])
		# val = pk.dumps(val)
		# res = r.set(self._id, val)
		if debug: print("::: Publishing x",fullkey)
		r.publish(fullkey, val)

	def _safePublish(self, fullkey, val, *args, **kwargs):
		return self._normalPublish(fullkey, val, *args, **kwargs)
	
	def _safePublishx(self, fullkey, val, *args, **kwargs):
		if fullkey not in self._root._lastPub or val != self._root._lastPub[fullkey]:
			self._root._lastPub[fullkey] = val
			print("::: Publishing safely.....",fullkey)
			# if key == "value":
			r = self._root._redis
			sender = hash(self._root._redis)
			val = pk.dumps([sender,val])
			# val = pk.dumps(val)
			# res = r.set(self._id, val)
			r.publish(fullkey, val)
			# r.publish(fullkey, [sender,val])
			# print("!!!!!!!!!!!!!! PUBLISHED", fullkey, val)
			# print(self._root._lastPub)
			# print("*************** PUBLISHED", fullkey, val)
		else:
			print("......skiping same publish..........",fullkey)

	def __setitem__(self, key, value, skip_publish = False, *args, **kwargs):
		res = super().__setitem__(key, value, *args, **kwargs)
		if key != "value" and not isinstance(value, xoBenedict):
			# self._safeUpdate(key, value)
			if debug:
				print("::: SAVING TO REDIS",self._id+"."+str(key),value)
			val = pk.dumps(value)
			res2 = self._root._redis.set(self._id+"."+str(key), val)
			if not skip_publish:
				self._safePublish(self._id+"."+str(key), value)
		return res
	
	def __setitemx__(self, key, value, doubleSkip = False, *args, **kwargs):
		skip = False
		# print("XSetting", self._id+"."+str(key), "to",type(value),)# value,)
		r = self._root._redis
		if key == "value":
			val = pk.dumps(value)
			if  value == self and not doubleSkip:
				# print("RRRRRRRRRRRRRRRRRRR333333333",r,self._id,val)
				res = r.set(self._id, val)


				print("XXXXX333333:",self._id)
				self._safePublish(self._id, value)
				# r.publish(self._id, val)
				return
				pass
			elif value is not None:# and not doubleSkip:
				pass
				print("RRRRRRRRRRRRRRRRRRR2222222",r,self._id,val)
				res = r.set(self._id, val)
				print("XXXXX22222:",self._id)
				r.publish(self._id, val)
			# else:

		# 	value._id = str(self._id)+str(key)
		# if isinstance(value, type(self)):
		elif not doubleSkip:
			# print("{{{{{{{{{{{-----")
			# if (key not in self or self[key] != value) and not isinstance(value, dict):
			if not isinstance(value, dict):
				# val = pk.dumps(value)
				# print("RRRRRRRRRRRRRRRRRRR1111111",isinstance(value, dict),value,self._id+"."+str(key),val)
				# res = r.set(self._id+"."+str(key), val)
				# print("XXXXX1111111:",self._id+"."+str(key))
				# r.publish(self._id+"."+str(key), val)
				# skip = True
				pass
				# notAgain = True
			else:
				if type(value) == dict:	print("is dict passing?",type(value),self._id+"."+str(key))
			# print("-----}}}}}}}}}}}")
			# print("nv",self._id+"."+str(key),"T:",type(value))
		# if value is None:
		# 	value = [None]
		if value != None:
			print("#######################",self._id,key, doubleSkip)
			# if key not in self or key == "value":
			res = super().__setitem__(key, value, skip = skip, *args, **kwargs)
			# print("#######################END")
			print(f"::: Key {self._id}.{key} Updated: {str(value)[:40] + '...' if len(str(value)) > 40 else str(value)}")
			# res = self[key]
			# res = self[key]
			#xxx
			return res
			return
		else:
			if key == "value":
				# self.value = None
				pass
			else:
				print(">>>>>>>>")
				self[key].value = None




class Fresh(xoBenedict):
	# def __init__(self,*args, **kwargs):
	# 	return super().__init__(*args, **kwargs)
	
	def __onchange__(self, fullkey, value, *args, **kwargs):
		'''This function is called whenever a value of a key changes'''
		print(f" : : : : {fullkey} CHANGING TO !!!{str(value).upper()}!!!",args, kwargs)
		# The value you return will be passed on as if it was the original value.
		return "!!!"+str(value).upper()+"!!!"


class FreshRedis(xoBenedict):
	# def __init__(self,*args, **kwargs):
	# 	return super().__init__(*args, **kwargs)
	
	def __onchange__(self, fullkey, value, *args, **kwargs):
		if debug: print(f"!!! : : : : {fullkey} REDIS CHANGING TO {str(value)}",args, kwargs)
		# Save and publish
		# sender = hash(self._root._redis)
		if False: #change value if you want before everything
			# Here you can modify value
			newVal = "!!!"+str(value).upper()+"!!!"
		
		newVal = value
		
		# print("vvvv",type(newVal),value)

		if isinstance(newVal,xoBenedict):
			#handle dicts
			if "value" in newVal:
				newVal = newVal.value
			
		val = pk.dumps(newVal)

		# val = pk.dumps([sender,val])
		# val = pk.dumps(val)
		fullkey = fullkey[:-6] if ".value" == fullkey[-6:] else fullkey
		res = self._root._redis.set(fullkey, val)
		if True and debug: print(f" : : : {res} SAVING TO REDIS",fullkey,newVal)
		# self._safePublish(self._id+"."+str(key), val) # maybe better to send pk and unpack
		if "skip_publish" not in kwargs:# and 'origin' not in kwargs:
		# if "skip_publish" not in kwargs:
			# print("PRE PUBLISH")
			self._safePublish(fullkey, newVal) 
		else:
			pass
			if debug: print(" : : : SKIPPING PUBLISH")

		# The value you return will be passed on as if it was the original value.
		return newVal 
	
	_host = host
	_port = port
	
	_db = 0
	_rootName = "root"
	_namespace = "namespace"
	# _parent = None
	_redis:RedisClient = None
	_pubsub = None
	_binded = None
	_live = None
	_clients = {}
	# _root:xoBenedict
	_root = None

	def new(self,*args, **kwargs):
		#TODO: Clear memory of current instance
		return type(self)(*args,**kwargs)

	def _redisSubscribe(self, key="Redis*", handler=lambda msg: print('XXXXXXXXXXXXHandler', msg), *args, **kwargs):
		# print("UUUUUUUUUUUUUUUUUUUUUUUU", key, handler, args, kwargs)
		# print("UUUUUUUUUUUUUUUUUUUUUUUU")
		# print("UUUUUUUUUUUUUUUUUUUUUUUU")
		# print("UUUUUUUUUUUUUUUUUUUUUUUU")
		# print(" ::: SUBSCRIBING TO REDIS CHANNEL", key, ":::", )
		try:
			self._pubsub.psubscribe(**{key: handler})
		# pubsub.psubscribe(key = key, handler = handler)
		# pubsub.subscribe(subscribe_key)
		# pubsub.subscribe(key)
		# pubsub.subscribe(**{key: event_handler if handler is None else handler})
		# print("........00000")
			# self._pubsub.run_in_thread(sleep_time=.00001, daemon=True)
			self._pubsub.run_in_thread(sleep_time=.00001, daemon=True)
		except Exception as e:
			# print(f"Failed to connect to Redis at {self._host}:{self._port} with error: {e.}")
			print(f"Failed: Redis is not connected")
			return False
		# for item in pubsub.listen():
		#     print(item, type(item))
		#     if item['type'] == 'message':
		#         print(item['data'])
		# print("DONE")
	
	# TODO: Also, implement option to lazy load, (set _needsUpdate or something like so)
	def _directBind(self, msg, *args, **kwargs):
		# print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
		# print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
		# print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu", msg, args, kwargs)
		# time.sleep(1)
		if isinstance(msg, dict) and "type" in msg:
			if "message" in msg["type"]:
				# do_something with the message
				channel = msg["channel"].decode() # .strip("Redis.")  # .split(".")[-1]
				# if channel.startswith(xoRedis._rootName+"."):
				# if channel.startswith(self._rootName+"/"):
				# print("ggggg", channel)
				if channel.startswith(self._id+"."):
					channel = ".".join(channel.split(".")[1:])  # .split(".")[-1]
				# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", msg, args, kwargs)
				# return message
				# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
				# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", str(msg["channel"]).replace("/", "."))
				# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
				# msg["channel"].decode().replace("/", "."))
				# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", msg["data"])

				# EDIT 1
				# f = xo._GetXO(channel, allow_creation=True)
				if True:
					# print("ggggg", channel)
					# f = self._GetXO(channel, allow_creation=False)
					# time.sleep(1)

					# f = self
					# print("PRE", self._id, "channel:", channel,"SELFID",self._id)
					
					# f = f[channel]
					# if channel.startswith(self._id):
					# 	channel = ".".join(channel.split(".")[1:])
					
					'''
					for c in channel.split("."):
						# print("c:",c)
						# if c not in f:
						# 	f[c] = xo()
						print("ccccccc",c)
						print("ffffffffff",f._id)
						f = f[c]
					'''
					# print("POST",f._id)
					
					# print("ggggg2")

					# f = xo[msg["channel"].decode().strip("xo/").replace("/", ".")]
					# f[channel] = msg["data"]
					# print("######  ", f)
					# sender, res = msg["data"]
					res = msg["data"]
					try:
						sender, res = final = pk.loads(res)
						# sender, res = final = pk.loads(res)
						# print("####@@@@@@",type(self._root))
						if sender == hash(self._root._redis):
							pass
							# print("@@@@@@@@@@@@@@@ WORKING! SKIPPING SELF UPDATE", channel, "")
							return 
						# print("try res:",res)
					except:
						print(" - - - COULD NOT UNPICKLE", self._id, ":::", res)
					'''
					print("@@@@@@@@@@@ UPDATING ",channel,self._id)
					if len(channel.split(".")) > 1:
						target = self[".".join(channel.split(".")[1:])]
						key = channel.split(".")[-1]

					else:
						target = self
						key = channel
					print("@@@@@@@@@@@ UPDATING ",target._id,key)
					print("$$$$$$$$",self._id, self._isRoot)


					# target = 
					# print("@@@@@@@@@@@2 UPDATING ", target._id, target._type)
					if key == "value" or key not in target or target[key].value != res:
						print("\n:::UUUUUUUUUUUUUUUUUUU Updating ",target._id+"."+key)
						pass
					'''
					# print("CCCCCCCCC",channel)
					channel = channel.replace("]","").replace("[",".")
					# print("CCCCCCCCC",channel)
					if channel not in self:
						# self[channel] = res
						# self[channel] = res
						getKeysYouDontHaveAlready = False
						if getKeysYouDontHaveAlready or funMode:
							if debug or funMode: print("::: Updating (new)", channel, "=", str(res)[:40] + '...' if len(str(res)) > 40 else str(res))
							# self.__setitem__(channel, res , skip_publish = True)
							pass
							# self.__setitem__(channel, res , skip_change = True)
							# self.__onchange__(channel, res, skip_publish= True)
							self.__setitem__(channel, res , skip_publish= True, sender=sender)
							
							
							pass
						# else:
						# 	print()
						return
					
					if channel in self:
						if channel not in self:
							print("Creating!!!!!!!!!!!! ",channel)
							done = False
							while not done:
								try:
									print(self[channel])
									done = True
								except:
									traceback.print_exc()
									print("Failed",channel,self._id,self)
									# time.sleep(1)
							print("Creating!!!!!!!!!!!! xxx")
						t = self
						l = len(channel.split("."))
						co = 0
						
						# print("ccccc",channel)
						'''
						for c in channel.split("."):
							# print("cccccc",c)
							if l-co == 1: channel = c
							# else:t = t[c]
							else:t:xoBenedict = t.__getitem__(c)
							co+=1
						'''
						if debug or funMode: print("::: Updating",t._id+"["+channel+"]","=",res)
						# t.__setitem__(channel, res, skip_publish = True)
						pass
						# t.__setitem__(channel, res, skip_change = True)
						# self.__onchange__(channel, res, skip_publish= True)
						# print("cccccc", self._id, channel, self.keys())
						self.__setitem__(channel,res, skip_publish = True, sender=sender, no_fetch=True)
						pass
						# t.__setitem__(channel, res, skip_publish = True, sender=sender, no_fetch=True)
						pass

					# self.__setitem__(channel, res)
					pass
						# xoRedis.__setitem__(target, key ,res)
					# print("@@@@@@@@@@@3 UPDATING ",channel)

					# f._setValue(res, skipUpdate=True)

				# f[self._valueArg] = res
				# f._updateSubscribers_(res)

				# print("######  ", f.value)
				# print("######  ", dict(f))
				# print(dict(f))
				# print("A@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",f)
				# print(">>>>>>>>>>>>>>>", msg["data"])
				# print(f._id, ":", dict(f))
				# print("<<<<<<<<<<<<<<<")
				# print()
			if msg["type"] == "subscribe":
				print(" ::: SUBSCRIBED TO CHANNEL", msg["pattern"])
				pass

	def __init__(self, *args, **kwargs):
		self._host = kwargs["host"] if "host" in kwargs else host
		self._port = kwargs["port"] if "port" in kwargs else port
		password = kwargs["password"] if "password" in kwargs else ""
		
		# if self._isRoot: # should work the same
		if "host" in kwargs: kwargs.pop("host")
		if "port" in kwargs: kwargs.pop("port")
		if "password" in kwargs: kwargs.pop("password")
		# kwargs.pop("pass")
		no_fetch = kwargs.pop("no_fetch") if "no_fetch" in kwargs else False
		super().__init__(*args, **kwargs)
		if type(self._root)!= type(self):
			self._root = self
		# if self._isRoot:
			# print("Host",self._host)
			# print("Port",self._port)
			# if password != "":		
				# print("Pass","************")
		# self._rootName = "xoRedis"
		# self._namespace = self._rootName
		self._rootName = self._type.__name__
		self._namespace = self._id

		
		# if self._getRoot()._redis:
		# 	pass
		# 	print("!!!!!!!!!!!!!")
		# time.sleep(1)
		if self._isRoot:
			# print("RRRRRRRRRRRRRRRRRRRRRRRRooooooooooot")
			if "host" not in kwargs:
				kwargs["host"] = self._host
			if "port" not in kwargs:
				kwargs["port"] = self._port
			if "db" not in kwargs:
				kwargs["db"] = self._db
			if password != "":
				kwargs["password"] = password
			
			# self._redis = RedisClient(host=self._host, port=self._port, db=self._db)
			# self._redis = RedisClient(**kwargs)
			client_address = str(kwargs["host"])+":"+str(kwargs["port"])+"@"+str(kwargs["db"])
			if client_address not in xoRedis._clients:
				try:
					safekwargs = kwargs.copy()
					if "password" in safekwargs: safekwargs["password"] = "************"
					print(f"::: Connecting to {client_address}",safekwargs)
					self._redis = RedisClient(**kwargs)
					xoRedis._redis = self._redis
					success = self._redis.ping()
					if not success:
						print(f"Failed to connect to Redis at {self._host}:{self._port}")
					xoRedis._clients[client_address] = self._redis
				except Exception as e:
					# print(f"Failed to connect to Redis at {self._host}:{self._port} with error: {e.}")
					print(f"Failed to connect to Redis at {self._host}:{self._port} with error")
				self._pubsub = self._redis.pubsub()
				self._redisSubscribe(key=self._namespace+"*", handler=self._directBind)
			else:
				print(f"::: Already connected to {client_address}")
				self._redis = xoRedis._clients[client_address]

		else:
			# print("__FETCHING ON CREATION!!!!!",self._id)
			# self.__call__()
			found = None
			if len(args)>0 and isinstance(args[0], dict) and "value" in args[0]:
				found = args[0]["value"]
			elif "value" in kwargs:
				found = kwargs["value"]
			
			if "skip_fetch" in self._params:
				# if debug or True: print(" YYYYYYYY SKIPPING FETCHING")
				self._params.pop("skip_fetch")
			elif found == None:
				# print("121212121212")
				# print("121212121212")
				# print("121212121212",args, kwargs)
				if not no_fetch:
					res = self.fetchRedis()
					if res != None:
						pass
						# self.value = res
						# print("12121212", type(self))
						self.__setitem__("value", res, skip_publish=True, origin='init:fetched',)
						# self.__setattr__("value", res)#, skip_publish=True,skip_change = True)
						# print("12121212xxxxxxxx")
						return
					else:
						pass
				'''
				'''
					# print("HANDLE NONE?")
			else:
				# print("SKIPPING FETCHING")
				# self.__setitem__("value", found, skip_change = True)
				# self.value = found
				pass
				

			# print("__FETCHING DONE",self._id)
			# print("__PRINTING DONE_____________")
		
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

	def fetchRedis(self,*args, **kwargs):
		# print("::: Fetching ",self._id, res)
		# print("::: Fetching ",self._id)
		res = self._root._redis.get(self._id)
		if res:
			res = pk.loads(res)
			gotRes = True
			return res
		else:
			pass
			# print("::: No Matching:",self._id)
		return 
			# ex

	def __call__(self,*args, **kwargs):
		if 'value' in self:
			if 'function' in str(type(self.value)):
				# print(55555555)
				return self.value(*args, **kwargs)
		if len(args) == 0:
			print("3434343434 call")
			print("3434343434 call")
			print("3434343434 call")
			res = self.fetchRedis()
			# print("MATCH:",res==self)
			if res and res != self:
				# print("Adding...",res)
				self(res, *args, **kwargs)
			# return res
			return self
		return super().__call__(*args,**kwargs)
		
	def _normalPublish(self, fullkey, val, *args, **kwargs):
		r:RedisClient = self._root._redis
		sender = hash(self._root._redis)
		orgVal = val
		val = pk.dumps([sender,val])
		# save = pk.dumps(orgVal)
		# res = r.set(self._id, save)
		if debug: print("::: Publishing",fullkey, orgVal)
		# time.sleep(1)
		r.publish(fullkey, val)

	def _safePublish(self, fullkey, val, *args, **kwargs):
		return self._normalPublish(fullkey, val, *args, **kwargs)

	# def _delete_(self, *args,**kwargs):
	def _delete_(self, element=None, *args, **kwargs):
		idToDelete = self._id if element == None else self._id+"/"+element
		print(" ::: Deleting ",  idToDelete,element,  args, kwargs, f" from redis ::: db: {self._db} namespace {self._namespace}")
		target = self
		if element is not None:
			target = self[element]
		# Send empy bytes to indecate it was deleted
		# delete entire tree ? make option available
		# target.value = bytes(), skipUpdate = False)
		target.value = bytes()
		r = self._root._redis
		r.delete(idToDelete)
		# print(" WILL DELETE ", id, args, kwargs, " FROM REDIS")
		# Delete key on redis
	


class xoBackend(FreshRedis): # change or add backends!
	pass
class xoMetric(xoBackend):
	# def __init__(self,*args, **kwargs):
	# 	return super().__init__(*args, **kwargs)
	
	def __onchange__(self, fullkey, value, *args, **kwargs):
		# print("PPPPPPPPPPPPPPPPPPPP ",self._id,fullkey,value, args, kwargs)
		# key = fullkey[len(self._id+"."):]
		# if self[key].value == value:
		# 	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
		# 	return value
		
		if "sender" not in kwargs: #kwargs include __setitem__ kwargs
			yourID = hash(self._root._redis)
			print("$ $ $ $ $ SYNCING METRICS! $ $ $ $ $", fullkey, value, args, kwargs)
		else: # Got metric from another xooMetric (redis) client
			print(f"$ $ $ $ $ Got METRICS from {kwargs['sender']}! $ $ $ $ $", fullkey, value, args, kwargs)
		# if "skip_publish" in kwargs:
		# 	return value
		return super().__onchange__(fullkey, value, *args, **kwargs) # make sure to call redis



# class xoFunctional(xoBenedict):	

#TODO fix functional updating from published sender
class xoFunctional(FreshRedis):	
	# @classmethod
	def _wrapper(self, *a,**kw):
		if self._func == None:
			return a[0] if len(a)==1 else a
		
		print(self._func)
		print("WWWWWWWW",type(self._func),a,kw)
		res = self._func(*a,**{**kw,**{"_self":self, "_fullkey":self._id if "_fullkey" not in kw else kw.pop("_fullkey")}})
		print(f"::: {self._id} Running Function : {res} :",a, kw)
		return res
	_func = None#lambda func,*a,**kw: func(*a,**kw)
	_target = None

	def __init__(self,*args, **kwargs):
		# if func: self._func = lambda *a,**kw: self._wrapper(func, *a,**kw)
		# if "function" in kwargs:
		# 	 = 

		F, T =  kwargs.pop("function") if "function" in kwargs else None, kwargs.pop('target') if 'target' in kwargs else None ,
		super().__init__(*args, **kwargs)
		if F:
			self._func, self._target  = F, T
			self._root._func ,self._root._target = F, T
		else:
			self._func, self._target = self._root._func ,self._root._target
		# else: self._func = self._root._func
		# self._func = lambda func, *a,**kw: _wrapper(func, *a,**kw)
		# self._target = None
	def __onchange__(self, fullkey, value, *args, **kwargs):
		'''This function is called whenever a value of a key changes'''
		print(f" : : : : {fullkey} Running Function {str(value).upper()}",args, kwargs)
		res = value
		# if "skip_target" not in kwargs:
		key = fullkey[len(self._id+"."):]
		print("kkkkkkkkk",key, ",", fullkey)
		# if "skip_target" not in kwargs: res = self._func(value, _fullkey=fullkey, _key=key, *args, **kwargs)
		if "skip_target" not in kwargs: res = self._wrapper(value, _fullkey=fullkey, _key=key, *args, **kwargs)
		else:
			print("SKIP RES",self._id, key)

		if key not in self:
			self.__setitem__(key,res, skip_target=True, skip_change=True)

		if self._target:
			print(f" : : : : {fullkey} Setting Results {str(res).upper()}",args, kwargs)
			print("fffff",key+'.'+self._target)
			print("ididid",self._id)
			if self._target not in key:
				pass # set one?
				print("111111111111111")
				# self.__setitem__(key+'.'+self._target, res)#, skip_change=True)
				child:xoBenedict =  self.__getitem__(key)
				# child.__setitem__(self._target, res, skip_target=True)#, skip_change=True)
				child.__setitem__(self._target, res)#, skip_target=True)#, skip_change=True)
				# self[key][self._target] = res
			elif self._target not in self._id: # set but dont rerun
				print("22222222222222",key)
				self.__setitem__(self._target, res, skip_change=True)
				# child =  self.__getitem__(key)
				# child.__setitem__(self._target, res, skip_target=True, skip_change=True)
				pass # to stop recursive processing 
		# else:
		if "skip_target"in kwargs: kwargs["skip_change"] = True

		print("333333333333",args,kwargs)
		# The value you return will be passed on as if it was the original value.
		return super().__onchange__(fullkey, res if res and False else value, *args, **kwargs) # make sure to call redis
		# return super().__onchange__(fullkey, res if res else value, *args, **kwargs) # make sure to call redis
		return res


def testFunctional():
	from xo import xoFunctional
	def plusOne(val, *args, **kwargs):
		print("  +1   !!!!!!! ",type(val),val, args, kwargs)
		try:
			return val+1
		except:
			return str(val)+"!"


	xo = xoFunctional(function = plusOne, target = "result")
	xo.a.b = 2
# testFunctional()


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



# m = xoMetric()
# m.fig
# m.msg @= lambda self, t, *a, **kw: m.fig(t)

# xo = xoBenedict()
# xo.a.b = 2
# print("......................")
# print(xo.a)
# xo.a.b.c.d.e.f = 3
# print(xo.a.b.c.d.e._id)
# print(xo.a.b.c.d.e)
# xo.a.b = 2
	# print(bx)
	# bi2 = xoBenedict(bi.json().replace("\"a\"","\"AAA\""), bi({"aa":1111111,"a":{"b":{"c":"cccccccc"}}}), **{**bi,**{"a":{"b":{"c":{"d":"DDDDDDDDDDDDDDDDDDDDDDDDDDD"}}}}})
	# print(bi2)
	
	# bi.a.b.c.set(3).d.set(4).e(5).f.set(6).g("777").set("h",888).set(7777, HH = "1000000000000000").HH.awesome.set(11111)

# from xo import xoRedis
# xo = xoRedis()
# xo.a = 3
# from xo import xoEvents
# xo = xoEvents()
# xo.a.b.c = 3

# xo = xoRedis()
# print("Ready")
# while(True):
# 	time.sleep(1)
# 	print("...")
# # xo.a.b.c.d.e = 5555555
# xo.a.b = 2
# print("DONE")
# # xo.a = 1
# print(xo)
# print("FINISH")
# print("GOODBYE")


def pnr(p, *a,**kw):
	print(p,a,kw)
	if a == () and kw == {}:
		return p
	return [p,a,kw]	


if __name__ == '__main__':
	testing()

# Hint: Ctrl+Alt+B to open outline


'''

#OG
up.fig = lambda v,Fore=color, figlet_format=figlet,*a,**kw: print(Fore.YELLOW+figlet_format(v)+Fore.WHITE)
up.msn = lambda self, color=color,msn=msn, *a,**kw: msn(self,color,*a,**kw)

# OG
from colorama import Fore as color
def msn(self, color=color,c="yellow", *a,**kw):
	self = self._root
	self.msg @= self.fig
	c = color.__getattribute__(c.upper())
	while True:
			self.msg = c+input(c+"Chat: "+color.WHITE)
up.msn = lambda self, color=color,msn=msn, *a,**kw: msn(self,color,*a,**kw)


# NEWER 

# Print with Yellow & Big Letters (colorama + figlet)
from colorama import Fore as color
from pyfiglet import figlet_format as figlet
def colorfig(v, figlet_format=figlet,Fore=color,c='yellow'):
	c = Fore.__getattribute__(c.upper())
	if "\x1b" in v:
	c, v = v[:5],v[5:]
	return c+figlet_format(v)+Fore.WHITE


up.fig = lambda v,c = 'yellow', Fore=color, figlet_format=figlet,colorfig=colorfig,*a,**kw: print(colorfig(v, figlet_format, Fore, c=c))


#NEWER

from colorama import Fore as color
def msn(self, color=color,c="yellow", *a,**kw):
	self = self._root
	self.msg @= self.fig
	c = color.__getattribute__(c.upper())
	while True:
		i = input(c+"Chat: "+color.WHITE)
		if len(i)>1 and i[0] == ":" and len(i.split(":"))>=3:
			try:
				c, i = color.__getattribute__(i.split(":")[1].upper()), ":".join(i.split(":")[2:])
			except:
				print(color.RED+i.split(":")[1]+" is not a correct color")
				continue
		final = c+i
		if len(i)>0:
			self.msg = final


up.msn = lambda self, color=color,msn=msn, *a,**kw: msn(self,color,*a,**kw)


'''


'''
#TODO/FIX:
- DONE! - value returns {} instead of None if it doesnt exits
- DONE! - fix flatten() not working for xoBranch
- DONE! - add None support
- DONE!!! - fix naming issue when new bid and updating

- Done - work with arrays, dicts - i think done, need to tese more thoroghly - 
- Done - i think, more testing - nest xo's comfturbly, meaning skip casting if type xo, so redis can be inside xobenedict and vise versa - Currently it inserted good, but str and tree dont render them properly (xo inside branch)
- fix _cast, update, setitem={} and call({}), Done - items()
- .a = {}, .a[0] = {}, .a({}) if call then update, if = , set and save as is.

- add namespace change (which works with redis, and changes _id)
- new_branch(clone_prev + overwrite with new data)
- export_keys <> import_keys[data/_key_store], on change update _root._key_store
- object as table, + multiple objects in table, compare branches, compare children

- fix show() when value is dict but not xo
- actually show() error is because on original FreshRedis, it sends a dict of nested keys instead of final key,value - need to Fix
- .tree for normal xoBenedict

- major code cleanup, refactoring, refiling


- write to @benedict 





- reorder __dir__() to show keys first!

- use aider! add ai unit tests - progressively harder (and maybe categories)
- IN NEW BRANCH - LEVEL 1 	- no changes, only codequaily improvement
							- start by cleaning all the junk comments (after unit tests), then factorize and generalize code, split to different files,
							- apply an ai loop to run the actual unit tests and try_fix/startover/recover if something breaks
- IN NEW BRANCH - LEVEL 2 	- Teach ai to write xo code, and have it generate functions to enter the skill_lib
- IN NEW BRANCH - LEVEL 3 	- 
- 
- 

- xoFiles - load folder tree and see files : data_preview txt/img in terminal
- xoFiles <> xoJS <> xoServer, Live code editing (with hot reload) save file -> see on web instantly, monitor and change, saved
	-LOP 
- use xo as syntax to genereate websites and [T] generic object, skill lib, 


- make xoBranch work on simple xo, and make new way to load inheritance, to mixmatch faster/better

# For Users
	xoGMoE, xoMagicLLight, xoAkeyo, xoEmployee, xoDelivery, xoStore 

# Frameworks For Developers
 		xoApps, LOP, xoAI, xoProjects, IFTAI
Basics: <xo>, <xoBench>, <xoDecorator>, <xoDeque>, <xoBranch> <xoMixo>
Special: <xoJS>, <xoCLI>, <xoMagicCLI> <xoDot> <xoMagic> <xApps>  
Advanced [yet easy]: <xoRedis> <xoMicro> <xoServer> <xoAPI> <xoMetric> <xoGraphana> <xoTrace> <xoLOP>
AI Basics: <xoAtom> <xoConv> <xoMemory+RAG> <xoLib> <xoResearcher> <xoLibAI> <xoAIxoCode>
AI Advanced: <xoAI> <xoAider> <xoJarvis> <xoEmployee> <xoStore> <xoJam> <xoDJ> <xoMagicLLight>
Utils: <xoFiles> <xoUsers> <xoAuth> <xoEnc> <xoDB> <xoEvents+watchdog[T,sys,wa,email,3rd,anyXo,]> <xoLinks/xoShorts> <xoThumbs> <xoDesign> <xoGit> 
Hooks: <xoCLI> <xoWeb> <xoWhatsapp> <xoTelegram> <xoDiscord> <xoSlack> <xoZoxide>
Network: <xoP2P> <xoZMQ> <xoMQTT> <xoFreeDNS> <xoVPCloud/xoDeploy> 
Magic: <xoGen> <xoMusic> <xoNLP> <xoeMotion-self/media> <xoVision>
Freedom: <xoFreeAPI> 



$$$$$$ <xoOpenSources> -> finds best open source packages, and mixes them to improve all of the non inovative aspects of all current popular services
find unique ways of futuristic thinking , for which quality of life improves through the new way of oproaching the data, **its all about distilling data into insights and actions** , everything is about how you make connections to what is coming, 

<xoAGI>
<xoFutureAI> - oracle that hallucinates the future, with leaps but progressions, and with the ability to predict the future, AND MAP IT! Simulate steps, current world live updating model


Extra: loving zoxide, need one for commands, for example, p live should find ~/wholesomegarden/xo-benedict/liveupdate.py and run it - WTF cli correct
learn rich -> rich skill for ai, live dynamic text

Tomorrow:
- Fix Naming issue when updating new bid
- make rich tables
- xoProjects - start feeding project data and content, it will be published and sorted later


OPUS - IM A COMPOSER
Opus 1 - Dev Composer										Entire xo Package, + Redhat service
Opus Initium - xoOpen$ource	aka OpenXource									Map The Uncharted Present and Future
Opus Genesis - import openxource.anything() magical psudo code + Global AI Skill Lib 				The Wikipedia of AI Skills
Opus Dawn - The Golden Plature
Opus Grand - Dev AI - Let Users bring their apis, sign in with claud/openai/etx, run locally + expose api, or charge for Package Pack + Real Life Apps IFTAI <xoEvents>
Opus Apex - Akeyo In Real Life
Opus Zenith - 
Opus Magnum - WholesomeGarden
Opus Crown - ananda 
Opus Eternal - Peace												For AGI , Life is just an API (#Everything is a function)

User
lets come up with new phrases that sound good and give the same energy
if Opus Grand - is level 5
and Opus Magnum - is level 8
what are all other levels 1-10?
Certainly! Let's create a scale of phrases from level 1 to level 10, each conveying a sense of accomplishment or significance:

1. Opus Prelude - Level 1
2. Opus Initium - Level 2
3. Opus Genesis - Level 3
5. Opus Grand - Level 5
6. Opus Apex - Level 6
7. Opus Zenith - Level 7
8. Opus Magnum - Level 8
9. Opus Crown - Level 9
10. Opus Eternal - Level 10

These phrases convey a progression from the initial stages of creation (Prelude, Initium, Genesis) to the pinnacle of achievement (Grand, Magnum, Crown) and even beyond (Eternal). Each term adds a layer of depth and grandeur to the significance of the work being described.

xoBranch on multiple models, save .meta for responses including model, recent events,

Do' should be read as DO (Re-Me) not as do (todo)

Do'pono in the morning - bless yourself (actively)
Do'opus in the day - Solve & Evolve
Do'magi in the evening - extraodinary & fun / dreamvisions -lucid
Do'pana in the night - thanks

Self-Optimize: Do Arcitecture at night, plan for tommorow, 


do kata
do rama
do pata
do kami
do bana
do shata 
do mana
do wapa
do zeta
do epa
do moda
do xahi
do leta
do geta
do fana
do rasa
do runi
do risha
do shira
do mika
do mina
do ora
do oma
do oshi
do wata
do emi
do imi
do nami
do kasa
do vana
do vani
do dani
do meta
do yuta
do yuma
do tami
do hopa
do hima
do gita
do vani
do ori
do oppo 


The Trick to: write a sentence that each word starts with a to z:
+ The meaning of the sentence should convey or tell a story, or a chunk from it, where the reader has no context, and the in the scene what happens is {scene}
[A]-complete_word [B]-complete_word ....... Fast consecutive runs, take 1 word, add the next letter, and repeat
eventually, this could be like an interupt mechanism for ais, where they asyncly talk to eachother, 
dynamically inserting eachothers words, with time delays and visuals, with a conversation manager that understands when it is appropriate to insert, and theres no cutoff, just rebranching and preloading ['unfinished thoughts'] 


'''

