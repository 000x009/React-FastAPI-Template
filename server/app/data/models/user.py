import uuid

from datetime import datetime

from sqlalchemy import UUID, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.data.models import Base


class UserModel(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
