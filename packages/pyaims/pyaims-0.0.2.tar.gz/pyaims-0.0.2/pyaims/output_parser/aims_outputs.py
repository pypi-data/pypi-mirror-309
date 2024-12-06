"""Object representing an aims output"""
from dataclasses import dataclass, field

import numpy as np
import json

from pyaims.output_parser.aims_out_calculation_section import AimsOutCalcSection
from pyaims.output_parser.aims_out_header_section import AimsOutHeaderSection
from pyaims.output_parser.aims_out_section import ParseError

from pyaims.control.control import AimsControlIn
from pyaims.geometry.geometry import AimsGeometry

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any

PARSABLE_RESULTS = [
    "energy",
    "free_energy",
    "forces",
    "stress",
    "stresses",
    "magmom",
    "dipole",
    "fermi_energy",
    "n_iter",
    "mulliken_charges",
    "mulliken_spins",
    "hirshfeld_charges",
    "hirshfeld_dipole",
    "hirshfeld_volumes",
    "hirshfeld_atomic_dipoles",
    "dielectric_tensor",
    "polarization",
    "homo",
    "lumo",
    "gap",
    "direct_gap",
]

@dataclass
class AimsCalculation:
    """Object to represent the aims outputs"""

    _geometry: AimsGeometry = None
    _results: dict[str, Any] = field(default=dict)

    def __getitem__(self, key:str) -> Any:
        """Get a particular result"""
        if key not in PARSABLE_RESULTS:
            raise ValueError("Requested item is not a parasable result")
        
        return self._results.get(key)
    
    @property
    def geometry(self):
        return self._geometry

@dataclass
class AimsOutput:
    _images: list[AimsCalculation] = None
    _input_geometry: AimsGeometry = None
    _input_control: AimsControlIn | None = None

    def get_image(self, ind):
        return self._images[ind]
    
    @property
    def get_n_images(self):
        return len(self._images)

    @classmethod
    def from_directory(cls, directory):
        """"""
        with open(f"{directory}/aims.out", "r") as fd:
            aims_out_lines = [line.strip() for line in fd.readlines()]

        with open(f"{directory}/parameters.json", "r") as param_json:
            parameters = json.load(param_json)
            aims_control_in = AimsControlIn.from_dict(parameters)

        return cls.from_aims_out_content(
            aims_out_lines,
            aims_control_in,
        )

    @classmethod
    def from_aims_out_file(cls, aims_outfile, aims_control_in=None):
        """"""
        with open(str(aims_outfile), "r") as fd:
            aims_out_lines = [line.strip() for line in fd.readlines()]

        return cls.from_aims_out_content(aims_out_lines, aims_control_in)
    
    @classmethod
    def from_aims_out_content(cls, aims_out_lines, aims_control_in=None):
        """"""
        header_lines = []
        stopped = False
        # Stop the header once the first SCF cycle begins
        for line in aims_out_lines:
            header_lines.append(line)
            if (
                "Convergence:    q app. |  density  | eigen (eV) | Etot (eV)" in line
                or "Begin self-consistency iteration #" in line
            ):
                stopped = True
                break

        if not stopped:
            raise ParseError("No SCF steps present, calculation failed at setup.")

        header = AimsOutHeaderSection(header_lines)
        if header.is_relaxation:
            section_end_line = "Geometry optimization: Attempting to predict improved coordinates."
        else:
            section_end_line = "Begin self-consistency loop: Re-initialization"

        # If SCF is not converged then do not treat the next chunk_end_line as a
        # new chunk until after the SCF is re-initialized
        ignore_chunk_end_line = False
        line_iter = iter(aims_out_lines)
        aims_sections = []
        while True:
            try:
                line = next(line_iter).strip()  # Raises StopIteration on empty file
            except StopIteration:
                break

            section_lines = []
            while section_end_line not in line or ignore_chunk_end_line:
                section_lines.append(line)
                # If SCF cycle not converged or numerical stresses are requested,
                # don't end chunk on next Re-initialization
                patterns = [
                    ("Self-consistency cycle not yet converged - restarting mixer to attempt better convergence."),
                    (
                        "Components of the stress tensor (for mathematical "
                        "background see comments in numerical_stress.f90)."
                    ),
                    "Calculation of numerical stress completed",
                ]
                if any(pattern in line for pattern in patterns):
                    ignore_chunk_end_line = True
                elif "Begin self-consistency loop: Re-initialization" in line:
                    ignore_chunk_end_line = False

                try:
                    line = next(line_iter).strip()
                except StopIteration:
                    break
            aims_sections.append(AimsOutCalcSection(section_lines, header))

        if header.is_relaxation and any("Final atomic structure:" in line for line in aims_sections[-1].lines):
            aims_sections[-2].lines += aims_sections[-1].lines
            aims_sections = aims_sections[:-1]
        
        aims_calculations = [AimsCalculation(_geometry=sec.geometry, _results=sec.results) for sec in aims_sections]

        return cls(
            _images=aims_calculations,
            _input_geometry=header.input_geometry,
            _input_control=aims_control_in,
        )
