# import eventlet
# eventlet.monkey_patch()


import time
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send, join_room, leave_room
# from xo import *
# from xo.redis import xoRedis
from xo import FreshRedis as xoRedis
# import eventlet
# from eventlet import wsgi
# eventlet.monkey_patch()

withOAuth = False

if withOAuth:
    from flask import Flask, redirect, url_for                                                                                                                                               
    from flask_oauthlib.client import OAuth                                                                                                                                                  
                                                                                                                                                                                             
    app = Flask(__name__)                                                                                                                                                                    
    app.secret_key = 'your_secret_key'                                                                                                                                                       
                                                                                                                                                                                             
    oauth = OAuth(app)      
    google = oauth.remote_app(                                                                                                                                                               
        'google',                                                                                                                                                                            
        consumer_key='your_google_consumer_key',                                                                                                                                             
        consumer_secret='your_google_consumer_secret',                                                                                                                                       
        request_token_params={'scope': 'email'},                                                                                                                                             
        base_url='https://www.googleapis.com/oauth2/v1/',                                                                                                                                    
        request_token_url=None,                                                                                                                                                              
        access_token_method='POST',                                                                                                                                                          
        access_token_url='https://accounts.google.com/o/oauth2/token',                                                                                                                       
        authorize_url='https://accounts.google.com/o/oauth2/auth'                                                                                                                            
    )
    
    github = oauth.remote_app(                                                                                                                                                               
        'github',                                                                                                                                                                            
        consumer_key='your_github_consumer_key',                                                                                                                                             
        consumer_secret='your_github_consumer_secret',                                                                                                                                       
        request_token_params={'scope': 'user:email'},                                                                                                                                        
        base_url='https://api.github.com/',                                                                                                                                                  
        request_token_url=None,                                                                                                                                                              
        access_token_method='POST',                                                                                                                                                          
        access_token_url='https://github.com/login/oauth/access_token',                                                                                                                      
        authorize_url='https://github.com/login/oauth/authorize'                                                                                                                             
    )   

         

# redis = lo = xoRedis(host="localhost",port=6379)
redis = lo = xoRedis(base = 'web')
# redis = xoRedis("demo",host='wise-coyote-46085.upstash.io',port=46085,password='7fdf57fde49e4eadb7a260d0e38230a2',ssl=True)
# redis = xoRedis("demo",host='ethical-monarch-46113.upstash.io',port=46113,password='7a984cbd2d4b408e8d84c4c44deea3c5',ssl=True)
port = 5000
# port = 8080
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app, cors_allowed_origins=['http://localhost:8080','http://localhost:5173','http://localhost:4173'],async_mode='threading')
socketio = SocketIO(app, cors_allowed_origins='*',async_mode='threading')

redis.count = 11

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    redis.lastSession = request.sid # type: ignore
    print('A user connected', redis.lastSession)

@socketio.on('disconnect')
def on_disconnect():
    print('A user disconnected', request.sid) # type: ignore

@socketio.on('count_update')
def on_count_update(message):
    print(f'CCCCCCCCCC Received message: {message}')

    # Send message back to the client that initiated the event
    # redis.sessions[request.sid].message = message
    print(":::",request.__dir__)
    # emit('server_update', {"data":message+"!","message":message+"@@"}, room = request.sid)
    # emit('server_update', {"data":{"_value":"{'Server Recieved': {message:'"+message+"'}}","extra":{"_value":"inner_data","meta":{}}},"message":str(message)+"!"}, room = request.sid)  # type: ignore
    redis.count = int(message)
    print(":::",request.sid)  # type: ignore

@socketio.on('user_msg')
def on_send_message(message):
    print(f'Received message: {message}')

    # Send message back to the client that initiated the event
    # redis.sessions[request.sid].message = message
    print(":::",request.__dir__)
    # emit('server_update', {"data":message+"!","message":message+"@@"}, room = request.sid)
    emit('server_update', {"data":{"_value":"{'Server Recieved': {message:'"+message+"'}}","extra":{"_value":"inner_data","meta":{}}},"message":str(message)+"!"}, room = request.sid)  # type: ignore
    redis.msg = message
    print(":::",request.sid)  # type: ignore
    # print(xo)
    # redis.lastSession = request.sid

    # send('server_update', message+"!", room=request.sid)

# redis.trigger.on = "off"
redis.trigger.on = "on"

# @socketio.on('disconnect')
def manualCount(*v,**kw):
    print("count transfer",v, kw)
    room = redis.lastSession.value  # type: ignore
    # socketio.emit('server_update', {"message":"countTransfer","count":int(v[0])}, to = room)
    # socketio.emit('server_update', {"data":{"_value":v[0],"extra":{"_value":"inner_data","meta":{}}},"message":str(v[0]),"count":int(redis.count.value)}, to = room)
    socketio.emit('server_update', {"data":{"_value":f"{v[0]}","extra":{"_value":"inner_data","meta":{}}},"message":str(v[0]),"count":int(v[0])}, to = room)
            
def manual(*v,**kw):
    print("!!!!!!!!!!!!!!",v, kw)
    redis.trigger.on.value  # type: ignore
    print("starting manual", str(redis.tigger.on.value), str(redis.tigger.on) == "on")  # type: ignore
    if str(redis.tigger.on.value) == "on" and False:  # type: ignore
        print("Running manual",v, kw)
        emit('server_update', {"data":v}, to = redis.lastSession.value)  # type: ignore
        print("done emmiting to", redis.lastSession.value )  # type: ignore
    else:
        print("....",redis.trigger.on.value, type(redis.trigger.on.value), redis.trigger.on.value == "on")  # type: ignore
        if redis.trigger.on.value == "on" or True:  # type: ignore
            print("YYYYYY")
            print("Running manual",v, kw)
            room = redis.lastSession.value  # type: ignore
            print("xxxxxxxxxxxxxxxxxxxx trying  emmiting to", room , redis.lastSession.value ) # type: ignore
            # socketio.emit('server_update', {"data":"aaaaaa"}, room = room)
            
            if True:
                # socketio.emit('server_update', {"data":v[0],"message":str(v[0])+"@@"}, to = room)
                socketio.emit('server_update', {"data":{"_value":f"Server Sent: {v[0]}","extra":{"_value":"inner_data","meta":{}}},"message":str(v[0]),"count":int(redis.count.value)}, to = room)  # type: ignore
                # socketio.emit('server_update', {"data":{"_value":message+"@","extra":{"_value":"inner_data","meta":{}}},"message":str(message)+"@@"}, room = request.sid)

            else:
                c = 0
                while(c<100):
                    socketio.emit('server_update', {"data":f"{v[0]} {c}"}, to = room)
                    time.sleep(redis.settings.delay.value)
                    c+=1
                    print("c....",c)
            # socketio.send('server_update', {"data":"cccccccccc"}, to = room)
            # socketio.call('server_update', {"data":"xxxxxxxxxxxx"}, room = room, namespace='/test')
            # socketio.send({"data":"ooooooo"},json = True, =room)
            print("done emmiting to", redis.lastSession.value ) # type: ignore
        else:
            print("XXXXXXXXXX")

redis.trigger @= lambda *v, **kw : manual(*v,**kw) # type: ignore
redis.count @= lambda *v, **kw : manualCount(*v,**kw) # type: ignore

def all(*v,**kw):
    print("ALL", v,kw)
    if v[0] is not None:
        room = redis.lastSession.value
#        socketio.emit('update_any', {'_id':v[0][0],'value':v[0][1]}, to = room)  # type: ignore
        socketio.emit('update_any', {'_id':v[0][0],'value':v[0][1]})  # type: ignore

    #socketio.emit('server_update', {"data":{"_value":f"Server Sent: {v[0]}","extra":{"_value":"inner_data","meta":{}}},"message":str(v[0]),"count":int(redis.count.value)}, to = room)  # type: ignore

redis.all @= all


if __name__ == '__main__':
    import argparse
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
    # socketio.run(app, debug=True)
    # wsgi.server(eventlet.listen(('0.0.0.0', port)), app)
