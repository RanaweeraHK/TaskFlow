from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=500)


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool

    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=500)
    completed: bool