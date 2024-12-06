"""Tests for AimsControlIn object."""

from pathlib import Path

from pyfhiaims.control import AimsControlIn


def test_control(data_dir):
    control_dir = data_dir / 'control'
    control_in = AimsControlIn.from_file(control_dir / "al2zns4.in")
    assert control_in is not None
    # print(control_in.species_defaults["Co"].content)