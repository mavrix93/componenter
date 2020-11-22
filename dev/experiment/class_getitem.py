from typing import TypeVar, Dict, Type


class Meta(type):

    _registry: Dict[Type["Model"], Type["SaveModel"]] = {}

    def __getitem__(self, model: Type["Model"]) -> Type["SaveModel"]:
        return self._registry[model]


class SaveModel(metaclass=Meta):
    # _registry = {}

    def __init_subclass__(cls, model=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if model:
            cls._registry[model] = cls

    @classmethod
    def save(cls):
        print("saving", cls)


class Model:
    pass


class User(Model):
    pass


class Group(Model):
    pass


class SaveUser(SaveModel, model=User):
    pass


if __name__ == "__main__":
    SaveModel[Group].save()
