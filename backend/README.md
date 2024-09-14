# Learning Path (backend)

O presente projeto foi desenvolvido com [Python](https://www.python.org/)
v3.12.3 usando as seguintes dependências:
- [Django](https://www.djangoproject.com/) v5.1.1

Para manutenção do código, foram usados:
- [Black](https://github.com/psf/black) v24.8.0
- [ISort](https://github.com/pycqa/isort) v5.13.2
- [Pre-Commit](https://pre-commit.com/) v3.8.0

## Configurações do ambiente de desenvolvimento

Antes de instalar as dependências:
1. mova o terminal para dentro do diretório backend
2. Se ainda não estiver com 
   [venv](https://docs.python.org/pt-br/3/library/venv.html) instalado, instale
   usando `python -m pip install venv`. 
3. crie um ambiente virtual Python com o comando `python -m venv ./venv`.
4. Ative o ambiente virtual com `./venv/bin/activate`.

> **Nota:** se estiver usando o VS Code como ambiente de desenvolvimento, ele
> deve pedir para adicionar a ambiente virtual como executor Python padrão. Se
> optar por fazer isso, o terminal integrado do VS Code deve iniciar o ambiente
> virtual sempre que uma nova instância dele for aberta - o que pode facilitar
> o desenvolvimento. PS.: isso só acontecerá se você estiver com a extensão de
> Python instalada no editor!

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
python3 -m src.manage runserver [<porta>]
```

Se estiver usando o VS Code, você pode rodar o projeto através da interface do
editor, usando o arquivo `launch.json`, dentro da pasta `.vscode` do backend.
Isso permite debugar o código!

## Criação apps Django

No Django, um app é uma aplicação web que faz parte do projeto. Cada app é
responsável por uma funcionalidade específica, como um sistema de
autenticação ou uma API.

1. Crie um novo app:
   ```bash
   # Inicia o servidor local
   python src.manage startapp <nome_do_app>
   ```

2. Adicione o app ao projeto: Abra o arquivo `backend/src/settings.py` e adicione o nome do novo app à lista `INSTALLED_APPS`. Por exemplo:
   ```bash
   INSTALLED_APPS = [
      ...
      'nome_do_app',
   ]
   ```

## Manutenção do Banco de dados
A gerência do banco de dados consiste nos seguintes passos:

1. Gerar migrações: sempre que um modelo for criado ou alterado, você deve
   gerar arquivos de migração que descrevem essas mudanças. Tais arquivos serão
   salvos na pasta `migrations` de cada app, descrevendo as alterações que serão
   aplicadas ao banco de dados:
   ```bash
   python manage.py makemigrations # gera migrações
   ```

- Aplicar migrações: Para aplicar as migrações ao banco de dados e criar ou alterar as tabelas conforme necessário, execute:
```bash
python3 manage.py migrate        # aplica migrações
```

### 4. Testes
Para rodar os testes do projeto, use o comando:
```bash
python3 manage.py test
```
- <b>Diretórios de Teste</b>: O Django procura por arquivos de teste (geralmente nomeados test*.py) dentro de cada app e executa os métodos de teste definidos nesses arquivos.

### 5. Shell
O Django Shell é uma ferramenta interativa que permite interagir com o banco de dados e o código do projeto diretamente do terminal. Para iniciar o Django Shell, use o comando:
```bash
python3 manage.py shell
```
- <b>Usos Comuns:</b> No shell, você pode criar, consultar, atualizar e excluir registros do banco de dados, testar funções e métodos, e executar scripts rápidos.
<!--
Use o comando `fastapi dev ./src/__main__.py` para executar o projeto em modo
de teste. Em modo de teste, o projeto espera que um banco postgres esteja
rodando na porta 5432 do localhost com as seguintes credenciais:
- nome do banco: postgres
- usuário: postgres
- senha: 1234

Você pode fazer isso vinculando um arquivo `.env` com essas variáveis ao seu
ambiente de desenvolvimento ou setando essas variáveis no terminal em que for
executar o comando de execução.

> **Nota:** se estiver usando o VS Code, ao adicionar o arquivo `.env`, tendo
> aberto o diretório backend como projeto, as variáveis nele já devem estar no
> terminal integrado!
-->
