


import traceback

import inspect
from xo import xoBenedict

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
		
class xoBranch(xoDeque):
	_branch = []
	_bid = -1
	_parent=None
	_marker = -1
	# def __init__(self, xoType=xoDeque, *a, **kw):
	def __init__(self,_bid=0,_parent=None,new = False, *a, **kw):
		self._branch = []
		self._bid = _bid
		self._parent=_parent
		# self._branch.append(xoType(*a,**kw))
		if len(a) >= 1:
			self._deque.append(a[0])
		elif "value" in kw:
			self._deque.append(kw["value"])
		super().__init__(*a, **kw)
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

		# elif self._isRoot:
		#     self.current()._branch.append(self)
		# elif self._branch == []:
		#     self._branch.append(self)
		#     self.current()._branch.append(self)
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

	def moveMarkerToStart(self):
		self.moveMarker(0)
	def moveMarkerToEnd(self):
		self.moveMarker(len(self._branch)-1)

	def moveMarker(self, newMarker):
		if len(self._branch) == 0:
			return 
		self._marker = newMarker
		self._marker = self._marker % len(self._branch)
		print("::: Marker moved to ",newMarker)
		self._id = "[".join(self._id.split("[")[:-1])+"["+str(self._marker)+"]"
		self._bid = self._marker
		# if self._parent != None:
		#     self._parent._marker = newMarker

	def __len__(self):
		if "value" in self.current():
			if hasattr(self.current().value,"__len__"):
				return len(self.current()["value"])
			
		
		return len(self._branch) if len(self._branch) > 0 else len(self.keys())
		

	def __onchange__(self,_id, value, *a, **kw):
		print("ONCHANGE",a,kw)
		print("CREATING A NEW BRANCH",self._id,":",_id,value)
		# newBranch = type(self)(_id = self._id,_bid=len(self._branch))
		# newBranch.value = value
		parent = self
		if self._parent != None:
			parent = self._parent
			parent._deque.append(value)
		else:
			self._deque.append(value)
		if self._parent != None:
			print("YYYYYYYYY")
			newBranch = type(self)(_parent = parent, _id = self._id,_bid=len(self._parent._branch),value = value)
			self._parent._bid = len(self._parent._branch)-1
		else:
			print("NNNNNNNNNN")
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

		
		return False
		if "new" not in kw:
			return False

	def __str__(self, *a, **kw):
		if "final" in kw:
			return str(super().__str__())
		return  self.current().__str__(final = True)
	def __repr__(self):
		return  str(self.current())

	def __getattr__(self, item, *args, **kwargs):
		if item == '_branch':
			print("!!!!!!!!!!!!!!!!!!!!")
		if "final" in kwargs:
			kwargs.pop("final")
			return super().__getitem__(item, *args, **kwargs)
		# if item not in self.current():
			
		return self.current().__getitem__(item,*args, **kwargs)
		
	
	def __getitem__(self, item, *args, **kwargs):
		print("GGGGGGG",item,args,kwargs)
		if item == '_branch':
			print("!!!!!!!!!!!!!!!!!!!!")
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
			if isinstance(item, int):# and item < len(self._branch):
				if item == 0 or item == -1 and len(self._branch)==0:
					return self
				if item >= len(self._branch) or item < -1 * len(self._branch):
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
				
				return self._branch[item]
			else:
				if isinstance(item,slice):
					return self._branch[item]
				self.current().__setattr__(item, type(self)( _bid = 0 , _id = self._id+"."+item, *args, **kwargs))
		kwargs["final"] = True
		return self.current().__getattr__(item,*args, **kwargs)
		
		
	
	def __setitem__(self, item, value, *args, **kwargs):
		print("SSSSSSSS",item, value, args, kwargs)
		if "current" not in kwargs and "final" not in kwargs:
			print("/////////")
			kwargs["current"] = True
			return self.current().__setitem__(item, value, *args, **kwargs)
		elif "current" in kwargs:
			kwargs.pop("current")
		if "final" in kwargs:
			kwargs.pop("final")
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