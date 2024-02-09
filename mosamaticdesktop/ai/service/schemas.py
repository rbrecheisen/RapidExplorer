from pydantic import BaseModel


class MyModelSchemaBase(BaseModel):
    name: str
    description: str


class MyModelSchemaCreate(MyModelSchemaBase):
    pass


class MyModelSchemal(MyModelSchemaBase):
    id: int

    class Config:
        orm_mode = True
