import os

def setupchecks():
    path = os.path.dirname(__file__) + "/srcimport.py"
    with open(path, "w") as file:
        file.write("""\"THIS FILE IS PREGENERATED. ANY CHANGE YOU MAKE WILL BE OVERWRITTEN\"

from pws256.src import _Password, Password, PwsType, defaultpass""")
        
    path = os.path.dirname(__file__) + "/usersrcimport.py"
    with open(path, "w") as file:
        file.write("""\"THIS FILE IS PREGENERATED. ANY CHANGE YOU MAKE WILL BE OVERWRITTEN\"

from pws256.src.users import User""")
        
    path = os.path.dirname(__file__) + "/rsasrcimport.py"
    with open(path, "w") as file:
        file.write("""\"THIS FILE IS PREGENERATED. ANY CHANGE YOU MAKE WILL BE OVERWRITTEN\"

from pws256.src.rsa import PublicKey, PrivateKey, KeyPair""")
        

