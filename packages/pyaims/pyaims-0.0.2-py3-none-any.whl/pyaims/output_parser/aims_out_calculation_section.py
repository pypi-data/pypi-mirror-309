"""AIMS output parser, taken from ASE with modifications."""

from __future__ import annotations

import numpy as np

from typing import Any, Sequence

from pyaims.geometry.atom import FHIAimsAtom
from pyaims.geometry.geometry import AimsGeometry
from pyaims.output_parser.aims_out_section import AimsOutSection, AimsParseError
from pyaims.output_parser.aims_out_header_section import AimsOutHeaderSection
from pyaims.utils.typecast import Vector3D, Matrix3D, to_vector3d

PARSE_CALC_KEYS = {
    "geometry_start": [
        "Atomic structure (and velocities) as used in the preceding time step",
        "Updated atomic structure",
        "Atomic structure that was used in the preceding time step of the wrapper",
    ],
    "geometry_end": ['Writing the current geometry to file "geometry.in.next_step"'],
    "forces": ["Total atomic forces"],
    "stresses": ["Per atom stress (eV) used for heat flux calculation"],
    "stress": [
        "Analytical stress tensor - Symmetrized",
        "Numerical stress tensor",
    ],
    "is_metallic": ["material is metallic within the approximate finite broadening function (occupation_type)"],
    "total_energy_uncorrected": ["Total energy uncorrected"],
    "total_energy_corrected": ["Total energy corrected"],
    "free_energy": ["| Electronic free energy"],
    "number_of_iterations": ["| Number of self-consistency cycles"],
    "magnetic_moment": ["N_up - N_down"],
    "fermi_energy": ["| Chemical potential (Fermi level)"],
    "dipole": ["Total dipole moment [eAng]"],
    "dielectric_tensor": ["PARSE DFPT_dielectric_tensor"],
    "polarization": ["| Cartesian Polarization"],
    "homo": ["Highest occupied state"],
    "lumo": ["Lowest unoccupied state"],
    "gap": ["verall HOMO-LUMO gap"],
    "direct_gap": ["Smallest direct gap"],
    "hirshfeld_charge": ["Hirshfeld charge"],
    "hirshfeld_volume": ["Hirshfeld volume"],
    "hirshfeld_dipole": ["Hirshfeld dipole vector"],
    "mulliken_charges": ["Summary of the per-atom charge analysis"],
    "mulliken_spins": ["Summary of the per-atom spin analysis"],
}


class AimsOutCalcSection(AimsOutSection):
    """A part of the aims.out file corresponding to a single structure."""

    def __init__(self, lines: list[str], header: AimsOutHeaderSection) -> None:
        """Construct the AimsOutCalcChunk.

        Args:
            lines (list[str]): The lines used for the structure
            header (.AimsOutHeaderChunk):  A summary of the relevant information from
                the aims.out header
        """
        super().__init__(lines)
        self._header = header
        self.set_prop_line_relations(PARSE_CALC_KEYS)

    def _parse_geometry(self) -> AimsGeometry:
        """Parse a structure object from the file.

        For the given section of the aims output file generate the
        calculated structure.

        Returns:
            The structure or molecule for the calculation
        """
        symbols, positions, velocities, lattice = self._parse_lattice_atom_pos()
        atoms = []
        for aa, atom in enumerate(self.initial_geometry.atoms):
            atoms.append(
                FHIAimsAtom(
                    symbol=symbols[aa],
                    position=positions[aa],
                    velocity=velocities.get(aa),
                    constraints=atom.constraints,
                    constraint_region=atom.constraint_region,
                    magnetic_response=atom.magnetic_response,
                    magnetic_moment=atom.magnetic_moment,
                    nuclear_spin=atom.nuclear_spin,
                    isotope=atom.isotope,
                    is_empty=atom.is_empty,
                    is_pseudocore=atom.is_pseudocore,
                    RT_TDDFT_initial_velocity=atom.RT_TDDFT_initial_velocity,
                )
            )
        return AimsGeometry(
            atoms=atoms,
            lattice_vectors=lattice,
            lattice_constraints=self.initial_geometry.lattice_constraints,
            hessian_block=self.initial_geometry.hessian_block,
            hessian_block_lv=self.initial_geometry.hessian_block_lv,
            hessian_block_lv_atoms=self.initial_geometry.hessian_block_lv_atoms,
            hessian_file=self.initial_geometry.hessian_file,
            trust_radius=self.initial_geometry.trust_radius,
            symmetry_n_params=self.initial_geometry.symmetry_n_params,
            symmetry_params=self.initial_geometry.symmetry_params,
            symmetry_lv=self.initial_geometry.symmetry_lv,
            symmetry_frac=self.initial_geometry.symmetry_frac,
            symmetry_frac_change_threshold=self.initial_geometry.symmetry_frac_change_threshold,
            homogeneous_field=self.initial_geometry.homogeneous_field,
            multipole=self.initial_geometry.multipole,
            esp_constraint=self.initial_geometry.esp_constraint,
            verbatim_writeout=self.initial_geometry.verbatim_writeout,
            calculate_friction=self.initial_geometry.calculate_friction,
        )

    def _parse_lattice_atom_pos(
        self,
    ) -> tuple[list[str], list[Vector3D], dict[int, Vector3D], Matrix3D | None]:
        """Parse the lattice and atomic positions of the structure.

        Returns:
            list[str]: The species symbols for the atoms in the structure
            list[Vector3D]: The Cartesian coordinates of the atoms
            list[Vector3D]: The velocities of the atoms
            Lattice or None: The Lattice for the structure
        """
        
        try:
            line_start = self.get_line_inds("geometry_start")[-1]
        except IndexError:
            return (
                self.initial_geometry.symbols, 
                self.initial_geometry.positions, 
                {aa: vel for aa, vel in enumerate(self.initial_geometry.velocities)},
                self.initial_geometry.lattice_vectors
            )


        lattice_vectors: list[list[float]] = []
        velocities: dict[int, Vector3D] = {}
        symbols: list[str] = []
        coords: list[Vector3D] = []

        line_start += 1
        try:
            line_end = self.get_line_inds("geometry_end")[-1]
        except IndexError:
            line_end = len(self.lines)

        for line in self.lines[line_start:line_end]:
            if "lattice_vector   " in line:
                lattice_vectors.append([float(inp) for inp in line.split()[1:]])
            elif "atom " in line:
                line_split = line.split()
                symbols.append(line_split[4])
                coords.append(to_vector3d([float(x) for x in line_split[1:4]]))
            elif "velocity " in line:
                velocities[len(symbols) - 1] = to_vector3d([float(x) for x in line.split()[1:4]])

        lattice = np.array(lattice_vectors) if len(lattice_vectors) == 3 else None
        return symbols, coords, velocities, lattice

    @property
    def symbols(self) -> list[str]:
        """The list of atomic symbols for all atoms in the structure."""
        return self.geometry.symbols

    @property
    def positions(self) -> list[str]:
        """The list of atomic positions for all atoms in the structure."""
        return self.geometry.positions

    @property
    def velocities(self) -> list[str]:
        """The list of atomic velocities for all atoms in the structure."""
        return self.geometry.velocities
    
    @property
    def lattice(self) -> Matrix3D | None:
        """The lattice vectors for the geometry."""
        return self.geometry.lattice_vectors

    @property
    def forces(self) -> np.array[Vector3D] | None:
        """The forces from the aims.out file."""
        if "forces" in self._cache:
            return self._cache["forces"]
        
        try:
            line_start = self.get_line_inds("forces")[-1]
        except IndexError:
            self._cache["forces"] = None
            return None

        line_start += 1
        self._cache["forces"] = np.array(
            [[float(inp) for inp in line.split()[-3:]] for line in self.lines[line_start : line_start + self.n_atoms]]
        )
        return self._cache["forces"]

    @property
    def stresses(self) -> np.array[Matrix3D] | None:
        """The stresses from the aims.out file and convert to kbar."""
        if "stresses" in self._cache:
            return self._cache["stresses"]
        
        try:
            line_start = self.get_line_inds("stresses")[-1]
        except IndexError:
            self._cache["stresses"] = None
            return None

        line_start += 3
        stresses = []
        for line in self.lines[line_start : line_start + self.n_atoms]:
            xx, yy, zz, xy, xz, yz = (float(d) for d in line.split()[2:8])
            stresses.append(np.array([[xx, xy, xz], [xy, yy, yz], [xz, yz, zz]]))

        self._cache["stresses"] = np.array(stresses)
        return  self._cache["stresses"]

    @property
    def stress(self) -> Matrix3D | None:
        """The stress from the aims.out file and convert to kbar."""
        if "stress" in self._cache:
            return self._cache["stress"]
        
        try:
            line_start = self.get_line_inds("stress")[-1]
        except IndexError:
            self._cache["stress"] = None
            return None
        stress = [[float(inp) for inp in line.split()[2:5]] for line in self.lines[line_start + 5 : line_start + 8]]
        self._cache["stress"] = np.array(stress)
        return self._cache["stress"]

    @property
    def is_metallic(self) -> bool:
        """Is the system is metallic."""
        return len(self.get_line_inds("is_metallic")) > 0

    @property
    def total_corrected_energy(self) -> float:
        """The total corrected energy from the aims.out file."""
        if "total_energy_corrected" in self._cache:
            return self._cache["total_energy_corrected"]
        
        try:
            line_ind = self.get_line_inds("total_energy_corrected")[-1]
        except IndexError:
            raise AimsParseError("No energy is associated with the structure.")

        self._cache["total_energy_corrected"] = float(self.lines[line_ind].split()[5])
        return self._cache["total_energy_corrected"]

    @property
    def total_uncorrected_energy(self) -> float:
        """The total uncorrected energy from the aims.out file."""
        if "total_energy_uncorrected" in self._cache:
            return self._cache["total_energy_uncorrected"]
        
        try:
            line_ind = self.get_line_inds("total_energy_uncorrected")[-1]
        except IndexError:
            raise AimsParseError("No energy is associated with the structure.")

        self._cache["total_energy_uncorrected"] = float(self.lines[line_ind].split()[5])
        return self._cache["total_energy_uncorrected"]

    @property
    def free_energy(self) -> float:
        """The total uncorrected energy from the aims.out file."""
        if "free_energy" in self._cache:
            return self._cache["free_energy"]
        
        try:
            line_ind = self.get_line_inds("free_energy")[-1]
        except IndexError:
            raise AimsParseError("No energy is associated with the structure.")

        self._cache["free_energy"] = float(self.lines[line_ind].split()[5])
        return self._cache["free_energy"]
    
    @property
    def total_energy(self) -> float:
        """The total energy of the structure"""
        if self.is_metallic and len(self.initial_geometry.lattice_vectors) == 3:
            return self.total_corrected_energy
        return self.total_uncorrected_energy

    @property
    def energy(self) -> float:
        """The force-consistent energy of the system"""
        return self.free_energy

    @property
    def dipole(self) -> Vector3D | None:
        """The electric dipole moment from the aims.out file."""
        if "dipole" in self._cache:
            return self._cache["dipole"]
        
        try:
            line_start = self.get_line_inds("dipole")[-1]
        except IndexError:
            self._cache["dipole"] = None
            return None

        print(self.lines[line_start])
        self._cache["dipole"] = np.array(
            [float(inp) for inp in self.lines[line_start].split()[6:9]]
        )
        return self._cache["dipole"]

    @property
    def dielectric_tensor(self) -> Matrix3D | None:
        """The dielectric tensor from the aims.out file."""
        if "dielectric_tensor" in self._cache:
            return self._cache["dielectric_tensor"]
        
        try:
            line_start = self.get_line_inds("dielectric_tensor")[-1]
        except IndexError:
            self._cache["dielectric_tensor"] = None
            return None

        # we should find the tensor in the next three lines:
        lines = self.lines[line_start + 1 : line_start + 4]

        # make ndarray and return
        self._cache["dielectric_tensor"] = np.array([np.fromstring(line, sep=" ") for line in lines])
        return self._cache["dielectric_tensor"]
    
    @property
    def polarization(self) -> Vector3D | None:
        """The polarization vector from the aims.out file."""
        if "polarization" in self._cache:
            return self._cache["polarization"]
        
        try:
            line_start = self.get_line_inds("polarization")[-1]
        except IndexError:
            self._cache["polarization"] = None
            return None
        
        self._cache["polarization"] = np.array([float(s) for s in self.lines[line_start].split()[-3:]])
        return self._cache["polarization"]


    def _parse_hirshfeld(
        self,
    ) -> None:
        """Parse the Hirshfled charges volumes, and dipole moments."""
        hirshfeld_charges = np.array(
            [float(self.lines[ind].split(":")[1]) for ind in self.get_line_inds("hirshfeld_charge")]
        )

        if len(hirshfeld_charges) != self.n_atoms:
            self._cache.update(
                {
                    "hirshfeld_charges": None,
                    "hirshfeld_volumes": None,
                    "hirshfeld_atomic_dipoles": None,
                    "hirshfeld_dipole": None,
                }
            )
            return
        
        hirshfeld_volumes = np.array(
            [float(self.lines[ind].split(":")[1]) for ind in self.get_line_inds("hirshfeld_volume")]
        )
        
        hirshfeld_atomic_dipoles = np.array(
            [[float(inp) for inp in self.lines[ind].split(":")[1].split()] for ind in self.get_line_inds("hirshfeld_dipole")]
        )

        if self.geometry.lattice_vectors is None:
            hirshfeld_dipole = np.sum(
                hirshfeld_charges.reshape((-1, 1)) * self.positions,
                axis=1,
            )
        else:
            hirshfeld_dipole = None

        self._cache.update(
            {
                "hirshfeld_charges": hirshfeld_charges,
                "hirshfeld_volumes": hirshfeld_volumes,
                "hirshfeld_atomic_dipoles": hirshfeld_atomic_dipoles,
                "hirshfeld_dipole": hirshfeld_dipole,
            }
        )

    def _parse_mulliken(
        self,
    ) -> None:
        """Parse the Mulliken charges and spins."""

        try:
            line_start = self.get_line_inds("mulliken_charges")[-1]
        except IndexError:
            self._cache.update(
                {
                    "mulliken_charges": None,
                    "mulliken_spins": None,
                }   
            )
            return
        
        mulliken_charges = np.array(
            [float(self.lines[ind].split()[3]) for ind in range(line_start + 3, line_start + 3 + self.n_atoms)]
        )

        try:
            line_start = self.get_line_inds("mulliken_spins")[-1]
        except IndexError:
            self._cache.update(
                {
                    "mulliken_charges": mulliken_charges,
                    "mulliken_spins": None,
                }   
            )
            return
        
        mulliken_spins = np.array(
            [float(self.lines[ind].split()[2]) for ind in range(line_start + 3, line_start + 3 + self.n_atoms)]
        )

        self._cache.update(
            {
                "mulliken_charges": mulliken_charges,
                "mulliken_spins": mulliken_spins,
            }
        )

    @property
    def geometry(self) -> AimsGeometry:
        """The pytmagen SiteCollection of the chunk."""
        if "geometry" not in self._cache:
            self._cache["geometry"] = self._parse_geometry()
        return self._cache["geometry"]

    @property
    def results(self) -> dict[str, Any]:
        """Get to a results dictionary for the section."""
        results = {
            "energy": self.energy,
            "free_energy": self.free_energy,
            "forces": self.forces,
            "stress": self.stress,
            "stresses": self.stresses,
            "magmom": self.magmom,
            "dipole": self.dipole,
            "fermi_energy": self.E_f,
            "n_iter": self.n_iter,
            "mulliken_charges": self.mulliken_charges,
            "mulliken_spins": self.mulliken_spins,
            "hirshfeld_charges": self.hirshfeld_charges,
            "hirshfeld_dipole": self.hirshfeld_dipole,
            "hirshfeld_volumes": self.hirshfeld_volumes,
            "hirshfeld_atomic_dipoles": self.hirshfeld_atomic_dipoles,
            "dielectric_tensor": self.dielectric_tensor,
            "polarization": self.polarization,
            "homo": self.homo,
            "lumo": self.lumo,
            "gap": self.gap,
            "direct_gap": self.direct_gap,
        }

        return {key: value for key, value in results.items() if value is not None}

    # Properties from the aims.out header
    @property
    def initial_geometry(self) -> AimsGeometry:
        """The initial structure for the calculation."""
        return self._header.initial_geometry

    @property
    def n_atoms(self) -> int:
        """The number of atoms in the structure."""
        return self._header.n_atoms

    @property
    def n_bands(self) -> int:
        """The number of Kohn-Sham states for the chunk."""
        return self._header.n_bands

    @property
    def n_electrons(self) -> int:
        """The number of electrons for the chunk."""
        return self._header.n_electrons

    @property
    def n_spins(self) -> int:
        """The number of spin channels for the chunk."""
        return self._header.n_spins

    @property
    def electronic_temperature(self) -> float:
        """The electronic temperature for the chunk."""
        return self._header.electronic_temperature

    @property
    def n_k_points(self) -> int:
        """The number of k_ppoints for the calculation."""
        return self._header.n_k_points

    @property
    def k_points(self) -> Sequence[Vector3D]:
        """All k-points listed in the calculation."""
        return self._header.k_points

    @property
    def k_point_weights(self) -> Sequence[float]:
        """The k-point weights for the calculation."""
        return self._header.k_point_weights

    @property
    def n_iter(self) -> int | None:
        """The number of steps needed to converge the SCF cycle for the chunk."""
        return self._parse_key_value_pair("number_of_iterations", allow_fail=True, dtype=int)

    @property
    def magmom(self) -> float | None:
        """The magnetic moment of the structure."""
        return self._parse_key_value_pair("magnetic_moment", allow_fail=True, dtype=float)

    @property
    def E_f(self) -> float | None:
        """The Fermi energy."""
        fermi_energy = self._parse_key_value_pair("fermi_energy", allow_fail=True)
        
        if isinstance(fermi_energy, str):
            self._cache["fermi_energy"] = float(fermi_energy.split(" eV")[0]) 

        return self._cache["fermi_energy"]

    @property
    def converged(self) -> bool:
        """True if the calculation is converged."""
        return (len(self.lines) > 0) and ("Have a nice day." in self.lines[-5:])

    @property
    def mulliken_charges(self) -> Sequence[float] | None:
        """The Mulliken charges of the system"""
        if "mulliken_charges" not in self._cache:
            self._parse_mulliken()
        return self._cache["mulliken_charges"]

    @property
    def mulliken_spins(self) -> Sequence[float] | None:
        """The Mulliken spins of the system"""
        if "mulliken_spins" not in self._cache:
            self._parse_mulliken()
        return self._cache["mulliken_spins"]

    @property
    def hirshfeld_charges(self) -> Sequence[float] | None:
        """The Hirshfeld charges of the system."""
        if "hirshfeld_charges" not in self._cache:
            self._parse_hirshfeld()
        return self._cache["hirshfeld_charges"]

    @property
    def hirshfeld_atomic_dipoles(self) -> Sequence[Vector3D] | None:
        """The Hirshfeld atomic dipoles of the system."""
        if "hirshfeld_atomic_dipoles" not in self._cache:
            self._parse_hirshfeld()
        return self._cache["hirshfeld_atomic_dipoles"]

    @property
    def hirshfeld_volumes(self) -> Sequence[float] | None:
        """The Hirshfeld atomic dipoles of the system."""
        if "hirshfeld_volumes" not in self._cache:
            self._parse_hirshfeld()
        return self._cache["hirshfeld_volumes"]

    @property
    def hirshfeld_dipole(self) -> None | Vector3D:
        """The Hirshfeld dipole of the system."""
        if "hirshfeld_dipole" not in self._cache:
            self._parse_hirshfeld()

        return self._cache["hirshfeld_dipole"]

    @property
    def homo(self) -> float:
        """The valance band maximum."""
        if "homo" in self._cache:
            return self._cache["homo"]
        
        if "homo" not in self._prop_line_relation:
            return None

        try:
            line_start = self.get_line_inds("homo")[-1]
        except IndexError:
            raise AimsParseError(f"No information about homo in the aims-output file")
        
        self._cache["homo"] = float(self.lines[line_start].split(" at ")[1].split(" eV")[0].strip())
        return self._cache["homo"]

    @property
    def lumo(self) -> float:
        """The conduction band minimnum."""
        if "lumo" in self._cache:
            return self._cache["lumo"]
        
        if "lumo" not in self._prop_line_relation:
            return None

        try:
            line_start = self.get_line_inds("lumo")[-1]
        except IndexError:
            raise AimsParseError(f"No information about lumo in the aims-output file")
        
        self._cache["lumo"] = float(self.lines[line_start].split(" at ")[1].split(" eV")[0].strip())
        return self._cache["lumo"]

    @property
    def gap(self) -> float:
        """The band gap."""
        return float(self._parse_key_value_pair("gap").split(" eV")[0])

    @property
    def direct_gap(self) -> float:
        """The direct bandgap."""
        direct_gap = self._parse_key_value_pair("direct_gap", allow_fail=True)
        if direct_gap is None:
            return self.gap
        
        return float(direct_gap.split(" eV")[0])

