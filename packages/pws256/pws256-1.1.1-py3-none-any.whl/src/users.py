import hashlib as hl
from io import TextIOWrapper
from . import _Password, PwsType


class User:
    def __init__(self, username: str, password: PwsType):
        self.username = username
        if not issubclass(type(password), _Password):
            raise TypeError(
                f"Password must be derived from _Password (eg. Password() or defaultpass())"
            )
        self.password = password

    @classmethod
    def load_from_file(cls, username: str, file: TextIOWrapper | str, hsh_func=hl.sha256, hsh_enter: str | bytes = bytes, hsh_after = ".hexdigest()", close=False):
        if isinstance(file, str):
            file = open(file)

        for line in file.readlines():
            line = line[:-1]
            if line.split(",")[0] == username:
                return User(username, _Password(
                    hashed = line.split(",")[1],
                    hsh_func = hsh_func,
                    hsh_enter = hsh_enter,
                    hsh_after = hsh_after,
                    salt = line.split(",")[2]
                ))
            
        if close:
            file.close()
        
    def save_to_file(self, file: TextIOWrapper | str, close=False):
        if isinstance(file, str):
            file = open(file, "a")
        file.write(f"{self.username},{self.password.hashed},{self.password.get_salt()}\n")
        if close:
            file.close()

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password.to_json()
        }
        
