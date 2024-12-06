"""A main pyaims class representing Calculation"""
from pyfhiaims.aims_input import AimsInput
from pyfhiaims.control import AimsControlIn
from pyfhiaims.geometry import AimsGeometry
from pyfhiaims.outputs.parser import StdoutParser


class AimsCalc:
    """An Aims calculation"""
    aims_input: AimsInput

    @classmethod
    def from_folder(cls, folder, aims_stdout: str = "aims.out", aims_stderr: str = None):
        """Get Aims Calculation from a folder with files."""

