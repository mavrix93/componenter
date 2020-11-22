import abc
from typing import Optional, Type, List, Generic, TypeVar, Dict, TypedDict, Protocol

ComponentGenConfigT = TypeVar("ComponentGenConfigT")
ComponentGenT = TypeVar("ComponentGenT", bound="ComponentT")


class ComponentConfigT(Generic[ComponentGenConfigT]):
    pass


class ComponentT(Generic[ComponentGenConfigT]):
    COMPONENTS_CLASSES: List[Type["ComponentT"]]
    CONFIG: Optional[Type[ComponentGenConfigT]]

    config: ComponentGenConfigT
    components: Dict[Type["ComponentT"], "ComponentT"]

    @abc.abstractmethod
    def __init__(self, configs: List[ComponentConfigT]):
        ...

    @abc.abstractmethod
    def __getitem__(self, item: Type["ComponentGenT"]) -> "ComponentGenT":
        ...
