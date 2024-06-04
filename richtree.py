from colorama import Fore as color
from rich import print as rprint
from rich.tree import Tree
from rich.text import Text
from .emojis import d as emojis
COMMON_KEYS_EMOJIS = {
	"email": "📧",
	"id": "🆔",
	"Settings": "⚙️",
	"language": "🌐"
}

COMMON_VALUES_EMOJIS = {
	"Default": "🔵",
	"Purple": "💜",
	"eng": "🇬🇧"
}
bpython = False
bpython = True
def tree(o, noplace=False, bpython=True, _type=None):
	rprint(display_xobranch(o,noplace=noplace) )
	# rprint(,end="")
	if not bpython: print(color.WHITE,end="")

def treeXoBranch(o, noplace=False, bpython=True, _type=None):
	return rprint(display_xobranch(o,noplace=noplace) )

def treeXo(o, noplace=False, bpython=True, _type=None):
	return rprint(display_objectOG(o))
	# return rprint(display_xobranch(o,noplace=noplace) )


import ast
# rprint(color.RESET)

def display_xobranch(obj, _tree=None, current = True, noplace=False, hideTop=True):
	if _tree is None:
		# print()
		if not hideTop:
			_tree = Tree("[bold deep_pink1]"+obj._id.split("[")[0] +"[/bold deep_pink1] : "+'[bold hot_pink]'+obj.__str__(noplace=noplace)+'[/bold hot_pink]'  if hasattr(obj,"_id") else (obj.__name__ if hasattr(obj, "__name__") else "Object"), guide_style="bold bright_blue")
		else:
			_tree = Tree("[bold deep_pink1]"+obj._id.split("[")[0] +"[/bold deep_pink1]", guide_style="bold bright_blue")
	# target = [b for b in obj._branch] if hasattr(obj,"_branch") and len(obj._branch)>0 else [obj]
	# print()
	brc = 0
	if len(obj._branch) <= 1 and _tree == None:
		return display_xobranch(obj[0],)
	for br in obj.branches():
		# print("TTTTTTTTTTT",type(br))
		# for key, value in obj.items():
		items = br.items()
		if items is not None:
			myplace = "("+str(brc+1)+"/"+str(len(obj.branches()))+")"
			isCurrent = current and myplace == obj.place().replace("[","(").replace("]",")")
			# key, value = br._id.split(".")[-1]+" "+myplace+" "+obj.place() , br
			key, value = br._id.split(".")[-1] , br
			node_text = f"{color.LIGHTYELLOW_EX+str(key)}"+f"{' : ' if 'value' in value else ''}"+f"{''+color.MAGENTA if 'value' in value and isinstance(value['value'], str) else ''+color.CYAN}"+f"{repr(value['value']) if 'value' in value else ''}"
			# if isCurrent: node_text = "*[bold]"+node_text
			icon = get_emoji(key,value.value if "value" in value else value)
			branch = _tree.add(f"{'[bold]' if isCurrent else ''}{'[magenta]' if 'value' in value and isinstance(value['value'], str) else '[yellow]'}{'*' if isCurrent else ''}{icon if icon else 'open_file_folder'} {node_text}")
			# branch = _tree.add("xxxxxxxxxx")

			for key, value in items:
				# print("ttttttttt",key)
				# print(f"::: K,V {key}:{value}")
				if key == "value":
					continue  # Skip displaying the "value" key
				if isinstance(value, dict):
					# print("WWWWWWW",key, type(value) )
					# node_text = format_node_text(key, value)
					# node_text = f"[bold]{color.LIGHTYELLOW_EX+str(key)}"+f"{' : '+color.MAGENTA if value.get('value') and isinstance(value['value'], str) else ' : '+color.CYAN}"+f"{repr(value['value']) if 'value' in value else ''}"
					node_text = f"xx [bold]{color.LIGHTYELLOW_EX+str(key)}"+f"{' : ' if 'value' in value else ''}"+f"{''+color.MAGENTA if 'value' in value and isinstance(value['value'], str) else ''+color.CYAN}"+f"{repr(value['value']) if 'value' in value else ''}"
					# print("@@@@@@",key,type(value),node_text, )
					icon = get_emoji(key,value)
					# branch = tree.add(f"[bold magenta]{icon if icon else 'open_file_folder'}: {node_text}")

					# branch2 = branch.add(f"{'[bold magenta]' if 'value' in value and isinstance(value['value'], str) else '[bold yellow]'}{icon if icon else 'open_file_folder'} {node_text}")
					# branch2 = branch.add(f"{'[bold magenta]' if 'value' in value and isinstance(value['value'], str) else '[bold yellow]'}{icon if icon else 'open_file_folder'} {node_text}")
					# branch2 = branch.add(f"{'[bold magenta]' if 'value' in value and isinstance(value['value'], str) else '[bold yellow]'}{icon if icon else 'open_file_folder'} {node_text}")
					display_xobranch(value, branch, current = isCurrent)
				else:
					print("xxxxWWWWWWW",key,type(value) )
					node_text = f"{key} : {color.MAGENTA if isinstance(value, str) else color.LIGHTCYAN_EX}{repr(value)}"
					icon = get_emoji(key,value)
					# branch = tree.add(f"[bold magenta]{icon if icon else 'open_file_folder'}: {node_text}")
					branch2 = branch.add(f"{icon if icon else 'open_file_folder'} {node_text}")
					# node_text = format_node_text(key, value)
					# tree.add(node_text)
		else:
			print(f"XXXXXXXXXXXX items {br} is None",)
		brc += 1
	return _tree

def display_objectOG(obj, _tree=None, hideTop=True):
	if _tree is None:
		# print()
		if not hideTop:
			_tree = Tree("[bold deep_pink1]"+obj._id.split("[")[0] +"[/bold deep_pink1] : "+'[bold hot_pink]'+obj.__str__(noplace=noplace)+'[/bold hot_pink]'  if hasattr(obj,"_id") else (obj.__name__ if hasattr(obj, "__name__") else "Object"), guide_style="bold bright_blue")
		else:
			_tree = Tree("[bold deep_pink1]"+obj._id.split("[")[0] +"[/bold deep_pink1]", guide_style="bold bright_blue")
	# if _tree is None:
	# 	_tree = Tree(obj._id if hasattr(obj,"_id") else (obj.__name__ if hasattr(obj, "__name__") else "Object"), guide_style="bold bright_blue")
	target = [b for b in obj._branch] if hasattr(obj,"_branch") and len(obj._branch)>0 else [obj]
	# print()
	for t in target:
		# print("TTTTTTTTTTT",type(t))
		# for key, value in obj.items():
		items = t.items()
		if items is not None:
			for key, value in items:
				# print("ttttttttt",key)
				# print(f"::: K,V {key}:{value}")
				if key == "value":
					continue  # Skip displaying the "value" key
				if isinstance(value, dict):
					# print("WWWWWWW",key, type(value) )
					# node_text = format_node_text(key, value)
					# node_text = f"[bold]{color.LIGHTYELLOW_EX+str(key)}"+f"{' : '+color.MAGENTA if value.get('value') and isinstance(value['value'], str) else ' : '+color.CYAN}"+f"{repr(value['value']) if 'value' in value else ''}"
					# node_text = f"[bold]{color.LIGHTYELLOW_EX+str(key)}"+f"{' : '+color.MAGENTA if 'value' in value and isinstance(value['value'], str) else ' : '+color.CYAN}"+f"{repr(value['value']) if 'value' in value else ''}"
					node_text = f"[bold]{color.LIGHTYELLOW_EX+str(key)}"+f"{' : ' if 'value' in value else ''}"+f"{''+color.MAGENTA if 'value' in value and isinstance(value['value'], str) else ''+color.CYAN}"+f"{repr(value['value']) if 'value' in value else ''}"
					# print("@@@@@@",key,type(value),node_text, )
					# icon = get_emoji(key,value)
					icon = get_emoji(key,value.value if "value" in value else value)
					# branch = tree.add(f"[bold magenta]{icon if icon else 'open_file_folder'}: {node_text}")
					branch = _tree.add(f"{'[bold magenta]' if 'value' in value and isinstance(value['value'], str) else '[bold yellow]'}{icon if icon else 'open_file_folder'} {node_text}")
					display_objectOG(value, branch)
				else:
					# print("xxxxWWWWWWW",key,type(value) )
					node_text = f"{key} : {color.MAGENTA if isinstance(value, str) else color.LIGHTCYAN_EX}{repr(value)}"
					# icon = get_emoji(key,value)
					icon = get_emoji(key,value.value if "value" in value else value)
					# branch = tree.add(f"[bold magenta]{icon if icon else 'open_file_folder'}: {node_text}")
					branch = _tree.add(f"{icon if icon else 'open_file_folder'} {node_text}")
					# node_text = format_node_text(key, value)
					# tree.add(node_text)
		else:
			pass
			# print(f"XXXXXXXXXXXX items {t} is None",)
	return _tree

def display_objectx(obj, _tree=None):
	if _tree is None:
		_tree = Tree(obj._id if hasattr(obj,"_id") else (obj.__name__ if hasattr(obj, "__name__") else "Object"), guide_style="bold bright_blue")
	# target = [b for b in obj._branch] if hasattr(obj,"_branch") and len(obj._branch)>0 else [obj]
	target= [obj]
	print()
	for t in target:
		print("TTTTTTTTTTT",type(t))
		# for key, value in obj.items():
		items = t.items()
		if items is not None:
			brcount = 0
			for br in items:
				for key, value in br.items():
					print("ttttttttt",key)
					# print(f"::: K,V {key}:{value}")
					branch = _tree
					# if isinstance(value, dict):
					#     display_object(value, branch)

					if True:
						key = key+f"[{brcount}]"
					#     continue  # Skip displaying the "value" key
						if isinstance(value, dict):
							print("WWWWWWW",key, type(value) )
							# node_text = format_node_text(key, value)
							# node_text = f"[bold]{color.LIGHTYELLOW_EX+str(key)}"+f"{' : '+color.MAGENTA if value.get('value') and isinstance(value['value'], str) else ' : '+color.CYAN}"+f"{repr(value['value']) if 'value' in value else ''}"
							node_text = f"[bold]{color.LIGHTYELLOW_EX+str(key)}"+f"{' : '+color.MAGENTA if 'value' in value and isinstance(value['value'], str) else ' : '+color.CYAN}"+f"{repr(value['value']) if 'value' in value else ''}"
							print("@@@@@@",key,type(value),node_text, )
							icon = get_emoji(key,value)
							# branch = tree.add(f"[bold magenta]{icon if icon else 'open_file_folder'}: {node_text}")
							branch = _tree.add(f"11111{'[bold magenta]' if 'value' in value and isinstance(value['value'], str) else '[bold yellow]'}{icon if icon else 'open_file_folder'} {node_text}")
							display_objectOG(value, branch)
						elif key == "value":
							print("xxxxWWWWWWW",key,type(value) )
							node_text = f"22222{key} : {color.MAGENTA if isinstance(value, str) else color.LIGHTCYAN_EX}{repr(value)}"
							icon = get_emoji(key,value)
							# branch = tree.add(f"[bold magenta]{icon if icon else 'open_file_folder'}: {node_text}")
							branch = _tree.add(f"{icon if icon else 'open_file_folder'} {node_text}")

						else:
							print("xxxxWWWWWWW",key,type(value) )
							node_text = f"{key} : {color.MAGENTA if isinstance(value, str) else color.LIGHTCYAN_EX}{repr(value)}"
							icon = get_emoji(key,value)
							# branch = tree.add(f"[bold magenta]{icon if icon else 'open_file_folder'}: {node_text}")
							branch = _tree.add(f"{icon if icon else 'open_file_folder'} {node_text}")
							# node_text = format_node_text(key, value)
						# tree.add(node_text)
				brcount +=1
		else:
			print(f"XXXXXXXXXXXX items {t} is None",)
	return _tree

def get_emoji(key, value, default = None):
	# print(f"EMOJI FOR:{key},{value}")
	return emojis[str(value).lower()] if str(value) in emojis else (emojis[str(key).lower()] if str(key).lower() in emojis  else (emojis[str(key)] if str(key) in emojis else get_emoji_type(value, default = default)))
# def format_node_text(key, value):
def format_node_text(key, value):
	emoji = get_emoji(key,value)
	return f"{emoji} {key} : {value}"


def get_emoji_type(value, default = "❓"):
	if isinstance(value, int):
		return "🔢"
	elif isinstance(value, str):
		return "📝"
	elif isinstance(value, bool):
		return "✅" if value else "❌"
	elif isinstance(value, dict):
		return "📂"
	elif isinstance(value, list):
		return "📃"
	elif isinstance(value, bytes):
		return "🔣"
	else:
		return default  # Placeholder emoji for other types


# Example object
obj = {
	"Users": {
		"Yo": {
			"value": ["abc",'Created on 18/2/24 21:01'],
			"email": 'xxx@gmail.com',
			"id": 11224427,
			"Settings": {
				"value": 'Default',
				"color": 'Purple',
				"language": 'eng'
			}
		}
	}
}

if False == "LEVEL1":
	from xoDeque import xoBranch; bx = xoBranch()
	bx.a(1).b(2).c(3); bx.a(11).b(22).c(33)
	print(bx)
	bx.show()
	bx.pr()
	bx.a.home()
	tree(bx)
if __name__=="__main__":
	from xoDeque import xoBranch; bx = xoBranch()
	rprint(display_objectOG(obj))
	if False == "LEVEL2":
		if True and not bpython: print(color.WHITE,end="")

		bx.a(1).b(1).c(1)
		# print("__________________________________________")
		bx.a(22).b(22).c(22)
		# print("__________________________________________")
		bx.a.b(333).c(333)
		# print("__________________________________________")
		# print("PRE",bx._id)
		bx.value = "XXX"
		bx.home()
		# bx.a.b.left()
		# bx.a.b.left()
		# print("POST",bx._id)
		# print("POST",bx.current()._id)
		# print("__________________________________________")
		# bx.System("System Prompt1").User("<First question>").Agent("<Agent Response 1>").User("<User Flowup 1>").Agent("<Agent Reply A>")
		# bx.System.User.Agent.User("<User EDIT Flowup!C>").Agent("<Agent SECOND Reply C>")
		# bx.end()
		# bx.show()
		# bx.pr()

		# assert bx.a.b.c == 22
		# tree(bx)
	bx.Users.Yo = ["username",'Created on 18/2/24 21:01']
	bx.Users.Yo.email = 'xxx@gmail.com'
	bx.Users.Yo.id = 11224427
	bx.Users.Yo.Settings = 'Default'
	bx.Users.Yo.Settings.color = 'Purple'
	bx.Users.Yo.Settings.language = 'eng'
	bx.tree()


	from xoDeque import xoBranch; bx = xoBranch()
	bx.System("System Prompt1").User("<First question>").Agent("<Agent Response 1>").User("<User Flowup 1>").Agent("<Agent Reply A>")
	bx.System.User.Agent.User("<User EDIT Flowup!C>").Agent("<Agent SECOND Reply C>")
	bx.tree()
	# if True and not bpython: print(color.WHITE,end="")

	# tree(bx.flatten())
obj = {
	"Users": {
		"Yo": {
			"value": ["abc",'Created on 18/2/24 21:01'],
			"email": 'xxx@gmail.com',
			"id": 11224427,
			"Settings": {
				"value": 'Default',
				"color": 'Purple',
				"language": 'eng'
			}
		}
	}
}




'''
# see nested.py

# RICH TODO:
# learn to do markdown in rich + load from file

# hide [0] if (1/1)
# hide : for empy values
# make branch into table, if condition or isTable, single, nested
# save

# invisible table borders, Side | Side , left | right, benedict | xo

#  how to align text inside colums?
# fin tree view
# add table view
# add hidden .rich and if exists, overides str it tree or table

'''
