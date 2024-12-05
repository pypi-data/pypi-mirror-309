# pws256
This is a python module for username and passwords with hash functions, which you can customise.


## Example
```
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
>>> pw2.hashed # Includes salt so when reversed, salt is at the back
"drowssap...bv4w75..."
>>> import pws256.users as u
>>> pw3 = pws256.Password("hello")
>>> usr = u.User("me", pw3)
>>> usr.save_to_file("test.csv")
>>> user = u.User.load_from_file("me", "test.csv")
>>> user.password.verify("hello")
True
>>> pw4 = pws256.defaultpass("hello")
>>> pw4.salt = "abc"
Traceback (most recent call last):
...
>>> pw4.salt_settable(True)
>>> pw4.salt = "abc"
>>> pw4.salt
"abc"
>>> pw4.salt_settable(False)
Traceback (most recent call last):
...
>>>
```