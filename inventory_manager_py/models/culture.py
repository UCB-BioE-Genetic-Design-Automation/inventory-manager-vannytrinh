from enum import Enum

class Culture(Enum):
    library = "library"
    primary = "primary"
    secondary = "secondary"
    tertiary = "tertiary"

    def __str__(self):
        return str(self.value)