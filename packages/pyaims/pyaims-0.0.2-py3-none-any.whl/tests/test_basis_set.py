"""Tests for BasisSet class"""

from textwrap import dedent

from pyaims.species_defaults.basis_set import BasisSet


def test_basis_set():
    basis_string = dedent("""\
    #  "First tier" - improvements: -1014.90 meV to -62.69 meV
     hydro 2 s 2.1
     hydro 2 p 3.5
    #  "Second tier" - improvements: -12.89 meV to -1.83 meV
         hydro 1 s 0.85
    #     hydro 2 p 3.7
    #     hydro 2 s 1.2
      for_aux    hydro 3 d 7
    #  "Third tier" - improvements: -0.25 meV to -0.12 meV
    #     hydro 4 f 11.2
    #     hydro 3 p 4.8
    #     hydro 4 d 9
    #     hydro 3 s 3.2
    """)
    basis_set = BasisSet.from_string(basis_string)
    assert basis_set.n_tiers == 3
    assert len(basis_set.tier(1)) == 2
    assert len(basis_set.tier(2)) == 3
    assert len(basis_set.tier(2, enabled=True)) == 1
    assert len(basis_set.tier(2, enabled=True, aux=True)) == 1
    assert len(basis_set.tier(3, enabled=True)) == 0
    basis_set.activate_tier(2, 1)
    assert len(basis_set.tier(2, enabled=True)) == 2
    basis_set.deactivate_tier(2, "all", aux=True)
    assert len(basis_set.tier(2, enabled=True, aux=True)) == 0
    basis_set.activate_tier(3, "all")
    assert len(basis_set.tier(3, enabled=True)) == 4

