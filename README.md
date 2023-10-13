# EnvClass

[:us:](docs/README-EN.md)

O `EnvClass` é uma classe Python projetada para simplificar o gerenciamento de variáveis de ambiente em seus aplicativos, reduzindo a repetição de código. O `EnvClass` utiliza a biblioteca `python-dotenv` por padrão, incorporando a função `load_dotenv`, de forma que cada nova instância de uma classe que herda de `EnvClass` executa essa ação automaticamente.

## Instalação
Você pode instalar o `EnvClass` através do pip com o seguinte comando:

```bash
pip install envclass
```

## Início Rápido
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

# Os argumentos são opcionais
my_env = MyEnv(env_file='.env')

# Acessando variáveis de ambiente como atributos
# >>> os.environ['DB_USER']
my_env.db_user

# >>> os.environ.get('DB_NAME', 'Dev')
my_env.db_host

# >>> True
my_env.testing

# >>> 8080
my_env.port
```

## Tipos de Atributos
Atualmente, os tipos primitivos dos atributos são: `str`, `int`, `bool` e `float`.

> Outros tipos podem funcionar também, mas não foram testados.

Os atributos são convertidos automaticamente assim que obtêm o valor das variáveis de ambiente.

`.env`
```
DEBUG=True
SECRET_KEY=mysecretkey
PORT=8080
DB_HOST=localhost DB_USER=username DB_PASSWORD=password

NONE_ENV=
```

Quando as variáveis de ambiente são criadas sem valor (ou seja, são lidas no `os.environ` como strings vazias `''`), os atributos são definidos como `None`, independentemente do tipo. Os atributos `bool` podem ser configurados como:

- `True`, `true` ou `1` para verdadeiro.
- `False`, `false` ou `0` para falso.

## Atributos Especiais

### Modo Estrito
Por padrão, o modo estrito está ativado (`_strict = True`).

Quando ativado, a tentativa de acessar uma variável de ambiente inexistente resultará em um erro `KeyError`.

Quando desativado (`_strict = False`), os atributos que não existem retornarão `None`.

#### Exemplos
```python
from envclass import EnvClass

class Ex(EnvClass):
    _strict = False
    not_exists: str

ex = Ex()

# Retorna None em vez de gerar um KeyError
ex.not_exists

class Strict(EnvClass):
    _strict = True
    not_exists: str

# Gera um KeyError quando a variável de ambiente não existe
strict_env = Strict()
```

### Prefixo
Por padrão, o prefixo é `None`.

Você pode adicionar uma string ao início do nome da variável de ambiente usando o atributo `_prefix`.

#### Exemplos
```python
from envclass import EnvClass

class DataBase(EnvClass):
    _prefix = 'DB'

    name: str = 'Dev'
    host: str = 'localhost'
    user: str
    password: str

db = DataBase()

# Exemplo: os.environ.get('DB_NAME', 'Dev')
db.name
```

### Separador
Por padrão, o separador é o caractere `_` (sublinhado).

Use o atributo `_joiner` para definir um caractere diferente que separa as palavras ao usar os prefixos.

#### Exemplos
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

### Classe Como Prefixo
Por padrão, o uso do nome da classe como prefixo está desativado (`_class_as_prefix = False`). Quando ativado, o nome da classe é usado no início do nome da variável de ambiente, especialmente útil se você seguir a convenção `PascalCase` para nomear suas classes.

```python
from envclass import EnvClass

class ApiService(EnvClass):
    _class_as_prefix = True

    key: str

api = ApiService()

# >>> os.environ['API_SERVICE_KEY']
api.key
```

### Observações
- Caso você utilize o `_prefix` em conjunto com o `_class_as_prefix`, o `_prefix` terá preferência e será usado no início do nome da variável de ambiente.

## Modificando o EnvClass
Caso você queira modificar algumas funcionalidades no `EnvClass`, como definir padrões diferentes, manipular informações e outras personalizações, é possível criar uma nova classe que herde de `EnvClass` e fazer as mudanças necessárias.

### Exemplos

#### Padrões
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

#### Nomes
O método `parse_label` utiliza os **atributos especiais** de prefixo, portanto, se você alterá-lo, eles podem deixar de funcionar.

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

#### Atributos
O método `parse_label` é usado no `parse_attrib`, então ele não será chamado se você sobrescrever esse método.

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
