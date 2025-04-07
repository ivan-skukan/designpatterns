class A:
    def __init__(self):
        pass
    def func(self):
        pass
    @classmethod
    def func(cls):
        pass

print(A().func)
print(A.func)