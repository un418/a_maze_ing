
from pydantic import BaseModel, Field, model_validator


class ConfigData(BaseModel):

    """Pydantic BaseModel that validates config data. Has defaults
    The project says that all of these values (except 'seed') are mandatory.
    They cannot have default values and pydantic should raise an exception"""
    width: int = Field(ge=0, le=100)
    height: int = Field(ge=0, le=100)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str = Field(min_length=5, max_length=50)
    perfect: bool
    seed: int = 0

    @model_validator(mode='after')
    def validation(self) -> 'ConfigData':

        """Custom validation for entry and exit coordinates"""
        if self.entry == self.exit:
            raise ValueError("Entry and Exit coordinades cannot be the same")

        for coords in (self.entry, self.exit):

            x, y = coords
            if x >= self.width or y >= self.height:
                raise ValueError("Coordinates cannot be larger/equal to the maze's size")
            if x < 0 or y < 0:
                raise ValueError("Coordinates cannot be less than zero")

        return self
