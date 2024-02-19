from colorama import Fore as color
from rich import print as rprint
from rich.tree import Tree
from rich.text import Text
from emojis import d as emojis
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
# bpython = True
bpython = False
def tree(o):
    rprint(display_object(o))
    # rprint(,end="")
    if not bpython: print(color.WHITE,end="")
    # return display_object(o)
import ast
# rprint(color.RESET)
def display_object(obj, _tree=None):
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
                            display_object(value, branch)
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

# rprint(display_object(obj))
# if True and not bpython: print(color.WHITE,end="")


from xoDeque import xoBranch; bx = xoBranch()
bx.a(1).b(1).c(1)
print("__________________________________________")
bx.a(22).b(22).c(22)
print("__________________________________________")
bx.a.b(333).c(333)
print("__________________________________________")
print("PRE",bx._id)
bx.value = "XXX"
print("POST",bx._id)
print("POST",bx.current()._id)
print("__________________________________________")
# bx.System("System Prompt1").User("<First question>").Agent("<Agent Response 1>").User("<User Flowup 1>").Agent("<Agent Reply A>")
# bx.System.User.Agent.User("<User EDIT Flowup!C>").Agent("<Agent SECOND Reply C>")
tree(bx)
bx.show()
bx.pr()
if True and not bpython: print(color.WHITE,end="")

# tree(bx.flatten())






