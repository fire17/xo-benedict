


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
        if self._parent != None:
            self._parent._branch.append(self)
        # elif self._isRoot:
        #     self.current()._branch.append(self)
        # elif self._branch == []:
        #     self._branch.append(self)
        #     self.current()._branch.append(self)

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

    def current(self):
        if len(self._branch) == 0:
            return self
        return self._branch[-1]

    def getBranch(self, item=None):
        if item != None:
            return self._branch[item]
        return self._branch
    def last(self):
        return self.current().getBranch(-1)
    def first(self):
        return self.current().getBranch(0)