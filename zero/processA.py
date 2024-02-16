#processA.py

	
    
shared = {"namespace":"hello", "url":"localhost","port":"1970"}
shared = {"namespace":"hello"}

from xo import xoBenedict, Server, Client, FreshRedis, 

# server = Server("default_hub", "localhost:1234")
# server = Server("localhost:1234@home")
server = Server(shared)
server = Server()

@server.home.public
def somePublicFunction(*a,**kw):
    return "THIS PUBLIC FUNCTION WAS TRIGGERED!", a, kw

xo = xoClient(shared)
xo.home.public("With Data")






