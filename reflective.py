# reflective.py

'''
# Self reflective (for metric)
'''
import traceback

def reflective(func):
    def wrapper(*args, **kwargs):
        call_stack = traceback.extract_stack()[:]  # Exclude the last two frames (wrapper and the call to wrapper)
        call_stack_names = [frame.name for frame in call_stack]
        return call_stack_names
    return wrapper

def main():
    return Foo()

def Foo():
    return Bar()

@reflective
def Bar(*args, **kwargs):
    print("BAR Function was called from stack:", args, kwargs)
    return args, kwargs

call_stack = main()
print("Bar function was called from stack:", call_stack)
