class A:
    def __new__(cls, y, *args, **kwargs):
        print(y, args, kwargs)
        return super().__new__(cls)

    def __init__(self, x):
        self.x = x


if __name__ == "__main__":
    A(x=1, y=2)
