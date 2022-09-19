from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


class DatedModel(Base):
    create_date = Column(DateTime, server_default=func.now())
    update_date = Column(DateTime, server_default=func.now())

    __abstract__ = True
