"""Classes for reading/manipulating/writing FHI-aims control.in files."""
from __future__ import annotations

import re
import time
from copy import deepcopy
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import TYPE_CHECKING
from warnings import warn

from monty.json import MontyDecoder, MSONable

from pyaims.control.kpoints import AimsKPoints
from pyaims.errors import PyaimsError
from pyaims.geometry.geometry import AimsGeometry
from pyaims.species_defaults.species import SpeciesDefaults

if TYPE_CHECKING:
    from typing import Any
    from typing_extensions import Self

__author__ = "Thomas A. R. Purcell"
__version__ = "1.0"
__email__ = "purcellt@arizona.edu"
__date__ = "July 2024"


@dataclass
class AimsControlIn(MSONable):
    """An FHI-aims control.in file.

    Attributes:
        parameters (dict[str, Any]): The parameters' dictionary containing all input
            flags (key) and values for the control.in file
    """

    parameters: dict[str, Any] = field(default_factory=dict)
    outputs: list[str] = field(default_factory=list)
    k_points: AimsKPoints = None
    species_defaults: dict[str, SpeciesDefaults] = field(default_factory=dict)  # None?

    def __getitem__(self, key: str) -> Any:
        """Get an input parameter.

        Args:
            key (str): The parameter to get

        Returns:
            The setting for that parameter

        Raises:
            KeyError: If the key is not in self._parameters
        """
        if key == "output":
            return self.outputs

        if key not in self.parameters:
            raise KeyError(f"{key} not set in AimsControlIn")
        return self.parameters[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """Set an attribute of the class.

        Args:
            key (str): The parameter to get
            value (Any): The value for that parameter
        """
        if key == "output":
            warn(
                "Outputs are set seperately, use the outputs property", 
                RuntimeWarning, 
                stacklevel=1
            )
        else:
            self.parameters[key] = value

    def __delitem__(self, key: str) -> Any:
        """Delete a parameter from the input object.

        Args:
        key (str): The key in the parameter to remove

        Returns:
            Either the value of the deleted parameter or None if key is
            not in self._parameters
        """
        if key == "output":
            self.outputs = []

        return self.parameters.pop(key, None)

    @staticmethod
    def get_aims_control_parameter_str(key: str, value: Any, fmt: str) -> str:
        """Get the string needed to add a parameter to the control.in file.

        Args:
            key (str): The name of the input flag
            value (Any): The value to be set for the flag
            fmt (str): The format string to apply to the value

        Returns:
            str: The line to add to the control.in file
        """
        if value is None:
            return ""
        return f"{key:50s}{fmt % value}\n"

    def get_content(
        self, geometry: AimsGeometry, verbose_header: bool = False, directory: str | Path | None = None
    ) -> str:
        """Get the content of the file.

        Args:
            geometry (AimsGeometry): The geometry to write the input file for
            verbose_header (bool): If True print the input option dictionary
            directory: str | Path | None = The directory for the calculation,

        Returns:
            str: The content of the file for a given geometry
        """
        parameters = deepcopy(self.parameters)

        if directory is None:
            directory = ""

        lim = "#" + "=" * 79
        content = ""

        if parameters["xc"] == "LDA":
            parameters["xc"] = "pw-lda"

        cubes = parameters.pop("cubes", [])

        if verbose_header:
            content += "# \n# List of parameters used to initialize the calculator:"
            for param, val in parameters.items():
                content += f"#     {param}:{val}\n"
        content += f"{lim}\n"

        if all([inp in parameters for inp in ["smearing", "occupation_type"]]):
            raise ValueError("Both smearing and occupation_type can't be in the same parameters file.")

        for key, value in parameters.items():
            if key in ["species_dir", "plus_u"]:
                continue
            if key == "smearing":
                name = parameters["smearing"][0].lower()
                if name == "fermi-dirac":
                    name = "fermi"
                width = parameters["smearing"][1]
                if name == "methfessel-paxton":
                    order = parameters["smearing"][2]
                    order = " %d" % order
                else:
                    order = ""

                content += self.get_aims_control_parameter_str("occupation_type", (name, width, order), "%s %f%s")
            elif key == "vdw_correction_hirshfeld" and value:
                content += self.get_aims_control_parameter_str(key, "", "%s")
            elif isinstance(value, bool):
                content += self.get_aims_control_parameter_str(key, str(value).lower(), ".%s.")
            elif isinstance(value, (tuple, list)):
                content += self.get_aims_control_parameter_str(key, " ".join(map(str, value)), "%s")
            elif isinstance(value, str):
                content += self.get_aims_control_parameter_str(key, value, "%s")
            else:
                content += self.get_aims_control_parameter_str(key, value, "%r")

        for output_type in self.outputs:
            content += self.get_aims_control_parameter_str("output", output_type, "%s")

        if cubes:
            for cube in cubes:
                content += cube.control_block

        content += f"{lim}\n\n"
        
        for sp in geometry.species_dict.values():
            content += sp.content

        return content

    def write_file(
        self,
        geometry: AimsGeometry,
        directory: str | Path | None = None,
        verbose_header: bool = False,
        overwrite: bool = False,
    ) -> None:
        """Write the control.in file.

        Args:
            geometry (AimsGeometry): The structure to write the input
                file for
            directory (str or Path): The directory to write the control.in file.
                If None use cwd
            verbose_header (bool): If True print the input option dictionary
            overwrite (bool): If True allow to overwrite existing files

        Raises:
            ValueError: If a file must be overwritten and overwrite is False
            ValueError: If k-grid is not provided for the periodic structures
        """
        directory = directory or Path.cwd()

        if (Path(directory) / "control.in").exists() and not overwrite:
            raise ValueError(f"control.in file already in {directory}")

        if (geometry.lattice_vectors is not None) and (
            "k_grid" not in self.parameters and "k_grid_density" not in self.parameters
        ):
            raise ValueError("k-grid must be defined for periodic systems")

        content = self.get_content(geometry, verbose_header)

        with open(f"{directory}/control.in", mode="w") as file:
            file.write(f"#{'=' * 72}\n")
            file.write(f"# FHI-aims geometry file: {directory}/geometry.in\n")
            file.write("# File generated from pyaims\n")
            file.write(f"# {time.asctime()}\n")
            file.write(f"#{'=' * 72}\n")

            file.write(content)

    def as_dict(self) -> dict[str, Any]:
        """Get a dictionary representation of the geometry.in file."""
        dct: dict[str, Any] = {
            "@module": type(self).__module__,
            "@class": type(self).__name__,
            "parameters": self.parameters,
            "outputs": self.outputs
        }
        return dct

    @classmethod
    def from_file(cls, control_file: str | Path) -> "AimsControlIn":
        """Instantiate the Control object """
        with open(control_file, "r") as f:
            lines = f.read()
        parameters = {}
        outputs = []

        # get species' defaults from the file first
        species = {}
        species_re = re.compile(r"(?<=\n) *species.*?(?=\n *species|$)", re.DOTALL)
        species_lines = re.findall(species_re, lines)
        element_re = re.compile(r" *species *(\S+)", re.DOTALL)

        for block in species_lines:
            if re.match(element_re, block) is not None:
                element = re.match(element_re, block).group(1)
                species[element] = SpeciesDefaults.from_strings(block.split("\n"))

        # then everything else
        for line in lines:
            # remove comments and blank lines
            line = line[:line.find("#")].strip()
            if not line:
                continue
            # stop at species
            if line.startswith("species "):
                break
            k, v = line.split(maxsplit=1)
            if k == "output":
                if "cube" in v:
                    # TODO: does not work with Cubes yet
                    raise PyaimsError("Reading control.in from file does not work with cubes yet")
                outputs.append(v)
            else:
                parameters[k] = v
        return AimsControlIn(
            parameters=parameters,
            outputs=outputs,
            species_defaults=species
        )

    @classmethod
    def from_dict(cls, dct: dict[str, Any]) -> Self:
        """Initialize from dictionary.

        Args:
            dct (dict[str, Any]): The MontyEncoded dictionary

        Returns:
            The AimsControlIn for dct
        """
        decoded = {key: MontyDecoder().process_decoded(val) for key, val in dct.items() if not key.startswith("@")}

        return cls(parameters=decoded["parameters"], outputs=decoded["outputs"])

