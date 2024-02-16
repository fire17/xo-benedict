'''

import sys
import dis
import re

class SelfNamed:
	def __init__(self):
		cur_frame = sys._getframe(1)
		if cur_frame.f_code.co_name == '<module>':
			instructions = dis.get_instructions(cur_frame.f_code)
			instructions_str = "".join(map(str, instructions))
			match = re.search(r"STORE_NAME.*argval='(\w+)'", instructions_str)
			if match:
				self._name = match.group(1)
			else:
				print("No match found!")
		else:
			pass
			#... rest of logic


abc = SelfNamed()
print(abc._name)









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
			match = re.search(r"STORE_NAME.*argval='(\w+)'", instructions_str)
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
import inspect
import dis
import re

class SelfNamed:
	def __init__(self):
		caller_frame = inspect.currentframe().f_back
		caller_name = caller_frame.f_globals['__name__']
		
		if caller_name == '__main__':
			# In a Python script
			instructions = dis.get_instructions(caller_frame.f_code)
			instructions_str = "".join(map(str, instructions))
			print("Instructions:")
			print(instructions_str)
			match = re.search(r"STORE_NAME.*argval=['\"](\w+)['\"]", instructions_str)
			if match:
				self._name = match.group(1)
			else:
				print("No match found!")
		else:
			# In an interpreter or Jupyter Notebook
			# Get the variable name from the local variables of the calling frame
			local_vars = caller_frame.f_locals
			for var_name, var_value in local_vars.items():
				if var_value is self:
					self._name = var_name
					break
			else:
				print('Failed to determine the variable name.')

# Test the class
abc = SelfNamed()
print(abc._name)
'''