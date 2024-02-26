
# xoJS <br> alows you to connect an xo object (state/data) between JS and python
## 1.connect and run frontend:
    - import xo [examples below]
    - choose your reactive library   (demo uses svelte)
    - use xo.keys.and.values througout your code   (they will be reactive across to python)
    - run `npm run dev` or whichever cmd you normally run to start your frontend
## 2.run JS.py
    - this will open a socket server to send (and recieve) data to clients in realtime
    - listens to changes in xo.redis and pushes updates
## 3.run your python with xo
    - ```
        from xo import FreshRedis as xoRedis
        xo = xoRedis() # you can add host, port, db, password
        xo.js.keys.and.values = 'your data is synced and reactive'
        # getting data from client coming soon```


### How to run the demo:
 - `cd freshSvelte && npm run dev`     (after installing dependencies)
    - open the site: http://localhost:5000/
 - `python3.11 JS.py`
    - socketio server should start and connect to your site
 - `python3.11 programB.py`
    - this simulates changing values and even loading completely new html to the page in realtime

### how the demo front was created:
```
npx degit sveltejs/template svelte-app
cd svelte-app
npm install svelte socket.io-client
npm install
# copy over xo.js
```
#### Example App.svelte:
```
<script>
import { onMount, onDestroy } from 'svelte';
import io from 'socket.io-client';
export let socket = io('http://127.0.0.1:5000');
import { xoJS } from './xo';
export let xo = xoJS("xo", 'Awesome!');

# setting up data in xo 
xo.welcome = '<welcome msg>'
xo.name = '<name>'
xo.html = '<h4>Awaiting dynamic html to change, <br>meanwhile using placeholders</h4>'
xo.a.b.c = 3

let newID = '';     # with these you can track the last id/value of the data that was updated
let newData = ''; 

  onMount(() => {
    // Listen for 'update_any' event from the JS.py server
    socket.on('update_any', msg => {
        let acceptJSfromServer = True # change to False to stop running new js from server and only accept new data
        if (acceptJSfromServer && msg['_id'] === "eval"){
             eval(msg['value']); 
        }
        else {
            # Set the new data into xo 
            xo[msg['_id']] = msg['value']

            console.log(":::::::: UPDATED! ", msg['_id'], xo[msg['value']], xo)
            newData = msg['value'];
            newID = msg['_id'];
            }
        });
  /*
    */
  });
  
  // Don't forget to disconnect from the socket when component is destroyed
  onDestroy(() => {
    socket.disconnect();
  });
</script>
<head>
    <style>
<!--     ....     your styles -->
    </style>
  </head>
<body>
  {@html xo.html.toString()}       <!-- render xo.html as html -->
<div>
  <h1>{xo.welcome.toString()} {xo.name.toString()}!</h1>
  <h4><div>newData: {newData}</div></h4>
  <h4><div>newID: {newID}:</div></h4>
  <h5><div>xo: {xo.toString()}:</div></h5>       <!-- display entire xo -->
  <h4><div>xo.a.b.c: {@html xo.a.b.c.toString()}</div></h4>
</div>
<dynamic>
</dynamic>
</body>
```

### Status: xoJS is a working poc [stable]

The reason its considered a poc is because frontend and js are not my strongest suites,
so fork + contribution is high encoraged, if it passes the tests, adds features, reduces complexity, increases security and benchmarks better performance than current main, it will happily be merged as the new standard.


### UPNEXT
- get data from client, id each client
- parse website with xo in js and wrap with <id=_id></id> so that in js it can be hotswapped always
- display chain of xo's as a tree, and a vertical list of current *path {'msg':{"value":'hi',"response":{"value":'hello how can i help?',"msg":"what is the time in hawaii?"}}}
- create a class xoJS(xoRedis) in JS.py that publishes every key in subspace, without xo['all']
- move to xoAtom(xoJS)
