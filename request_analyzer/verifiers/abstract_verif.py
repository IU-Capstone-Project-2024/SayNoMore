from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple

class BaseVerifier(ABC):
    """
    Abstract base class for verifiers.
    """

    class ValueStages(Enum):
        OK = 1
        FIELD_NOT_FOUND = 2
        INCORRECT_VALUE = 3
    
    @abstractmethod
    def verify(self, retrieved_value: str) -> Tuple[ValueStages, str]:
        pass
