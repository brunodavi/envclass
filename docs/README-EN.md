# EnvClass
[:br:](/README.md)

> Translated by ChatGPT

`EnvClass` is a Python class designed to simplify the management of environment variables in your applications, reducing code repetition. By default, `EnvClass` uses the `python-dotenv` library and incorporates the `load_dotenv` function, so every new instance of a class that inherits from `EnvClass` automatically executes this action.

## Installation
You can install `EnvClass` using pip with the following command:

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

# Accessing environment variables as attributes
# >>> os.environ['DB_USER']
my_env.db_user

# >>> os.environ.get('DB_NAME', 'Dev')
my_env.db_host

# >>> True
my_env.testing

# >>> 8080
my_env.port
```

## Attribute Types
Currently, the primitive types of attributes are: `str`, `int`, `bool`, and `float`.

> Other types may also work, but have not been tested.

Attributes are automatically converted as they obtain values from environment variables.

`.env`
```
DEBUG=True
SECRET_KEY=mysecretkey
PORT=8080
DB_HOST=localhost DB_USER=username DB_PASSWORD=password

NONE_ENV=
```

When environment variables are created without a value (i.e., read from `os.environ` as empty strings `''`), attributes are set to `None`, regardless of their type. `bool` attributes can be configured as:

- `True`, `true`, or `1` for true.
- `False`, `false`, or `0` for false.

## Special Attributes

### Strict Mode
By default, strict mode is enabled (`_strict = True`).

When enabled, attempting to access a nonexistent environment variable will result in a `KeyError`.

When disabled (`_strict = False`), nonexistent attributes return `None`.

#### Examples
```python
from envclass import EnvClass

class Ex(EnvClass):
    _strict = False
    not_exists: str

ex = Ex()

# Returns None instead of raising a KeyError
ex.not_exists

class Strict(EnvClass):
    _strict = True
    not_exists: str

# Raises a KeyError when the environment variable does not exist
strict_env = Strict()
```

### Prefix
By default, the prefix is `None`.

You can add a string to the beginning of the environment variable name using the `_prefix` attribute.

#### Examples
```python
from envclass import EnvClass

class DataBase(EnvClass):
    _prefix = 'DB'

    name: str = 'Dev'
    host: str = 'localhost'
    user: str
    password: str

db = DataBase()

# Example: os.environ.get('DB_NAME', 'Dev')
db.name
```

### Separator
By default, the separator is the `_` (underscore) character.

Use the `_joiner` attribute to set a different character that separates words when using prefixes.

#### Examples
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
By default, the use of the class name as a prefix is disabled (`_class_as_prefix = False`). When enabled, the class name is used at the beginning of the environment variable name, especially useful if you follow the `PascalCase` convention for naming your classes.

```python
from envclass import EnvClass

class ApiService(EnvClass):
    _class_as_prefix = True

    key: str

api = ApiService()

# >>> os.environ['API_SERVICE_KEY']
api.key
```

### Notes
- If you use `_prefix` in conjunction with `_class_as_prefix`, the `_prefix` takes precedence and is used at the beginning of the environment variable name.

## Modifying EnvClass
If you want to modify certain functionalities in `EnvClass`, such as setting different defaults, manipulating information, and other customizations, you can create a new class that inherits from `EnvClass` and make the necessary changes.

### Examples

#### Defaults
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

#### Names
The `parse_label` method uses special prefix attributes, so if you change it, they may no longer work.

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

#### Attributes
The `parse_label` method is used in `parse_attrib`, so it won't be called if you override this method.

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
