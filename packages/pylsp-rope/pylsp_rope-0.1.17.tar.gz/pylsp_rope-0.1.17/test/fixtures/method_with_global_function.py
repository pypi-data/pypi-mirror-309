import sys


class MyClass:
    def my_method(self):
        local_var = 10
        print(extracted_method())
        print(local_var)
        print(sys.stdin.read())

def extracted_method():
    return sys.stdin.read()
