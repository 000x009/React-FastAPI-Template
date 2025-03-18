from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class UserDTO:
    id: UUID
    full_name: str
    joined_at: datetime
    email: str


@dataclass
class CreateUserDTO:
    id: UUID
    full_name: str
    joined_at: datetime
    email: str


@dataclass
class GetUserDTO:
    id: UUID
