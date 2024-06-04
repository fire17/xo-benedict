


from functools import reduce
import traceback

import inspect
from .xo import xoBenedict, FreshRedis, debug
import dill as pk

from .richtree import treeXoBranch as richtree

class xoDeque(xoBenedict):
	_deque = []
	def __init__(self, *a, **kw):
		self._deque = []
		if len(a) >= 1:
			self._deque.append(a[0])
		elif "value" in kw:
			self._deque.append(kw["value"])
		super().__init__(*a, **kw)

	def __onchange__(self,_id, value, *a, **kw):
		print("ONCHANGE",a,kw)
		self._deque.append(value)
		return self._deque
		if "new" not in kw:
			return False
	def getQueue(self, item=None):
		if item != None:
			return self._deque[item]
		return self._deque
	def last(self):
		return self.getQueue(-1)
	def first(self):
		return self.getQueue(0)


import re

def remove_brackets(input_string):
	return re.sub(r'\[.*?\]', '', input_string)

def remove_round_brackets(input_string):
	return re.sub(r'\(.*?\)', '', input_string)

def _flatten_key(base_key, key, separator):
	if base_key and separator:
		return f"{base_key}{separator}{key}"
	return key


def _flatten_item(d, base_dict, base_key, separator, b=-1,current=False, hide_place = False):
	new_dict = base_dict
	# print("ddddddddd",d,type(d),d._id if hasattr(d,"_id") else None, d._bid if hasattr(d,"_bid") else None)
	keys = list(d.keys())
	for key in keys:
		# print("KKKK",key)
		value = d[key]
		# if hasattr(value,"_bid"):
		# 	print("!!!!!!!!!!!!!!!",key,b,value._bid)
		# 	# key = value._id.split(".")[-1]
		# 	# key = key+f"[{value._bid}]"
		# 	# key = key+f"[{b}]"
		# 	print("::::::::::::::::",key)
		# else:
		# 	print("xxxxxxx",key, type(value),value,"xxxxxxx")
		new_key = _flatten_key(base_key, key, separator)
		# print("$$$$$$$$$$$",new_key)
		if isinstance(value,dict):
			if not current and hasattr(value,"_branch") and len(value._branch)>0:
				bcount = 0
				for br in value._branch:
					# place = f"({bcount+1}%-%--%-%{len(value._branch)})"
					# place = f" {place}" if place != "" and place != "(1/1)" else ""
					new_value = _flatten_item(
						br, base_dict=new_dict, base_key=new_key+(f"[{bcount}]"), separator=separator, b = bcount, hide_place = hide_place
						# br, base_dict=new_dict, base_key=new_key+(place), separator=separator, b = bcount
					)
					new_dict.update(new_value)
					bcount+=1
			else:
				# place = f"({value._bid}%-%--%-%{len(value._branch)})" if not hide_place and hasattr(value,"_bid") else ""
				# place = f" {place}" if place != "" and place != "(1/1)" else ""
				new_value = _flatten_item(
					value, base_dict=new_dict, base_key=new_key+(f"[{value._bid}]" if not hide_place and hasattr(value,"_bid") else ""), separator=separator, b = b,
					# value, base_dict=new_dict, base_key=new_key+(place), separator=separator, b = b,
					current = current, hide_place = hide_place
				)
				new_dict.update(new_value)
			continue
		# place = f"({value._bid}%-%--%-%{len(value._branch)})" if hasattr(value,"_bid") and not hide_place and not current else ""
		# place = f" {place}" if place != "" and place != "(1/1)" else ""
		new_key = new_key +f"[{value._bid}]" if hasattr(value,"_bid") and not hide_place and not current else new_key
		# new_key = new_key + place
		# print("NNNNNNNNNNN",new_key,b,)
		if hide_place and remove_brackets(new_key) not in new_dict:
			new_dict[remove_brackets(new_key)] = value
		else:
			if new_key in new_dict:
				raise KeyError(f"Invalid key: {new_key!r}, key already in flatten dict.")
			new_dict[new_key] = value
	return new_dict


def flatten(d, current=False, hide_place=False, separator="_"):
	new_dict = {}
	if not current and hasattr(d, "_branch") and len(d._branch)>0:
		bcount = 0
		for b in d._flatten_item(d, base_dict=new_dict, base_key="", separator=separator, hide_place = hide_place):
			new_dict.update(_flatten_item(b, base_dict=new_dict, base_key="", separator=separator, b=bcount), hide_place = hide_place)
			bcount += 1
		return new_dict
	return _flatten_item(d, base_dict=new_dict, base_key="", separator=separator, b=0, current=current, hide_place = hide_place)

# class xoBranch(xoBenedict): # Untested but should work!
# class xoBranch(xoDeque): # Working Structure!
class xoBranch(FreshRedis):
	_branch = []
	_bid = -1
	_parent=None
	_marker = 0
	_floor_branch = None
	_deque = []
	# def __init__(self, xoType=xoDeque, *a, **kw):
	def __init__(self,_bid=0,_parent=None,init = False, *a, **kw):
		self._branch = []
		self._bid = _bid
		self._parent=_parent
		# print("<<<<<<<<<<init - ",self._bid,self._parent._id if self._parent is not None else "- Parent None", init, a, kw)
		# self._branch.append(xoType(*a,**kw))
		if len(a) >= 1:
			self._deque.append(a[0])
		elif "value" in kw:
			self._deque.append(kw["value"])

		if "yes_fetch" not in kw: kw["no_fetch"] = True
		skip_reid = False
		if "_id" in kw:
			if kw['_id'][-1] == "]":
				kw['_id'] = "[".join(kw['_id'].split("[")[:-1])+"["+str(self._bid)+"]"
				self._bid = self._marker
			else:
				kw['_id'] = kw['_id']+f"[{self._bid}]"
			skip_reid = True
		# print(">>>>>>>>>",_bid)
		super().__init__(*a, **kw)
		# print(">>>>>>>>>",self._id)
		if False:
			if self._isRoot:
				print("SHOULD NOT FETCH",self._id)
			else:
				print("X SHOULD NOT FETCH",self._id)
			# print("XXXXXXXXXXXXXXXXXXXXXXXXX")
			# print("XXXXXXXXXXXXXXXXXXXXXXXXX")
			# print("XXXXXXXXXXXXXXXXXXXXXXXXX")
		if not skip_reid:
			if self._id[-1] == "]":
				self._id = "[".join(self._id.split("[")[:-1])+"["+str(self._bid)+"]"
				self._bid = self._marker
			else:
				self._id = self._id+f"[{self._bid}]"
		if self._parent != None:
			self._parent._branch.append(self)
			self._bid = len(self._parent._branch) - 1
			setMarker = True
			if setMarker:
				self._parent._marker = self._bid
				# This moves the marker
		if not init and "value" not in self.keys() and ('value' not in kw and "skip_change" not in kw):
			# Not expecting change
			parent = self
			if self._parent != None:
				parent = self._parent
			# 	parent._deque.append(value)
			# else:
			# 	self._deque.append(value)
			if True:
				if self._parent != None:
					# print("YYYYYYYYY222222222")
					if False: # This just adds a useless branch
						newBranch = type(self)(_parent = parent, _id = self._id,_bid=len(self._parent._branch), init =True)
					if False: #NOT SURE ABOUT THIS ONE,was ok before, but seems ok now off too #XXX
						self._parent._bid = len(self._parent._branch)-1
				else:
					# print("NNNNNNNNNN3333333333")
					newBranch = type(self)(_parent = parent, _id = self._id,_bid=len(self._branch), init = True)
		elif "value" in kw and "skip_change" in kw:
			v = kw.pop("value")
			_id = kw.pop("_id")
			self.__setitem__("value",v, *a, **kw)
		# elif self._isRoot:
		#     self.current()._branch.append(self)
		# elif self._branch == []:
		#     self._branch.append(self)
		#     self.current()._branch.append(self)



	#xxxx
	# def show(self, t="    ", count=0, inLoop=False, ret=False):

	def show(self, t="    ", count=0, inLoop=False, ret=False, marker = True):
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
		elif count==0:
			# print("zzzzzzzzzzzz")
			pass
			print(p.replace("\t", "    "))
		brc = 0
		# for brr in self._branch:
		# 	# print(000000000000,hasattr(brr,"_branch"),brr, brr._parent._branch)
		# 	for brk in brr:
		# 		# print("BBBBBBBBBBBBBBB",bbc, self._id, brk)
		# 		bbc+=1
		# 		if not hasattr(brr[brk],"_branch"):
		# 			if not brk.startswith("_"):
		# 				if isinstance(brr[brk], type(self)) or isinstance(brr[brk], dict) or "dict" in str(type(brr[brk])):
		# 						# print("33334",a)
		# 					if ret:
		# 						# print("33335555",a)
		# 						res = brr[brk].show(count=count+1, ret=ret)
		# 					else:
		# 						# print("3333466666",a)
		# 						brr[brk].show(count=count+1, ret=ret)
		# 				else:
		# 					print("    "*len(brr._id.split(".")[1:])+".".join(brr._id.split(".")[-1:]), "=", brr[brk])
		# 		else:
		# for br in brr[brk]._branch:
		bid = self._marker
		for br in self._branch:
			# print(":::",bid, br, br._marker, brc, bid, current, brc==bid)
			isCurrent = self._marker == brc and marker
			# bid = br._marker
			for a in br:
				mark = "*" if isCurrent else ""
				# print("aaaaaaaaaaaa",a, bbc, br[a])
				# print("33333", a, type(br[a]))
				# if "_" not in a:
				# print("st2", s)
				if not a.startswith("_"):
					if isinstance(br[a], type(self)) or isinstance(br[a], dict) or "dict" in str(type(br[a])):
							# print("33334",a)
						if ret:
							# print("33335555",a)
							# res = br[a].show(count = count + 1, ret = ret, marker = isCurrent)
							# res.append(br[a].show(count = count + 1, ret = ret, marker = isCurrent))
							[res.append(final) for final in (br[a].show(count = count + 1, ret = ret, marker = isCurrent))]
						else:
							# print("3333466666",a)
							br[a].show(count = count + 1, ret = ret, marker = isCurrent)
					else:
						final = "    "*len(br._id.split(".")[1:])+mark+".".join(br._id.split(".")[-1:])+ " = "+str(br[a])
						print(final)
						res.append(final)
					# print("!",tab,f"{a} = {br[a]}")
					# print("33337",a)
			brc+=1
		if count == 0 and inLoop:
			print("\n\nPress Ctrl+C to stop whileShow()\n")

		if ret:
			# print("444444444")
			if count == 0:
				# print("4444444445",type(retList),type(res),res)
				return retList + res
			# print("55555555",count)
			return retList + res
		# print("777777",ret,count,retList,res,)
		# return dict(self)


	# def __ifloordiv__(self, other):
	# 	# change self.on_branch
	# 	print(self._floor_branch, self._parent._floor_branch)
	# 	if self._parent != None and self._parent._floor_branch != None:
	# 		print("########")
	# 		self._parent._branch[self._parent._floor_branch].__setitem__("value", other, skip_change=True)
	# 		self._parent._floor_branch = None
	# 		# return res

	# 	print("??????????22222222")
	# 	res =  self.__setitem__("value",other, skip_change=True)
	# 	return res

	@classmethod
	def _import(cls, d):
		if isinstance(d, bytes):
			return cls().import_branches(pk.loads(d))
		return cls().import_branches(d)

	def pr(d):
		print(":::",d._id)
		d = d.flatten()
		# print("............")
		[print(k,":",v) for k,v in d.items()]
		# print("............!")

	def right(self,times=1, cycle=False, end = False):
		if end: return self.moveMarkerToEnd()
		return self.moveRight(times,cycle)
	def home(self, *a,**kw):return self.left(start=True,*a,**kw)
	def end(self,*a,**kw):return self.right(end=True,*a,**kw)
	def left(self,times=1, cycle=False, end = False, start=False):
		if end or start: return self.moveMarkerToStart()
		return self.moveLeft(times,cycle)

	def moveRight(self,times=1, cycle = False):
		print(f"::: Moving Marker +{times} ", end="")
		if len(self._branch) == 0: return
		if self._marker < 0 : self._marker = self._marker % len(self._branch)
		if self._marker + times < len(self._branch):
			self.moveMarker(self._marker + times)
		elif not cycle:
			self.moveMarker(-1)
		else:
			self.moveMarker((self._marker + times)% len(self._branch))
		return self.current()

	def moveLeft(self,times=1, cycle = False):
		print(f"::: Moving Marker -{times} ",end="")
		if len(self._branch) == 0: return
		if self._marker < 0 : self._marker = self._marker % len(self._branch)
		if self._marker - times >= 0:
			self.moveMarker(self._marker - times)
		elif not cycle:
			self.moveMarker(0)
		else:
			self.moveMarker((self._marker - times)% len(self._branch))
		return self.current()

	def moveMarkerToStart(self):
		self.moveMarker(0)
		return self.current()
	def moveMarkerToEnd(self):
		self.moveMarker(len(self._branch)-1)
		return self.current()

	def moveMarker(self, newMarker, debug=False):
		if len(self._branch) == 0:
			return
		# self._marker = newMarker
		# print(type(len(self._branch)), type(newMarker), newMarker, self._branch)
		self._marker = newMarker % len(self._branch)
		# self._floor_branch = self._marker
		if debug: print("::: Marker moved to ",newMarker)
		self._id = "[".join(self._id.split("[")[:-1])+"["+str(self._marker)+"]"
		self._bid = self._marker
		# if self._parent != None:
		#     self._parent._marker = newMarker
		return self.current()

	def get(self, key, default=None):
		res = self.__getattr__(key)
		if res == None:
			return default
		return res

	def __len__(self):
		# if "value" in self.current():
		# 	if hasattr(self.current().value,"__len__"):
		# 		return len(self.current()["value"])


		return len(self._branch) if len(self._branch) > 0 else len(self.keys())



	def branches(self, fast = False, useSuper = False):
		ret = []
		if useSuper:
			res = super().items(fast=fast)
			print(f"GOT {len(list(res))} with super",res)
			ret.append(res)
			# yield res
			# return res
		if len(self._branch) == 0:
			for a in [list(i.items()) for i in (b for b in self._parent._branch)]:
				pass
				# ret.append(a)
				# yield
		else:
		# return self._branch
			for a in self._branch:
				ret.append(a)
				# yield a
		return ret


	def itemsy(self, fast = False, useSuper = False):
		if useSuper:
			res = super().items(fast=fast)
			print(f"GOT {len(list(res))} with super")
			return res
		print(f"iiiii:{self._id}",useSuper)
		if len(self._branch) > 0:

			# return [item for d in self._branch for item in d.items(useSuper=True)]
			print("Getting Branches of",self._id)
			# res = [item for d in self._branch for item in d.items(useSuper=True)]
			res = [d for d in self._branch]
			print("GOT:",len(res), res)
			return res
			return [item for d in self._branch for item in d.items()]
		else: #lif self._parent is not None:
			print("NO BRANCHES",self._id, self._bid, self.value if "value" in self else "- NO VALUE")
			# return self._parent.items()
		return super().items()
		# list_of_dicts = [{"items": [1, 2]}, {"items": [3, 4]}]
		# final = combined_list = [item for d in self._branch for item in d.items(useSuper=True)]
		# print(combined_list)
		# final = [sublist.items() for sublist in self._branch for item in sublist]
		# return final
	def itemsx(self, fast = False, useSuper = False):
		if useSuper:
			return super().items(fast=fast)
		# list_of_dicts = [{"items": [1, 2]}, {"items": [3, 4]}]
		# final = combined_list = [item for d in self._branch for item in d.items(useSuper=True)]
		final = combined_list = [item for d in self._branch for item in d.items(useSuper=True)]
		# print(combined_list)
		# final = [sublist.items() for sublist in self._branch for item in sublist]
		return final

	# def clear(self):
	# 	[a.clear() for a in self._branch]
	# 	self._branch.clear()

	def __onchange__(self,_id, value, *a, **kw):
		# print("ONCHANGE",a,kw)
		if False: print("::: Creating a new branch for ",self._id,self.place(),":",_id,value, a,kw)
		# newBranch = type(self)(_id = self._id,_bid=len(self._branch))
		# newBranch.value = value
		# if "value" not in self.keys() and value != "____init____":
		# 	self["value"] = "____init____"
			# self.pop("value")

		parent = self
		if self._parent != None:
			parent = self._parent
			parent._deque.append(value)
		else:
			self._deque.append(value)
		def isEmpty(obj):
			# print("XXXXXXX",obj.keys(),len(obj.keys()))
			return len(obj.keys()) == 0
			# print("DELETING EMPTY BRANCH!!!")

		if self._parent != None:
			if len(self._parent._branch)>0 and isEmpty(self._parent._branch[-1]):
				# print("DELETING EMPTY BRANCH!!!")
				self._parent._branch.pop(-1)
			else:
				pass
				# print("NOT DELETING EMPTY BRANCH!!!", self._parent._branch[-1],)
			# print("YYYYYYYYY")
			newBranch = type(self)(_parent = parent, _id = self._id,_bid=len(self._parent._branch),value = value)
			self._parent._bid = len(self._parent._branch)-1
		else:
			# print("NNNNNNNNNN")
			newBranch = type(self)(_parent = parent, _id = self._id,_bid=len(self._branch),value = value)
		# newBranch = type(self)(new = True, _parent = parent, _id = self._id,_bid=len(self._branch),value = value)
		# if "new" in kw:
		#     kw.pop("new")
		# else:
		#     return self._deque
		# if len(a) >= 1:
		#     self._deque.append(a[0])
		# elif "value" in kw:
		# if self._parent != None:
		#     return self._parent._deque
		# newBranch.value = value
		# if self._parent != None:
		#     self._parent._branch.append(newBranch)
		# self._branch.append(newBranch)
		if False and "skip_publish" not in kw:
			if "__onchagne__" in super().__dir__():
				print("!!!!!!!!!!!!")
				super().__onchange__(_id, value, *a, **kw)
			elif True:
				FreshRedis.__onchange__(self, _id, value, *a, **kw)
				# since rebranching, run on change only after setting
		# print("FFFFFFFFF","__onchagne__" in super().__dir__())

		return False
		if "new" not in kw:
			return False

	# def __str__(self, *a, **kw):
	# 	if "final" in kw:
	# 		return str(super().__str__())
	# 	return  self.current().__str__(final = True)
	def __repr__(self):
		if self.current() != None:
			return str(self.current())
		return super().__repr__()

	def __getattr__(self, item, *args, **kwargs):
		# if item == '_branch':
		# 	pass
		if item == "items" or item == "_branch":
			print("$$$$$$$$$$$$$$$$$$$$",item)
			# print("!!!!!!!!!!!!!!!!!!!!")
		if "final" in kwargs:
			kwargs.pop("final")
			return super().__getitem__(item, *args, **kwargs)
		# if item not in self.current():
		return self.current().__getitem__(item,*args, **kwargs)


	def __getitem__(self, item, *args, **kwargs):
		if item == "items" or item == "_branch":
			print("$$$$$$$$$$$$$$$$$$$$iiiii",item)
		# if isinstance(item, tuple) or isinstance(item,list):
		# 	# return reduce(lambda x, y: x[y], [1,0,1], [[1],[[0,17],2]])
		# 	return reduce(lambda x, y: x[y], list(item), self)
		# else:
		# 	print("<<<<<<<<<<<<<<<<<")
		# 	print("<<<<<<<<<<<<<<<<<")
		# 	print("<<<<<<<<<<<<<<<<<")
		# 	print("<<<<<<<<<<<<<<<<<",type(item))
		# print("\nGGGGGGG",item,args,kwargs)
		if item == '_branch':
			pass
			# print("!!!!!!!!!!!!!!!!!!!!")
		if "final" in kwargs:
			kwargs.pop("final")
			if "current" in kwargs: kwargs.pop("current")
			return super().__getitem__(item, *args, **kwargs)
		if item == "value":
			kwargs["final"] = True
			return self.current().__getattr__(item, *args, **kwargs)
			# return self.current()._deque
		if "current" in kwargs:
			kwargs.pop("current")
			return super().__getitem__(item,*args, **kwargs)
		if item in self.current():
			# kwargs["current"] = True
			kwargs["final"] = True
			return self.current().__getattr__(item, *args, **kwargs)
		else:
			def canBeInt(string):
				try:
					# print(f"@{string}@")
					return int(string)
				except:
					# traceback.print_exc()
					return False
			isInt = canBeInt(item)
			if isInt is not False:
				item = isInt
			# print("ISISISISIS", isInt, item, len(self._branch)==0)
			if isinstance(item, int):# and item < len(self._branch):
				if (item == 0 or item == -1) and len(self._branch)==0:
					# print("!!!!!!!!!!!!!!!!!!!!!!!",item)
					return self
				if False and (item >= len(self._branch) or item < -1 * len(self._branch)):
					# print("!!!!!!!!!!!!!!!!!!!!!!!222222222",item)
					class OutOfIndexError(Exception):
						pass
					calling_frame = inspect.currentframe().f_back
					calling_line_number = inspect.getframeinfo(calling_frame).lineno

					if not hasattr (inspect.getframeinfo(calling_frame), "filename"):
						raise OutOfIndexError(f"Index {item} is out of range for an object with {len(self._branch)} branches\n(line {calling_line_number})")
					calling_file_name = inspect.getframeinfo(calling_frame).filename
					# print(calling_file_name,"!!!!!!!!!")
					if len(str(calling_file_name))>0 and calling_file_name[0]!="<":
						with open(calling_file_name, 'r') as file:
							lines = file.readlines()
							error_line = lines[calling_line_number - 1].strip()
						raise OutOfIndexError(f"Index {item} is out of range for an object with {len(self._branch)} branches\n(line {calling_line_number}): {error_line}\n{'^'*len(error_line)}")
					raise OutOfIndexError(f"Index {item} is out of range for an object with {len(self._branch)} branches\n({calling_file_name}:line {calling_line_number})")
				else:
					while (item >= len(self._branch) or item < -1 * len(self._branch)):
						parent = self
						if self._parent != None:
							parent = self._parent
						print("NEW BID",len(parent._branch))
						newBranch = type(self)(_parent = parent, _id = self._id,_bid=len(parent._branch),)

				# print("FFFFFFFFFFFFFFFFF",item)
				# self.moveMarker(item)
				self._floor_branch = item
				return self._branch[item]
				return self._branch[item]
			else:
				# print("???????????",item, self._marker, len(self._branch))
				# self.moveMarker(item)
				if isinstance(item,slice):
					return self._branch[item]
				self.current().__setattr__(item, type(self)( _bid = 0 , _id = self._id+"."+item, *args, **kwargs))
		kwargs["final"] = True
		return self.current().__getattr__(item,*args, **kwargs)

	def place(self):
		return f"[{self._marker+1}/{len(self._branch) if len(self._branch)>0 else 1}]"

	def flatten(self, sep=None,rep="/", current=False, init=True, hide_place=False, *a, **kw):
		def fix(key):#,counter):
			key = key.replace(rep, sep if sep else self.keypath_separator).replace("%-%--%-%","/")
			if len(key)>6 and key[-6:] == self.keypath_separator + "value":
				key = key[:-6]
			# counter[0]+=1
			# print("ccccccccccccccc",counter)
			return key
		if not init:
			# final = flatten(self,current,rep).items()
			final = flatten(self,current,hide_place, rep).items()
			# print("FFFFFFFFFFF",final)
			return final
		if current==True:
			return { fix(k):v for k,v in self.current().flatten(sep,rep,current,False, hide_place)}
		final = []
		for br in self._branch:
			for k,v in br.flatten(sep,rep,current, False, hide_place):
				final.append((k,v))
		return {fix(k):v for k,v in final}


	def export_branches(self, key = None):
		return self.flatten()

	def import_branches(self, flat_branches):
		[self[remove_brackets(k)].set("value",v) for k,v in flat_branches.items()]
		return self

	def clone(self, *a, **kw):
		return self(type)().import_branches(self.export_branches())

	def keys(self,*a,**kw):
		# print("iiiiiiiii",id(self), id(self.current()))
		if id(self) != id(self.current()):
			return self.current().keys()
		return super().keys()

	def clone(self,*a,**kw):
		# print("iiiiiiiii",id(self), id(self.current()))
		if id(self) != id(self.current()):
			return self.current().clone()
		return super().clone()

	def _updateID(self, newID, base_id=None):
		_id = self._id if base_id is None else base_id
		# print("uuuu",_id, newID, base_id)
		res = "[".join(_id.split("[")[:-1])+"[" + str(newID) + "]" if "[" in _id.split(".")[-1] else _id+"["+str(newID)+"]"
		# print("uuuuuuu",res)
		return res

	def __setitem__(self, item, value, *args, **kwargs):
		# print("Setting...", item, value, kwargs)
		def canBeInt(string):
			try:
				# print(f"@{string}@")
				return int(string)
			except:
				# traceback.print_exc()
				return False
		# if isinstance(item, str) and len(item.split(".")) > 1:
		# 	return self.__setitem__(item.split("."), value, *args, **kwargs)
		# if isinstance(item, tuple) or isinstance(item,list):
		# 	# return reduce(lambda x, y: x[y], [1,0,1], [[1],[[0,17],2]])
		# 	if canBeInt(list(item)[-1]) is not False:
		# 		return  reduce(lambda x, y: x[y], list(item)[:-1], self)._parent._branch[int(list(item)[-1])].__setitem__("value",value, *args, **kwargs)
		# 	return reduce(lambda x, y: x[y], list(item)[:-1], self).__setitem__(list(item)[-1],value, *args, **kwargs)
		# print("SSSSSSSS",item, type(value),value, args, kwargs)

		isInt = canBeInt(item)
		if isInt is not False: item = isInt
		# print("ISISISISIS", isInt, item, len(self._branch)==0)
		if isinstance(item, int) :
			self.moveMarker(item)
			self._floor_branch = item
			# print("PPPPPPPP",self._id, self._parent)
			# return self._branch[item].__setitem__('value',value,*args, **kwargs)# skip_change="skip_change"in kwargs)
			# res = self.current()._parent._branch[item].__setitem__('value',value,*args, **kwargs)# skip_change="skip_change"in kwargs)
			# res = self.__setitem__('value',value,skip_change=True, *args, **kwargs)# skip_change="skip_change"in kwargs)
			kwargs["bid"] = isInt
			res = self.__setitem__('value',value,skip_change=True, *args, **kwargs)# skip_change="skip_change"in kwargs)
			self.end()
			if hasattr(super(),'__onchange__'):
				print("HHHHHHHHHHHHHHHHHHH")
				print("HHHHHHHHHHHHHHHHHHH")
				print("HHHHHHHHHHHHHHHHHHH",self._id)
				print("HHHHHHHHHHHHHHHHHHH",item)
				# return super().__onchange__(self._updateID(item, self._id), value, *args, **kwargs)
				return res
			return res
			return self.current()._parent._branch[item].__setitem__('value',value,*args, **kwargs)# skip_change="skip_change"in kwargs)
		elif self._floor_branch == None:
			self.end()

		if "current" not in kwargs and "final" not in kwargs:
			# print("/////////")
			kwargs["current"] = True
			return self.current().__setitem__(item, value, *args, **kwargs)
		elif "current" in kwargs:
			kwargs.pop("current")
		if "final" in kwargs:
			kwargs.pop("final")
			if item == "value":
				final_id = self._updateID(self._bid+(1 if len(self.keys())>0 else 0 ), self._id)
				if "bid" in kwargs:
					final_id = self._updateID(kwargs.pop("bid"), self._id)
					print("FINAL!",final_id)
				# print("^^^^^^", self._id, item, len(self._branch), len(self._parent._branch), isInt, ":::",len(self.keys()), ":", 1 if len(self.keys())>0 else 0 )
				res = FreshRedis.__onchange__(self, final_id, value, *args, **kwargs)
				# print("^^^^^^",res, self._id, self._bid, final_id, self._id)
				# return res
			# else:
			# 	pass
				# print("?????",item, value, len(self._branch), len(self._parent._branch))
			return super().__setitem__(item, value, *args, **kwargs)
		if item == "value":
			kwargs["final"] = True
			# self.current()._deque.append(value)
			# return self.current()._deque

			return self.current().__setitem__(item, value, *args, **kwargs)
		return super().__setitem__(item, value,*args, **kwargs)


	# def __getattr__(self, item, *args, **kwargs):
	#     if "final" in kwargs:
	#         # kwargs.pop("final")
	#         return super().__getitem__(item, *args, **kwargs)
	#     return self.__getitem__(self, item, *args, **kwargs)
	def __contains__(self, item, *a, **kw):
		# return super().__contains__(item)
		if 'final' not in kw:
			kw["final"] = True
			if isinstance(item,slice):
				return self._branch[item]
			return self.current(skip_change=True).__contains__(item, *a, **kw)
		else:
			# if "final" in kw: kw.pop("final")
			return super().__contains__(item)


	def current(self, skip_change = False):
		if len(self._branch) == 0:
			return self
		if self._marker != None and self._marker < len(self._branch):
			if self._marker >= len(self._branch):
				self._marker = len(self._branch) - 1
			elif self._marker < -1 * len(self._branch):
				self._marker = 0
			if not skip_change:
				self._id = "[".join(self._id.split("[")[:-1])+"["+str(self._marker)+"]"
				self._bid = self._marker
			return self._branch[self._marker]
		return self._branch[-1]
	def currentx(self):
		if len(self._branch) == 0:
			return self
		return self._branch[-1]

	def getBranch(self, item=None, safeguard_range = True):
		if safeguard_range:
			if item != None and item >= len(self._branch):
				item = len(self._branch) - 1
			elif item != None and item < -1 * len(self._branch):
				item = 0
		if item != None:
			return self._branch[item]
		return self._branch
	def last(self):
		return self.current().getBranch(-1)
	def first(self):
		return self.current().getBranch(0)

	def items(self, fast=True):
		for k in self.keys():
			yield k, self[k]

	def __str__(self, bid = 0, noplace=False):
		# print("STR",self._id, len(self._branch))
		if self._branch == []:
			if bid is None:
				return self._parent[self._bid].__str__(bid = self._bid, noplace=noplace)
			return str(self._parent)
		if "value" in self and len(self.keys()) == 1:
			# print("JUST VALUE",self.value)
			return f'{self.value!r}'
		result = {}
		brc = 0
		# for br in self.branches():
		# for br in self.branches():
		if True:
			br = self[self._marker]
			# print("BR",)
			# target = br[bid] if bid is not None else br

			for key, val in br[br._marker].items():
				# print("KV",key,type(val))
				# print("BR branches",len(br._branch), br._b	id)
				if len(str(key)) > 0 and str(key)[0] != "_":
					# if isinstance(val,dict) and "value" in val and len(val.keys())==1:
					# 	result[key+f':{br._bid}:'] = val
					# else:
					# 	result[key+f':{br._bid}:'] = val
					if isinstance(val, type(self)):
						# result[key+f':{val.place()}-{val._bid}:'] = val
						result[key] = val
					else:
						result[key] = val

			if "value" in result:
				val = result.pop("value")
				result = {"value":val,**result}
			brc += 1
		# print("GGGGGGGGGG")
		# print(result)
		# print("GGGGGGGGGG")
		final = "{" + ", ".join([f"\"{k}\" {str(v.place() if not noplace and hasattr(v,'place') and v.place() != '[1/1]' else '').replace('[','(').replace(']',')')}: {v.__str__(noplace=noplace) if isinstance(v,type(self)) else v}" for k,v in result.items()]) + "}"
		return final

	def __strx__(self):
		if "value" in self and len(self.keys()) == 1:
			return f'{self.value!r}'


		result = {}  # Start with an empty dictionary to store the key-value pairs
		# Iterate over each key-value pair in self.items()
		# for key, val in self.items(fast=True,  useSuper = True):
		for key, val in self.items(fast=True,  useSuper = True):
			# Check if the key is not empty and doesn't start with "_"
			if len(str(key)) > 0 and str(key)[0] != "_":
				# key += " "
				# Add the key-value pair to the result dictionary
				if isinstance(val,dict) and "value" in val and len(val.keys())==1:
					# print("@@@@@@@@@@@@@@@@",val["value"])
					pass
					# result[key] = f'{val["value"]!r}'
					pass
					# result[key] = val["value"]
					result[key] = val
				else:
					# print(":::",val)
					# result[key] = val
					pass
					# result[key] = f'{val!r}'
					pass
					result[key] = val

		if "value" in result:
			val = result.pop("value")
			result = {"value":val,**result}

		# # Convert the dictionary to a JSON-like string
		# output = "{" + ", ".join(f"\"{key}\": {val}" for key, val in result.items()) + "}"

		# # Return the JSON-like string
		# return output

		# final = "{" + ", ".join([f"\"{k}\" {str(v.place() if hasattr(v,'place') and v.place() != '[1/1]' else '').replace('[','(').replace(']',')')}: {v.__str__()}" for k,v in self.items()]) + "}"
		final = "{" + ", ".join([f"\"{k}\" {str(v.place() if hasattr(v,'place') and v.place() != '[1/1]' else '').replace('[','(').replace(']',')')}: {v!r}" for k,v in result.items()]) + "}"
		# for k in self.keys():
		# 	final +=
		return final
		# return "{"+super().__str__()[1:-1]+str(self.place())+"}"
	def tree(self, noplace=True, ret=False):
		print()
		res = richtree(self, noplace=noplace)
		if ret:
			return res



if __name__ == "__main__":
	bx = xoBranch();
	print("::: xoBranch Started")
	# bx = xoBranch(); xo = bx
	# bx.a = 1
	# xo.tree()
	# bx.a(222).b(2222)#.c(1)
	# xo.tree()
	# input("ENABLE BRAKEPOINT!")
	# xo.a.b(3333).c(4444)
	# xo.tree()

	bx.tree()
	while(True):
		d = input("Press Enter to display: ")
		if d == "":
			bx.tree()
		elif len(d)>3 and "fetch:" in d[:6]:
			_,k = d.split(":")[0], ":".join(d.split(":")[1:])
			print(f"::: Fetching {k}",k, bx[k])
			bx[k].fetchRedis()
			print(f"::: Fetched {k}",k, bx[k])
			bx.tree()
		elif len(d)>3 and "del:" in d[:4]:
			_,k = d.split(":")[0], ":".join(d.split(":")[1:])
			print(f"::: Deleting {k}",k, bx[k])
			bx.delete(k)
			bx.tree()
		elif len(d)>3 and "call:" in d[:4]:
			dd,k = d.split(":")[0], ":".join(d.split(":")[1:])
			if ":" in k[0]:
				k,v = d.split(":")[0], ":".join(d.split(":")[1:])
				print(f"::: Calling {k} with argument! {v}", bx[k],"\n") # use ast.literal_eval to add dictionary
				bx[k](v)
			else:
				print(f"::: Calling {k}",k, bx[k],"\n")
				bx[k]()
			bx.tree()

		elif ":" in d:
			k,v = d.split(":")[0], ":".join(d.split(":")[1:])
			print("::: Setting",bx[k]._id, "to", v)
			bx[k] = v
			bx.tree()
		else:
			print("::: Showing",bx[d]._id)
			bx[d].tree()



# bx = xoBranch()
# bx.a = 1111111
# bx.a = 2222222
# bx.flatten()
