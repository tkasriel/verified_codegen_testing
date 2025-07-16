from abc import ABC, abstractmethod
class Model (ABC):
    def __init__(self):
        ...

    @abstractmethod
    async def send (self, message: str) -> str:
        ...
    
    @abstractmethod
    def clear_history (self):
        ...