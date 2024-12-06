"""Some tests for the AimsStdout object."""

from math import isclose

from pyaims import AimsStdout


def test_stdout(data_dir):
    stdout_data_dir = data_dir / "stdout"
    file_name = stdout_data_dir / "relax.out.gz"
    stdout = AimsStdout(file_name)
    assert len(stdout.warnings) == 1
    assert len(stdout.errors) == 0
    assert stdout.is_finished_ok
    assert stdout.final["geometry_converged"]
    assert isclose(stdout.energy, -1071304.321815)
    assert stdout.forces is not None
    assert stdout.metadata["num_atoms"] == 2




