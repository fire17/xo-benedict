// since there's no dynamic data here, we can prerender
// it so that it gets served as a static asset in production
// export const prerender = true;



class expando{
	constructor(namespace, value) {
    this._name = namespace;
    this._value = value;
  }

  toString() {
    return `Namespace: ${this._name}, Value: ${this._value}`;
  }
  get(target, name) {
    return `Value for attribute ${target} ${name}`
  };
}
function displayNestedProxy(proxy) {
  if (typeof proxy !== 'object' || proxy === null) {
    // If it's not an object or null, just return it
    return proxy;
  }

  const result = {};
  for (let key of Object.keys(proxy)) {
	  if (key !== 'str' && key !== "_name" && key !== "_parent" && key !== "run_once" && key !== "_value"){
		  console.log(key)
	  result[key] = displayNestedProxy(proxy[key]);}
  }
  return result;
}
function proxyToString(proxy) {
  if (typeof proxy !== 'object' || proxy === null) {
	  //if ( proxy === null){ return JSON.stringify("");}
    return JSON.stringify(proxy);
  }

  let result = '{';
  const keys = Object.keys(proxy);
  
	let found = []
  keys.forEach((key, index) => {
	  if (key !== 'str' && key !== "_name" && key !== "_parent" && key !== "run_once" && key !== "toString"){

    const value = proxy[key];
	let k = `${JSON.stringify(key)}`
	const v = `${proxyToString(value)}`;
	if (v !== 'null' && v != "{}" && v != ""){
		if (k === '"_value"'){k = "value"}
		result += `${k}: ${v}`;
		found.push(k)
		if (index < keys.length - 1) {
		  result += ', ';
		  }}
		 
	  }
  });
  if (found.length === 1 && (found[0] === '"_value"' || found[0] === "value")) {
	  	console.log("YYY",found)

        return proxy["_value"];
    }
	console.log("F",found.length,found)
  result += '}';
  if (result === "{}"){ return ""}
  return result;
}

export function _exp(_name = "", _value=null, _parent = null){
  	let payload = {"_name":_name}
  	if (_value != null){
      payload["_value"]=_value
    }
	let x = new Proxy({"_name":_name,"_parent":_parent, "_value":_value}, handler);
	x._name = _name;
	x._value = _value;
	x.str = function str(){    return proxyToString(x)}
	x.toString = function toString(){    return proxyToString(x)}
	
	//x.str2 = function str(){    return Object.toString(Object.keys(displayNestedProxy(x))) + '\n'+Object.toString(x.values)}

	//x.strog = function str(){    return `Namespace: ${x._name}, Value: ${x._value}, Keys ${Object.keys(x)}`; }

	return x
}
let handler = {
  apply(target, name, data){
    return target._name+"/"+name+"!!!!!!!!!!!!!!!!!!!!!!!"
    console.log("@@@@@@@@@@@@@@",target,name,data)
    target[name] = data
     console.log("@@@ apply",target)

    return target
    
  },
  toString(t) {
    return `Namespace: ${t._name}, Value: ${t._value}`;
  },
  set(target, name, data) {
    const spc = {"toString":1,"_value":1,"_name":1,"toJSON":1,"nodeType":1,"id":1,"className":1,"nodeName":1,"parentNode":1,"currentStyle":1,"outerHTML":1,"window":1,"length":1, "str":1};

    if (name in spc) {
        return Reflect.set(target, name, data);
    }

    const keys = name.split('.');
    let currentTarget = target;
    for (let i = 0; i < keys.length - 1; i++) {
        if (!(keys[i] in currentTarget)) {
            currentTarget[keys[i]] = {};
        }
        currentTarget = currentTarget[keys[i]];
    }

    const finalKey = keys[keys.length - 1];
    if (finalKey in currentTarget) {
        currentTarget[finalKey]._value = data;
        return currentTarget[finalKey]._value;
    } else {
        currentTarget[finalKey] = _exp(target._name + "/" + name, data, target);
        return currentTarget[finalKey]._value;
    }
},
  get(target, name, reciever) {
    
    if (typeof target[name] === 'function') {
      //return target[name].bind(target);
      return target[name];

    }

    
    if (name in target){
      if (target[name] != null && typeof target[name]._value === 'function') {
        //return target[name]._value.bind(target);
        //return target[name]._value;

      }
      return target[name]
    }
    
    //return Reflect.get(...arguments);
    // console.log("..........2....",name)
    let spc = {"_value":1,"_name":1,"toJSON":1,"nodeType":1,"id":1,"className":1
               ,"nodeName":1,"parentNode":1,"currentStyle":1,"outerHTML":1, 
              "window":1,"length":1}
    if (name in spc)
    {
       return Reflect.get(target, name, reciever)
    }
    else{ 
      // target[name] = exp(target._name+"/"+name,null,parent=target)
      target[name] = _exp(target._name+"/"+name,null,target)
        }
  
    
    return target[name]
    return `Value for attribute ${target} ${name}`
  },
  
}
export let xoJS = _exp

import io from 'socket.io-client';
// export let _io = io
//export let socket = io('http://127.0.0.1:5000');

//import { _exp } from './xo';
/*
export let _xo = _exp("xo", 'Awesome!');
export let xo = _xo;
export let newData = '';
export let newID = '';
*/
// Listen for 'data' event from the server
export let listen = (socket,xo)=>{socket.on('update_any', msg => {
  console.log(":::::::: Updating: ", msg)
    xo[msg['_id']] = msg['value']
    console.log(":::::::: UPDATED! ", msg['_id'], xo[msg['value']])
    console.log(xo);
  newData = msg['value'];
  newID = msg['_id'];
});}
/*

  import { onMount, onDestroy } from 'svelte';
//  import io from 'socket.io-client';

  //let socket;
  onMount(() => {
    // Connect to your Socket.IO server

  });
  
  //// Don't forget to disconnect from the socket when component is destroyed
  //onDestroy(() => {
  //  socket.disconnect();
  //});

*/

// let xo = exp("namespace", "Awesome!")
// export const _xo = exp("namespace", "Awesome!")
// export let xo = _exp("svelte", "Awesome!")
// let xo = _exp("xo", "Awesome!")
// // // export let xo = exp("svelte", "Awesome!");


// // console.log('.......')
// // // let x = new Proxy({}, expando);
// console.log(xo); // produces message: "Value of attribute 'lskdjoau'"

// // // console.log(x.lskdjoau); // produces message: "Value of attribute 'lskdjoau'"
// xo.a = 3
// xo.a.b.c.d.e.f.g.h = 3
// xo.a.b.c.d.e = () => {return "EEEEEEEEEEEEEEEEEEE"}
// xo.a.b.c = () => {return "CCCCCCCCCCCCC"}


// console.log(xo); // produces message: "Value of attribute 'lskdjoau'"
// console.log(xo._name); // produces message: "Value of attribute 'lskdjoau'"
// console.log(xo.a.b.c._value()); // produces message: "Value of attribute 'lskdjoau'"
// console.log(xo.a.b.c.d.e._value()); // produces message: "Value of attribute 'lskdjoau'"
// console.log(xo.a.b.c.d.e.f.g.h._value); // produces message: "Value of attribute 'lskdjoau'"
// // console.log(xo.a.b.c.d.e.f.g.h); // produces message: "Value of attribute 'lskdjoau'"
// // export let _xo=xo
