
# print("herexx")

from .xo import xoBenedict
from .xoServer import xoClient
from threading import Thread
class FreshClient(xoBenedict):
	_client = None
	_request_port=1970
	_publish_port=19701
	_inc = 0
	def __init__(self, client=None, _request_port=1970, _publish_port=19701, _inc=0, *a, **kw):
		self._client = client
		_request_port += _inc
		_publish_port += _inc
		# print(a,kw)
		if "_request_port" in kw:
			kw.pop("_request_port")
		if "_publish_port" in kw:
			kw.pop("_publish_port")
		if "_inc" in kw:
			kw.pop("_inc")
		# print("KKKKKKK",a,kw)
		super().__init__(*a, **kw)
		if self._isRoot and client==None:
			self._client = client = xoClient(_reqPort=_request_port , _pubPort=_publish_port) # xoClient(_id = self._id)
			print("Created client ONCE", self._client)
		if client:#"client" not in self._root:
			print(f"{self._isRoot=} {id(self)==id(self._root)}")
			self._root._client = client
			print("Got client", self._root._client)
			def fetch_public(*a,**kw):
				for k,desc in self.index():
					self[k] = k
					self[k].pop('value')
					self[k]["desc"] = desc if desc is not None else "No Description, no __doc__ strings found";
					print(f"Found {k} function from server")
			t = Thread(target=fetch_public)
			t.start()
	def __call__(self, *a, **kw):
		debug=False
		_id = ".".join(self._id.split(".")[1:]) if len(self._id.split("."))>1 else self._id
		if debug or 'debug' in kw: print("Requesting...",_id, a, kw)
		res = self._root._client.request(_id, *a, **kw)
		self.value = res
		return res


c = FreshClient()

# c.index()
