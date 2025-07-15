from pydantic import BaseModel

class ProgramFile (BaseModel):
    name: str
    code: str