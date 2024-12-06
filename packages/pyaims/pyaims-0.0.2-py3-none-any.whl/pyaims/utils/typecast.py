"""Type casting utils from pymatgen that are useful"""
from typing import TypeVar, Sequence, Literal, Annotated
import numpy as np
import numpy.typing as npt


_T = TypeVar("_T", bound=np.generic)

Vector3D = Annotated[npt.NDArray[_T], Literal[3]]
Matrix3D = Annotated[npt.NDArray[_T], Literal[3, 3]]


def to_vector3d(sequence: Sequence, dtype=float) -> Vector3D:
    """Type casting to 3D vector of floats."""
    assert len(sequence) == 3
    return np.array(sequence, dtype=dtype)

def to_matrix3d(sequence: Sequence, dtype=float) -> Matrix3D:
    """Type casting to 3D matrix of floats."""
    assert len(sequence) == 3 and all([len(row) == 3 for row in sequence])
    return np.array(sequence, dtype=dtype)
