## TODO

1. cleanup

2. new xo(benedict) based on latest benedic
    2.b new xo(beneidct-lean) based on benedict on pypi

3. validate inherent behaviors, add _id, redis
    3.b new xo(benedict-flat) for performance

4. multi inheritance, redis, vis_performance, flask-html, socketio
    4.b xo values to graphana, graphana inputs to xo funcs

5. micro-service app framework
    5.b connect xo-js to xo-py
    5.c x-state integration LOP

6. xo-ai agent framework
    - atom agent buildblocks with special characteristics
    - stream to chat / wa / custom interface



dev blocks:
- super dynamic object with syntax sugar
- data persistance & realtime states
- high performance monitoring
- multi-service coordination
- self improving and growing
- easy to push to pip, pypi advanced pkgmanager, easy deployer + poetry
- cross-stack events and data pipes
- web routing and api
- autodocs, multi-lang support
- beautiful cli, easy run after install, 
- user management, permisssions, roles, authentications
- abstract infastructure, plan, mock, simulate, itterate
- 3rd party integrations
- easy abstractions, DAL,
- admin & user dashboards, CMS, ORM, 
- security
- ai batteries included
- easy community -> polar.sh + discord



better python:
- expanable syntax
- auto venv, auto dependencies
- easy deployer

Extras:

### #codec xo (first line in the file) https://blog.veitheller.de/A_Bad_Idea.html

### Meta Path Import external files at runtime, https://yyc.solvcon.net/en/latest/nsd/12advpy/advpy.html#meta-path-finder

### DXOS Echo for python to js realtime bind




### String replace match whole word
'''
replacements = {'the':'a',
                'this':'that'}

def replace(match):
    return replacements[match.group(0)]

# notice that the 'this' in 'thistle' is not matched

print re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in replacements),
        replace, 'the cat has this thistle.')
'''

# super-py logs & func monitor https://github.com/Marthe-M/SuperPy https://pypi.org/project/super-py/



AIDER PLANS:

lvl 0 - zeroshot changes (with current context)
lvl 1 - stackoverflow, google, look for solutions
lvl 2 - Github search

lvl v1 - aider + tldraw , xo
lvl v2 - mission board, LOP


Hi everyone, just found out about Polar, looks amazing
what really stood out to me is that I found you out after creating an issue a repo
and somehow your message "Fund this issue" was automatically added
So I can see you have some really well designed integrations to say the least

Got some questions and suggestions,
After joining, the only place where i can explore is by choosing people from the Highlighted Creators section, but even following them, I can't see who they are following.
So beside the social-subscriber system...
I would imagine, a github style explorer, where I can see all of the projects with open rewards, globally,
and be able to search queries (ie "ai python", etc) and filter by topics, stacks, reponames, trending, stars, reward count, total open reward, etc
This way we will be able to stay with current tide of oss
and easily find new bounties to solve. Any ideas when this will be possible?

Currently I cant wait to explore all the issues with open rewards,
but not sure where to find them, can anyone help? Thx and all the best!



[x] poetry 
[ ] dxos echo
[ ] super-py


url = 'https://www.google.com/url?q=http://xn--vnx.io&source=gmail&ust=1707493827421000&usg=AOvVaw23x5jRb3D6jX_KKSFUdzBB'

obfuscate_url = lambda url, n=2, start="?q=": (url.split(start)[0]+start+"://".join([ "%"+"%".join([text.encode().hex()[i:i+2] for i in range(0, len(text.encode().hex()), 2)]) for text in start.join(("&".join(url.split("&")[:-n]) if n>0 else url).split(start)[1:]).split("://") ]) + "&"+"&".join( url.split("&")[-n:] if n>0 else [] )).replace("%26","&").replace("%2e",".").replace("%3d","=").replace("%3f","?").replace("%2f","/")

import re

reveal_url = lambda url: re.sub(r'%([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), url)

obf = obfuscate_url(url,0, start=".com/")
print(obf)
print(":::::::::::")
print(reveal_url(obf))




# Turn repo into github pages
export GHT=<github token>
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GHT" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/fire17/xo-benedict/pages \
  -d '{"cname":"xo.akeyo.io", "source":{"branch":"main","path":"/"}}'
### UPDATE EXISTING
curl -L \                                   3:59:19
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GHT" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/fire17/xo-benedict/pages \
  -d '{"cname":"xo.akeyo.io", "source":{"branch":"main","path":"/docs"}}'

