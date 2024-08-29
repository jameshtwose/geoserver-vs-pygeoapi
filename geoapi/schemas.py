from pydantic import BaseModel, Field

class HsSchema(BaseModel):
    id: int
    shape: dict
    
class MsSchema(BaseModel):
    id: int
    shape: dict

class LsSchema(BaseModel):
    id: int
    shape: dict
    
class MetersSchema(BaseModel):
    id: int
    timestamp: str
    address: str
    info: str
    shape: dict