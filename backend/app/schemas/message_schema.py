from pydantic import BaseModel, Field


class MessageSchema(BaseModel):
    message: str = Field(..., description="Mensagem de retorno")
