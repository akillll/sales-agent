from pydantic import BaseModel


class ProspectRequest(BaseModel):
    name: str
    company: str


class ReplyRequest(BaseModel):
    name: str
    company: str
    reply: str