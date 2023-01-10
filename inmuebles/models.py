import uuid
from pydantic import BaseModel, Field
from typing import Optional


class Inmueble(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    build_status: int
    is_active: bool
    start_month: int
    construction_type: int | None = None
    date_diff: int = 0
    description: str = ""
    date_in: str
    property_type: int
    end_week: int
    typology_type: int
    x_coord: float
    y_coord: float
    boundary_id: int | None = None
    id_uda: str
    title: str = ""
    listing_type: int
    date: str

