from abc import ABC, abstractmethod
from typing import Tuple


class BaseSSO(ABC):
    @abstractmethod
    def get_authorization_url(self) -> str:
        pass

    @abstractmethod
    def get_access_token(self, code: str) -> str:
        pass

    @abstractmethod
    def get_user_info(self, access_token: str) -> Tuple[str, str, str, str]:
        # returns email, first_name, last_name, profile_pic
        pass
