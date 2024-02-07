from benedict.core import clean as _clean
from benedict.core import clone as _clone
from benedict.core import dump as _dump
from benedict.core import filter as _filter
from benedict.core import find as _find
from benedict.core import flatten as _flatten
from benedict.core import groupby as _groupby
from benedict.core import invert as _invert
from benedict.core import items_sorted_by_keys as _items_sorted_by_keys
from benedict.core import items_sorted_by_values as _items_sorted_by_values
from benedict.core import keypaths as _keypaths
from benedict.core import match as _match
from benedict.core import merge as _merge
from benedict.core import move as _move
from benedict.core import nest as _nest
from benedict.core import remove as _remove
from benedict.core import rename as _rename
from benedict.core import search as _search
from benedict.core import standardize as _standardize
from benedict.core import subset as _subset
from benedict.core import swap as _swap
from benedict.core import traverse as _traverse
from benedict.core import unflatten as _unflatten
from benedict.core import unique as _unique
from benedict.dicts.io import IODict
from benedict.dicts.keyattr import KeyattrDict
from benedict.dicts.keylist import KeylistDict
from benedict.dicts.keypath import KeypathDict
from benedict.dicts.parse import ParseDict
from benedict.serializers import JSONSerializer, YAMLSerializer

import json, ast

__all__ = [
	"benedict",
	"IODict",
	"KeyattrDict",
	"KeylistDict",
	"KeypathDict",
	"ParseDict",
	"xo",
]
counter = 0


#BUG
#TODO: fix update()
#TODO: fix _call_ kwargs override instead of update - push kwargs into args as one dict


#TODO bring show from xo og + add colors indicating on performance metrics (usage) (size) (weight of data)
#TODO functional chaining functions and pipe results
#TODO make indepenent class
#TODO make class multi flavors [redis, vis_performance, web front [js], remote network [mqtt,zero] , tables[csv,df,sql]]
#TODO make easy micro services communication
class benedict(KeyattrDict, KeypathDict, IODict, ParseDict):
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
		print("aaaaaaaaaaaaaa",args,kwargs)#, args[0] == self)
		if len(args) == 1 and isinstance(args[0], benedict):
			print("zZZZZZZZZ")
			obj = args[0]
			kwargs.setdefault("keyattr_enabled", obj.keyattr_enabled)
			kwargs.setdefault("keyattr_dynamic", obj.keyattr_dynamic)
			# kwargs.setdefault("keyattr_dynamic", True)
			kwargs.setdefault("keypath_separator", obj.keypath_separator)
			super().__init__(obj.dict(), **kwargs)
			# self.update(kwargs)
			print("OOOOOOOOO o o ")
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
			print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOO",len(args),args)
			for a in args:
				if isinstance(a,dict) and not isinstance(a,type(self)):
					for k in a:
						final[k] = a[k]
						kwargs[k] = a[k]
				else:
					extras.append(a)
			if len(final) > 0:
				args = [final]
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
		print("eeeeeeeeeeee",extras)
		print("yo yo yo ", kwargs == self)
		
		if "value" not in extra_keys and len(extras) > 0:
			extra_keys["value"] = extras[0] if len(extras)==1 else extras
		
		update_incoming = True # Set to False to work leaner (checking for self[key] doubles the calls)
		# update_incoming = False # Set to False to work leaner (checking for self[key] doubles the calls)
		if update_incoming:
			for key, value in extra_keys.items():
				print("mmm",key,value, key in self)
				print("WWWWWWWW",type(value))
				if key != "value" and key in self and type(self[key]) != type(self):
				# if key != "value" and key in self:# and type(self[key]) != type(self):
					print("kkk",key,type(self[key]) != type(self))
					print("MMMMMMMMMMMMM",key,value, key in self)
					self[key] = value
					print(".x.",key)
				elif key not in self:
					print("!!!!!!!!!!!!!!!!!!",key)
					if key == "value":
						self[key] = value
					else:
						self[key] = value
						pass
				else:
					print("...")

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

	def __deepcopy__(self, memo):
		obj_type = type(self)
		obj = obj_type(
			keyattr_enabled=self._keyattr_enabled,
			keyattr_dynamic=self._keyattr_dynamic,
			keypath_separator=self._keypath_separator,
		)
		for key, value in self.items():
			obj[key] = _clone(value, memo=memo)
		return obj

	def __call__(self,*args, **kwargs):
		print("ccccccccccccccCCCCCCCALLLLLLLLLLLLLLLLLL")
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

	# def __str__(self):
	#     if "value" in self.keys() and len(self.keys()) == 1:
	#         print("1LLLLLLLLLLLLLLLL:",len(self.keys()),self.keys())
	#         return str(self.value)
	#     print("2LLLLLLLLLLLLLLLL:",len(self.keys()),self.keys())
	#     return super().__str__()
	
	# def __repr__(self):
	#     print("RRRRRRRRRRRRRRR:",len(self.keys()),self.keys())
	#     if "value" in self.keys() and len(self.keys()) == 1:
	#         return self.value.__repr__()
	#     return super().__repr__()
	
	def __getitem__(self, key):
		res = self._cast(super().__getitem__(key))
		if key not in self.__dict__:
			print("WORKING !!!!!!!!!!!!")
			self.__dict__[key] = res
		return res

	def set(self,*args, **kwargs):
		print("SSSSSSSSSSSSSSSSS",)
		print("SSSSSSSSSSSSSSSSS")
		print("SSSSSSSSSSSSSSSSS")
		print("SSSSSSSSSSSSSSSSS",args,kwargs,)
		print("CCCCCCCCCCCCCCCCC",self)
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
		print("######################")
		print("######################")
		print("######################")
		print("######################")
		print("######################",args, kwargs)
		if len(args) > 1:
			res = super().set(*args, **kwargs)
		# if res: return res;
		return self

	def __setitem__(self, key, value, skip = False):
		obj_type = type(self)
		# obj_type()
		print("set KKKKKKKK",key)
		if key != "value" and not isinstance(value, dict) and not isinstance(value, obj_type) and not skip:
			print("111111111111", value)
			
			value = obj_type({"value":value}, keyattr_dynamic=True)
			print("set 22222222222", value)
			# value.__setitem__(,value, skip = True)
			print("value", value)
			print("key", key)
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
		print("set 3333333", value)
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

	def clean(self, strings=True, collections=True):
		"""
		Clean the current dict instance removing all empty values: None, '', {}, [], ().
		If strings or collections (dict, list, set, tuple) flags are False,
		related empty values will not be deleted.
		"""
		_clean(self, strings=strings, collections=collections)

	def clone(self):
		"""
		Creates and return a clone of the current dict instance (deep copy).
		"""
		return self._cast(_clone(self))

	def copy(self):
		"""
		Creates and return a copy of the current instance (shallow copy).
		"""
		return self._cast(super().copy())

	def deepcopy(self):
		"""
		Alias of 'clone' method.
		"""
		return self.clone()

	def deepupdate(self, other, *args):
		"""
		Alias of 'merge' method.
		"""
		self.merge(other, *args)

	def dump(self, data=None):
		"""
		Return a readable string representation of any dict/list.
		This method can be used both as static method or instance method.
		"""
		return _dump(data or self)

	def filter(self, predicate):
		"""
		Return a new filtered dict using the given predicate function.
		Predicate function receives key, value arguments and should return a bool value.
		"""
		return _filter(self, predicate)

	def find(self, keys, default=None):
		"""
		Return the first match searching for the given keys.
		If no result found, default value is returned.
		"""
		return _find(self, keys, default)

	def flatten(self, separator="_"):
		"""
		Return a new flattened dict using the given separator
		to join nested dict keys to flatten keypaths.
		"""
		if separator == self._keypath_separator:
			raise ValueError(
				f"Invalid flatten separator: {separator!r}, "
				"flatten separator must be different from keypath separator."
			)
		return _flatten(self, separator)

	def get(self, key, default=None):
		return self._cast(super().get(key, default))

	def get_dict(self, key, default=None):
		return self._cast(super().get_dict(key, default))

	def get_list_item(self, key, index=0, default=None, separator=","):
		return self._cast(super().get_list_item(key, index, default, separator))

	def groupby(self, key, by_key):
		"""
		Group a list of dicts at key by the value of the given by_key and return a new dict.
		"""
		return self._cast(_groupby(self[key], by_key))

	def invert(self, flat=False):
		"""
		Return a new inverted dict, where values become keys and keys become values.
		Since multiple keys could have the same value, each value will be a list of keys.
		If flat is True each value will be a single value (use this only if values are unique).
		"""
		return _invert(self, flat)

	def items(self):
		for key, value in super().items():
			yield (key, self._cast(value))

	def items_sorted_by_keys(self, reverse=False):
		"""
		Return items (key/value list) sorted by keys.
		If reverse is True, the list will be reversed.
		"""
		return _items_sorted_by_keys(self, reverse=reverse)

	def items_sorted_by_values(self, reverse=False):
		"""
		Return items (key/value list) sorted by values.
		If reverse is True, the list will be reversed.
		"""
		return _items_sorted_by_values(self, reverse=reverse)

	def keypaths(self, indexes=False):
		"""
		Return a list of all keypaths in the dict.
		If indexes is True, the output will include list values indexes.
		"""
		return _keypaths(self, separator=self._keypath_separator, indexes=indexes)

	def match(self, pattern, indexes=True):
		"""
		Return a list of all values whose keypath
		matches the given pattern (a regex or string).
		If pattern is string, wildcard can be used
		(eg. [*] can be used to match all list indexes).
		If indexes is True, the pattern will be matched also against list values.
		"""
		return _match(self, pattern, separator=self._keypath_separator, indexes=indexes)

	def merge(self, other, *args, **kwargs):
		"""
		Merge one or more dict objects into current instance (deepupdate).
		Sub-dictionaries will be merged together.
		If overwrite is False, existing values will not be overwritten.
		If concat is True, list values will be concatenated together.
		"""
		_merge(self, other, *args, **kwargs)

	def move(self, key_src, key_dest):
		"""
		Move a dict instance value item from 'key_src' to 'key_dst'.
		If key_dst exists, its value will be overwritten.
		"""
		_move(self, key_src, key_dest)

	def nest(
		self, key, id_key="id", parent_id_key="parent_id", children_key="children"
	):
		"""
		Nest a list of dicts at the given key and return a new nested list
		using the specified keys to establish the correct items hierarchy.
		"""
		return _nest(self[key], id_key, parent_id_key, children_key)

	def pop(self, key, *args):
		return self._cast(super().pop(key, *args))

	def remove(self, keys, *args):
		"""
		Remove multiple keys from the current dict instance.
		It is possible to pass a single key or more keys (as list or *args).
		"""
		_remove(self, keys, *args)

	def setdefault(self, key, default=None):
		return self._cast(super().setdefault(key, default))

	def rename(self, key, key_new):
		"""
		Rename a dict item key from 'key' to 'key_new'.
		If key_new exists, a KeyError will be raised.
		"""
		_rename(self, key, key_new)

	def search(
		self, query, in_keys=True, in_values=True, exact=False, case_sensitive=False
	):
		"""
		Search and return a list of items (dict, key, value, ) matching the given query.
		"""
		return _search(self, query, in_keys, in_values, exact, case_sensitive)

	def standardize(self):
		"""
		Standardize all dict keys (e.g. 'Location Latitude' -> 'location_latitude').
		"""
		_standardize(self)

	def subset(self, keys, *args):
		"""
		Return a new dict subset for the given keys.
		It is possible to pass a single key or multiple keys (as list or *args).
		"""
		return _subset(self, keys, *args)

	def swap(self, key1, key2):
		"""
		Swap items values at the given keys.
		"""
		_swap(self, key1, key2)

	def traverse(self, callback):
		"""
		Traverse the current dict instance (including nested dicts),
		and pass each item (dict, key, value) to the callback function.
		"""
		_traverse(self, callback)

	def unflatten(self, separator="_"):
		"""
		Return a new unflattened dict using the given separator
		to split dict keys to nested keypaths.
		"""
		return _unflatten(self, separator)

	def unique(self):
		"""
		Remove duplicated values from the current dict instance.
		"""
		_unique(self)

	def values(self):
		for value in super().values():
			yield self._cast(value)



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
	
	# def __contains__(self, item):
	# 	''' Check if the item is in the dictionary or the value. '''
	# 	if "value" in self:
	# 		return item in self["value"] or item in self
	# 	return self._cast(super().__contains__(item))

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
	
	


	


# fix benedict json dumps support - #57 #59 #61
JSONSerializer.disable_c_make_encoder()

# fix benedict yaml representer - #43
YAMLSerializer.represent_dict_for_class(benedict)


# from benedict import benedict


def testing():
	bi = benedict()
	bi.a.b.c = "yooooooooooooooo'\""
	bi.a.b.c.d = 444444444
	bi2 = benedict(bi.json().replace("\"a\"","\"AAA\""), bi({"aa":1111111,"a":{"b":{"c":"cccccccc"}}}), **{**bi,**{"a":{"b":{"c":{"d":"DDDDDDDDDDDDDDDDDDDDDDDDDDD"}}}}})
	print(bi2)
	
	bi.a.b.c.set(3).d.set(4).e(5).f.set(6).g("777").set("h",888).set(7777, HH = "1000000000000000").HH.awesome.set(11111)
	print(bi)


class xo(benedict):
	''' Expando Object Based on BeneDict 
	- https://github.com/fire17/xo-benedict

	## Example:
	xo = xo({"a":1,"b":2})
	xo.a.b.c = 3
	xo.show() # xo.whileShow() is also available (lazy updates,dash)
	xo.dash()

	
	'''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.show = self.whileShow
		# remList = [k for k in self.__dict__keys() if k.startswith("_")]
		remList = [k for k in self.__dict__.keys() if k not in self.keys()]
		for k in remList:
			# self.__dict__.pop(k)
			pass

		# self.dash = self.whileDash
		# self.show()
	def xxx(self, *args, **kwargs):
		print("XXXXXXXXXXXXXXXXXXX")

	def search(self, query, *args, **kwargs):
		''' Search for a key in the dictionary. '''
		#TODO: currently choosing defult, add params to get more/all results from super()

		return list(super().search(query)[0])[0][query]
		# return self.find(query, *args, **kwargs)
# testing()

