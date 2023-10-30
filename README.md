# EnvClass

[![python_versions][BadgePyVersions]][PYPI]
[![gnu][BadgeGNU]][PYPI]
[![version][BadgeVersion]][PYPI]
[![testing][BadgeTest]][CI]


Manage environment variables in a simple and elegant way

Made from 100% pure Python


## Why does this exist

To manage environment variables in an easy
way that works for any device (like a cell phone
with termux)


### Installation
```sh
pip install envclass
```

### Quick Start

`.env`
```env
HOST=0.0.0.0
PORT=1234

CONFIG_FILE=
```

```python
from envclass import EnvClass


# When declaring the class with _env_file it
# reads the file and casts all attributes
class MyEnv(EnvClass):
    _env_file = '.env'

    TESTING: bool = False

    HOST: str = 'localhost'
    PORT: int

    CONFIG_FILE: str


# Return: '0.0.0.0'
MyEnv.HOST

# Return: False
MyEnv.TESTING

# Return: 1234
MyEnv.PORT

# Return: None
MyEnv.CONFIG_FILE
```

### Supported Types
Currently, only primitive types have been tested, such as:

- `str`
- `int`
- `bool`
- `float`

#### Booleans

Attributes follow Python language conventions
for conversion, but `bool` attributes have specific
interpretations when reading environment variables:

`bool` attributes can be:

- `True`, `true`, or `1` for true.
- `False`, `false`, or `0` for false.


### Read Only Attributes

When this configuration is defined,
it is not possible to change the attributes

Example:

```python
from envclass import EnvClass


class EnvLock(EnvClass)
    KEY: str = None

# Generates an AttributeError stating 
# that it is read-only
EnvLock.KEY = 'Value'
```

### Lower Attrubutes

Lowercase attributes work the same way,
I just thought leaving everything capitalized
would look better

Since the name is closest to the environment variable read

Example:

`.env`
```env
LOWER_KEY='lower'
```

```python
from envclass import EnvClass

class EnvLower(EnvClass):
    lower_key = 'upper'

# Return: 'lower'
EnvLower.lower_key
```

### See your variables

The class is seen this way:

`env`
```env
ENV_A=3
ENV_B=1
ENV_C=10
```

```python
from envclass import EnvClass

class Env(EnvClass):
    _prefix = 'ENV'

    A: str
    B: bool = False
    C: int

print(Env)

## OutPut:
# ENV_A='3'
# ENV_B=True
# ENV_C=10
```


### Special Attributes

#### Env File
By default, this is set to `None`.

It is used to read the file like `.env`


Example:

```python
# file: no_load_env.py

from envclass import EnvClass


class NoEnv(EnvClass):
    WAIT_TIME: int = 10


print(NoEnv.WAIT_TIME)
```

Execution on Linux:

```sh
$ WAIT_TIME=5 python no_load_env.py
5
```

#### Strict Mode
By default, this is set to `True`.

This allows using `environ[key]` to signal when an
environment variable is not defined, generating
the default `KeyError` error if the variable
does not have a default value. If set to
`False`, attributes that do not exist
will return `None`.

Examples:

```python
from envclass import EnvClass

# Disabled strict mode
class NotStrict(EnvClass):
    _strict = False
    NOT_EXISTS: str

# Returns None
NotStrict.NOT_EXISTS


# Enabled strict mode
# Generates a KeyError
class Strict(EnvClass):
    _strict = True
    NOT_EXISTS: str
```

#### Prefix
By default, there is `None`

This allows adding a string at the beginning
of the environment variable name,
making it easier to organize.

Example:

`.env`
```env
DB_USER=dev_user
DB_KEY=dev_key_123
```

```python
from envclass import EnvClass

class DataBase(EnvClass):
    _prefix = 'DB'

    NAME: str = 'Dev'
    HOST: str = 'localhost'

    USER: str
    KEY: str

# Return: 'Dev'
DataBase.NAME

# Return: dev_key_123
DataBase.KEY
```


[PYPI]: https://pypi.python.org/pypi/envclass
[CI]: https://github.com/brunodavi/envclass/actions/workflows/python-test.yml

[BadgeGNU]: https://img.shields.io/pypi/l/envclass.svg
[BadgeVersion]: https://img.shields.io/pypi/v/envclass.svg
[BadgePyVersions]: https://img.shields.io/pypi/pyversions/envclass.svg
[BadgeTest]: https://github.com/brunodavi/envclass/actions/workflows/python-test.yml/badge.svg
