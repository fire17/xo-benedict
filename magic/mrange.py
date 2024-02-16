import inspect

# Not working from interpreter

class MagicRange:
	def __init__(self, count, names= None):
		self.count = count
		self.current = 0
		self.names = names

	def __iter__(self):
		return self

	def __next__(self):
		if self.current >= self.count:
			raise StopIteration
		
		if self.names:
			res = self.names[self.current].strip()
			self.current += 1
			return res
			
		self.current += 1
		return self.current

def magicRange():
	# Get the count of variables on the left side of the assignment
	caller_frame = inspect.currentframe().f_back
	caller_frame_info = inspect.getframeinfo(caller_frame)
	code = caller_frame_info.code_context[0].strip()
	count = len(code.split("=")[0].strip().split(","))
	if count < 1:
		raise ValueError("Must have at least one variable to unpack")
	elif count ==1:
		return 1
	return MagicRange(count, names = code.split("=")[0].strip().split(","))





a, b, c, d = magicRange()
print(a, b, c, d)  # returns 1, 2, 3, 4
# Test cases
abc = magicRange()
print(abc)  # returns 1

x, y = magicRange()
print(x, y)  # returns 1, 2

