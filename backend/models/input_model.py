from enum import Enum

from pydantic import BaseModel


# Creating Enums for categorical fields and automating value assignment and error handling.
class BuildingType(str, Enum):
    maison = "maison"
    appartement = "appartement"
    immeuble = "immeuble"


class HeatingType(str, Enum):
    electricite = "Électricité"
    gaz = "Gaz naturel"
    autre = "Autre"


# -------------------------------- Main Model for the input data.
class InputData(BaseModel):
    Location: str
    cost: float
    area: float
    n_floors: int
    age: int
    main_heating_energy: HeatingType
    building: BuildingType
