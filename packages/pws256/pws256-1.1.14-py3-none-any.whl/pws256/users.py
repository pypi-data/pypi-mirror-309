"""
Module used for custom user classes to write in files

--- pws256/users

>>> import pws256 as pws
>>> from pws256.users import User
>>> pw = pws.Password("hallo")
>>> u = User("sigma123", pw)
>>> u.save_to_file("test.csv")
>>> usr = User.load_from_file("sigma123", "test.csv")
>>> usr.password.validate("hallo")
True
"""
from pws256._setup.setup import setupchecks

setupchecks()
del setupchecks
from pws256._setup.usersrcimport import *