# magic.py
'''
# if False: #good for interpreter
import sys
import dis
import re
import __main__
import inspect

def is_interactive():
	return not bool(getattr(__main__, '__file__', False))


class selfName:
	def __init__(self):
		cur_frame = sys._getframe(1)
		instructions = dis.get_instructions(cur_frame.f_code)
		instructions_str = "".join(map(str, instructions))
		print(instructions_str)
		if is_interactive():
			for test in ["STORE_NAME", "STORE_FAST","LOAD_FAST", ]:
				match = re.search(rf"{test}.*argval='(\w+)'", instructions_str)
				if match:
					print("!!!!!!!!!!",match.group(1))
					return 
					self._name = match.group(1)
				else:
					print("No match found!") 
		else:
			print("-------------NON INTERACTIVE--------------")
# class MagicGetLine:
#     @staticmethod
#     def get_line():
			# Get the caller's frame
			frame = inspect.currentframe().f_back
			# Get the source code of the line where the caller is
			line = inspect.getframeinfo(frame).code_context[0].strip()
			print("!!!!!!!!!!!",line.split("=")[0].strip())
			return


def main():
	selfNamed1 = selfName()
	selfNamedX = selfName()
	selfNamedABC = selfName()
	abc = selfName()  
	print(selfNamed1, selfNamedX, selfNamedABC,abc)
	print()
	print(abc)


main()
'''



import sys
import dis
import re

import inspect
import os

class MagicSelfNamed:
	count = 0
	icount = 0
	lastline = None
	interpreter_script = None
	def __str__(self):
		return str(self._name)
	def __repr__(self):
		return self.__str__()
	# @staticmethod
	# def get_line():
	def __init__(self, *a,**kw):
		self._name = "NONE"
		# Check if running in a file or the interpreter
		if inspect.currentframe().f_back is not None:
			# Get the caller's frame
			try:
				frame = inspect.currentframe().f_back
				# Get the source code of the line where the caller is
				line = inspect.getframeinfo(frame).code_context[0].strip()
				print("+++++++++++",frame)
				res = line.split("=")[0].strip()
				if MagicSelfNamed.lastline != res:
					MagicSelfNamed.lastline = res
					MagicSelfNamed.count = 0
				# print(res,MagicGetLine.count)
				if "," in res:
					res = res.split(",")[MagicSelfNamed.count].strip()
					MagicSelfNamed.count+=1
				else:
					MagicSelfNamed.count = 0
				self._name = res
				# return res
			except:
				print("IIIIIIIIIIIIIIII")
				for i in range(10):
					cur_frame = sys._getframe(i)        
					if cur_frame.f_code.co_name == '<module>':
						instructions = dis.get_instructions(cur_frame.f_code)
						instructions_str = "".join(map(str, instructions))
						matches = re.findall(r"STORE_NAME.*?argval='(.*?)'", instructions_str)
						if instructions_str != MagicSelfNamed.interpreter_script:
							MagicSelfNamed.icounter = 0
							MagicSelfNamed.interpreter_script = instructions_str
						current = matches[MagicSelfNamed.icounter]
						MagicSelfNamed.icounter+=1
						if current!= None:
							self._name = current
							return
		else:
			print("iiiiiiiiiiiiiiiiiiiiiiii")
			# When running in the interpreter, use readline to get the last line
			histfile = os.path.join(os.path.expanduser("~"), ".python_history")
			if os.path.exists(histfile):
				with open(histfile, "r") as f:
					lines = f.readlines()
				res = lines[-1].strip().split("=")[0].strip()
				if "," in res:
					res = res.split(",")[MagicSelfNamed.count].strip()
					MagicSelfNamed.count+=1
				else:
					MagicSelfNamed.count = 0
				return res
			else:
				print("No history file found. Ensure you've used the interpreter with history enabled.")
				return None


def main():
	selfNamed1 = MagicSelfNamed()#.get_line()
	selfNamedX = MagicSelfNamed()#.get_line()
	selfNamedABC = MagicSelfNamed()#.get_line()
	print(selfNamed1, selfNamedX, selfNamedABC)

main()

abc =  MagicSelfNamed()#.get_line()
print(abc)
xxx, yyy = MagicSelfNamed(), MagicSelfNamed()#.get_line(), MagicGetLine.get_line()
print(xxx, yyy)
x, y, z= MagicSelfNamed(), MagicSelfNamed(), MagicSelfNamed()#.get_line(), MagicGetLine.get_line()
# x, y, z = MagicGetLine.get_line(), MagicGetLine.get_line(), MagicGetLine.get_line()
print(x, y, z)


abc = MagicSelfNamed()
print(abc._name)


def inner3():
	xxx = MagicSelfNamed()
	def x(a):
		return a
	yyyyy = MagicSelfNamed()
	zzz =  MagicSelfNamed()
	return xxx, yyyyy, zzz, 4444

x, y, z, O = inner3()
print(x, y, z, O)



if __name__ == "__main__":
	main()
