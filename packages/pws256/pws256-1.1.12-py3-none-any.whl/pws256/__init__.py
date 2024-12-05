"""
This is used to verify passwords with custom hash functions (or sha256 by default)

--- pws256/

>>> import pws256
>>> pw = pws256.Password("password")
>>> pw.verify("password")
True
>>> pw.verify("pasword")
False
>>> pw.hsh_func
<built-in function openssl_sha256>
>>> pw2 = pws256.Password(
...    raw = "password",
...    hsh_func = lambda x : "".join(reversed(x)),
...    hsh_enter = str,
...    hsh_after = None
...)
...
>>> pw2.verify("password")
True
>>> pw2.hashed
"drowssap"
>>>
"""

__version__ = "1.1.12"

import os, datetime
try:
    if os.environ["PWS256-VERBOSE"] == "3":
        now = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] pws256 start")
except:
    pass


from pws256._setup.setup import setupchecks

setupchecks()
del setupchecks, datetime, os
try:
    del now
except:
    pass

from pws256._setup.srcimport import *