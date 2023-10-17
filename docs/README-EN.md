# EnvClass

[🇧🇷](/)
[🇺🇲](docs/README-EN.md)

A Python class that simplifies the management of environment variables in your applications, eliminating the need for code repetition.

This class does not require any external libraries to function.

## Installation
To install, use pip:

```bash
pip install envclass
```

## Quick Start
```python
from envclass import EnvClass

class MyEnv(EnvClass):
    testing: bool
    log_level: str = 'INFO'
    port: int

    api_base_url: str
    api_key: str

    db_name: str = 'Dev'
    db_host: str = 'localhost'
    db_user: str
    db_password: str

# Arguments are optional
my_env = MyEnv(env_file='.env')

# Example usage:
# >>> os.environ['DB_USER']
my_env.db_user

# >>> os.environ.get('DB_NAME', 'Dev')
my_env.db_host

# Returns True
my_env.testing

# Returns 8080
my_env.port
```

### Supported Types
Currently, only primitive types have been tested, such as:

- str
- int
- bool
- float

Every time you instantiate a class that inherits from `EnvClass`, it reads and defines environment variables from the `.env` file.

Example `.env` file:

```
DEBUG=True
SECRET_KEY=mysecretkey
PORT=8080
DB_HOST=localhost
DB_USER=username
DB_PASSWORD=password

NONE_ENV=
```

When environment variables are created without a value, meaning they are read in `os.environ` but are empty strings `''`, they are treated as `None`, regardless of their type.

Attributes follow Python language conventions for conversion, but `bool` attributes have specific interpretations when reading environment variables:

`bool` attributes can be:

- `True`, `true`, or `1` for true.
- `False`, `false`, or `0` for false.

## Special Attributes

### Load Env
By default, this is set to `True`.

This allows reading the `.env` file and defining environment variables when instantiating the class. If set to `False`, the `.env` file will not be read, and environment variables will not be defined, requiring manual definition of environment variables during program execution.

Example:

```python
# no_load_env.py
from envclass import EnvClass

class NoLoadEnv(EnvClass):
    _load_env = False
    wait_time: int = 10

env = NoLoadEnv()

# Returns 5
env.wait_time
```

Execution on Linux:

```bash
WAIT_TIME=5 python no_load_env.py
```

### Strict Mode
By default, this is set to `True`.

This allows using `environ[key]` to signal when an environment variable is not defined, generating the default `KeyError` error if the variable does not have a default value. If set to `False`, attributes that do not exist will return `None`.

Examples:

```python
from envclass import EnvClass

# Disabled strict mode
class NotStrict(EnvClass):
    _strict = False
    not_exists: str

not_strict = NotStrict()

# Returns None
not_strict.not_exists

# Enabled strict mode
class Strict(EnvClass):
    _strict = True
    not_exists: str

# Generates a KeyError
strict_env = Strict()
```

### Prefix
By default, there is no prefix defined.

This allows adding a string at the beginning of the environment variable name, making it easier to organize.

Example:

```python
from envclass import EnvClass

class DataBase(EnvClass):
    _prefix = 'DB'

    name: str = 'Dev'
    host: str = 'localhost'
    user: str
    password: str

db = DataBase()

# >>> os.environ.get('DB_NAME', 'Dev')
db.name
```

### Join
By default, the `_` character is used to separate words when using prefixes.

This allows inserting a custom character to separate words when using prefixes.

Example:

```python
from envclass import EnvClass

class Env(EnvClass):
    _prefix = 'MY'
    _joiner = '__'

    key: str

env = Env()

# >>> os.environ['MY__KEY']
env.key
```

### Class as Prefix
By default, this is set to `False`.

This allows using the class name as part of the environment variable name. Currently, it only separates classes in `PascalCase`, so if you use it differently, the result may not be satisfactory.

Example:

```python
from envclass import EnvClass

class ApiService(EnvClass):
    _class_as_prefix = True
    key: str

api = ApiService()

# >>> os.environ['API_SERVICE_KEY']
api.key
```

> **Note:**
> If you use both `_prefix` and `_class_as_prefix`, the `_prefix` will be used.

## Modifying EnvClass
If you want to modify some functionalities in `EnvClass`, such as setting different defaults or manipulating information, you can do so:

### Defaults
You can create a new class that inherits from `EnvClass` and change its defaults.

Example:

```python
from envclass import EnvClass

class PascalEnv(EnvClass):
    _class_as_prefix = True

class Cloud(PascalEnv):
    api_key: str

cloud = Cloud()

# >>> os.environ['CLOUD_API_KEY']
cloud.api_key
```

### Names
The `parse_label` method uses the special prefix attributes, so if you change it, they may stop working.

Example:

```python
from envclass import EnvClass

class ReverseEnv(EnvClass):
    def parse_label(self, label: str):
        return '_'.join(
            label.split('_')[::-1]
        ).upper()

class Api(ReverseEnv):
    api_key: str

api = Api()

# >>> os.environ['KEY_API']
api.api_key
```

### Attributes
The `parse_label` method is used in `parse_attrib`, so it will not be called if you override it.

Example:

```python
from envclass import EnvClass
from os import getenv

class LowerEnv(EnvClass):
    def parse_attrib(
        self,
        label: str,
        attrib: type,
        default=None,
    ):
        return getenv(label)

class Env(LowerEnv):
    api_key: str

env = Env()

# >>> getenv('api_key')
env.api_key
```

### Reading
The `parse_env` method reads the `.env` file and defines the variables with `os.environ`. If you prefer, you can use a library like `python-dotenv` to perform this action.

Example:

```python
from dotenv import load_env
from envclass import EnvClass

class DotClass(EnvClass):
    def parse_env(self, env_file: str):
        load_env(env_file)

class Service(DotClass):
    host: str = 'localhost'

# By default, it runs the parse_env
service = Service()

# >>> os.environ.get('HOST', 'localhost')
service.host
```
