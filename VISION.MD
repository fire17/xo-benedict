
# xo()
#### (stands for xobject or expando obj)
## designed to be the primitive foundation for many advanced applications

It's basically a wrapper around an expando but adds a default `value` key for each dict
which means that it can keep holding children, even after it has been set, or re-set

Another thing it does is exposes and runs `_onchange_` and `_subscribe_` whenever a value changes, which means you can hook anything into it, making it super easy to create more advanced objects like:


```
# For Users
	xoGMoE, xoMagicLLight, xoAkeyo, xoEmployee, xoDelivery, xoStore 

# Frameworks For Developers
 		xoApps, LOP, xoAI, xoProjects, IFTAI
Basics: <xo>, <xoBench>, <xoDecorator>, <xoDeque>, <xoBranch> <xoMixo>
Special: <xoJS>, <xoCLI>, <xoMagicCLI> <xoDot> <xoMagic> <xApps>  
Advanced [yet easy]: <xoRedis> <xoMicro> <xoServer> <xoAPI> <xoMetric> <xoGraphana> <xoTrace> <xoLOP>
AI Basics: <xoAtom> <xoConv> <xoMemory+RAG> <xoLib> <xoResearcher> <xoLibAI> <xoAIxoCode>
AI Advanced: <xoAI> <xoAider> <xoJarvis> <xoEmployee> <xoStore> <xoJam> <xoDJ> <xoMagicLLight>
Utils: <xoFiles> <xoUsers> <xoAuth> <xoEnc> <xoDB> <xoEvents+watchdog[T,sys,wa,email,3rd,anyXo,]> <xoLinks/xoShorts> <xoThumbs> <xoDesign> <xoGit> 
Hooks: <xoCLI> <xoWeb> <xoWhatsapp> <xoTelegram> <xoDiscord> <xoSlack> <xoZoxide>
Network: <xoP2P> <xoZMQ> <xoMQTT> <xoFreeDNS> <xoVPCloud/xoDeploy> 
Magic: <xoGen> <xoMusic> <xoNLP> <xoeMotion-self/media> <xoVision>
Freedom: <xoFreeAPI> 
```

##### [Examples Below]

### - xoRedis - realtime synced objects

    - auto saves every key by id & value
    - listens/publishes on changes
    - easy as using a dictionary or object
    - syncs in real time across processes! **(as promised in the issue)**
    - use Upstach or another Web Exposed Redis Server for multiprocessing across Networks!

### - xoServer[ZMQ] - call functions from other services

    - uses zero to create a request/response server, which allows for multiprocess function calls with high performance
    - decorate functions to easily expose them to other processes
        # programA.py
        @public.api.img.gen
        def image_generation(prompt, style="4k realistic")
                ... 
    - call it from another process! 
        # programB.py
        image = myxo.api.img.gen("A beautiful sunrise", style="vibrant colorful")
    - your dict/obj turned into an easy api

### - xoBranch - Multiverese object, changeing a value creates a new branch (in dict/in reality)

    - setting `xo.a.b.c = 'new value'` will not overwrite any value in `c` instead it will save it to `c[1]`
    - use `xo.a.b[3].c[1] = 'xxx'` to explicitly edit a value in branch[id] (overwrites)
    - entire history tree is preserved, navigate and move the current branch,
    - good for easy versioning, edits, ctrl+z/y branched mechanism, ai conversations with edits
    - xoBranch(xoRedis) makes it persistant and realtime multiprocessed dictionary

### - xoJS - reatime sync with JS<>Python

    - DOM <- JS <-> PY -> DB    :    synced objects 
    - change a value in the BE - see it immediately change in the front end!
    - change a value in the FE - get it immediately in the BE and decide how to deal with it
    - beautiful object syntax, expandoJS, easy as pie link to xoServer[FastAPI/other]

### - xoAtom - atomic ai object  (wip)

    - a small agentic object with special capabilites, (wraps a model/multi-model/multi-modal)
    - function calling for any function inside itself 
    - user.chat memory persistance, branching support & navigation, included feedback, stars, bookmarks and more
        - auto improve its own prompts, benchmark variations (based on human/ai self-feedback pipeline)
    - self reflective - meaning that its prompts (system, user, and agent) are dynamic - auto formatted with data inside it
     - able to set (all/subset) of internal or external attributes
     - cached & persistant adaptive function/skill library,
         - doesnt need to generate code it already wrote, can just call it
         - can expand it's library and improve it (like Voyager)
         - can share library with other agents
     - easy api & frontend with xoServer/REST/socket/Embeded/MagicLLight/whatsapp/etc (streaming included)
     - seemless agent-to-agent conv
     - uses OpenRouter to compress pipeline and skip llm calls where possible, adaptive retroactive
         - for example it will call a strong model to produce code, but a weak model to call it (to enter params appropriately)
     - easyRAG coming soon - common files lookup, import oai and other's history, your youtube comments, etc
     - GMoE - Global Mixture of Experts (Top Level MoE with all agents in the world, decentralized)
     - 3Party apis, web researcher, aider text-code, open-interpreter computer control, and other ai/non-ai tools
     - Many more from the AI Bingo

#### More Special objects coming soon, see [Vision & xoObjects page](https://github.com/fire17/xo-benedict/blob/xo1/VISION.md) for the full list (wip)<br>[currently on branch `xo1`]

## Examples

#### # Basic with **benedict**

```
>>> from benedict import benedict
>>> ben = benedict(keyattr_dynamic=True)
>>> ben.a = 1
>>> ben.a.b = 2
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'int' object has no attribute 'b'
```

#### # Basic with **xo**

```
>>> from xo import xoBenedict
>>> xo = xoBenedict()
>>> xo.a.b.c = 3
>>> xo.a.b.c.d.e = "Hello Fabio :)"
>>> xo.show()
xoBenedict =
    xoBenedict.a =
        xoBenedict.a.b =
            xoBenedict.a.b.c = 3
                xoBenedict.a.b.c.d =
                    xoBenedict.a.b.c.d.e = 'Hello Fabio :)'
>>> xo
{"a": {"b": {"c": {"value": 3, "d": {"e": 'Hello Fabio :)'}}}}}
```

#### # inheritance and `_onchange_` hook

```
>>> class Foo(xoRedis):
>>>     def _onchange_(self, id, value, *args, **kwargs):
>>>         if isinstance(value, int):
>>>             changedValue = value * 10
>>>             self.meta.event = ["adding metadata and changing value"]
>>>         return value
>>> 
>>> foo = Foo()
>>> foo.test.a = 5
>>> foo
{"test" : {"a" : {"value" : 50, "meta" : {"event": ["adding metadata and changing value"]}}}}
```

#### # subscribe to value change hook     (using `xo.bar @= foo` aka `__imatmul__`)

```
# subscribe to any key with any function
>>> xo.bar @= lambda v, *a, **kw: print(f"::: Bar ::: {kw['_id']} changed to {v} with params {a}, {kw}") 
::: Subscribed to xo.bar
>>> xo.bar = 100
::: Bar ::: xo.bar changed to 100 with params [], { '_id' : 'xo.bar' }
```

#### xoRedis - local/upstash - 2 processes side by side view

#### xoBranch - editing and navigating object's history

#### Rich Support - xoRedis, xoBranch, and all other xo's

#### xoJS - py<>js realtime objects

#### xoAtom - run & orchestrate dynamic ai agents

```
# basic
>>> # no need for templates, and passing keys, 
>>> atom.system.default = "Always start by greeting the customer to {business.name}. use their name if available "
>>> atom.business.name = "Ace's Beers"
>>> atom.users['user1'].name = "Fabio" 
>>> atom.chat("Hi", user="fabio", streaming=True)
"Hi Fabio welcome back to Ace's Beers, how can we help you today? :) the ususal?"
```

```
will edit to add more code & screenshots soon
```

i still need to refactor, cleanup, publish to pip, write/gen tests, docs, move off of benedic[all] as it has a cold-start, etc
but i feel like it's stable enough for me to present,
