

from xo import xoBenedict
from xoServer import xoClient

class FreshClient(xoBenedict):
	_client = None
	def __init__(self, client=None, *a, **kw):
		self._client = client
		print(a,kw)
		super().__init__(*a, **kw)
		if self._isRoot and client==None:
			self._client = client = xoClient() # xoClient(_id = self._id)
			print("Created client ONCE", self._client)
		if client:#"client" not in self._root:
			print(f"{self._isRoot=} {id(self)==id(self._root)}")
			self._root._client = client
			print("Got client", self._root._client)
	def __call__(self, *a, **kw):
		_id = ".".join(self._id.split(".")[1:]) if len(self._id.split("."))>1 else self._id
		print("Requesting",_id, a, kw)
		res = self._root._client.request(_id, *a, **kw)
		self.value = res
		return res


c = FreshClient()

# c.index()
