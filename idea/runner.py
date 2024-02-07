'''
# The following import will automatically register a codec
import lambda_codec  # noqa
# from my_program import go  # noqa
# go()
# import my_program
from my_program import start
# import my_program  # noqa
# go()
start()
'''

# from special import hook, program






"""lambda_codec.py
------------------------

This codec replaces any Python identifier (token) represented by the
single Greek letter 'λ' by the corresponding string 'lambda' which is
the Python keyword.

The source is assumed to be actually encoded in utf-8.
"""

from ideas import import_hook

from ideas import custom_encoding
import token_utils



# def transform_source(source, **_kwargs):
#     """This performs a simple replacement of ``function`` by ``lambda``."""
#     new_tokens = []
#     for token in token_utils.tokenize(source):
#         # token_utils allows us to easily replace the string content
#         # of any token
#         if token == "function":
#             token.string = "lambda"
#         new_tokens.append(token)

#     return token_utils.untokenize(new_tokens)


encoding_name = "xo_encoding"




def add_hook(**_kwargs):
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(
        transform_source=transform_source,
        hook_name=__name__,  # optional
    )
    return hook


def go():
    # print("GOOOOOOO")
    custom_encoding.register_encoding(
    encoding_name=encoding_name,
    transform_source=transform_source,
    hook_name=__name__,)
    add_hook()
    # print("GOOOOOOO")


def transform_source_org(source, **_kwargs):
    """Simple transformation: replaces any single token λ by lambda.

    By defining this function, we can also make use of Ideas' console.
    """
    tokens = token_utils.tokenize(source)
    for token in tokens:
        if token == "λ":
            token.string = "lambda"
        # if token == "<>":
        #     token.string = "@"
        # if token == "$=":
        #     token.string = "@="
        if token == ":=":
            token.string = "-="
    return token_utils.untokenize(tokens)

import ast
import builtins
import importlib.abc
import importlib.util
import tokenize
import sys
from io import BytesIO


def transform_source(code, **_kwargs):
    # print("\nTokenizing code...")
    tokens = tokenize.tokenize(BytesIO(code.encode('utf-8')).readline)
    transformed_tokens = []
    for toktype, tokval, _, _, _ in tokens:
        # print("\nCurrent token type:", tokenize.tok_name[toktype], "Value:", repr(tokval))
        if toktype == tokenize.OP and tokval == "<" and transformed_tokens and transformed_tokens[-1][1] == "<":
            # print("Replacing <> with __bind__")
            transformed_tokens.pop()
            transformed_tokens.append((tokenize.NAME, "__bind__"))
        else:
            transformed_tokens.append((toktype, tokval))
    for token in tokens:
        if token == "λ":
            token.string = "lambda"
    # transformed_tokens.append(("λ","lambda"))
    # print("\nRe-tokenizing code...")
    transformed_code = tokenize.untokenize(transformed_tokens)
    # print("Transformed code:", repr(transformed_code))
    return transformed_code.replace(b"<>", b"**").replace(b"$=", b"*") \
        .replace(b":=", b"-").replace(bytes("λ","utf-8"),b"lambda")

'''

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
'''

# Install the import hook
# sys.meta_path.insert(0, SpecialSyntaxImporter())
# i = SpecialSyntaxImporter()

# def go2():
#     # print("GOOOOOOO")
#     custom_encoding.register_encoding(
#     encoding_name=encoding_name,
#     # transform_source=transform_source,
#     transform_source=i.transform_code,
#     hook_name=__name__,)
#     add_hook()
    # print("GOOOOOOO")
go()
# go2()

# import special.program as program
import program

program.start(cool = "awesome")

# import my_program  # noqa
# def test_import():
#     import my_program  # noqa

# test_import()

