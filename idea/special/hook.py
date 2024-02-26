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


def transform_source(source, **_kwargs):
    """Simple transformation: replaces any single token λ by lambda.

    By defining this function, we can also make use of Ideas' console.
    """
    tokens = token_utils.tokenize(source)
    for token in tokens:
        if token == "λ":
            token.string = "lambda"
    return token_utils.untokenize(tokens)


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


encoding_name = "lambda_encoding"




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

go()