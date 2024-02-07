#program.py

def start(*args, **kwargs):
    a = 17
    #TODO: instead of a use obj that has ** __pow__
    # a := 3
    print("::: STARTING WITH NEW SYNTAX ::: ", a, args, kwargs)

    print("<<<< <> >>>>", a <> a)
    print("$$$$ $= ====", a $= a)
    print(":::: := ====", a := a)
    square = λ x: x**2
    # if token == "<>":
    #         token.string = "@"
    #     if token == "$=":
    #         token.string = "@="
    assert square(3) == 9
    print("Using lambda-encoding: λ",(λ x: x**2)(9))  # λ is not converted inside strings

    print("DONE",args,kwargs)
    # print("The square of 5 is", square(5))

if __name__ == '__main__':
    print("The square of 5 is", square(5))