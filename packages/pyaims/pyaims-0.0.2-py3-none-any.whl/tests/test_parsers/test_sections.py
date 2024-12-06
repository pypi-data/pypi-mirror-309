from __future__ import annotations

import gzip
from pathlib import Path

import numpy as np
import pytest
from numpy.testing import assert_allclose
from pyaims.output_parser.aims_out_section import (
    AimsParseError,
    AimsOutSection
)
from pyaims.output_parser.aims_out_header_section import AimsOutHeaderSection
from pyaims.output_parser.aims_out_calculation_section import AimsOutCalcSection

eps_hp = 1e-15  # The epsilon value used to compare numbers that are high-precision
eps_lp = 1e-7  # The epsilon value used to compare numbers that are low-precision

parser_file_dir = Path(__file__).parent / "parser_checks"


@pytest.fixture()
def default_section():
    lines = ["TEST", "A", "TEST", "| Number of atoms: 200"]
    return AimsOutSection(lines)


def test_get_line_inds(default_section):
    test_keys = {"test": ["TEST"], "a": "A", "n_atoms": "| Number of atoms", "test_A": "TEST A"}

    default_section.set_prop_line_relations(test_keys)

    assert default_section.get_line_inds("test") == [0, 2]
    assert default_section.get_line_inds("test_A") == []
    assert default_section.get_line_inds("a") == [1]


def test_parse_key_value_pair(default_section):
    test_keys = {"test": ["TEST"], "a": "A", "n_atoms": "| Number of atoms", "n_electrons": "Number of electrons"}
    default_section.set_prop_line_relations(test_keys)
    assert default_section._parse_key_value_pair("n_atoms", dtype=int) == 200
    assert default_section._parse_key_value_pair("n_bands", dtype=int) is None
    assert default_section._parse_key_value_pair("n_electrons", allow_fail=True, dtype=int) is None


@pytest.fixture()
def empty_header_section():
    return AimsOutHeaderSection([])


@pytest.mark.parametrize("attr_name", ["n_atoms", "n_bands", "n_electrons", "n_spins", "initial_geometry", "initial_lattice", "initial_charges", "initial_magnetic_moments"])
def test_missing_parameter(attr_name, empty_header_section):
    with pytest.raises(AimsParseError, match="No information about"):
        getattr(empty_header_section, attr_name)


def test_default_header_electronic_temperature(empty_header_section):
    assert empty_header_section.electronic_temperature == 0.0


def test_default_header_is_md(empty_header_section):
    assert not empty_header_section.is_md


def test_default_header_is_relaxation(empty_header_section):
    assert not empty_header_section.is_relaxation


def test_default_header_n_k_points(empty_header_section):
    assert empty_header_section.n_k_points is None


def test_default_header_k_points(empty_header_section):
    assert empty_header_section.k_points is None


def test_default_header_k_point_weights(empty_header_section):
    assert empty_header_section.k_point_weights is None


@pytest.fixture()
def initial_lattice():
    return np.array(
        [
            [1, 2.70300000, 3.70300000],
            [4.70300000, 2, 6.70300000],
            [8.70300000, 7.70300000, 3],
        ]
    )


@pytest.fixture()
def header_section():
    with open(f"{parser_file_dir}/header_section.out", mode="rt") as hc_file:
        lines = hc_file.readlines()

    for ll, line in enumerate(lines):
        lines[ll] = line.strip()

    return AimsOutHeaderSection(lines)


def test_header_n_atoms(header_section):
    assert header_section.n_atoms == 2


def test_header_n_bands(header_section):
    assert header_section.n_bands == 3


def test_header_n_electrons(header_section):
    assert header_section.n_electrons == 28


def test_header_n_spins(header_section):
    assert header_section.n_spins == 2


def test_header_initial_geometry(header_section, initial_lattice):
    initial_positions = np.array([[0.000, 1.000, 2.000], [2.703, 3.703, 4.703]])
    assert len(header_section.initial_geometry) == 2
    assert_allclose(header_section.initial_geometry.lattice_vectors, initial_lattice)
    assert_allclose(header_section.initial_geometry.positions, initial_positions, atol=1e-12)
    assert [sym for sym in header_section.initial_geometry.symbols] == ["Na", "Cl"]


def test_header_electronic_temperature(header_section):
    assert header_section.electronic_temperature == 0.05


def test_header_is_md(header_section):
    assert header_section.is_md


def test_header_is_relaxation(header_section):
    assert header_section.is_relaxation


def test_header_n_k_points(header_section):
    assert header_section.n_k_points == 8


@pytest.fixture()
def k_points():
    return np.array(
        [
            [0.000, 0.000, 0.000],
            [0.000, 0.000, 0.500],
            [0.000, 0.500, 0.000],
            [0.000, 0.500, 0.500],
            [0.500, 0.000, 0.000],
            [0.500, 0.000, 0.500],
            [0.500, 0.500, 0.000],
            [0.500, 0.500, 0.500],
        ]
    )


def test_header_k_point_weights(
    header_section,
):
    assert_allclose(header_section.k_point_weights, np.full((8), 0.125))


def test_header_k_points(header_section, k_points):
    assert_allclose(header_section.k_points, k_points)


def test_header_header_summary(header_section, k_points):
    header_summary = {
        "initial_geometry": header_section.initial_geometry,
        "initial_lattice": header_section.initial_lattice,
        "is_relaxation": True,
        "is_md": True,
        "n_atoms": 2,
        "n_bands": 3,
        "n_electrons": 28,
        "n_spins": 2,
        "electronic_temperature": 0.05,
        "n_k_points": 8,
        "k_points": k_points,
        "k_point_weights": np.full((8), 0.125),
    }
    for key, val in header_section.header_summary.items():
        if isinstance(val, np.ndarray):
            assert_allclose(val, header_summary[key])
        else:
            assert val == header_summary[key]


@pytest.fixture()
def empty_calc_section(header_section):
    return AimsOutCalcSection([], header_section)


def test_header_transfer_n_atoms(empty_calc_section):
    assert empty_calc_section.n_atoms == 2


def test_header_transfer_n_bands(empty_calc_section):
    assert empty_calc_section.n_bands == 3


def test_header_transfer_n_electrons(empty_calc_section):
    assert empty_calc_section.n_electrons == 28


def test_header_transfer_n_spins(empty_calc_section):
    assert empty_calc_section.n_spins == 2


def test_header_transfer_initial_geometry(empty_calc_section, initial_lattice):
    initial_positions = np.array([[0.000, 1.000, 2.000], [2.703, 3.703, 4.703]])

    assert len(empty_calc_section.initial_geometry) == 2
    assert_allclose(empty_calc_section.initial_geometry.lattice_vectors, initial_lattice)
    assert_allclose(empty_calc_section.initial_geometry.positions, initial_positions, atol=1e-12)
    assert [sym for sym in empty_calc_section.initial_geometry.symbols] == ["Na", "Cl"]


def test_header_transfer_electronic_temperature(empty_calc_section):
    assert empty_calc_section.electronic_temperature == 0.05


def test_header_transfer_n_k_points(empty_calc_section):
    assert empty_calc_section.n_k_points == 8


def test_header_transfer_k_point_weights(empty_calc_section):
    assert_allclose(empty_calc_section.k_point_weights, np.full((8), 0.125))


def test_header_transfer_k_points(empty_calc_section, k_points):
    assert_allclose(empty_calc_section.k_points, k_points)


def test_default_calc_energy_raises_error(empty_calc_section):
    with pytest.raises(AimsParseError, match="No energy is associated with the structure."):
        _ = empty_calc_section.energy

def test_default_calc_total_energy_raises_error(empty_calc_section):
    with pytest.raises(AimsParseError, match="No energy is associated with the structure."):
        _ = empty_calc_section.total_energy

@pytest.mark.parametrize(
    "attr",
    [
        "forces",
        "stresses",
        "stress",
        "n_iter",
        "magmom",
        "E_f",
        "dipole",
        "mulliken_charges",
        "mulliken_spins",
        "hirshfeld_charges",
        "hirshfeld_volumes",
        "hirshfeld_atomic_dipoles",
        "hirshfeld_dipole",
    ],
)
def test_section_defaults_none(attr, empty_calc_section):
    assert getattr(empty_calc_section, attr) is None


def test_default_calc_is_metallic(empty_calc_section):
    assert not empty_calc_section.is_metallic


def test_default_calc_converged(empty_calc_section):
    assert not empty_calc_section.converged


@pytest.fixture()
def calc_section(header_section):
    with open(f"{parser_file_dir}/calc_section.out", mode="rt") as file:
        lines = file.readlines()

    for ll, line in enumerate(lines):
        lines[ll] = line.strip()
    return AimsOutCalcSection(lines, header_section)


@pytest.fixture()
def numerical_stress_section(header_section):
    with open(f"{parser_file_dir}/numerical_stress.out", mode="rt") as file:
        lines = file.readlines()

    for ll, line in enumerate(lines):
        lines[ll] = line.strip()
    return AimsOutCalcSection(lines, header_section)


def test_calc_structure(calc_section, initial_lattice):
    initial_positions = np.array([[0.000, 1.000, 2.000], [2.703, 3.703, 4.703]])

    assert len(calc_section.geometry) == 2
    assert_allclose(calc_section.geometry.lattice_vectors, initial_lattice)
    assert_allclose(calc_section.geometry.positions, initial_positions, atol=1e-12)
    assert [sym for sym in calc_section.geometry.symbols] == ["Na", "Cl"]


def test_calc_forces(calc_section):
    forces = np.array([[1.0, 2.0, 3.0], [6.0, 5.0, 4.0]])
    assert_allclose(calc_section.forces, forces)

    # Different because of the constraints
    assert_allclose(calc_section.results["forces"], forces)


# def test_calc_stresses(calc_section):
#     stresses = 1.0 * np.array(
#         [
#             Tensor.from_voigt([-10.0, -20.0, -30.0, -60.0, -50.0, -40.0]),
#             Tensor.from_voigt([10.0, 20.0, 30.0, 60.0, 50.0, 40.0]),
#         ]
#     )
#     assert_allclose(calc_section.stresses, stresses)
#     assert_allclose(calc_section.results["stresses"], stresses)


def test_calc_stress(calc_section):
    stress = 1.0 * np.array([[1.0, 2.0, 3.0], [2.0, 5.0, 6.0], [3.0, 6.0, 7.0]])
    assert_allclose(calc_section.stress, stress)
    assert_allclose(calc_section.results["stress"], stress)


def test_calc_num_stress(numerical_stress_section):
    stress = 1.0 * np.array([[1.0, 2.0, 3.0], [2.0, 5.0, 6.0], [3.0, 6.0, 7.0]])
    assert_allclose(numerical_stress_section.stress, stress)
    assert_allclose(numerical_stress_section.results["stress"], stress)


def test_calc_free_energy(calc_section):
    free_energy = -3.169503986610555e05
    assert np.abs(calc_section.free_energy - free_energy) < eps_hp
    assert np.abs(calc_section.results["free_energy"] - free_energy) < eps_hp


def test_calc_energy(calc_section):
    energy = -3.169503986610555e05
    assert np.abs(calc_section.energy - energy) < eps_hp
    assert np.abs(calc_section.results["energy"] - energy) < eps_hp


def test_calc_magnetic_moment(calc_section):
    magmom = 0
    assert calc_section.magmom == magmom
    assert calc_section.results["magmom"] == magmom


def test_calc_n_iter(calc_section):
    n_iter = 58
    assert calc_section.n_iter == n_iter
    assert calc_section.results["n_iter"] == n_iter


def test_calc_fermi_energy(calc_section):
    Ef = -8.24271207
    assert np.abs(calc_section.E_f - Ef) < eps_lp
    assert np.abs(calc_section.results["fermi_energy"] - Ef) < eps_lp


def test_calc_dipole(calc_section):
    assert calc_section.dipole is None


def test_calc_is_metallic(calc_section):
    assert calc_section.is_metallic


def test_calc_converged(calc_section):
    assert calc_section.converged


def test_calc_mulliken_charges(calc_section):
    mulliken_charges = [0.617623, -0.617623]
    assert_allclose(calc_section.mulliken_charges, mulliken_charges)
    assert_allclose(calc_section.results["mulliken_charges"], mulliken_charges)


def test_calc_mulliken_spins(calc_section):
    # TARP: False numbers added to test parsing
    mulliken_spins = [-0.003141, 0.002718]
    assert_allclose(calc_section.mulliken_spins, mulliken_spins)
    assert_allclose(calc_section.results["mulliken_spins"], mulliken_spins)


def test_calc_hirshfeld_charges(calc_section):
    hirshfeld_charges = [0.20898543, -0.20840994]
    assert_allclose(calc_section.hirshfeld_charges, hirshfeld_charges)
    assert_allclose(calc_section.results["hirshfeld_charges"], hirshfeld_charges)


def test_calc_hirshfeld_volumes(calc_section):
    hirshfeld_volumes = [73.39467444, 62.86011074]
    assert_allclose(calc_section.hirshfeld_volumes, hirshfeld_volumes)
    assert_allclose(calc_section.results["hirshfeld_volumes"], hirshfeld_volumes)


def test_calc_hirshfeld_atomic_dipoles(calc_section):
    hirshfeld_atomic_dipoles = np.zeros((2, 3))
    assert_allclose(calc_section.hirshfeld_atomic_dipoles, hirshfeld_atomic_dipoles)
    assert_allclose(calc_section.results["hirshfeld_atomic_dipoles"], hirshfeld_atomic_dipoles)


def test_calc_hirshfeld_dipole(calc_section):
    assert calc_section.hirshfeld_dipole is None


@pytest.fixture()
def molecular_header_section():
    with open(f"{parser_file_dir}/molecular_header_section.out", mode="rt") as file:
        lines = file.readlines()

    for ll, line in enumerate(lines):
        lines[ll] = line.strip()

    return AimsOutHeaderSection(lines)


@pytest.mark.parametrize(
    "attr_name",
    ["k_points", "k_point_weights", "n_k_points"],
)
def test_section_molecular_header_defaults_none(attr_name, molecular_header_section):
    assert getattr(molecular_header_section, attr_name) is None


def test_molecular_header_n_bands(molecular_header_section):
    assert molecular_header_section.n_bands == 7


def test_molecular_header_initial_geometry(molecular_header_section, molecular_positions):
    assert len(molecular_header_section.initial_geometry) == 3
    assert [sym for sym in molecular_header_section.initial_geometry.symbols] == ["O", "H", "H"]
    assert_allclose(
        molecular_header_section.initial_geometry.positions,
        [[0, 0, 0], [0.95840000, 0, 0], [-0.24000000, 0.92790000, 0]],
    )


@pytest.fixture()
def molecular_calc_section(molecular_header_section):
    with open(f"{parser_file_dir}/molecular_calc_section.out", mode="rt") as file:
        lines = file.readlines()

    for idx, line in enumerate(lines):
        lines[idx] = line.strip()
    return AimsOutCalcSection(lines, molecular_header_section)


@pytest.fixture()
def molecular_positions():
    return np.array([[-0.00191785, -0.00243279, 0], [0.97071531, -0.00756333, 0], [-0.25039746, 0.93789612, 0]])


def test_molecular_calc_atoms(molecular_calc_section, molecular_positions):
    print(molecular_calc_section.geometry)
    assert len(molecular_calc_section.geometry.symbols) == 3
    assert_allclose(molecular_calc_section.geometry.positions, molecular_positions)
    assert [sym for sym in molecular_calc_section.geometry.symbols] == ["O", "H", "H"]


def test_molecular_calc_forces(molecular_calc_section):
    forces = np.array(
        [
            [0.502371357164392e-03, 0.518627676606471e-03, 0.000000000000000e00],
            [-0.108826758257187e-03, -0.408128912334209e-03, -0.649037698626122e-27],
            [-0.393544598907207e-03, -0.110498764272267e-03, -0.973556547939183e-27],
        ]
    )
    assert_allclose(molecular_calc_section.forces, forces)
    assert_allclose(molecular_calc_section.results["forces"], forces)


@pytest.mark.parametrize("attrname", ["stresses", "stress", "magmom", "E_f"])
def test_section_molecular_defaults_none(attrname, molecular_calc_section):
    assert getattr(molecular_calc_section, attrname) is None


def test_molecular_calc_free_energy(molecular_calc_section):
    free_energy = -2.206778551123339e04
    assert np.abs(molecular_calc_section.free_energy - free_energy) < eps_hp
    assert np.abs(molecular_calc_section.results["free_energy"] - free_energy) < eps_hp


def test_molecular_calc_energy(molecular_calc_section):
    energy = -2.206778551123339e04
    assert np.abs(molecular_calc_section.energy - energy) < eps_hp
    assert np.abs(molecular_calc_section.results["energy"] - energy) < eps_hp


def test_molecular_calc_n_iter(molecular_calc_section):
    n_iter = 7
    assert molecular_calc_section.n_iter == n_iter
    assert molecular_calc_section.results["n_iter"] == n_iter


def test_molecular_calc_dipole(molecular_calc_section):
    dipole = [0.260286493869765, 0.336152447755231, 0.470003778119121e-15]
    assert_allclose(molecular_calc_section.dipole, dipole)
    assert_allclose(molecular_calc_section.results["dipole"], dipole)


def test_molecular_calc_is_metallic(molecular_calc_section):
    assert not molecular_calc_section.is_metallic


def test_molecular_calc_converged(molecular_calc_section):
    assert molecular_calc_section.converged


def test_molecular_calc_hirshfeld_charges(molecular_calc_section):
    molecular_hirshfeld_charges = np.array([-0.32053200, 0.16022630, 0.16020375])
    assert_allclose(molecular_calc_section.hirshfeld_charges, molecular_hirshfeld_charges)
    assert_allclose(molecular_calc_section.results["hirshfeld_charges"], molecular_hirshfeld_charges)


def test_molecular_calc_hirshfeld_volumes(molecular_calc_section):
    hirshfeld_volumes = np.array([21.83060659, 6.07674041, 6.07684447])
    assert_allclose(molecular_calc_section.hirshfeld_volumes, hirshfeld_volumes)
    assert_allclose(molecular_calc_section.results["hirshfeld_volumes"], hirshfeld_volumes)


def test_molecular_calc_hirshfeld_atomic_dipoles(molecular_calc_section):
    hirshfeld_atomic_dipoles = np.array(
        [[0.04249319, 0.05486053, 0], [0.13710134, -0.00105126, 0], [-0.03534982, 0.13248706, 0]]
    )
    assert_allclose(molecular_calc_section.hirshfeld_atomic_dipoles, hirshfeld_atomic_dipoles)
    assert_allclose(
        molecular_calc_section.results["hirshfeld_atomic_dipoles"],
        hirshfeld_atomic_dipoles,
    )


def test_molecular_calc_hirshfeld_dipole(molecular_calc_section, molecular_positions):
    molecular_hirshfeld_charges = np.array([-0.32053200, 0.16022630, 0.16020375])
    hirshfeld_dipole = np.sum(molecular_hirshfeld_charges.reshape((-1, 1)) * molecular_positions, axis=1)

    assert_allclose(molecular_calc_section.hirshfeld_dipole, hirshfeld_dipole)
    assert_allclose(molecular_calc_section.results["hirshfeld_dipole"], hirshfeld_dipole)
