"""An object representing parse results of FHI-aims standard output."""
import os.path
from pathlib import Path
from typing import IO, Any
from pyaims.outputs.parser import StdoutParser


class AimsStdout:

    def __init__(self, stdout_file: str | Path | IO):
        if isinstance(stdout_file, str | Path):
            self.file_name = Path(stdout_file).resolve().as_posix()
            file_path = Path(stdout_file)
            if not file_path.is_file():
                raise FileNotFoundError(f"FHI-aims output file {self.file_name} "
                                        f"does not exist")
        else:
            self.file_name = os.path.realpath(stdout_file.name)
        self._parser = StdoutParser(stdout_file)
        self._results = self._parser.parse()

    @property
    def results(self) -> dict[str, Any]:
        """A dictionary with results for FHI-aims calculation."""
        return self._results

    @property
    def metadata(self) -> dict[str, Any]:
        """A metadata dictionary for FHI-aims calculation, including runtime choices and
        some background calculation checks."""
        return self._parser.run_metadata

    @property
    def warnings(self) -> list[str]:
        """A list of warning messages for FHI-aims calculation.
        A warning message is the one beginning with an optional space and one or several
        asterisks."""
        return self._parser.warnings

    @property
    def errors(self) -> list[str]:
        """A list of error messages for FHI-aims calculation.
        An error message is a warning at the end of the file."""
        return self._parser.errors

    @property
    def is_finished_ok(self) -> bool:
        """A check if the calculation is finished successfully."""
        return self._results.get("is_finished_ok", False)

    @property
    def energy(self) -> float:
        """Energy value given after the calculation has finished"""
        if not self.is_finished_ok:
            raise ValueError("Calculation has not finished successfully")
        return self._results["final"]["energy"]

    @property
    def band_gap(self) -> float:
        """Band gap value from the last SCF step."""
        if not self.is_finished_ok:
            raise ValueError("Calculation has not finished successfully")
        return self._results["ionic_steps"][-1]["scf_steps"][-1]["gap"]

    @property
    def forces(self) -> list[float]:
        """Forces from the last ionic step if present."""
        return self._results["ionic_steps"][-1].get("atomic_forces", None)

    def __getattr__(self, item):
        """A shortcut to getting results."""
        if item in self._results:
            return self._results[item]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")