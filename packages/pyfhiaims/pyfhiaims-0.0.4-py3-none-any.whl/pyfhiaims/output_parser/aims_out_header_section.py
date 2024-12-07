"""AIMS output parser for the header section, taken from ASE with modifications."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING
import numpy as np

from pyfhiaims.geometry.geometry import AimsGeometry
from pyfhiaims.geometry.geometry import Matrix3D
from pyfhiaims.output_parser.aims_out_section import AimsOutSection, AimsParseError
if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any

    from pymatgen.util.typing import Vector3D

__author__ = "Thomas A. R. Purcell and Andrey Sobolev"
__version__ = "1.0"
__email__ = "purcellt@arizona.edu and andrey.n.sobolev@gmail.com"
__date__ = "July 2024"

# TARP: Originally an object, but type hinting needs this to be an int
LINE_NOT_FOUND = -1000
EV_PER_A3_TO_KBAR = 1.60217653e-19 * 1e22

PARSE_HEADER_KEYS: dict[str, list[str]] = {
    "commit_hash": ["Commit number"],
    "aims_uuid": ["aims_uuid"],
    "version_number": ["FHI-aims version"],
    "fortran_compiler": ["Fortran compiler      :"],
    "c_compiler": ["C compiler            :"],
    "fortran_compiler_flags": ["Fortran compiler flags"],
    "c_compiler_flags": ["C compiler flags"],
    "linked_against": ["Linking against:"],
    "initial_geometry": ["Parsing geometry.in (first pass over file, find array dimensions only)."],
    "is_md": ["Complete information for previous time-step:"],
    "is_relaxation": ["Geometry relaxation:"],
    "n_atoms": ["| Number of atoms"],
    "n_bands": [
        "Number of Kohn-Sham states",
        "Reducing total number of  Kohn-Sham states",
        "Reducing total number of Kohn-Sham states",
    ],
    "n_electrons": ["The structure contains"],
    "n_kpts": ["| Number of k-points"],
    "n_spins": ["| Number of spin channels"],
    "electronic_temp": ["Occupation type:"],
    "k_points": ["| K-points in task"],
    "end_k_points": ["| k-point:"],
    "build_type": ["Using"],
}

@dataclass
class AimsOutHeaderSection(AimsOutSection):
    """The header of the aims.out file containing general information."""

    def __post_init__(self):
        """Setup line parsing"""
        self.set_prop_line_relations(PARSE_HEADER_KEYS)
    
    @property
    def commit_hash(self) -> str:
        """The commit hash for the FHI-aims version."""
        return self._parse_key_value_pair("commit_hash")

    @property
    def aims_uuid(self) -> str:
        """The aims-uuid for the calculation."""
        return self._parse_key_value_pair("aims_uuid")

    @property
    def version_number(self) -> str:
        """The version number for the FHI-aims version."""
        return self._parse_key_value_pair("version_number")

    @property
    def fortran_compiler(self) -> str | None:
        """The fortran compiler used to make FHI-aims."""
        return self._parse_key_value_pair("fortran_compiler")

    @property
    def c_compiler(self) -> str | None:
        """The C compiler used to make FHI-aims."""
        return self._parse_key_value_pair("c_compiler", True)

    @property
    def fortran_compiler_flags(self) -> str | None:
        """The fortran compiler flags used to make FHI-aims."""
        return self._parse_key_value_pair("fortran_compiler_flags")

    @property
    def c_compiler_flags(self) -> str | None:
        """The C compiler flags used to make FHI-aims."""
        return self._parse_key_value_pair("c_compiler_flags", True)

    @property
    def build_type(self) -> list[str]:
        """The optional build flags passed to cmake."""
        if "build_type" in self._cache:
            return self._cache["build_type"]
        
        line_inds = self.get_line_inds("build_type")
        end_line = 0
        while end_line < len(line_inds) and "parallel tasks." not in self.lines[line_inds[end_line]]:
            end_line += 1

        self._cache["build_type"] = [" ".join(self.lines[line_inds[ind]].split()[1:]).strip() for ind in line_inds[:end_line]]
        return self._cache["build_type"]

    @property
    def linked_against(self) -> list[str]:
        """All libraries used to link the FHI-aims executable."""
        if "linked_against" in self._cache:
            return self._cache["linked_against"]
        
        try:
            line_start = self.get_line_inds("linked_against")[-1]
        except IndexError:
            self._cache["linked_against"] = []
            return []

        linked_libs = [self.lines[line_start].split(":")[1].strip()]
        line_start += 1
        while "lib" in self.lines[line_start]:
            linked_libs.append(self.lines[line_start].strip())
            line_start += 1

        self._cache["linked_against"] = linked_libs
        return linked_libs

    @property
    def initial_lattice(self) -> Matrix3D | None:
        """The initial lattice vectors from the aims.out file."""
        return self.initial_geometry.lattice_vectors

    @property
    def initial_geometry(self) -> AimsGeometry:
        """The initial structure.

        Using the FHI-aims output file recreate the initial structure for
        the calculation.
        """
        if "initial_geometry" in self._cache:
            return self._cache["initial_geometry"]
        
        try:
            line_start = self.get_line_inds("initial_geometry")[-1]
        except IndexError:
            raise AimsParseError("No information about the geometry in the section.")

        while "---------" not in self.lines[line_start]:
            line_start += 1
        
        line_start += 1
        line_end = line_start + 1
        while "---------" not in self.lines[line_end]:
            line_end += 1
        
        self._cache["initial_geometry"] = AimsGeometry.from_strings(self.lines[line_start:line_end])
        return self._cache["initial_geometry"]

    @property
    def initial_charges(self) -> Sequence[float]:
        """The initial charges for the structure."""
        return self.initial_geometry.initial_charge

    @property
    def initial_magnetic_moments(self) -> Sequence[float]:
        """The initial magnetic Moments."""
        return self.initial_geometry.initial_moment

    @property
    def is_md(self) -> bool:
        """Is the output for a molecular dynamics calculation?"""
        return len(self.get_line_inds("is_md")) > 0

    @property
    def is_relaxation(self) -> bool:
        """Is the output for a relaxation?"""
        return len(self.get_line_inds("is_relaxation")) > 0

    def _parse_k_points(self) -> None:
        """Parse the list of k-points used in the calculation."""
        n_kpts = self.n_k_points
        if n_kpts is None:
            self._cache.update(
                {
                    "k_points": None,
                    "k_point_weights": None,
                }
            )
            return

        try:
            line_start = self.get_line_inds("k_points")[-1]
            line_end = self.get_line_inds("end_k_points")[-1]
        except IndexError:
            self._cache.update(
                {
                    "k_points": None,
                    "k_point_weights": None,
                }
            )
            return

        k_points = np.zeros((n_kpts, 3))
        k_point_weights = np.zeros(n_kpts)
        for kk, line in enumerate(self.lines[line_start + 1 : line_end + 1]):
            k_points[kk] = [float(inp) for inp in line.split()[4:7]]
            k_point_weights[kk] = float(line.split()[-1])

        self._cache.update(
            {
                "k_points": k_points,
                "k_point_weights": k_point_weights,
            }
        )

    @property
    def n_atoms(self) -> int:
        """The number of atoms for the material."""
        return self._parse_key_value_pair("n_atoms", dtype=int)


    @property
    def n_bands(self) -> int | None:
        """The number of Kohn-Sham states for the chunk."""
        if "n_bands" in self._cache:
            return self._cache["n_bands"]
        
        if "n_bands" not in self._prop_line_relation:
            return None

        try:
            line_start = self.get_line_inds("n_bands")[-1]
        except IndexError:
            raise AimsParseError(f"No information about n_bands in the aims-output file")
        
        self._cache["n_bands"] = int(self.lines[line_start].split(" ")[-1].split(".")[0].strip())
        return self._cache["n_bands"]

    @property
    def n_electrons(self) -> int | None:
        """The number of electrons for the chunk."""
        if "n_electrons" in self._cache:
            return self._cache["n_electrons"]
        
        try:
            line_start = self.get_line_inds("n_electrons")[-1]
        except IndexError:
            raise AimsParseError(f"No information about n_electrons in the aims-output file")
        
        self._cache["n_electrons"] = float(self.lines[line_start].split()[-2].strip())
        return self._cache["n_electrons"]

    @property
    def n_k_points(self) -> int | None:
        """The number of k_ppoints for the calculation."""
        n_kpts = self._parse_key_value_pair("n_kpts", allow_fail=True, dtype=int)
        if isinstance(n_kpts, str):
            self._cache["n_kpts"] = int(self._cache["n_kpts"])
        return self._cache["n_kpts"]

    @property
    def n_spins(self) -> int | None:
        """The number of spin channels for the chunk."""
        return self._parse_key_value_pair("n_spins", dtype=int)

    @property
    def electronic_temperature(self) -> float:
        """The electronic temperature for the chunk."""
        if "electronic_temperature" in self._cache:
            return self._cache["electronic_temperature"]
        
        try:
            line_start = self.get_line_inds("electronic_temp")[-1]
        except IndexError:
            # TARP: Default FHI-aims value
            self._cache["electronic_temperature"] = 0.0
            return 0.00

        line = self.lines[line_start]
        self._cache["electronic_temperature"] =  float(line.split("=")[-1].strip().split()[0])
        return self._cache["electronic_temperature"]

    @property
    def k_points(self) -> Sequence[Vector3D]:
        """All k-points listed in the calculation."""
        if "k_points" not in self._cache:
            self._parse_k_points()

        return self._cache["k_points"]

    @property
    def k_point_weights(self) -> Sequence[float]:
        """The k-point weights for the calculation."""
        if "k_point_weights" not in self._cache:
            self._parse_k_points()

        return self._cache["k_point_weights"]

    @property
    def header_summary(self) -> dict[str, Any]:
        """Dictionary summarizing the information inside the header."""
        return {
            "initial_geometry": self.initial_geometry,
            "initial_lattice": self.initial_lattice,
            "is_relaxation": self.is_relaxation,
            "is_md": self.is_md,
            "n_atoms": self.n_atoms,
            "n_bands": self.n_bands,
            "n_electrons": self.n_electrons,
            "n_spins": self.n_spins,
            "electronic_temperature": self.electronic_temperature,
            "n_k_points": self.n_k_points,
            "k_points": self.k_points,
            "k_point_weights": self.k_point_weights,
        }

    @property
    def metadata_summary(self) -> dict[str, list[str] | str | None]:
        """Dictionary containing all metadata for FHI-aims build."""
        return {
            "commit_hash": self.commit_hash,
            "aims_uuid": self.aims_uuid,
            "version_number": self.version_number,
            "fortran_compiler": self.fortran_compiler,
            "c_compiler": self.c_compiler,
            "fortran_compiler_flags": self.fortran_compiler_flags,
            "c_compiler_flags": self.c_compiler_flags,
            "build_type": self.build_type,
            "linked_against": self.linked_against,
        }

