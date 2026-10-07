
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Any


class ConfigData(BaseModel):
    """
    Pydantic BaseModel that validates config data. No Defalts for mandatories.
    The project says that all of these values (except 'seed') are mandatory.
    They cannot have default values and pydantic should raise an exception

    Raises:
        ValidationError: If the parsed data violates constraints.
        ValueError: for entry and exit coordinate violation.
    """
    WIDTH: int = Field(ge=0, le=100)
    HEIGHT: int = Field(ge=0, le=100)
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str = Field(min_length=5, max_length=50)
    PERFECT: bool
    SEED: int = 0

    @field_validator("ENTRY", "EXIT", mode='before')
    @classmethod
    def tuple_conv(cls, coords: str) -> tuple[int, int]:
        """
        Converting 'ENTRY' and 'EXIT' to tuple[int, int].
        Before BaseModel check.

        Raises:
            ValueError: if 'ENTRY' or 'EXIT' hold > 2 coordinates
        """
        x, y = coords.split(',')
        return (int(x), int(y))


    @model_validator(mode='after')
    def validation(self) -> 'ConfigData':
        """
        Custom validation for entry and exit coordinates.

        Raises:
            ValueError: for entry and exit coordinate violation.
        """
        if self.ENTRY == self.EXIT:
            raise ValueError("Entry and Exit coordinades cannot be the same")

        for coords in (self.ENTRY, self.EXIT):
            x, y = coords
            if x >= self.WIDTH or y >= self.HEIGHT:
                raise ValueError("Coordinates cannot be larger/equal to the maze's size")
            if x < 0 or y < 0:
                raise ValueError("Coordinates cannot be less than zero")

        return self
