""" Type converters for parsed values
"""
import re
import datetime
import tempfile
from pathlib import Path



def _to_builtin(pattern, builtin_type):
    """Converter to the builtin type"""
    def _helper(line, _):
        match = re.search(pattern, line, re.DOTALL | re.MULTILINE)
        if match:
            return builtin_type(match.group(1))
        return None
    return _helper


def to_atoms(pattern, from_input=False):
    """Convert aims.out geometry representation to ase.Atoms"""
    from ase.io import read

    def _helper(line, _):
        # Capture everything to the next dashed line including it
        match = re.search(rf"(?:{pattern}).*\n([\s\S]*?)\n *-{{60,}}", line, re.MULTILINE)
        if match is None:
            return None
        lines = match.group()
        # remove fractional coordinates
        lines = lines[:lines.find("Fractional coordinates")]
        lines = lines.split("\n")[2:-1]
        with tempfile.TemporaryDirectory() as tmp:
            file_name = Path(tmp) / "geometry.in"
            with open(file_name, "w") as f:
                f.write("\n".join(lines))
            atoms = read(file_name, format="aims")
        return atoms
    return _helper


def to_bool(pattern):
    def _helper(line, _):
        return bool(re.search(pattern, line, re.DOTALL | re.MULTILINE))
    return _helper


def to_float(pattern):
    return _to_builtin(pattern, float)


def to_int(pattern):
    return _to_builtin(pattern, int)


def to_str(pattern):
    return _to_builtin(pattern, str)


def to_date(pattern):
    return _to_builtin(pattern, lambda x: datetime.datetime.strptime(x, '%Y%m%d').date())


def to_time(pattern):
    return _to_builtin(pattern, lambda x: datetime.datetime.strptime(x, '%H%M%S.%f').time())


def to_table(pattern, *, num_rows: int | str, header: int = 1, dtype: list[type] | tuple[type] = None):
    """Convert `num_rows` lines after `header` indicated by `pattern` to Python 2D list"""
    dtype = dtype if dtype is not None else []
    def _helper(line, metadata):
        # we need a local scope variable for not to lose access to num_rows
        n_rows = num_rows if isinstance(num_rows, int) else metadata[num_rows]
        match = re.search(rf"{pattern}\n((?:.*\n){{{header+n_rows-1}}})", line, re.MULTILINE)
        if match is None:
            return None
        table = match.group(1).split("\n")[header-1:-1]
        types = dtype + ([None] * (len(table[0].split()) - len(dtype)))
        result = []
        for line in table:
            result.append([t(v) for t, v in zip(types, line.split()) if t is not None])
        # make it 1D list if only one column is asked for in the parser
        if len(result[0]) == 1:
            result = [r[0] for r in result]
        return result
    return _helper


def to_vector(pattern, *, dtype: type = float, multistring: bool = False):
    """Convert a set of numbers to a 1D numpy array.

    Args:
          pattern (str): A regular expression pattern.
          dtype (type): A Python type to convert to.
          multistring (bool): If True, checks for different occurrences of the pattern in a line
          (different matches).
          If False, finds the numbers written in one line (different groups within one match).
    """
    def _helper(line, _):
        match = re.findall(pattern, line, re.DOTALL | re.MULTILINE)
        if not match:
            return None
        return [dtype(x) for x in match] if multistring else [dtype(x) for x in match[0]]
    return _helper