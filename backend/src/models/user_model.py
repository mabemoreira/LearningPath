from src.configurations.database import Database
from src.models import DatabaseModel


class UserModel(Database, DatabaseModel):
    __tablename__ = "tb_user"
