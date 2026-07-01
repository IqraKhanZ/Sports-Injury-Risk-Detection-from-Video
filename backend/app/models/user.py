import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base

class UserRole(str, enum.Enum):
    ATHLETE = "athlete"
    COACH = "coach"
    PHYSIOTHERAPIST = "physiotherapist"
    SPORTS_SCIENTIST = "sports_scientist"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.ATHLETE)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    athlete_profile = relationship("Athlete", back_populates="user", uselist=False, cascade="all, delete-orphan")
