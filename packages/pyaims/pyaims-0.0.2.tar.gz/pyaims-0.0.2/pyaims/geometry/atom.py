from  __future__ import annotations
from dataclasses import dataclass

import numpy as np

from pyaims.utils.typecast import Vector3D

CHEMICAL_SYMBOLS = [
    'emptium',
    'H', 
    'He',
    'Li', 
    'Be', 
    'B', 
    'C', 
    'N', 
    'O', 
    'F', 
    'Ne',
    'Na', 
    'Mg', 
    'Al', 
    'Si', 
    'P', 
    'S', 
    'Cl', 
    'Ar',
    'K', 
    'Ca', 
    'Sc', 
    'Ti', 
    'V', 
    'Cr', 
    'Mn', 
    'Fe', 
    'Co', 
    'Ni', 
    'Cu', 
    'Zn',
    'Ga', 
    'Ge', 
    'As', 
    'Se', 
    'Br', 
    'Kr',
    'Rb', 
    'Sr', 
    'Y', 
    'Zr', 
    'Nb', 
    'Mo', 
    'Tc', 
    'Ru', 
    'Rh', 
    'Pd', 
    'Ag', 
    'Cd',
    'In', 
    'Sn', 
    'Sb', 
    'Te', 
    'I', 
    'Xe',
    'Cs', 
    'Ba', 
    'La', 
    'Ce', 
    'Pr', 
    'Nd', 
    'Pm', 
    'Sm', 
    'Eu', 
    'Gd', 
    'Tb', 
    'Dy',
    'Ho', 
    'Er', 
    'Tm', 
    'Yb', 
    'Lu',
    'Hf', 
    'Ta', 
    'W', 
    'Re', 
    'Os', 
    'Ir', 
    'Pt', 
    'Au', 
    'Hg', 
    'Tl', 
    'Pb', 
    'Bi',
    'Po', 
    'At', 
    'Rn',
    'Fr', 
    'Ra', 
    'Ac', 
    'Th', 
    'Pa', 
    'U', 
    'Np', 
    'Pu', 
    'Am', 
    'Cm', 
    'Bk',
    'Cf', 
    'Es', 
    'Fm', 
    'Md', 
    'No', 
    'Lr',
    'Rf', 
    'Db', 
    'Sg', 
    'Bh', 
    'Hs', 
    'Mt', 
    'Ds', 
    'Rg', 
    'Cn', 
    'Nh', 
    'Fl', 
    'Mc',
    'Lv', 
    'Ts', 
    'Og',
]

ATOMIC_SYMBOLS_TO_NUMBERS = {symbol: zz for zz, symbol in enumerate(CHEMICAL_SYMBOLS)}

@dataclass
class FHIAimsAtom:
    """Atom object for FHI-aims

    Parameters
    ----------
    symbol: Sequence[str]
        List of symbols for each nucleus in the structure
    number: Optional[Sequence[int]]
        Atomic number for the nuclei
    position: Sequence[Vector3D]
        The position of each nucleus in space
    fractional_position: Optional[Sequence[Vector3D]]
        The fractional_position of the atoms
    velocity: Optional[Sequence[Vector3D]]
        The velocity of each nucleus in space
    initial_charge: Sequence[float]
        The initial charge for each nuclei
    initial_moment: Sequence[float]
        The initial magnetic moment for each nuclei
    constraints: Sequence[tuple[bool, bool, bool]]
        Fix_atom constraints for each nucleus and direction
    is_empty: Optional[Sequence[bool]]
        Specifies if site is for an empty_site
    constraint_region: Optional[Sequence[int | None]]
        Assigns the immediately preceding atom to the region labelled number. 
        number is the integer number of a spatial region, which must correspond to a 
        region defined by keyword constraint_electrons in file control.in
    is_pseudocore: Optional[Sequence[bool]]
        True if site is a pseudocore
    magnetic_response: Optional[Sequence[bool]]
        Includes the current atom in the magnetic response calculations. If only
        the magnetizability is required, this keyword need not be used in geometry.in.
        Otherwise, the calculation of the shieldings or J-couplings is aborted if no atoms
        are flagged for MR calculations in geometry.in
    magnetic_moment: Optional[Sequence[float]]
        Overrides the default magnetic moment for the given atom. The default values 
        (in units of the nuclear magneton µN ) can be found in 
        MagneticResponse/MR_nuclear_data.f90. In case of J-couplings, the isotopes 
        used are also printed in the output.
    nuclear_spin: Optional[Sequence[float]]
        Overrides the default nuclear spin for the given atom. The default
        values can be found in MagneticResponse/MR_nuclear_data.f90 and are also
        printed in the output for J-coupling calculations.
    isotope: Optional[Sequence[int]]
        Overrides the default isotope mass number for the given atom. For
        more flexibility, the magnetic moment and spin can be specified separately
        with the above keywords. The default isotopes numbers can be found in
        MagneticResponse/MR_nuclear_data.f90.
    RT_TDDFT_initial_velocity: Sequence[Vector3D]
        Initial velocity of corresponding (i.e. last specified) atom when
        peforming RT-TDDFT-Ehrenfest dynamics
    """
    symbol: str = None
    number: int | None = None
    position: Vector3D = None
    fractional_position: Vector3D | None = None
    velocity: Vector3D | None = None
    initial_charge: float = 0.0
    initial_moment: float = 0.0
    constraints: tuple[bool, bool, bool] | None = None
    constraint_region: int | None = None
    magnetic_response: bool | None = None
    magnetic_moment: float | None = None
    nuclear_spin: float | None = None
    isotope: int | None = None 
    is_empty: bool = None
    is_pseudocore: bool = None
    RT_TDDFT_initial_velocity: Vector3D | None = None

    def __post_init__(self):
        self.number = ATOMIC_SYMBOLS_TO_NUMBERS[self.symbol]

    def set_fractional(self, lattice_vectors):
        self.fractional_position = np.linalg.solve(lattice_vectors.T, np.transpose(self.position)).T

    @property
    def geometry_in_block(self):
        content_str = "\natom      "
        pos = self.position
        if self.fractional_position is not None:
            content_str = "\natom_frac "
            pos = self.fractional_position

        if self.is_empty:
            content_str = "\nempty     "
        elif self.is_pseudocore:
            content_str = "\npseudocore"
        
        content_str += " " + " ".join([f"{pi:>20.12e}" for pi in pos]) 
        content_str += f" {self.symbol}"

        if self.velocity is not None:
            content_str += f"\n    velocity " + " ".join([f"{vel:>20.12e}" for vel in self.velocity])

        if np.abs(self.initial_charge) > 1e-12:
                content_str += f"\n    initial_charge {self.initial_charge:.12f}"
            
        if self.initial_moment > 1e-12:
            content_str += f"\n    initial_moment {self.initial_moment:.12f}"
        
        if self.constraints is not None and np.any(self.constraints):
            content_str += f"\n    constrain_relaxation "
            if self.constraints[0]:
                content_str += "x "
            if self.constraints[1]:
                content_str += "y "
            if self.constraints[2]:
                content_str += "z "
        if self.constraint_region is not None and self.constraint_region > 0:
            content_str += f"\n    constraint_region {self.constraint_region}"

        if self.magnetic_response is not None and self.magnetic_response:
            content_str += f"\n    magnetic_response"
        if self.magnetic_moment is not None and np.abs(self.magnetic_moment) > 1e-12:
            content_str += f"\n    magnetic_moment {self.magnetic_moment:.12f}"
        if self.nuclear_spin is not None and np.abs(self.nuclear_spin) > 1e-12:
            content_str += f"\n    nuclear_spin {self.nuclear_spin:.12f}"
        if self.isotope is not None and self.isotope > 0:
            content_str += f"\n    isotope {self.isotope}"
        if self.RT_TDDFT_initial_velocity is not None:
            content_str += f"\n    RT_TDDFT_initial_velocity "
            content_str += " ".join([f"{vel:>20.12e}" for vel in self.RT_TDDFT_initial_velocity])

        return content_str

