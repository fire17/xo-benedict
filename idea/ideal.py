# ideal.py

class SpecialOps(object):
    #TODO: add logic for dynamic func swaping and syntax swapping (ideas)
    pass

class XOperations(SpecialOps):
    def __init__(self, hook, program, *args, **kwargs):
        self.hook = hook
        self.program = program
        # SPECIAL NEW SYNTAX - Override Dunder Methods
        self._special.append(magic("$=", "__iformula__", "//=", "__ifloordiv__"))  # sacrifices //= __ifloordiv__
        self._special.append(magic("<--", "__iinclude__", "<<=", "__ilshift__"))   # sacrifices <<= __ilshift__
        self._special.append(magic("-->", "__ishare__", ">>=", "__irshift__"))     # sacrifices >>= __irshift__
        self._special.append(magic("<>", "__ibind__", "^=", "__ixor__"))            # sacrifices ^= __ixor__
        self._special.append(magic(":=", "__icall__", "|=", "__ior__"))             # sacrifices |= __ior__
        # OVERIDE EXISTING SYNTAX - Native Dunder Methods
        self._special.append(magic("|", "__ipipe__", "|", "__or__"))         # sacrifices \| __or__
        self._special.append(magic("%=", "__iconnect__", "%=", "__imod__"))   # sacrifices %= __imod__
        self._special.append(magic("&=", "__ibehavior__", "&=", "__iand__"))  # sacrifices &= __iand__
        self._special.append(magic("@=", "__isubscribe__", "@=", "__imatmul__")) # sacrifices @= __imatmul__

    def __idollar__(self, other):
        # return self.hook.transform_source(other)
        return f'{str(self)} $$$$$$$$$$$$ {str(other)}'
    
    def __iwalrus__(self, other):
        return f'{str(self) :=:=:=:=: {str(other)}}'

class xoSpecial(XOperations):
    def __init__(self, *a, **kw):
        def magic(token,function,placeholder):
            return [token,function,placeholder]

        return super().__init__(*a,**kw)


magic1, magic2 = xoSpecial("aaa"), xoSpecial("bbb")
# Use all new syntax 
magic1 $= magic2 ; print("Formula ::: ", magic1, magic2)
magic1 <-- magic2 ; print("Include ::: ", magic1, magic2)
magic1 --> magic2 ; print("Share ::: ", magic1, magic2)
magic1 <> magic2 ; print("Bind ::: ", magic1, magic2)
magic1 := magic2 ; print("Call ::: ", magic1, magic2)
magic1 | magic2 ; print("Pipe ::: ", magic1, magic2)
magic1 %= magic2 ; print("Connect ::: ", magic1, magic2)
magic1 &= magic2 ; print("Behavior ::: ", magic1, magic2)
magic1 @= magic2 ; print("Subscribe ::: ", magic1, magic2)



'''

Here are the two tables based on your specifications:

Override Table:

| Dunder Method  | Syntax Example | New Dunder      | New Syntax      | Title     |
|----------------|----------------|-----------------|-----------------|-----------|
| `__ifloordiv__`| `obj1 //= obj2`| `__iformula__`  | `obj1 $= obj2`  | Formula   |
| `__ilshift__`  | `obj1 <<= obj2`| `__iinclude__`  | `obj1 <-- obj2` | Include   |
| `__irshift__`  | `obj1 >>= obj2`| `__ishare__`    | `obj1 --> obj2` | Share     |
| `__ixor__`     | `obj1 ^= obj2` | `__ibind__`     | `obj1 <> obj2`  | Bind      |
| `__ior__`      | `obj1 |= obj2` | `__icall__`     | `obj1 := obj2`  | Call      |

Native Table:

| Dunder Method  | Syntax Example | New Dunder      | New Syntax      | Title     |
|----------------|----------------|-----------------|-----------------|-----------|
| `__or__`       | `obj1 \| obj2` | `__ipipe__`     | `servA \| servB`| Pipe      |
| `__imod__`     | `obj1 %= obj2` | `__iconnect__`  | `servA % servB` | Connect   |
| `__iand__`     | `obj1 &= obj2` | `__ibehavior__` | `obj1 &= foo`   | Behavior  |
| `__imatmul__`  | `obj1 @= obj2` | `__isubscribe__`| `obj1 @= foo`   | Subscribe |

'''
These tables provide a clear comparison between the original dunder methods and their proposed replacements, along with the corresponding syntax examples and titles for each.
# changes to <>