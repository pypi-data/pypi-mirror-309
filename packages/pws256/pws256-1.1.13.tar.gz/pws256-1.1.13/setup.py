from setuptools import setup, find_packages
setup(
    name='pws256',
    version='1.1.13',
    description="pws256: A module that is used for users and passwords, and also has validation methods to check passwords with strings",
    packages=["pws256", "pws256.src", "pws256._setup"],
    author='Hector Robertson',
    py_modules=["rsa", "users"],
    install_requires=["numpy"],
    readme="pws256/README.md"
)