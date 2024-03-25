from enum import Enum


class CellType(Enum):
    EMPTY = 0
    BLOCK = 1
    CAN = 2
    SELECTED = 3


def get_type(i: int):
    match i:
        case 0:
            return CellType.EMPTY
        case 1:
            return CellType.BLOCK
        case 2:
            return CellType.CAN
        case 3:
            return CellType.SELECTED
