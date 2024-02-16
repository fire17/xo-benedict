from ideas import import_hook

def transform(source, **kwargs):
    return source.replace("function", "lambda")

import_hook.create_hook(transform_source=transform)










class SpecialOperations(object):
	def __idollar__(self, value):
		print(f'__idollar__ called with value: {value}')
	def __iwalrus__(self, value):
		print(f'__iwalrus__ called with value: {value}')
	def __bind__(self, other):
		print(f'__bind__ called with: {self} and {other}')
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		def run(self, func):
			return self[func](self)
		def idollar(self, value):
			return run(self, "__$=__")(value)
		def iwalrus(self, value):
			return run(self, "__:=__")(value)
		def bind(self, other):
			return run(self, "__<>__")(other)
		self.__setattr__("__$=__", idollar)
		self.__setattr__("__:=__", iwalrus)
		self.__setattr__("__<>__", bind)


special_ops = SpecialOperations()
for op in ['$=', ':=', '<>']:
    setattr(SpecialOperations, f'__{op}__', getattr(special_ops, f'__{op}__'))




import ast
import builtins
import importlib.abc
import importlib.util
import sys

class SpecialSyntaxImporter(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_spec(self, fullname, path, target=None):
        spec = importlib.util.find_spec(fullname, path)
        if spec is None:
            return None
        return importlib.util.spec_from_loader(fullname, self)
    def create_module(self, spec):
        return None
    def exec_module(self, module):
        code = module.__spec__.loader.get_code(module.__spec__.name)
        tree = ast.parse(code)
        transformer = SpecialOperationTransformer()
        tree = transformer.visit(tree)
        code_object = compile(tree, filename=module.__spec__.origin, mode='exec')
        exec(code_object, module.__dict__)

class SpecialOperationTransformer(ast.NodeTransformer):
    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Lt):
            new_op = ast.Attribute(
                value=node.left,
                attr="__bind__",
                ctx=ast.Load()
            )
            args = [node.right]
            call = ast.Call(func=new_op, args=args, keywords=[])
            return ast.copy_location(call, node)
        return node

# Install the import hook
sys.meta_path.insert(0, SpecialSyntaxImporter())

# Example usage
class MyClass:
    pass

# Now you can use the custom operation <> (which is mapped to __bind__)
a = MyClass()
b = MyClass()
result = a <> b
print(result)  # Just to demonstrate that it runs without syntax error


'''
import ast
import builtins
import importlib.abc
import importlib.util
import sys
import tokenize
from io import BytesIO

class SpecialSyntaxImporter(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_spec(self, fullname, path, target=None):
        spec = importlib.util.find_spec(fullname, path)
        if spec is None:
            return None
        return importlib.util.spec_from_loader(fullname, self)
    def create_module(self, spec):
        return None
    def exec_module(self, module):
        code = module.__spec__.loader.get_code(module.__spec__.name)
        print("Original code:")
        print(code)
        transformed_code = self.transform_code(code)
        print("\nTransformed code:")
        print(transformed_code)
        code_object = compile(transformed_code, filename=module.__spec__.origin, mode='exec')
        exec(code_object, module.__dict__)
    def transform_code(self, code):
        print("\nTokenizing code...")
        tokens = tokenize.tokenize(BytesIO(code.encode('utf-8')).readline)
        transformed_tokens = []
        for toktype, tokval, _, _, _ in tokens:
            print("\nCurrent token type:", tokenize.tok_name[toktype], "Value:", repr(tokval))
            if toktype == tokenize.OP and tokval == "<" and transformed_tokens and transformed_tokens[-1][1] == "<":
                print("Replacing <> with __bind__")
                transformed_tokens.pop()
                transformed_tokens.append((tokenize.NAME, "__bind__"))
            else:
                transformed_tokens.append((toktype, tokval))
        print("\nRe-tokenizing code...")
        transformed_code = tokenize.untokenize(transformed_tokens)
        print("Transformed code:", repr(transformed_code))
        return transformed_code

# Install the import hook
sys.meta_path.insert(0, SpecialSyntaxImporter())

'''