import numpy as np
from pathlib import Path

from pyaims.geometry.geometry import AimsGeometry
from pyaims.geometry.atom import ATOMIC_SYMBOLS_TO_NUMBERS

from tests import DATA_DIR

GEO_DATA_DIR = DATA_DIR / "geometry"

h2o_content = """# Making from pyaims
atom         0.000000000000e+00   0.000000000000e+00   0.000000000000e+00 O
    magnetic_response
    nuclear_spin 1.000000000000
    isotope 17.0
atom         7.070000000000e-01  -7.070000000000e-01   0.000000000000e+00 H
    magnetic_response
    magnetic_moment 0.500000000000
atom        -7.070000000000e-01  -7.070000000000e-01   0.000000000000e+00 H
empty       -1.000000000000e+00   0.000000000000e+00   0.000000000000e+00 O
pseudocore   1.000000000000e+00   0.000000000000e+00   0.000000000000e+00 O"""

scr_content = """# Making from pyaims
lattice_vector -2.612201390000000e+00 2.612201390000000e+00 5.091086090000000e+00
lattice_vector 2.612201390000000e+00 -2.612201390000000e+00 5.091086090000000e+00
lattice_vector 2.612201390000000e+00 2.612201390000000e+00 -5.091086090000000e+00
atom_frac    5.000000000000e-01   5.000000000000e-01  -5.000000000000e-03 Al
atom_frac    7.500000000000e-01   2.500000000000e-01   5.000000000000e-01 Al
atom_frac    1.604770860000e+00   1.622146130000e+00   1.491642500000e+00 S
atom_frac    1.305036200000e-01   1.131283600000e-01  -1.491642500000e+00 S
atom_frac   -1.622146130000e+00  -1.305036200000e-01  -1.737527000000e-02 S
atom_frac   -1.131283600000e-01  -1.604770860000e+00   1.737527000000e-02 S
atom_frac    0.000000000000e+00  -0.000000000000e+00   0.000000000000e+00 Zn
symmetry_n_params 5 2 3
symmetry_params a c x4 y4 z4
symmetry_lv -(1.0/2.0)*a , (1.0/2.0)*a , (1.0/2.0)*c
symmetry_lv (1.0/2.0)*a , -(1.0/2.0)*a , (1.0/2.0)*c
symmetry_lv (1.0/2.0)*a , (1.0/2.0)*a , -(1.0/2.0)*c
symmetry_frac (1.0/2.0) , (1.0/2.0) , 0.0
symmetry_frac (3.0/4.0) , (1.0/4.0) , (1.0/2.0)
symmetry_frac (y4+z4) , (z4+x4) , (x4+y4)
symmetry_frac (z4-y4) , (z4-x4) , -(x4+y4)
symmetry_frac -(z4+x4) , (y4-z4) , (y4-x4)
symmetry_frac (x4-z4) , -(y4+z4) , (x4-y4)
symmetry_frac 0.0 , 0.0 , 0.0"""

mg2mn4o8_content = """# Making from pyaims
lattice_vector 5.068823430000000e+00 1.248800000000000e-04 -2.661101670000000e+00
lattice_vector -1.397042340000000e+00 4.872499110000000e+00 -2.661102030000000e+00
lattice_vector 9.860910000000001e-03 1.308528000000000e-02 6.176493590000000e+00
    constrain_relaxation z 
atom_frac    3.748972600000e-01   6.251027400000e-01   7.500000200000e-01 Mg
atom_frac    6.251027400000e-01   3.748972600000e-01   2.499999800000e-01 Mg
atom_frac   -2.692415593343e-19  -3.560208392073e-19   5.000000000000e-01 Mn
    initial_charge 0.500000000000
    initial_moment 4.500000000000
atom_frac    0.000000000000e+00   5.000000000000e-01   0.000000000000e+00 Mn
    initial_moment 5.000000000000
atom_frac    5.000000000000e-01   0.000000000000e+00   5.000000000000e-01 Mn
    initial_moment 5.000000000000
atom_frac    0.000000000000e+00   0.000000000000e+00   0.000000000000e+00 Mn
    initial_moment 5.000000000000
atom_frac    7.540230900001e-01   7.782675000001e-01   5.080588200001e-01 O
    velocity   1.000000000000e+00   2.000000000000e+00   3.000000000000e+00
atom_frac    7.702028500000e-01   2.459477900001e-01   9.919131600001e-01 O
    RT_TDDFT_initial_velocity   1.000000000000e+01   2.000000000000e+01   3.000000000000e+01
atom_frac    2.217325400000e-01   2.459768899999e-01   9.919411600000e-01 O
atom_frac    2.459769100000e-01   2.217324999999e-01   4.919411800000e-01 O
    constrain_relaxation x y 
    constraint_region 1
atom_frac    2.459476500000e-01   7.702028800001e-01   4.919131300000e-01 O
atom_frac    2.297971500000e-01   7.540522099999e-01   8.086839999943e-03 O
atom_frac    7.540523500000e-01   2.297971199999e-01   5.080868700000e-01 O
atom_frac    7.782674600000e-01   7.540231100001e-01   8.058839999985e-03 O"""

def test_h2o():
    geometry = AimsGeometry.from_file(f"{GEO_DATA_DIR}/h2o.in")
    positions = np.array(
        [
            [0.0, 0.0, 0.0],
            [0.707, -0.707, 0.0],
            [-0.707, -0.707, 0.0],
            [-1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
        ]
    )
    all_none_atom_attrs = [
        "velocities",
        "RT_TDDFT_initial_velocities",
        "nuclear_constraints",
        "constraint_regions",
    ]
    geo_none_attrs = [
        "lattice_vectors",
        "lattice_constraints",
        "hessian_block",
        "hessian_block_lv",
        "hessian_block_lv_atoms",
        "hessian_file",
        "trust_radius",
        "symmetry_n_params",
        "symmetry_params",
        "symmetry_lv",
        "symmetry_frac",
        "symmetry_frac_change_threshold",
        "homogeneous_field",
        "multipole",
        "esp_constraint",
        "calculate_friction",
    ]
    assert geometry.symbols == ["O", "H", "H", "O", "O"]
    assert geometry.numbers == [8, 1, 1, 8, 8]
    assert np.allclose(geometry.positions, positions)
    assert np.allclose(geometry.initial_charges, np.zeros(5))
    assert np.allclose(geometry.initial_moments, np.zeros(5))
    assert geometry.is_empty_atoms == [False, False, False, True, False]
    assert geometry.is_pseudocore_atoms == [False, False, False, False, True]
    assert geometry.magnetic_responses == [True, True, None, None, None]
    assert geometry.nuclear_spins == [1.0, None, None, None, None]
    assert geometry.isotopes == [17, None, None, None, None]
    assert geometry.magnetic_moments == [None, 0.5, None, None, None]

    for attr in all_none_atom_attrs:
        assert all([val is None for val in getattr(geometry, attr)])

    for attr in geo_none_attrs:
        assert getattr(geometry, attr) is None

    assert geometry.file_content == h2o_content

def test_scr():
    geometry = AimsGeometry.from_file(f"{GEO_DATA_DIR}/scr.in")
    positions = np.array(
        [
            [ 0.50000000, 0.50000000, -0.00500000],
            [ 0.75000000, 0.25000000,  0.50000000],
            [ 1.60477086, 1.62214613,  1.49164250],
            [ 0.13050362, 0.11312836, -1.49164250],
            [-1.62214613,-0.13050362, -0.01737527],
            [-0.11312836,-1.60477086,  0.01737527],
            [ 0.00000000, 0.00000000,  0.00000000],
        ]
    )
    symmetry_lv = [
        ["-(1.0/2.0)*a", "(1.0/2.0)*a", "(1.0/2.0)*c"],
        ["(1.0/2.0)*a", "-(1.0/2.0)*a", "(1.0/2.0)*c"],
        ["(1.0/2.0)*a", "(1.0/2.0)*a", "-(1.0/2.0)*c"],
    ]
    symmetry_frac = [
        ["(1.0/2.0)", "(1.0/2.0)", "0.0"],
        ["(3.0/4.0)", "(1.0/4.0)", "(1.0/2.0)"],
        ["(y4+z4)", "(z4+x4)", "(x4+y4)"],
        ["(z4-y4)", "(z4-x4)", "-(x4+y4)"],
        ["-(z4+x4)", "(y4-z4)", "(y4-x4)"],
        ["(x4-z4)", "-(y4+z4)", "(x4-y4)"],
        ["0.0", "0.0", "0.0"],
    ]
    all_none_atom_attrs = [
        "velocities",
        "RT_TDDFT_initial_velocities",
        "nuclear_constraints",
        "constraint_regions",
        "magnetic_responses",
        "magnetic_moments",
        "nuclear_spins",
        "isotopes",
    ]
    geo_none_attrs = [
        "hessian_block",
        "hessian_block_lv",
        "hessian_block_lv_atoms",
        "hessian_file",
        "trust_radius",
        "homogeneous_field",
        "multipole",
        "esp_constraint",
        "calculate_friction",
    ]
    assert geometry.symbols == ["Al", "Al", "S", "S", "S", "S", "Zn"]
    assert geometry.numbers == [ATOMIC_SYMBOLS_TO_NUMBERS[sym] for sym in ["Al", "Al", "S", "S", "S", "S", "Zn"]]
    assert np.allclose(geometry.fractional_positions, positions)
    assert np.allclose(geometry.initial_charges, np.zeros(7))
    assert np.allclose(geometry.initial_moments, np.zeros(7))
    assert not any(geometry.is_empty_atoms)
    assert not any(geometry.is_pseudocore_atoms)
    assert not any(np.array(geometry.lattice_constraints).flatten())
    for attr in all_none_atom_attrs:
        assert all([val is None for val in getattr(geometry, attr)])

    for attr in geo_none_attrs:
        assert getattr(geometry, attr) is None

    assert geometry.symmetry_n_params == (5, 2, 3)
    assert geometry.symmetry_params == ["a", "c", "x4", "y4", "z4"]
    assert geometry.symmetry_lv == symmetry_lv
    assert geometry.symmetry_frac == symmetry_frac
    assert geometry.file_content == scr_content

def test_mg2mn4o8():
    geometry = AimsGeometry.from_file(f"{GEO_DATA_DIR}/mg2mn4o8.in")
    positions = np.array(
        [
            [1.034388703398e+00, 3.055673321740e+00,  1.971268420993e+00],
            [2.647253296602e+00, 1.830035948260e+00, -1.116978530993e+00],
            [4.930455000000e-03, 6.542640000000e-03,  3.088246795000e+00],
            [-6.985211700000e-01, 2.436249555000e+00, -1.330551015000e+00],
            [2.539342170000e+00, 6.605080000000e-03,  1.757695960000e+00],
            [0.000000000000e+00, 0.000000000000e+00,  0.000000000000e+00],
            [2.739747178306e+00, 3.798849955412e+00, -9.395592830776e-01],
            [3.570203942272e+00, 1.211456032248e+00,  3.422465020960e+00],
            [7.900644064579e-01, 1.211529695387e+00,  4.882095782598e+00],
            [9.418948216942e-01, 1.086859314588e+00,  1.793849173078e+00],
            [1.755098882262e-01, 3.759280382304e+00,  3.342181446544e-01],
            [1.114380577281e-01, 3.674253237752e+00, -2.568175130960e+00],
            [3.506132111774e+00, 1.126428887696e+00,  5.200717453456e-01],
            [2.891577593542e+00, 3.674179574613e+00, -4.027805892598e+00],
        ]
    )

    symbols = ["Mg", "Mg", "Mn", "Mn", "Mn", "Mn", "O", "O", "O", "O", "O", "O", "O", "O"]
    initial_charges = np.zeros(14)
    initial_charges[2] = 0.5
    initial_moments = np.zeros(14)
    initial_moments[2:6] = [4.5, 5, 5, 5]
    constraint_regions = 14 * [None]
    constraint_regions[-5] = 1
    nuclear_constraints = 14 * [None]
    nuclear_constraints[-5] = [True, True, False]
    RT_TDDFT_initial_velocities = 14 * [None]
    RT_TDDFT_initial_velocities[-7] = [10.0, 20.0, 30.0]
    velocities = 14 * [None]
    velocities[-8] = [1.0, 2.0, 3.0]
    all_none_atom_attrs = [
        "magnetic_responses",
        "magnetic_moments",
        "nuclear_spins",
        "isotopes",
    ]
    geo_none_attrs = [
        "hessian_block",
        "hessian_block_lv",
        "hessian_block_lv_atoms",
        "hessian_file",
        "trust_radius",
        "symmetry_n_params",
        "symmetry_params",
        "symmetry_lv",
        "symmetry_frac",
        "symmetry_frac_change_threshold",
        "homogeneous_field",
        "multipole",
        "esp_constraint",
        "calculate_friction",
    ]
    assert geometry.symbols == symbols
    assert geometry.numbers == [ATOMIC_SYMBOLS_TO_NUMBERS[sym] for sym in symbols]
    assert np.allclose(geometry.positions, positions, 1e-08)
    assert np.allclose(geometry.initial_charges, initial_charges)
    assert np.allclose(geometry.initial_moments, initial_moments)
    assert geometry.constraint_regions == constraint_regions
    for test, ref in zip (geometry.nuclear_constraints, nuclear_constraints):
        assert test == ref
    for test, ref in zip (geometry.RT_TDDFT_initial_velocities, RT_TDDFT_initial_velocities):
        assert test == ref
    for test, ref in zip(geometry.velocities, velocities):
        assert test == ref

    assert np.allclose(
        geometry.lattice_vectors, 
        np.array(
            [
                [ 5.068823430000e+00,  1.248800000000e-04, -2.661101670000e+00], 
                [-1.397042340000e+00,  4.872499110000e+00, -2.661102030000e+00], 
                [ 9.860910000000e-03,  1.308528000000e-02,  6.176493590000e+00]
            ]
        )
    )
    assert np.all(
        np.array(geometry.lattice_constraints) == np.array([[False, False, False], [False, False, False], [False, False, True]])
    )
    
    for attr in all_none_atom_attrs:
        assert all([val is None for val in getattr(geometry, attr)])

    assert not any(geometry.is_empty_atoms)
    assert not any(geometry.is_pseudocore_atoms)

    for attr in geo_none_attrs:
        assert getattr(geometry, attr) is None

    # assert geometry.file_content == mg2mn4o8_content
