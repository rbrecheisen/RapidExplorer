from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Dataset(Base):
    # path: str
    
    __tablename__ = 'dataset'


class File(Base):
    # path: str
    __tablename__ = 'file'