from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from pyfhiaims.geometry.atom import FHIAimsAtom, ATOMIC_SYMBOLS_TO_NUMBERS
from pyfhiaims.species_defaults.species import SpeciesDefaults

from typing import Sequence

from pathlib import Path

from pyfhiaims.utils.typecast import Vector3D, Matrix3D, to_matrix3d
from typing import Optional, Any


class InvalidGeometryError(Exception):
    """Exception raised if there is a problem with the input geometry"""

    def __init__(self, message: str) -> None:
        """Initialize the error with the message, message"""
        self.message = message
        super().__init__(self.message)


@dataclass
class AimsGeometry:
    """Geometry for the structure to run the calculation for
    
    Parameters
    ----------
    atoms: Sequence[FHIAimsAtom]
        The Atoms for the geometry
    lattice_vectors: Optional[Matrix3D]
        The initial set of lattice vectors for the structure
    lattice_constraints: Sequence[tuple[bool, bool, bool]]
        fix lattice constraints for each nucleus and direction
    species_dict: dict[str, SpeciesDefaults]
        Dictionary to get the species for each symbol in the structure
    hessian_block: Optional[Sequence[tuple[int, int, Matrix3D]]]
        In geometry.in, allows to specify a Hessian matrix explicitly, with one
        line for each 3×3 block.
        The option block consists of nine numbers in column-first
        (Fortran) order. The 3×3 block corresponding to j_atom, i_atom is initialized
        by the transposed of block. The Hessian matrix is input in units of eV/Å2.
    hessian_block_lv: Optional[Sequence[tuple[float, float, Matrix3D]]]
        hessian_block for lattice vectors
    hessian_block_lv_atoms: Optional[Sequence[tuple[float, float, Matrix3D]]]
        hessian_block for degrees of freedom between lattice vectors and atoms
    hessian_file: Optional[bool]
        Indicates that there exists a hessian.aims file to be used to construct 
        the Hessian.
    trust_radius: Optional[float]
        allows to specify the initial trust radius value for the trm 
        relaxation algorithm
    symmetry_n_params: Optional[tuple[int, int]]
        Number of parameters for the lattice and fractional degrees of freedom
    symmetry_params: Optional[Sequence[str]]
        The list of all parametric constraints parameters
    symmetry_lv: Optional[tuple[str, str, str]]
        The list of parametric constraints for the lattice_vectors
    symmetry_frac: Optional[Sequence[tuple[str, str, str]]]
        The list of parametric constraints for the fractional coordinates
    symmetry_frac_change_threshold: Optional[float]
        Specifies the maximum allowed change in the initial structure to any
        fractional coordinate after applying the parametric constraints. If set to 1.0,
        then these tests will be ignored. max_change is the maximum allowed change in 
        the fractional coordinates of an atom
    homogeneous_field: Optional[Vector3D]
        Allows performing a calculation for a system in a homogeneous electrical
        field E in units of V/AA.
    multipole: Optional[Sequence[tuple[float, float, float, int, float]]]
        Places the center of an electrostatic multipole field at a specified location, 
        to simulate an embedding potential.
            x : x coordinate of the multipole.
            y : y coordinate of the multipole.
            z : z coordinate of the multipole.
            order : Integer number, which specifies the order of the multipole
                    (0 or 1 ≡ monopole or dipole).
            charge : Real number, specifies the charge associated with the multipole.
    esp_constraint: Optional[tuple[float, float, float] | tuple[float, float]]
        PBC only. Define the constraints for the fit of the ESP-charges for
        each atom. Depending on the chosen method (`esp_constraint` method in
        control.in). Method 1 needs three parameters (χ, J00, w) 3.167 and method 2
        needs two parameters (q0, β) 3.169 as defined above
    verbatim_writeout: Optional[bool]
        If True write the geometry.in file into the output file
    calculate_friction: Optional[bool]
        Calculate friction for this geometry
    """
    atoms: Sequence[FHIAimsAtom] = None
    lattice_vectors: Optional[Matrix3D[float]] = None
    lattice_constraints: Optional[Vector3D[bool]] = None
    species_dict: Optional[dict[str, SpeciesDefaults]] = field(default_factory=dict)
    hessian_block: Optional[Sequence[tuple[int, int, Matrix3D]]] = None
    hessian_block_lv: Optional[Sequence[tuple[float, float, Matrix3D]]] = None
    hessian_block_lv_atoms: Optional[Sequence[tuple[float, float, Matrix3D]]] = None
    hessian_file: Optional[bool] = None
    trust_radius: Optional[float] = None
    symmetry_n_params: Optional[tuple[int, int, int]] = None
    symmetry_params: Optional[Sequence[str]] = None
    symmetry_lv: Optional[tuple[str, str, str]] = None
    symmetry_frac: Optional[Sequence[tuple[str, str, str]]] = None
    symmetry_frac_change_threshold: Optional[float] = None
    homogeneous_field: Optional[Vector3D] = None
    multipole: Optional[Sequence[tuple[float, float, float, int, float]]] = None
    esp_constraint: Optional[tuple[float, float, float] | tuple[float, float]] = None
    verbatim_writeout: Optional[bool] = None
    calculate_friction: Optional[bool] = None

    def __post_init__(self):
        """Setup some optional inputs given information and verify all inputs are correct"""
        if self.lattice_vectors is not None:
            self.lattice_vectors = np.array(self.lattice_vectors)
            if self.lattice_vectors.shape != (3, 3):
                raise InvalidGeometryError("Lattice vectors must be None or a 3x3 matrix")
            
            if np.linalg.det(self.lattice_vectors) < 1e-12:
                raise InvalidGeometryError("Lattice vectors must be linearly independent")
                
            if self.lattice_constraints is None:
                self.lattice_constraints = np.zeros((3, 3), dtype=bool)            
        else:
            if self.lattice_constraints is not None:
                raise InvalidGeometryError("Lattice vectors must be defined for lattice_constraints to be defined.")
                        
            if any([inp is not None for inp in [
                self.symmetry_n_params,
                self.symmetry_params,
                self.symmetry_lv,
                self.symmetry_frac,
                self.symmetry_frac_change_threshold
            ]]):
                raise InvalidGeometryError("Lattice vectors must be defined when using parametric constraints.")
        self.verify_object_lens()

    def __len__(self):
        """Get the length of the geometry"""
        return len(self.symbols)
    
    def verify_object_lens(self):
        """Verifies the sizes of each input"""            
        for item in ["lattice_constraints", "symmetry_lv"]:
            val = getattr(self, item, None)
            if val is not None and np.array(val).shape != (3, 3):
                raise InvalidGeometryError(f"The shape of {item} must be 3x3 not {np.array(val).shape}")

    @classmethod
    def from_file(cls, filename: Path | str) -> "AimsGeometry":
        """Read in a geometry.in file and construct a Geometry object
        
        Parameters
        ----------
        filename: str | Path
            File to load in

        Returns
        -------
        AimsGeometry
            The Geometry associated with the file
        """
        with open(filename, "r") as fd:
            lines = [line.strip() for line in fd.readlines()]
        
        return cls.from_strings(lines)
        
    @classmethod
    def from_strings(cls, lines: list[str]) -> "AimsGeometry":
        """Read in a geometry.in file and construct a Geometry object
        
        Parameters
        ----------
        lines: list[str]
            a list of all lines in the file.

        Returns
        -------
            The Geometry object associated with the file
        """
        lattice_vectors = []
        symbols: list[str] = []
        coords: list[Vector3D] = []

        is_empty: list[bool] = []
        is_pseudocore: list[bool] = []
        is_fractional: list[bool] = []

        hessian_block: None | list[tuple[int, int, Matrix3D]] = []
        hessian_block_lv: None | list[tuple[float, float, Matrix3D]] = []
        hessian_block_lv_atoms: None | list[tuple[float, float, Matrix3D]] = []

        symmetry_n_params: None | tuple[int, int, int] = (0, 0, 0)
        symmetry_params: None | Sequence[str] = []
        symmetry_lv: None | list[list[str]] = []
        symmetry_frac: None | list[list[str]] = []

        multipole: None |  list[tuple[float, float, float, int, float]] = []

        symmetry_frac_change_threshold: None | float = None
        hessian_file: None | bool = None
        trust_radius: None | float = None
        homogeneous_field: Vector3D = None
        esp_constraint: None | tuple[float, ...] = None
        verbatim_writeout: None | bool = None
        calculate_friction: None | bool = None

        velocities: dict[int, Vector3D] = {}
        initial_charge: dict[int, float] = {}
        initial_moment: dict[int, float] = {}
        nuclear_constraints: dict[int, list[bool]] = {}
        lattice_constraints: None | dict[int, list[bool]] = {}
        constraint_regions: dict[int, int | None] = {}
        magnetic_response: dict[int, bool] = {}
        magnetic_moment: dict[int, float] = {}
        nuclear_spin: dict[int, float] = {}
        isotope: dict[int, float] = {}
        RT_TDDFT_initial_velocity: dict[int, Vector3D] = {}

        last_add: str = ""
        for line in lines:
            if len(line) == 0 or line[0] == "#":
                continue
            inp = line.split("#")[0].split()
        
            if inp[0] in ["atom", "atom_frac", "empty", "pseudocore"]:
                symbols.append(inp[4])
                coords.append([float(ii) for ii in inp[1:4]])
                is_fractional.append(inp[0] == "atom_frac")
                is_empty.append(inp[0] == "empty")
                is_pseudocore.append(inp[0] == "pseudocore")
                last_add = "atom"
            elif inp[0] == "lattice_vector":
                lattice_vectors.append([float(ii) for ii in inp[1:4]])
                last_add = "lattice"
            elif inp[0] == "initial_moment":
                initial_moment[len(coords) - 1] = float(inp[1])
            elif inp[0] == "initial_charge":
                initial_charge[len(coords) - 1] = float(inp[1])
            elif inp[0] == "constrain_relaxation":
                if last_add == "atom":
                    nuclear_constraints[len(coords) - 1] = _create_constraints(inp)
                if last_add == "lattice":
                    lattice_constraints[len(coords) - 1] = _create_constraints(inp)
            elif inp[0] == "velocity":
                velocities[len(coords) - 1] = [float(ii) for ii in inp[1:4]]
            elif inp[0] == "RT_TDDFT_initial_velocity":
                RT_TDDFT_initial_velocity[len(coords) - 1] = [float(ii) for ii in inp[1:4]]
            elif inp[0] == "constraint_region":
                constraint_regions[len(coords) - 1] = int(inp[1])
            elif inp[0] == "magnetic_response":
                magnetic_response[len(coords) - 1] = True
            elif inp[0] == "magnetic_moment":
                magnetic_moment[len(coords) - 1] = float(inp[1])
            elif inp[0] == "nuclear_spin":
                nuclear_spin[len(coords) - 1] = float(inp[1])
            elif inp[0] == "isotope":
                isotope[len(coords) - 1] = float(inp[1])
            elif inp[0] == "symmetry_frac_change_threshold":
                symmetry_frac_change_threshold = float(inp[1])
            elif inp[0] == "hessian_file":
                hessian_file = True
            elif inp[0] == "trust_radius":
                trust_radius = float(inp[1])
            elif inp[0] == "homogeneous_field":
                homogeneous_field = np.array([float(e) for e in inp[1:]])
            elif inp[0] == "multipole":
                multipole.append((float(inp[1]), float(inp[2]), float(inp[3]), int(inp[4]), float(inp[5])))
            elif inp[0] == "esp_constraint":
                esp_constraint = tuple([float(ii) for ii in inp[1:]])
            elif inp[0] == "verbatim_writeout":
                verbatim_writeout = ".true." in inp[1]
            elif inp[0] == "calculate_friction":
                calculate_friction = ".true." in inp[1]
            elif inp[0] == "hessian_block":
                hessian_block.append((int(inp[1]), int(inp[2]), np.array([float(ii) for ii in inp[3:12]]).reshape((3,3))))
            elif inp[0] == "hessian_block_lv":
                hessian_block_lv.append((int(inp[1]), int(inp[2]), np.array([float(ii) for ii in inp[3:12]]).reshape((3,3))))
            elif inp[0] == "hessian_block_lv_atoms":
                hessian_block_lv_atoms.append((int(inp[1]), int(inp[2]), np.array([float(ii) for ii in inp[3:12]]).reshape((3,3))))
            elif inp[0] == "symmetry_n_params":
                symmetry_n_params = (int(inp[1]), int(inp[2]), int(inp[3]))
            elif inp[0] == "symmetry_params":
                symmetry_params = inp[1:]
            elif inp[0] == "symmetry_lv":
                symmetry_lv.append([ii.strip() for ii in line[11:].strip().split(",")])
            elif inp[0] == "symmetry_frac":
                symmetry_frac.append([ii.strip() for ii in line[13:].strip().split(",")])

        def dct2arr(dct: dict[int, Any], n_comp:int) -> np.ndarray[Any, np.dtype[bool]] | None:
            """Convert a dictionary of atom indexes and values to an array"""
            if len(dct) == 0:
                return None
            values = list(dct.values())
            if isinstance(values[0], (Sequence, np.ndarray)):
                to_ret = np.zeros((n_comp, len(values[0])), dtype=type(values[0]))
            else:
                to_ret = np.zeros(n_comp, dtype=type(values[0]))
            for key, val in dct.items():
                to_ret[key] = val
            return to_ret
        
        if len(lattice_vectors) > 0:
            try:
                lattice_vectors = to_matrix3d(lattice_vectors)
            except AssertionError:
                raise InvalidGeometryError("There must be 3 lattice vectors")

            lattice_constraints = dct2arr(lattice_constraints, 3)

        for cc, coord in enumerate(coords):
            if is_fractional[cc]:
                coords[cc] = list(np.dot(coord, lattice_vectors))
        
        atoms = []
        for aa, sym in enumerate(symbols):
            atoms.append(
                FHIAimsAtom(
                    symbol=sym,
                    position=coords[aa],
                    velocity=velocities.get(aa),
                    initial_charge=initial_charge.get(aa, 0.0),
                    initial_moment=initial_moment.get(aa, 0.0),
                    constraints=nuclear_constraints.get(aa),
                    constraint_region=constraint_regions.get(aa),
                    magnetic_response=magnetic_response.get(aa),
                    magnetic_moment=magnetic_moment.get(aa),
                    nuclear_spin=nuclear_spin.get(aa),
                    isotope=isotope.get(aa),
                    is_empty=is_empty[aa],
                    is_pseudocore=is_pseudocore[aa],
                    RT_TDDFT_initial_velocity=RT_TDDFT_initial_velocity.get(aa),
                )
            )

        if len(lattice_vectors) > 0:
            for aa in range(len(atoms)):
                atoms[aa].set_fractional(lattice_vectors)

        if symmetry_n_params == (0, 0, 0):
            symmetry_lv = None
            symmetry_frac = None
            symmetry_params = None
            symmetry_n_params = None
            symmetry_frac_change_threshold = None

        if len(lattice_vectors) == 0:
            lattice_vectors = None
            lattice_constraints = None

        if len(hessian_block) == 0:
            hessian_block = None
        if len(hessian_block_lv) == 0:
            hessian_block_lv = None
        if len(hessian_block_lv_atoms) == 0:
            hessian_block_lv_atoms = None
        if len(multipole) == 0:
            multipole = None

        return cls(
            atoms=atoms,
            lattice_vectors=lattice_vectors,
            lattice_constraints=lattice_constraints,
            hessian_block=hessian_block,
            hessian_block_lv=hessian_block_lv,
            hessian_block_lv_atoms=hessian_block_lv_atoms,
            hessian_file=hessian_file,
            trust_radius=trust_radius,
            symmetry_n_params=symmetry_n_params,
            symmetry_params=symmetry_params,
            symmetry_lv=symmetry_lv,
            symmetry_frac=symmetry_frac,
            symmetry_frac_change_threshold=symmetry_frac_change_threshold,
            homogeneous_field=homogeneous_field,
            multipole=multipole,
            esp_constraint=esp_constraint,
            verbatim_writeout=verbatim_writeout,
            calculate_friction=calculate_friction,
        )

    def to_atoms(self):
        """Convert AimsGeometry to an ase.Atoms object."""
        from ase import Atoms
        atoms = Atoms(
            symbols=self.symbols,
            positions=self.positions,
            magmoms=self.magnetic_moments,
            charges=self.initial_charges,
            pbc=self.lattice_vectors is not None,
            cell=self.lattice_vectors if self.lattice_vectors is not None else (0, 0, 0),
        )
        return atoms


    def load_species(self, species_directory:str | Path):
        """Create a species dictionary for the atoms
        
        Parameters
        ----------
        species_directory:str | Path
            The Path to load the species into
        """
        for sym in np.unique([at.symbol for at in self.atoms]):
            number = ATOMIC_SYMBOLS_TO_NUMBERS[sym]
            if number < 100:
                self.species_dict[sym] = SpeciesDefaults.from_file(f"{species_directory}/{number:02d}_{sym}_default")
            else:
                self.species_dict[sym] = SpeciesDefaults.from_file(f"{species_directory}/{number:03d}_{sym}_default")

    def set_species(self, sym: str, species: SpeciesDefaults):
        """Sets a species default for a given symbol
        
        Parameters
        ----------
        sym: str
            The symbol to add the species for
        species: SpeciesDefaults
            The species for the symbol
        """
        self.species_dict[sym] = species

    def get_species(self, sym: str) -> SpeciesDefaults:
        """Gets a species default for a given symbol
        
        Parameters
        ----------
        sym: str
            The symbol to add the species for
        
        Returns
        -------
            The species for the symbol
        """
        return self.species_dict[sym]
        
    @property
    def file_content(self):
        """Get the file content for this geometry"""
        content_str = ["# Making from pyaims", ]
        if self.lattice_vectors is not None and 3 == len(self.lattice_vectors):
            for lv, lv_const in zip(self.lattice_vectors, self.lattice_constraints):
                content_str.append(f"lattice_vector {lv[0]:.15e} {lv[1]:.15e} {lv[2]:.15e}")
                if np.any(lv_const):
                    content_str.append(f"    constrain_relaxation "
                                       f"{'x ' if lv_const[0] else ''}"
                                       f"{'y ' if lv_const[1] else ''}"
                                       f"{'z' if lv_const[2] else ''}"
                                       )
        for atom in self.atoms:
            content_str.append(atom.to_string)

        if self.homogeneous_field is not None:
            if len(self.homogeneous_field) != 3:
                raise InvalidGeometryError("The provided homogeneous_field value is invalid")
            content_str.append(f"homogeneous_field {self.homogeneous_field[0]:>20.12e} "
                               f"{self.homogeneous_field[1]:>20.12e} {self.homogeneous_field[2]:>20.12e}")

        if self.multipole is not None:
            if len(self.multipole) != 5:
                raise InvalidGeometryError("The provided multipole value is invalid")
            content_str.append(f"multipole {self.multipole[0]:>20.12e} {self.multipole[1]:>20.12e} "
                               f"{self.multipole[2]:>20.12e} {self.multipole[3]} "
                               f"{self.multipole[4]:>20.12e}")
            # TODO: Specify a dipole moment to multipoles

        if self.esp_constraint is not None:
            if len(self.esp_constraint) not in (2, 3):
                raise InvalidGeometryError("The provided esp_constraint value is invalid")
            content_str.append(f"esp_constraint {' '.join(f'{x:>20.12e}' for x in self.esp_constraint)}")

        if self.verbatim_writeout is not None:
            content_str.append(f"verbatim_writeout {'.true.' if self.verbatim_writeout else '.false.'}")

        if self.calculate_friction is not None:
            content_str.append(f"calculate_friction {'.true.' if self.calculate_friction else '.false.'}")

        if self.symmetry_n_params:
            content_str.append(f"symmetry_n_params {self.symmetry_n_params[0]} {self.symmetry_n_params[1]} "
                            f"{self.symmetry_n_params[2]}")
 
        if self.symmetry_params:
            content_str.append(f"symmetry_params " + " ".join(self.symmetry_params))
        if self.symmetry_lv is not None:
            for line in self.symmetry_lv:
                content_str.append(f"symmetry_lv " + " , ".join(line))
        if self.symmetry_frac is not None:
            for line in self.symmetry_frac:
                content_str.append(f"symmetry_frac " + " , ".join(line))
        if self.symmetry_frac_change_threshold:
            content_str.append(f"symmetry_frac_change_threshold {self.symmetry_frac_change_threshold}")

        if self.hessian_block is not None:
            for line in self.hessian_block:
                content_str.append(f"hessian_block {line[0]} {line[1]} " +
                                   " ".join([f"{ll:>20.12e}" for ll in line[2:]]))
        if self.hessian_block_lv is not None:
            for line in self.hessian_block_lv:
                content_str.append(f"hessian_block_lv {line[0]} {line[1]} " +
                                   " ".join([f"{ll:>20.12e}" for ll in line[2:]]))
        if self.hessian_block_lv_atoms is not None:
            for line in self.hessian_block_lv_atoms:
                content_str.append(f"hessian_block_lv_atoms {line[0]} {line[1]} " +
                                   " ".join([f"{ll:>20.12e}" for ll in line[2:]]))
        
        if self.hessian_file:
            content_str.append("hessian_file")
        if self.trust_radius is not None:
            content_str.append(f"trust_radius {self.trust_radius}")
        return "\n".join(content_str)

    @property
    def symbols(self):
        return [at.symbol for at in self.atoms]
    
    @property
    def numbers(self):
        return [at.number for at in self.atoms]
    
    @property
    def positions(self):
        return [at.position for at in self.atoms]
    
    @property
    def fractional_positions(self):
        return [at.fractional_position for at in self.atoms]
    
    @property
    def velocities(self):
        return [at.velocity for at in self.atoms]
    
    @property
    def RT_TDDFT_initial_velocities(self):
        return [at.RT_TDDFT_initial_velocity for at in self.atoms]
    
    @property
    def initial_charges(self):
        return [at.initial_charge for at in self.atoms]
    
    @property
    def initial_moments(self):
        return [at.initial_moment for at in self.atoms]
    
    @property
    def nuclear_constraints(self):
        return [at.constraints for at in self.atoms]
    
    @property
    def constraint_regions(self):
        return [at.constraint_region for at in self.atoms]
    
    @property
    def is_empty_atoms(self):
        return [at.is_empty for at in self.atoms]
    
    @property
    def is_pseudocore_atoms(self):
        return [at.is_pseudocore for at in self.atoms]
    
    @property
    def magnetic_responses(self):
        return [at.magnetic_response for at in self.atoms]
    
    @property
    def magnetic_moments(self):
        return [at.magnetic_moment for at in self.atoms]
    
    @property
    def nuclear_spins(self):
        return [at.nuclear_spin for at in self.atoms]
    
    @property
    def isotopes(self):
        return [at.isotope for at in self.atoms]

    @property
    def species_block(self):
        """Get the species block for the control.in file"""
        if any([sym not in self.species_dict for sym in np.unique(self.symbols)]):
            raise InvalidGeometryError("Species are not defined for all atoms in the structure")
        return "\n".join([self.species_dict[sym].content for sym in np.unique(self.symbols)])

    @property
    def n_atoms(self):
        """The number of atoms in the structure"""
        return len(self.symbols)
    
    @property
    def masses(self) -> np.ndarray:
        """Get the masses of the structure"""
        return self._species_property("mass")

    @property
    def nuclear_charges(self) -> np.ndarray:
        """Gets the nuclear charges of the structure"""
        return self._species_property("nucleus")

    def _species_property(self, prop: str) -> np.ndarray:
        """Returns an array with property values corresponding to atomic Species."""
        if any([sym not in self.species_dict for sym in np.unique(self.symbols)]):
            raise InvalidGeometryError("Species are not defined for all atoms in the structure")
        return np.array([getattr(self.species_dict[sym], prop) * (not self.is_empty_atoms[ss])
                         for ss, sym in enumerate(self.symbols)])


def _create_constraints(line: list[str]) -> list[bool]:
    """Sets constraints"""
    constraints = [False, False, False]
    if "x" in line[1:]:
        constraints[0] = True
    if "y" in line[1:]:
        constraints[1] = True
    if "z" in line[1:]:
        constraints[2] = True
    if "true" in line[1:]:
        constraints[:] = True
    return constraints
