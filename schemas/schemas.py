from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: str
    status: bool = False


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: bool | None = None


class TaskRead(TaskCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)