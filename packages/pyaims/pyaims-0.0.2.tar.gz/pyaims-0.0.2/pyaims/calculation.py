"""A main pyaims class representing Calculation"""
from pyaims.aims_input import AimsInput
from pyaims.control import AimsControlIn
from pyaims.geometry import AimsGeometry
from pyaims.outputs.parser import StdoutParser


class AimsCalc:
    """An Aims calculation"""
    aims_input: AimsInput

    @classmethod
    def from_folder(cls, folder, aims_stdout: str = "aims.out", aims_stderr: str = None):
        """Get Aims Calculation from a folder with files."""

