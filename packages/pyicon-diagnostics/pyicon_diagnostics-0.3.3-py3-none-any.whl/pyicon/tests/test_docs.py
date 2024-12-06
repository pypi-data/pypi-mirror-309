import subprocess
import pytest
import pyicon as pyic
from pathlib import Path


def test_docs_build(tmpdir_factory):
    base_dir = Path(pyic.__file__).parent / ".."
    doc_dir = base_dir.resolve() / "doc"
    build_dir = tmpdir_factory.mktemp("_build")

    # Run the sphinx-build command
    try:
        subprocess.check_call(["sphinx-build", "-b", "html", doc_dir, build_dir])
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Documentation build failed with exit code {e.returncode}")
