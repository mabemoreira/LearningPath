# Learning Path (backend)

O presente projeto foi desenvolvido com [Python](https://www.python.org/)
v3.12.3 usando as seguintes dependências:
- [Alembic](https://alembic.sqlalchemy.org/) v1.13.2
- [FastAPI](https://fastapi.tiangolo.com/) v0.114.0
- [SQLAlchemy](https://www.sqlalchemy.org/) v2.0.34

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

Após ativar o ambiente virtual, você pode instalar as dependências com 
`pip install -r requirements.txt` ou pode seguir os passos abaixo:

```bash
# Instale FastAPI
pip install "fastapi[standard]"

# Instale SQLAlchemy
pip install SQLAlchemy

# Instale o Alembic
pip install Alembic
```