from xodal import MicroXO, service
from xoServer import xoClient as C

c = C()

from magic import MagicSelfNamed

# class server(MagicSelfNamed, MicroXO):
class server(MagicSelfNamed):
	def __init__(self, func = None, *a,**kw):
		# self._name = "server"
		print("FFFFFFFOOOOOO",func)
		super().__init__(*a,**kw)
		self.realF = [lambda *a,**kw: print("CHANGE THIS",a,kw)]
		self.func = lambda *a,**kw: self.realF[0](*a,**kw)
		kw.pop('_rootName') if '_rootName' in kw else None
		print("New Server Called", self._name,a,kw)
		# self._server = MicroXO(self._name, None, *a, **kw)
	def __call__(self, func = None, *a, **kw):
		print("CALL",func, a,kw)
		self.server = MicroXO(_id = self._name,_func=func, *a, **kw)
		if func:
			def wrapper(f,*a,**kw):
				print("CALLING WRAPPER",f,a,kw)
				self.realF[0] = f
				return f(*a,**kw)
				# self.func = lambda *a,**kw: self.realF[0](*a,**kw)
				# self.server = MicroXO(self.func, _id = self._name, *a, **kw)
				# return self.server
			return wrapper(func,*a,**kw)
	def reg(self, *a,**kw):
		self._server = MicroXO.register(self._name, None, _id = self._name, *a,**kw)

# server("aaa")
# import mxo
# from RobeeServices import RobeeSystem
aaa = server()
import time
DemoSystem = {
	"main": 1111,
	"a": 1112,
	"processA": 1112,
	"processB": 1113,
}

class Main(MicroXO):
	pass


class A(MicroXO):
	pass


@Main
def hello(*args,**kwargs):
	return {"res": " !!! @@@@ Hello from MAIN SERVICE !!!"+str(args) , "args":args,"kwargs":kwargs}

@A
def hi(*args,**kwargs):
	return {"res": " !!! @@@@ Hi from MAIN SERVICE !!!"+str(args) , "args":args,"kwargs":kwargs}

aa  = MicroXO.register("a", _services = DemoSystem ) 

# main = MicroXO.register("Main", _services = DemoSystem ) 











# server().reg()










'''
@Main
def Hello(*args,**kwargs):
	return {"res": " !!! @@@@ Hello from MAIN SERVICE !!!"+str(args) , "args":args,"kwargs":kwargs}


# main = Main().register()
main = MicroXO.register("Main", _services = DemoSystem ) 

while(True):
	time.sleep(1)
'''