import abc


class Component(abc.ABCMeta):
    def do_something(cls):
        pass

    @abc.abstractmethod
    def do_something_else(cls):
        pass


class ComponentsMeta(type):
    def __new__(mcs, name, bases, class_attributes, components=None):
        cls = super().__new__(mcs, name, bases, class_attributes)
        return cls


class Human(components=[Component], metaclass=ComponentsMeta):
    pass


if __name__ == "__main__":
    print(Human())
