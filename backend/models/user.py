from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserSearch(BaseModel):
    email: str

