from typing import Type, List, Optional


class Component:
    pass


class Factory(type):
    components: List[Component]

    def __new__(mcs, name, bases, class_attributes, components: Optional[List[Component]] = None):
        print("--", class_attributes)
        return super().__new__(mcs, name, bases, {**class_attributes, "components": components})

    def method(cls):
        print("bb", cls)

    @classmethod
    def create(mcs: type, name: str, components: List[Component]) -> "Factory":
        return mcs(name, (object,), {}, components=components)

    def __getitem__(self, item):
        print(item)
        return 1


if __name__ == "__main__":

    # class Bla(metaclass=Factory):
    #     pass

    print(Factory.create("TestClass", components=[Component()])[333])
