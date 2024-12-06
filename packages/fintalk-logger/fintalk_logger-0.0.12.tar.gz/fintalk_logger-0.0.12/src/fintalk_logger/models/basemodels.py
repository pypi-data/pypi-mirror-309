from pydantic import BaseModel
from typing import Dict, Optional, List, Callable

class LoggerConfig(BaseModel):
    service:str
    request_id:str
    
class LogHttp(BaseModel):
    url: str
    useragent: str
    method: str
    host: str

class LogMask(BaseModel):
    path: str
    maskFunction: Optional[Callable[[str], str]] = None

class MaskList(BaseModel):
    masks: Optional[List[LogMask]] = None
        
class LogUser(BaseModel):
    id: str
    status: Optional[str] = None
    phone: Optional[str] = None
    client: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[str] = None
    groups: Optional[str] = None
    scope: Optional[str] = None
    type: Optional[str] = None