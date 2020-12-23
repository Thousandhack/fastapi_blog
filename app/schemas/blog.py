from pydantic import BaseModel, Field, EmailStr, UUID4
from typing import Optional
from typing import List, Set, Dict


class Paginate(BaseModel):
    page: int = Field(1, description="页码数")
    page_size: int = Field(None, description="每页数量")
    total: int = Field(description="数据总量")