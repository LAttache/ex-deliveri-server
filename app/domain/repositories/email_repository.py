from abc import ABC, abstractmethod

class EmailRepository(ABC):
    @abstractmethod
    async def send_email(self, to: str, subject: str, body: str, code: str) -> None:
        pass
