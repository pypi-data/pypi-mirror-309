"""Tests for basis_function module."""

from pyaims.species_defaults.basis_function import (
    BasisFunction,
    HydroBasisFunction,
    IonicBasisFunction, GaussianBasisFunction
)

def test_basis_function():
    """Tests a generic BasisFunction constructor."""
    string = "    hydro 4 f 5.6"
    basis_function = BasisFunction.from_string(string)
    assert basis_function.type == "hydro"
    assert basis_function.enabled
    string = "#    hydro 4 f 5.6"
    basis_function = BasisFunction.from_string(string)
    assert basis_function.type == "hydro"
    assert not basis_function.enabled


def test_hydro_basis_function():
    """Tests hydrogen-like BasisFunction constructor."""
    string = "    hydro 4 f 5.6"
    basis_function = HydroBasisFunction.from_string(string)
    assert basis_function.type == "hydro"
    assert basis_function.z_eff == 5.6


def test_ionic_basis_function():
    """Tests ionic BasisFunction constructor."""
    string = "    ionic 4 d auto"
    basis_function = IonicBasisFunction.from_string(string)
    assert basis_function.n == 4
    assert basis_function.radius == "auto"
    string = "    ionic 3 d 2.5"
    basis_function = IonicBasisFunction.from_string(string)
    assert basis_function.n == 3
    assert basis_function.radius == 2.5


def test_gaussian_basis_function():
    """Tests Gaussian-based BasisFunction constructor."""
    string = "gaussian 0 1  0.105555E+08"
    basis_function = GaussianBasisFunction.from_string(string)
    assert basis_function.enabled
    assert basis_function.type == "gaussian"
    assert basis_function.n == 1
    assert len(basis_function.alpha_i) == 1
    assert basis_function.alpha_i[0] == 1.05555e7
    string = "# gaussian 0 1  0.105555E+08"
    basis_function = BasisFunction.from_string(string)
    assert not basis_function.enabled
