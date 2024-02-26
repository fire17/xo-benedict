
<script>
import io from 'socket.io-client';
export let socket = io('http://127.0.0.1:5000');

import { xoJS } from './xo';
export let xo = xoJS("xo", 'Awesome!');

xo.welcome = '<welcome msg>'
xo.name = '<name>'
xo.html = '<h4>Awaiting dynamic html to change, <br>meanwhile using placeholders</h4>'
xo.a.b.c = 3
// alert();
import { onMount, onDestroy } from 'svelte';
//  import io from 'socket.io-client';

  //let socket;
  let newData = '';
let newID = '';
  onMount(() => {
    // Connect to your Socket.IO server
    //socket = io('http://127.0.0.1:5000');
    //listen(socket,xo);
    // Listen for 'data' event from the server
    socket.on('update_any', msg => {
        console.log(":::::::: Updating: ", msg)
		if (msg['_id'] === "eval"){ console.log("EEEE");eval(msg['value']); 
    } else { // remove this else to save last eval in xo but you might happen to render it again
      
      xo[msg['_id']] = msg['value']
      console.log(":::::::: UPDATED! ", msg['_id'], xo[msg['value']])
      console.log(xo);
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
    body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            text-align: center;
            margin: 0;
            padding: 0;
        }
      </style>
  </head>
<body>
  {@html xo.html.toString()}
<div>
  <h1>{xo.welcome.toString()} {xo.name.toString()}!</h1>
  <table>
    <tr>
      <th>Name</th>
      <th>Value / Render</th>
    </tr>
    <tr><td><h4>newData</h4></td> <td>{newData}</td></tr>
    <tr><td><h4>newID</h4></td><td> {newID}:</td></tr>
    <tr><td><h4>xo: </h4></td><td>{xo.toString()}:</td></tr>
    <tr><td><h4>xo.a.b.c: </h4></td><td>{@html xo.a.b.c.toString()}</td></tr>
</table>
  <!-- <h4><div>newData: {newData}</div></h4>
  <h4><div>newID: {newID}:</div></h4>
  <h4><div>xo: {xo.toString()}:</div></h4>
  <h4><div>xo.a.b.c: {@html xo.a.b.c.toString()}</div></h4> -->
</div>
<dynamic>
</dynamic>
</body>
