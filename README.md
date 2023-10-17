# EnvClass

[🇺🇲](docs/README-EN.md)

Uma classe Python que simplifica o gerenciamento de variáveis de ambiente em seus aplicativos, eliminando a necessidade de repetir código.

Esta classe não requer nenhuma biblioteca externa para funcionar.

## Instalação
Para instalar, utilize o pip:

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

# Exemplo de uso:
# >>> os.environ['DB_USER']
my_env.db_user

# >>> os.environ.get('DB_NAME', 'Dev')
my_env.db_host

# Retorna True
my_env.testing

# Retorna 8080
my_env.port
```

### Tipos Suportados
Atualmente, apenas os tipos primitivos foram testados, como:

- str
- int
- bool
- float

Toda vez que você instancia uma classe que herda de `EnvClass`, ela realiza a leitura e definição das variáveis de ambiente a partir do arquivo `.env`.

Exemplo de arquivo `.env`:

```
DEBUG=True
SECRET_KEY=mysecretkey
PORT=8080
DB_HOST=localhost
DB_USER=username
DB_PASSWORD=password

NONE_ENV=
```

Quando as variáveis de ambiente são criadas sem valor, ou seja, são lidas em `os.environ`, mas são strings vazias `''`, elas são tratadas como `None`, independentemente do tipo.

Os atributos seguem as convenções da linguagem Python para conversão, mas os atributos do tipo `bool` têm interpretações específicas ao ler as variáveis de ambiente:

Os atributos `bool` podem ser:

- `True`, `true` ou `1` para verdadeiro.
- `False`, `false` ou `0` para falso.

## Atributos Especiais

### Carregar Env
Por padrão, está definido como `True`.

Isso permite ler o arquivo `.env` e definir as variáveis de ambiente ao instanciar a classe. Se definido como `False`, o arquivo `.env` não será lido e as variáveis de ambiente não serão definidas, tornando necessário definir as variáveis de ambiente manualmente durante a execução do programa.

Exemplo:

```python
# no_load_env.py
from envclass import EnvClass

class NoLoadEnv(EnvClass):
    _load_env = False
    wait_time: int = 10

env = NoLoadEnv()

# Retorna 5
env.wait_time
```

Execução do comando no Linux:

```bash
WAIT_TIME=5 python no_load_env.py
```

### Modo Estrito
Por padrão, está definido como `True`.

Isso permite usar `environ[key]` para sinalizar quando uma variável de ambiente não foi definida, gerando o erro padrão `KeyError` se a variável não tiver um valor padrão. Se definido como `False`, os atributos que não existem retornarão `None`.

Exemplos:

```python
from envclass import EnvClass

# Modo Estrito desativado
class NotStrict(EnvClass):
    _strict = False
    not_exists: str

not_strict = NotStrict()

# Retorna None
not_strict.not_exists

# Modo Estrito ativado
class Strict(EnvClass):
    _strict = True
    not_exists: str

# Gera um KeyError
strict_env = Strict()
```

### Prefixo
Por padrão, não possui um prefixo definido.

Isso permite adicionar uma string no início do nome da variável de ambiente, facilitando a organização.

Exemplo:

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

### Juntar
Por padrão, o caractere `_` é usado para separar as palavras ao usar os prefixos.

Isso permite inserir um caractere personalizado para separar as palavras ao usar os prefixos.

Exemplo:

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
Por padrão, está definido como `False`.

Isso permite usar o nome da classe como parte do nome da variável de ambiente. Atualmente, ele separa apenas classes em `PascalCase`, portanto, se você usar de outra forma, o resultado pode não ser satisfatório.

Exemplo:

```python
from envclass import EnvClass

class ApiService(EnvClass):
    _class_as_prefix = True
    key: str

api = ApiService()

# >>> os.environ['API_SERVICE_KEY']
api.key
```

> **Observação:**
> Se você usar `_prefix` e `_class_as_prefix` juntos, o `_prefix` será o utilizado.

## Modificando EnvClass
Se você deseja modificar algumas funcionalidades no `EnvClass`, como definir padrões diferentes ou manipular informações, é possível fazer isso:

### Padrões
Você pode criar uma nova classe que herde de `EnvClass` e alterar seus padrões.

Exemplo:

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

### Nomes
O método `parse_label` usa os atributos especiais de prefixo, portanto, se você alterá-lo, eles podem deixar de funcionar.

Exemplo:

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

### Atributos
O método `parse_label` é usado no `parse_attrib`, portanto, não será chamado se você sobrescrevê-lo.

Exemplo:

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

env =

 Env()

# >>> getenv('api_key')
env.api_key
```

### Leitura
O método `parse_env` realiza a leitura do arquivo `.env` e define as variáveis com `os.environ`. Se preferir, pode usar uma biblioteca, como `python-dotenv`, para realizar essa ação.

Exemplo:

```python
from dotenv import load_env
from envclass import EnvClass

class DotClass(EnvClass):
    def parse_env(self, env_file: str):
        load_env(env_file)

class Service(DotClass):
    host: str = 'localhost'

# Por padrão, executa o parse_env
service = Service()

# >>> os.environ.get('HOST', 'localhost')
service.host
```
