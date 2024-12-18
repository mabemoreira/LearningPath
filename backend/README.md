# Learning Path (backend)

O presente projeto foi desenvolvido com [Python](https://www.python.org/) v3.12.3 usando 
as seguintes dependências:
- [Django](https://www.djangoproject.com/) v5.1.1

Para manutenção do código, foram usados:
- [Black](https://github.com/psf/black) v24.8.0
- [ISort](https://github.com/pycqa/isort) v5.13.2
- [Pre-Commit](https://pre-commit.com/) v3.8.0

Para criação do swagger:
- [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/) v0.27.2

## Configurações do ambiente de desenvolvimento

Antes de instalar as dependências:
1. Mova o terminal para dentro do diretório backend
2. Se ainda não estiver com [venv](https://docs.python.org/pt-br/3/library/venv.html)
   instalado, instale usando `python -m pip install venv`. 
3. crie um ambiente virtual Python com o comando `python -m venv ./venv`.
4. Ative o ambiente virtual com `./venv/bin/activate`.

> **VS Code:** o VS Code deve pedir para adicionar a ambiente virtual como executor
> Python padrão. Se optar por fazer isso, o terminal integrado do editor deve iniciar o
> ambiente virtual sempre que uma nova instância dele for aberta - o que pode facilitar o
> desenvolvimento. PS.: isso só acontecerá se você estiver com a extensão
> [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
> instalada!

Após ativar o ambiente virtual, instale as dependências com o comando
`pip install -r requirements.txt`.

Por fim, configure o pre-commit:
```bash
# Instale as dependências do pre-commit
pre-commit install

# Rode o pre-commit pela primeira vez (necessário)
pre-commit run --all-files
```

## Execução do projeto

Para iniciar o servidor de desenvolvimento local, use o comando:

```bash
# Inicia o servidor local (porta opcional)
python -m src.manage runserver [<porta>]
```

> **VS Code:** o arquivo `launch.json`, dentro do diretório `.vscode` do backend deve
> te permitir debugar o código! Use a opção: "Python Debugger: Application".

### Swagger

Com o servidor local rodando, é possível acessar a UI da API (swagger) acessando:
`http://localhost:<porta>/swagger/`!

### Autenticação

A authenticação por token requer que o cabeçalho de toda requisição feita à aplicação
contenha:

```json
{
   "authorization": "Token <token>"
}
```

Note que `<token>` é o token obtido durante o login e que ele deve ser precedido pela
palavra chave "Token" e um espaço.

## Criação apps Django

No Django, um app é uma aplicação web que faz parte do projeto. Cada app é
responsável por uma funcionalidade específica, como um sistema de
autenticação ou uma API.

1. Crie um novo app:
   ```bash
   # Inicia o servidor local
   python -m src.manage startapp <nome_do_app>
   ```

2. Adicione o app ao projeto: Abra o arquivo `backend/src/settings.py` e 
   adicione o nome do novo app à lista `INSTALLED_APPS`. Por exemplo:
   ```bash
   INSTALLED_APPS = [
      ...
      'nome_do_app',
   ]
   ```

## Manutenção do Banco de dados

A gerência do banco de dados consiste nos seguintes passos:

1. No arquivo `models/__init__`, é necessário importar os modelos (tabelas)

2. Gerar migrações: sempre que um modelo for criado ou alterado, você deve gerar arquivos
   de migração que descrevem essas mudanças. Tais arquivos serão salvos na pasta
   `migrations` de cada app, descrevendo as alterações que serão aplicadas ao banco de
   dados:
   ```bash
   python -m src.manage makemigrations # gera migrações
   ```

3. Aplicar migrações: Para aplicar as migrações ao banco de dados e criar ou alterar
   as tabelas conforme necessário, execute:
   ```bash
   python -m src.manage migrate # aplica migrações
   ```

## Testes

Para rodar os testes do projeto, use o comando:
```bash
python -m src.manage test
```
- **Diretórios de Teste:** O Django procura por arquivos de teste (geralmente nomeados
  test_*.py) dentro de cada app e executa os métodos de teste definidos nesses arquivos.

> **VS Code:** a execução dos testes através da extensão Python está configurada, então
> você também deve ser capaz de usar a interface do VS Code para rodar os testes! Por
> outro lado, não foi encontrada uma forma de rodar o debug dos testes via extensão. Se
> estiver com um **problema nos testes**, use a opção "Python Debugger: Tests" dentro do
> arquivo de teste que você deseja debugar!

## Shell
O Django Shell é uma ferramenta interativa que permite interagir com o banco de dados e o código do projeto diretamente do terminal. Para iniciar o Django Shell, use o comando:
```bash
python -m src.manage shell
```
- **Usos Comuns:** No shell, você pode criar, consultar, atualizar e excluir registros do banco de dados, testar funções e métodos, e executar scripts rápidos.
