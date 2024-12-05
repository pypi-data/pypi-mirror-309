import hashlib
import json
import os
from .. import Password
from ..src import _Password
from ..users import User


class Error:
    def __init__(self, args):
        self.msg = self.__class__.__name__ + ": " + args

class FunctionNotExistError(Error): pass
class InvalidArgumentsError(Error): pass
class STMkeyNotExistError(Error): pass


class Raised:
    def __init__(self, error):
        self.error = error

stm = {} # Short Term Memory (STM)


class FuncRunner:
    def __init__(self, func, *args):
        self.func = func
        self.args = args

    def run(self):
        return self.func(*self.args)
    

#################################################
# CONSOLE METHODS ###############################
#################################################


def test(stm, *args):
    print(*args)
    return None, stm

def exit_(stm, *code):
    if len(code) == 0:
        exit(0)
    if len(code) > 1:
        return InvalidArgumentsError("Must have 1 argument"), stm
    try:
        code = int(code[0])
    except:
        return InvalidArgumentsError(f"Must be a number, not '{code[0]}'."), stm
    
    exit(code)

def create(stm, *args):
    if len(args) < 2:
        return InvalidArgumentsError("Must have 2 arguments: create [username] [password] {--flags}"), stm
    
    try:
        use512 = args[2] == "--use-sha512"
    except IndexError:
        use512 = False
    if not use512 and len(args) > 2:
        return InvalidArgumentsError("Must have 2 arguments: create [username] [password] {--flags}"), stm
    if use512 and len(args) > 3:
        return InvalidArgumentsError("Must have 2 arguments: create [username] [password] {--flags}"), stm

    stm[args[0]] = User(args[0], Password(args[1], hsh_func = hashlib.sha256 if not use512 else hashlib.sha512))
    return None, stm

def clean_stm(stm, *args):
    if len(args) != 0:
        return InvalidArgumentsError("Must have no arguments: clean_stm"), stm
    
    return None, {}

def clear(stm, *args):
    os.system("cls" if os.name == "nt" else "clear")
    return None, stm


def save(stm, *args):
    if len(args) != 1:
        return InvalidArgumentsError("Must have 1 argument: save [filename]"), stm

    with open(args[0], "w") as file:
        temp = {user: stm[user].to_dict() for user in stm}
        json.dump(temp, file, indent=4)
    
    return None, stm


def load(stm, *args):
    if len(args) != 1:
        return InvalidArgumentsError("Must have 1 argument: load [filename]"), stm
    
    with open(args[0]) as file:
        temp = json.load(file)
        stm = {
            user: User(temp[user]["username"],
                       _Password(temp[user]["password"]["hashed"],
                                 hashlib.sha256 if temp[user]["password"]["hsh_func"] == "sha256" else hashlib.sha512,
                                 eval(temp[user]["password"]["hsh_enter"]),
                                 temp[user]["password"]["hsh_after"],
                                 temp[user]["password"]["salt"])) for user in temp
        }

    return None, stm


def verify(stm, *args):
    if len(args) != 2:
        return InvalidArgumentsError("Must have 2 arguments: validate [username] [password]"), stm
    
    try:
        return stm[args[0]].password.validate(args[1]), stm
    except KeyError:
        return STMkeyNotExistError(f"User '{args[0]}'"), stm
    
    



funcs = {
    "test": test,
    "exit": exit_,
    "create": create,
    "clean_stm": clean_stm,
    "cls": clear,
    "clear": clear,
    "save": save,
    "load": load,
    "validate": verify
}

def rs(error):
    print("ERR IN PWS256 SHELL:")
    print("\t"+error.msg)

def get_arglist(txt):
    args = txt.split(" ")
    return args[0], args[1:]

def get_func(name):
    return funcs[name]


def get_runner_from_arglist(arglist, stm):
    if arglist[0] not in funcs:
        return FunctionNotExistError(
            "Function " + arglist[0] + " does not exist")
    
    else:
        return FuncRunner(get_func(arglist[0]), stm, *arglist[1])
        
    
def run(txt: str, stm={}, raise_=True):
    if txt.isspace() or txt == "":
        return stm
    if txt[0] == " ":
        txt = txt.lstrip()

    arglist = get_arglist(txt)
    func = get_runner_from_arglist(arglist, stm)
    if issubclass(func.__class__, Error):
        if raise_:
            rs(func)
        return Raised(func), None
    else:
        ans, stm = func.run()
        if issubclass(ans.__class__, Error):
            if raise_:
                rs(ans)
            return Raised(ans), None

    return ans, stm


def _test():
    stm = {}
    while True:
        try:
            ans, stm = run(input("> "), stm)
        except KeyboardInterrupt:
            break
        if ans != None:
            print(ans)



if __name__ == "__main__":
    _test()