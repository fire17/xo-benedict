import sys
import dis
import re

# magicInterpreterAllLevels

class SelfNamed:
	counter = 0
	instructions_str = None
	_name = None
	def __str__(self):
		return str(self._name)
	def __repr__(self) -> str:
		return self.__str__()
	def __init__(self):
		for i in range(10):
			cur_frame = sys._getframe(i)        
			if cur_frame.f_code.co_name == '<module>':
				instructions = dis.get_instructions(cur_frame.f_code)
				instructions_str = "".join(map(str, instructions))
				matches = re.findall(r"STORE_NAME.*?argval='(.*?)'", instructions_str)
				if instructions_str != SelfNamed.instructions_str:
					SelfNamed.counter = 0
					SelfNamed.instructions_str = instructions_str
				current = matches[SelfNamed.counter]
				SelfNamed.counter+=1
				if current!= None:
					self._name = current
					return
				# if match:
				# 	self._name = match
				# else:
				# 	print("No match found!")
			else:
				pass
			#... rest of logic


abc = SelfNamed()
print(abc._name)


def inner3():
	xxx = SelfNamed()
	def x(a):
		return a
	yyyyy = SelfNamed()
	return xxx, yyyyy, SelfNamed()

x, y, z = inner3()
print(x, y, z)
