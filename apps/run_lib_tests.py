import sys
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).parent

if __name__ == "__main__":
    tests_folder = [
        BASE_DIR / 'utils' / 'tests',
        BASE_DIR / 'common' / 'tests'
    ]
    sys.exit(pytest.main(['-vv'] + tests_folder))
