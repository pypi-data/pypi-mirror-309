""" Parsers for FHI-aims standard output file."""
import numpy as np

from .abc import FileParser, ChunkParser
from . import converters


class RootParser(FileParser):
    name = "root"
    initial_chunk = "preamble"


class PreambleParser(ChunkParser):
    name = "preamble"
    values = {
        "aims_version": r"FHI-aims version *: (\w*)",
        "start_date": converters.to_date(r"Date *:  (\d*)"),
        "start_time": converters.to_time(r"Time *:  ([\d.]*)")
    }
    metadata = {
        "num_tasks": converters.to_int(r"Using *(\d+) parallel tasks."),
    }
    next_chunks = ["control_in"]
    parsed_key = ""


class ControlInParser(ChunkParser):
    name = "control_in"
    title_line = r"Parsing control.in"
    values = {
        "control_in": r"-{71}\n(.+)  -{71}\n  Completed first pass"
    }
    next_chunks = ["geometry_in"]
    parsed_key = "input"

    def parse(self):
        parse_results = super(ControlInParser, self).parse()
        # get the runtime choices
        choices = {}
        for line in parse_results["control_in"].split("\n"):
            if "species" in line:
                break
            hash_idx = line.find("#")
            keywords = (line[:hash_idx] if hash_idx >= 0 else line).strip().split()
            if keywords:
                choices[keywords[0]] = " ".join(keywords[1:])
        self.parent.run_metadata.update(choices)
        return parse_results


class GeometryInParser(ChunkParser):
    name = "geometry_in"
    title_line = r"Parsing geometry.in"
    values = {
        "geometry_in": r"-{71}\n(.+)  -{71}\n  Completed first pass"
    }
    metadata = {
        "num_species": converters.to_int(r"Number of species *: *(\d+)"),
        "num_atoms": converters.to_int(r"Number of atoms *: *(\d+)"),
    }
    next_chunks = ["reading_control_in"]
    parsed_key = "input"


class ReadingControlParser(ChunkParser):
    name = "reading_control_in"
    title_line = r"Reading file control.in"
    next_chunks = ["reading_geometry_in"]
    parsed_key = "input"
    metadata = {"relax": converters.to_bool(r"Geometry relaxation"),
                "md": converters.to_bool(r"Molecular dynamics"),}


class ReadingGeometryParser(ChunkParser):
    name = "reading_geometry_in"
    title_line = r"Reading geometry description geometry.in"
    values = {
        "geometry": converters.to_atoms(r"Input geometry:\n(.*?)$^\n", from_input=True)
    }
    next_chunks = ["consistency_checks"]
    parsed_key = "input"


class ConsistencyChecksParser(ChunkParser):
    name = "consistency_checks"
    title_line = r"Consistency checks .* are next"
    next_chunks = ["fixed_parts"]
    parsed_key = ""


class FixedPartsParser(ChunkParser):
    name = "fixed_parts"
    title_line = r"Preparing all fixed parts"
    next_chunks = ["scf_init"]
    parsed_key = ""


class SCFInitParser(ChunkParser):
    name = "scf_init"
    title_line = r"Begin self-consistency loop"
    next_chunks = ["init_values"]
    parsed_key = "ionic_steps[]"


class ScfInitValuesParser(ChunkParser):
    name = "init_values"
    title_line = r"-{60}"
    values = {
        "chemical_potential": converters.to_float(r"  \| Chemical potential \(Fermi level\): *([-+.E\d]*) eV"),
        "vbm": converters.to_float(r"Highest occupied state \(VBM\) at *([-.\d]*) eV"),
        "cbm": converters.to_float(r"Lowest unoccupied state \(CBM\) at *([-.\d]*) eV"),
        "gap": converters.to_float(r"HOMO-LUMO gap: *([-+.E\d]*) eV"),
        "total_energy": converters.to_float(r"  \| Total energy *: *[-.\d]* Ha *([-.\d]*) eV"),
        "free_energy": converters.to_float(r"  \| Electronic free energy *: *[-.\d]* Ha *([-.\d]*) eV"),
    }
    next_chunks = [
        {
            "runtime_choices": {"output_level": "MD_light"},
            "chunk": "mdlight_scf"
        },
        "scf_init",
        "scf_step",
        "final_values"]
    parsed_key = "ionic_steps.scf_init"


class SCFStepParser(ChunkParser):
    name = "scf_step"
    title_line = r"Begin self-consistency iteration"
    values = {
        "chemical_potential": converters.to_float(r"  \| Chemical potential \(Fermi level\): *([-+.E\d]*) eV"),
        "vbm": converters.to_float(r"Highest occupied state \(VBM\) at *([-.\d]*) eV"),
        "cbm": converters.to_float(r"Lowest unoccupied state \(CBM\) at *([-.\d]*) eV"),
        "gap": converters.to_float(r"HOMO-LUMO gap: *([-+.E\d]*) eV"),
        "total_energy": converters.to_float(r"  \| Total energy *: *[-.\d]* Ha *([-.\d]*) eV"),
        "free_energy": converters.to_float(r"  \| Electronic free energy *: *[-.\d]* Ha *([-.\d]*) eV"),
        "charge_density_change": converters.to_float(r"  \| Change of charge density *: *([-+.E\d]*)"),
        "eigenvalues_sum_change": converters.to_float(r"  \| Change of sum of eigenvalues *: *([-+.E\d]*)"),
        "total_energy_change": converters.to_float(r"  \| Change of total energy *: *([-+.E\d]*)"),
        "change_of_forces": converters.to_float(r"  \| Change of forces *: *([-+.E\d]*) eV/A"),
    }
    next_chunks = [
        "scf_step",
        "converged_scf",
        "final_values"
    ]
    parsed_key = "ionic_steps.scf_steps[]"


class MDLightSCFParser(ChunkParser):
    name = "mdlight_scf"
    title_line = r"Convergence:"
    next_chunks = [
        "mdlight_energy"
    ]
    parsed_key = "ionic_steps"

    def parse(self):
        content = self.collect()
        step_lines = []
        for line in content.splitlines()[1:-1]:
            if line.startswith("  SCF"):
                step_lines.append(line)
            else:
                step_lines[-1] += line
        # Each step:  q app. | density  | eigen (eV) | Etot (eV) | forces (eV/A) | CPU time | Clock time
        steps = []
        for step in step_lines:
            results = step.split("|")
            steps.append({
                "charge_density_change": float(results[1]),
                "eigenvalues_sum_change": float(results[2]),
                "total_energy_change": float(results[3]),
                "cpu_time": float(results[5].split()[0]),
                "wall_time": float(results[6].split()[0])
            })
            try:
                steps[-1]["change_of_forces"] = float(results[4])
            except ValueError:
                pass
        return {"scf_steps": steps}


class MDLightEnergyParser(SCFStepParser):
    name = "mdlight_energy"
    title_line = r"Total energy components:"
    next_chunks = [
        "scf_init",
        "converged_scf",
        "mulliken",
        "final_values",
    ]
    parsed_key = "ionic_steps"


class ConvergedSCFParser(ChunkParser):
    name = "converged_scf"
    title_line = r"Self-consistency cycle converged"
    values = {
        "total_energy": converters.to_float(r"  \| Total energy uncorrected *: *([-+.E\d]*) eV"),
        "free_energy": converters.to_float(r"  \| Electronic free energy *: *([-+.E\d]*) eV"),
        "vdw_correction": converters.to_float(r"  \| vdW energy correction *: *[-.\d]* Ha *([-.\d]*) eV"),

        # charge / dipole moments
        "total_charge": converters.to_float(r"  \| Total charge \[e\] *: *([-+.E\d]*)"),
        "total_dipole_moment": converters.to_vector(r"  \| Total dipole moment \[eAng\] *: "
                                                    r"*([-+.E\d]*) *([-+.E\d]*) *([-+.E\d]*)", dtype=float),
        "absolute_dipole_moment": converters.to_float(r"  \| Absolute dipole moment *: *([-+.E\d]*)"),
        "hirshfeld_charges": converters.to_vector(r"  \|   Hirshfeld charge *: *([-+.\d]*)", multistring=True),
        # forces and stress
        "atomic_forces": converters.to_table(r"Total atomic forces [\s\S]* \[eV\/Ang\]:",
                                             num_rows="num_atoms",
                                             dtype=[None, None, float, float, float]),
        "analytical_stress": converters.to_table(r"  \| *Analytical stress tensor - Symmetrized *\|",
                                      header=5,
                                      num_rows=3,
                                      dtype=[None, None, float, float, float, None]),
        "numerical_stress": converters.to_table(r"  \| *Numerical stress tensor *\|",
                                                 header=5,
                                                 num_rows=3,
                                                 dtype=[None, None, float, float, float, None]),
        "pressure": converters.to_float(r"Pressure: *([-+.E\d]*)"),
    }
    next_chunks = [
        "scf_init",
        "ionic_step_geometry",
        {
            "runtime_choices": {"md": True},
            "chunk": "md_values",
        },
        {
            "runtime_choices": {"qpe_calc": "gw_expt"},
            "chunk": "periodic_gw"
        },
        "final_geometry",
        "mulliken",
        "hirshfeld",
        "final_values"
    ]
    parsed_key = "ionic_steps"


class MullikenAnalysisParser(ChunkParser):
    name = "mulliken"
    title_line = r" *Starting Mulliken Analysis"
    values = {
        "mulliken_charges": converters.to_table(
            r"Performing (?:scalar-relativistic )?Mulliken charge[\s\S]*?"
            r"Summary of the per-atom charge analysis:",
            header=3,
            num_rows="num_atoms",
            dtype=[None, None, None, float, None, None, None, None]
        ),
        "mulliken_charges_soc": converters.to_table(
            r"Performing spin-orbit-coupled Mulliken charge[\s\S]*?"
            r"Summary of the per-atom charge analysis:",
            header=3,
            num_rows="num_atoms",
            dtype=[None, None, None, float, None, None, None, None]
        )
    }
    next_chunks = [
        "hirshfeld",
        "final_values"
    ]
    parsed_key = "final"

class HirshfeldAnalysisParser(ChunkParser):
    name = "hirshfeld"
    title_line = r"Performing Hirshfeld analysis of fragment charges and moments."
    values = {
        "hirshfeld_charges": converters.to_vector(r"  \|   Hirshfeld charge *: *([-+.\d]*)",
                                                  multistring=True),
}
    next_chunks = ["final_values"]
    parsed_key = "final"

class PeriodicGWParser(ChunkParser):
    name = "periodic_gw"
    title_line = r"Initializing LVL tricoefficents in reciprocal space for GW ..."
    values = {
        "vbm": converters.to_float(r"\"GW Band gap\" of total set of bands:[\s\S]*?"
                                   r"  \| Highest occupied state : *([-.\d]*) eV"),
        "cbm": converters.to_float(r"\"GW Band gap\" of total set of bands:[\s\S]*?"
                                   r"  \| Lowest unoccupied state: *([-.\d]*) eV"),
        "gap": converters.to_float(r"\"GW Band gap\" of total set of bands:[\s\S]*?"
                                   r"  \| Energy difference      : *([-.\d]*) eV"),
        "se_on_k_grid": r" *GW quasi-particle energy levels\n"
                        r"(?:[^\n]*\n){5}([\s\S]*)\n\n"
                        r"  Valence band maximum",
        "se_states": converters.to_vector("states to compute self-energy: *([\d]*) *([\d]*)",
                                          dtype=int)
    }
    next_chunks = ["final_values"]
    parsed_key = "gw"

    def parse(self) -> dict:
        """Additionally, parse the table of the self-energy on the regular k-point grid."""
        parse_results = super().parse()
        # parse the table the usual way
        try:
            se_str = parse_results.pop("se_on_k_grid")
            states = parse_results.pop("se_states")
        except KeyError:
            return parse_results
        se_lines = se_str.split("\n")
        headers = se_lines[0].split()[1:]
        n_states = states[1] - states[0] + 1
        n_k_points = (len(se_lines) - 1) / (n_states + 4)
        se = {
            "states": list(range(states[0], states[1] + 1)),
        }
        result = []
        for i_k in range(int(n_k_points)):
            result.append([])
            for i_line in range(i_k*(n_states + 4) + 4, (i_k + 1)*(n_states + 4)):
                result[i_k].append(list(map(float, se_lines[i_line].split()[1:])))
        result = np.array(result)
        for i_head, head in enumerate(headers):
            se[head] = result[:, :, i_head].T
        parse_results["self_energy"] = se
        return parse_results


class MDValuesParser(ChunkParser):
    name = "md_values"
    title_line = r"  Complete information for previous time-step:"
    values = {
        "time_step": converters.to_int(r"  \| Time step number *: *(\d+)"),
        "electronic_free_energy": converters.to_float(r"  \| Electronic free energy *: *([-+.E\d]*) eV"),
        "temperature": converters.to_float(r"  \| Temperature \(nuclei\) *: *([-+.E\d]*) K"),
        "kinetic_energy": converters.to_float(r"  \| Nuclear kinetic energy *: *([-+.E\d]*) eV"),
        "total_energy": converters.to_float(r"  \| Total energy \(el.+nuc.\) *: *([-+.E\d]*) eV"),
        "gle_H": converters.to_float(r"  \| GLE pseudo hamiltonian *: *([-+.E\d]*) eV")
    }
    next_chunks = ["ionic_step_geometry"]
    parsed_key = "ionic_steps.md"


class IonicStepGeometry(ChunkParser):
    name = "ionic_step_geometry"
    title_line = (r"Atomic structure \(and velocities\) as used in the preceding time step:|"
                  r"Final atomic structure \(and velocities\) as used in the preceding time step:|"
                  r"Atomic structure that was used in the preceding time step of the wrapper:|"
                  r"Updated atomic structure:")
    values = {
        "geometry": converters.to_atoms(r"Atomic structure \(and velocities\) as used in the preceding time step:|"
                                        r"Final atomic structure \(and velocities\) as used in the preceding time step:|"
                                        r"Atomic structure that was used in the preceding time step of the wrapper|"
                                        r"Updated atomic structure:")
    }
    next_chunks = [
        "scf_init",
        "mulliken",
        "final_values"
    ]
    parsed_key = "ionic_steps"


class FinalGeometry(ChunkParser):
    name = "final_geometry"
    title_line = r"Present geometry is converged|Aborting optimization"
    values = {
        "geometry_converged": converters.to_bool(r"Present geometry is converged"),
        "geometry": converters.to_atoms(r"  Final atomic structure:")
    }
    next_chunks = [
        "mulliken",
        "final_values"
    ]
    parsed_key = "final"


class FinalValuesParser(ChunkParser):
    name = "final_values"
    title_line = r"Final output of selected total energy values"
    values = {
        "energy": converters.to_float(r"  \| Total energy of the DFT / Hartree-Fock s.c.f. "
                                            r"calculation *: *([-.\d]*)"),
    }
    parsed_key = "final"
    next_chunks = ["final"]


class FinalParser(ChunkParser):
    name = "final"
    title_line = r"Leaving FHI-aims"
    values = {
        "end_date": converters.to_date(r"Date *:  (\d*)"),
        "end_time": converters.to_time(r"Time *:  ([\d.]*)"),
        "num_scf_steps": converters.to_int(r"Number of self-consistency cycles *: *(\d+)"),
        "num_ionic_steps": converters.to_int(r"Number of SCF \(re\)initializations *: *(\d+)"),
        "num_relax_steps": converters.to_int(r"Number of relaxation steps *: *(\d+)"),
        "num_md_steps": converters.to_int(r"Number of molecular dynamics steps *: *(\d+)"),
        "num_force_evals": converters.to_int(r"Number of force evaluations *: *(\d+)"),
    }
    next_chunks = ["final_times"]
    parsed_key = ""


class FinalTimesParser(ChunkParser):
    name = "final_times"
    title_line = r"Detailed time accounting"
    values = {
        "total": converters.to_vector(r"Total time *: *([\d.]+) s *([\d.]+) s"),
        "preparation": converters.to_vector(r"Preparation time *: *([\d.]+) s *([\d.]+) s"),
        "bc_init": converters.to_vector(r"Boundary condition initalization *: *([\d.]+) s *([\d.]+) s"),
        "grid_part": converters.to_vector(r"Grid partitioning *: *([\d.]+) s *([\d.]+) s"),
        "preloading_free_atom": converters.to_vector(r"Preloading free-atom quantities on grid"
                                                     r" *: *([\d.]+) s *([\d.]+) s"),
        "free_atom_sp_e": converters.to_vector(r"Free-atom superposition energy *: *([\d.]+) s *([\d.]+) s"),
        "integration": converters.to_vector(r"Total time for integrations *: *([\d.]+) s *([\d.]+) s"),
        "ks_equations": converters.to_vector(r"Total time for solution of K.-S. equations *: *([\d.]+) s *([\d.]+) s"),
        "ev_reortho": converters.to_vector(r"Total time for EV reorthonormalization *: *([\d.]+) s *([\d.]+) s"),
        "density_force": converters.to_vector(r"Total time for density & force components *: *([\d.]+) s *([\d.]+) s"),
        "mixing": converters.to_vector(r"Total time for mixing *: *([\d.]+) s *([\d.]+) s"),
        "hartree_update": converters.to_vector(r"Total time for Hartree multipole update *: *([\d.]+) s *([\d.]+) s"),
        "hartree_sum": converters.to_vector(r"Total time for Hartree multipole sum *: *([\d.]+) s *([\d.]+) s"),
        "total_energy_eval": converters.to_vector(r"Total time for total energy evaluation *: *([\d.]+) s *([\d.]+) s"),
        "nsc_force": converters.to_vector(r"Total time NSC force correction *: *([\d.]+) s *([\d.]+) s"),
        "scaled_zora": converters.to_vector(r"Total time for scaled ZORA corrections *: *([\d.]+) s *([\d.]+) s"),
        "pert_soc": converters.to_vector(r"Total time for perturbative SOC *: *([\d.]+) s *([\d.]+) s"),
        "wannier_evol": converters.to_vector(r"Total time for Wannier Center Evolution *: *([\d.]+) s *([\d.]+) s"),
    }
    next_chunks = ["have_a_nice_day"]
    parsed_key = "final.time"


class HaveANiceDayParser(ChunkParser):
    name = "have_a_nice_day"
    title_line = r"Have a nice day"
    values = {
        "is_finished_ok": converters.to_bool(r"(Have a nice day.)")
    }
    parsed_key = ""
