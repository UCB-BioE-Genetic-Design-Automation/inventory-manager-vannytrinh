from dataclasses import dataclass
from typing import List
from .sample import Sample

@dataclass(frozen=True)
class Box:
    name: str                # name of the box, i.e., lysis1, and of the file
    description: str         # a description of the contents of the box
    location: str            # i.e., which freezer
    samples: List[List[Sample]]  # What's in each well, or None

    def get_size(self) -> tuple[int, int]:
        # assume that box is rectangular
        num_row = len(self.samples)
        if num_row > 0:
            num_col = len(self.samples[0]) 
        else:
            num_col = 0

        return (num_row, num_col) 


