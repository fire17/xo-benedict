
def start(*args, **kwargs):
    square = λ x: x**2

    assert square(3) == 9

    print("Using lambda-encoding: λ",(λ x: x**2)(10))  # λ is not converted inside strings
    print(args,kwargs)
    print("start DONE")
    # print("The square of 5 is", square(5))

if __name__ == '__main__':
    print("The square of 5 is", square(5))