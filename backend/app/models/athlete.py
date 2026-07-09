import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class AthleteDoc(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    sport_type: Optional[str] = None
    position: Optional[str] = None
    age: Optional[int] = None
    height: Optional[float] = None  # in cm
    weight: Optional[float] = None  # in kg
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "some-user-uuid",
                "sport_type": "Soccer",
                "position": "Forward",
                "age": 22,
                "height": 180.5,
                "weight": 75.0
            }
        }
