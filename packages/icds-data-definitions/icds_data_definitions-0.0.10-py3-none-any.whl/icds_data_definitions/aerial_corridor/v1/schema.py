from enum import Enum

class AerialCorridorRead(BaseModel):
    "A class to read data from the Aerial Corridor table "
    
    url: str
    min_cell_level: int
    max_cell_level: int
    start_datetime: str
    end_datetime: str
    created_at: str
    updated_at: str
