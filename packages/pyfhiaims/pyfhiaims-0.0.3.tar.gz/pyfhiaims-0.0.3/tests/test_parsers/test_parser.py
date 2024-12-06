"""Test new FHI-aims standard output parser."""

import yaml

from pyfhiaims.outputs.parser import StdoutParser
from tests.utils import is_subset


def test_parser(data_dir):
    """Checks parsing given output files against reference values."""
    stdout_data_dir = data_dir / "stdout"
    for file_name in stdout_data_dir.iterdir():
        if file_name.is_file():
            parser = StdoutParser(file_name)
            results = parser.parse()
            with open(stdout_data_dir / "ref" / (file_name.stem + ".yaml"), "r") as f:
                ref_data = yaml.safe_load(f)
            assert is_subset(ref_data, results)


# def test_print_parsed_results(data_dir):
#     """This test is for development purposes only."""
#     file_name = data_dir / "stdout" / "relax.out.gz"
#     parser = StdoutParser(file_name)
#     results = parser.parse()
#     from pprint import pprint
#     pprint(results)