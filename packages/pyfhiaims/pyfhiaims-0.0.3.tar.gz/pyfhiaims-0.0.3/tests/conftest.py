"""Fixtures for pyaims tests."""

from pathlib import Path
import pytest


@pytest.fixture
def data_dir():
    return Path(__file__).parent / 'test_data'