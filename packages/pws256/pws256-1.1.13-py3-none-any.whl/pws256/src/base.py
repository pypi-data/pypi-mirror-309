class Validator:
    def __init__(self, hashed, hsh_func, hsh_enter, hsh_after, salt):
        self.hashed, self.__hsh_func, self.__hsh_enter, self.__hsh_after, self._salt = hashed, hsh_func, hsh_enter, hsh_after, salt
    
    def hash_password_validator(self, raw):
        return hash_password(raw, self.__hsh_func, self.__hsh_enter, self.__hsh_after, self._salt)

    def validate(self, other):
        return self.hash_password_validator(other) == self.hashed
    



def hash_password(raw, hsh_func, hsh_enter, hsh_after, salt):
    encoded = hsh_func(((salt + raw) if hsh_enter == str else (salt + raw).encode()))
    if hsh_after:
        encoded = eval("encoded" + hsh_after, dict({"encoded": encoded}))

    return encoded