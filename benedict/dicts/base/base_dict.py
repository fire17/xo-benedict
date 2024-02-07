from benedict.core import clone as _clone


# class ValueDict(dict):
#     def __rep__(self):
#         return str(self)
    
#     def __str__(self):
#         print("S S S",len(self.keys()), self.keys())
#         if "value" in self.keys() and len(self.keys()) == 1:
#             print(" VLAST ")
#             return str(self.value)
#         return "{x{"+", ".join((f"\'{key}\': {ValueDict(val) if type(val) == dict else val}") for key, val in self.items())+"}"

class BaseDict(dict):
    _dict = None
    _pointer = False

    
    def _get_obj(self, value):
        print("Gooooooooooooooooooooo",type(value),value)
        value = {"value":value} if not isinstance(value, dict) else value
        if isinstance(value, dict) and not isinstance(value, type(self)):
            print("0000000000",type(value), value)
            for key in value.keys():
                print("111111 k",key)
                key_val = value[key]
                if isinstance(key_val, dict):
                    print("dddddddd",type(key_val),key_val)
                    key_val = self._get_obj(value[key])
                    value[key] = key_val
                    
                else:
                    print("vvvvv",type(key_val),key_val)
                    if key not in self:
                        self[key] = type(self)()
                    self[key]["value"] = key_val
                    print("FFFFFFFFFinal SV",self)
                    return  self
        print("FFFFFFFFFinal",value)
        
        return value
    
    @classmethod
    def _get_dict_or_value(cls, value):
        value = value.dict() if isinstance(value, cls) else value
        if isinstance(value, dict):
            for key in value.keys():
                key_val = value[key]
                if isinstance(key_val, cls):
                    key_val = cls._get_dict_or_value(value[key])
                    value[key] = key_val
        return value

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            self._dict = self._get_dict_or_value(args[0])
            self._pointer = True
            super().__init__(self._dict)
            return
        self._dict = None
        self._pointer = False
        super().__init__(*args, **kwargs)

    def __bool__(self):
        if self._pointer:
            return bool(self._dict)
        return len(self.keys()) > 0

    def __contains__(self, key):
        if self._pointer:
            return key in self._dict
        return super().__contains__(key)

    def __deepcopy__(self, memo):
        obj = self.__class__()
        for key, value in self.items():
            obj[key] = _clone(value, memo=memo)
        return obj

    def __delitem__(self, key):
        if self._pointer:
            del self._dict[key]
            return
        super().__delitem__(key)

    def __eq__(self, other):
        if self._pointer:
            return self._dict == other
        return super().__eq__(other)

    def __getitem__(self, key):
        print("ggggg",key)
        if self._pointer:
            print("gpppppppp")
            return self._dict[key]
        return super().__getitem__(key)

    def __ior__(self, other):
        if self._pointer:
            return self._dict.__ior__(other)
        return super().__ior__(other)

    def __iter__(self):
        if self._pointer:
            return iter(self._dict)
        return super().__iter__()

    def __len__(self):
        if self._pointer:
            return len(self._dict)
        return super().__len__()

    def __or__(self, other):
        if self._pointer:
            return self._dict.__or__(other)
        return super().__or__(other)

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
            print(" VLAST ",str(self.value))
            x,y = '\"','\\"'
            if isinstance(self.value, str) and ("'" in self.value or '"' in self.value):
                print("EEEEEEEEEEEEEEEEEE",self.value,)
                print("EEEEEEEEEEEEEEEEEe",self.value.replace(x,y),)
                return f'"{self.value.replace(x,y)}"'
            elif isinstance(self.value, str):
                print("eeeeeeeeee",self.value,)
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
        print("DDDDDDDDDDDDDDDDDDD")
        # return "{"+""", """.join((f"""{repr(key)}: {type(self)(val) if type(val) == dict else val}""") for key, val in self.items())+"}"
        # return "{"+", ".join((f"\'{key}\': {val}") for key, val in self.items())+"}"
        return "{"+", ".join((f"\"{key}\": {val}") for key, val in self.items())+"}"


    def __setitem__(self, key, value):
        # if type(value) != type(self):
        #     print("real value",value)
        #     value = self._get_dict_or_value(value)
        #     self.value = value
        #     return 
        # else:
        #     print("virtual value",value)
            
        value = self._get_dict_or_value(value)
        if self._pointer:
            is_dict_item = key in self._dict and isinstance(self._dict[key], dict)
            is_dict_value = isinstance(value, dict)
            if is_dict_item and is_dict_value:
                if self._dict[key] is value:
                #     print("??????????????????",key,value,type(value))
                #     if isinstance(value,dict) and "value" in value:
                #         self._dict[key] = value["value"]
                #     return
                # if self._dict[key] is "value":
                #     print("??????????????????2222222222",key,value)
                # # if self._dict[key] is "value":
                #     # prevent clearing dict instance when assigning value to itself. fix #294
                    return
                self._dict[key].clear()
                self._dict[key].update(value)
                return
            if isinstance(value,type(self)) and "value" in value:
                self._dict[key] = value["value"]
            else:
                self._dict[key] = value
            return
        super().__setitem__(key, value)

    def __setstate__(self, state):
        self._dict = state["_dict"]
        self._pointer = state["_pointer"]


    def clear(self):
        if self._pointer:
            self._dict.clear()
            return
        super().clear()

    def copy(self):
        if self._pointer:
            return self._dict.copy()
        return super().copy()

    def dict(self):
        if self._pointer:
            return self._dict
        return self

    def get(self, key, default=None):
        if self._pointer:
            return self._dict.get(key, default)
        return super().get(key, default)

    def items(self):
        if self._pointer:
            return self._dict.items()
        return super().items()

    def keys(self):
        if self._pointer:
            return self._dict.keys()
        return super().keys()

    def pop(self, key, *args):
        if self._pointer:
            return self._dict.pop(key, *args)
        return super().pop(key, *args)

    def setdefault(self, key, default=None):
        default = self._get_dict_or_value(default)
        if self._pointer:
            return self._dict.setdefault(key, default)
        return super().setdefault(key, default)

    def update(self, other):
        # other = self._get_dict_or_value(other)
        other = self._get_obj(other)
        if self._pointer:
            self._dict.update(other)
            return
        super().update(other)

    def values(self):
        if self._pointer:
            return self._dict.values()
        return super().values()
