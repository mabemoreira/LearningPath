# Learning Path (backend)

O presente projeto foi desenvolvido com [Python](https://www.python.org/)
v3.12.3 usando as seguintes dependências:
- [Alembic](https://alembic.sqlalchemy.org/) v1.13.2
- [FastAPI](https://fastapi.tiangolo.com/) v0.114.0
- [SQLAlchemy](https://www.sqlalchemy.org/) v2.0.34

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
