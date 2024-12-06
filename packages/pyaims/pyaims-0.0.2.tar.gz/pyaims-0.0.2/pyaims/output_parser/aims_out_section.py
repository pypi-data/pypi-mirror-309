"""AIMS output parser base class."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

__author__ = "Thomas A. R. Purcell and Andrey Sobolev"
__version__ = "1.0"
__email__ = "purcellt@arizona.edu and andrey.n.sobolev@gmail.com"
__date__ = "July 2024"

# TARP: Originally an object, but type hinting needs this to be an int
LINE_NOT_FOUND = -1000
EV_PER_A3_TO_KBAR = 1.60217653e-19 * 1e22


class ParseError(Exception):
    """Parse error during reading of a file."""


class AimsParseError(Exception):
    """Exception raised if an error occurs when parsing an Aims output file."""

    def __init__(self, message: str) -> None:
        """Initialize the error with the message, message."""
        self.message = message
        super().__init__(self.message)


@dataclass
class AimsOutSection:
    """Base class for AimsOutSections.

    Attributes:
        _lines (list[str]): The list of all lines in the chunk
        _prop_line_relation (dict[str, list[int]]): Dictionary containing where     
    """

    _lines: list[str] = field(default_factory=list)
    _prop_line_relation: dict[str, list[int]] = field(default_factory=dict)
    _cache: dict[str, Any] = field(default_factory=dict)
    
    def set_prop_line_relations(self, prop_line_keys: dict[str, list[str]]):
        """Setup the property line maps
        
        Args:
            prop_line_keys (dict[str, str]): Dictionary mapping a property to a keystring in the aims.out file
        """
        for key in prop_line_keys.keys():
            if key not in self._prop_line_relation:
                self._prop_line_relation[key] = []
        
        for ll, line in enumerate(self._lines):
            for key, val in prop_line_keys.items():
                if any([vv in line for vv in val]):
                    self._prop_line_relation[key].append(ll)
                    break


    def _parse_key_value_pair(self, key: str, allow_fail=False, dtype: type=str) -> Any:
        """Parse a peice of compilation information
        
        Args:
            key (str): The key to parse
            allow_fail (bool): If True if line is not present return None, else raise an Exception
            dtype (type): Type of the data
        """
        if key in self._cache:
            return self._cache[key]
        
        if key not in self._prop_line_relation:
            return None

        try:
            line_start = self.get_line_inds(key)[-1]
        except IndexError:
            if not allow_fail:
                raise AimsParseError(f"No information about {key} in the aims-output file")
            self._cache[key] = None
            return None
        
        self._cache[key] = dtype(self.lines[line_start].split(":")[1].strip())
        return self._cache[key]
    
    @property 
    def prop_line_relation(self):
        """Get all instences where a particular keyword is found in the section"""
        return self._prop_line_relation

    @property
    def lines(self):
        """The content lines for the calculation"""
        return self._lines
    
    def get_line_inds(self, prop_key: str) -> list[int]:
        """Get all line indexes for particular property key
        
        Args:
            prop_key (str): property key to get the lines for

        Returns:
            list[int]: All lines where that property key is found
        """
        if prop_key not in self._prop_line_relation:
            raise ValueError(f"The property key {prop_key} was not found")

        return self._prop_line_relation[prop_key]
