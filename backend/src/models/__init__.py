from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, String


class DatabaseModel:
    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(String)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    updated_by = Column(String)
