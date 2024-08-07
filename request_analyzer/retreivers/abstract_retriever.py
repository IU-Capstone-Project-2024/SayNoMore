from abc import ABC, abstractmethod


class BaseRetriever(ABC):
    """
    Abstract base class for retrievers.
    """

    @abstractmethod
    async def retrieve(self, request: str) -> str:
        pass
