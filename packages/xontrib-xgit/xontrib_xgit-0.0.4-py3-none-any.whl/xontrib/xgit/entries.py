"""
An reference to a `GitObject` in the repository.

This incudes `GitCommit`, `GitTree`, `GitTagObject` objects, as well as
refs and entries in trees.
"""

from typing import Any, Optional
from pathlib import Path

from xonsh.lib.pretty import RepresentationPrinter
from xontrib.xgit.types import (
    GitEntryMode,
)
from xontrib.xgit.git_types import (
    GitObject, GitTreeEntry,
)


class _GitTreeEntry(GitTreeEntry):
    """
    An entry in a git tree. In addition to referencing a `GitObject`,
    it supplies the mode and name.
    """

    _name: str
    _object: GitObject
    _mode: GitEntryMode
    _path: Path

    @property
    def type(self):
        return self._object.type

    @property
    def hash(self):
        return self._object.hash

    @property
    def mode(self):
        return self._mode

    @property
    def size(self):
        return self._object.size

    @property
    def object(self):
        return self._object

    @property
    def prefix(self):
        """
        Return the prefix for the entry type.
        """
        if self.type == "tree":
            return "D"
        elif self.mode == "120000":
            return "L"
        elif self.mode == "160000":
            return "S"
        elif self.mode == "100755":
            return "X"
        else:
            return"-"

    @property
    def name(self):
        return self._name

    @property
    def entry(self):
        rw = self.prefix
        return f"{rw} {self.type} {self.hash}\t{self.name}"

    @property
    def entry_long(self):
        size = str(self.size) if self.size >= 0 else '-'
        rw = self.prefix
        return f"{rw} {self.type} {self.hash} {size:>8s}\t{self.name}"

    @property
    def path(self):
        return self._path

    def __init__(self, object: GitObject, name: str, mode: GitEntryMode, path: Optional[Path] = None):
        self._object = object
        self._name = name
        self._mode = mode
        self._path = path or Path(name)

    def __getattr__(self, name):
        try:
            return getattr(self._object, name)
        except AttributeError:
            raise AttributeError(f"GitTreeEntry has no attribute {name!r}") from None

    #def __hasattr__(self, name):
    #    return hasattr(self._object, name)

    def __getitem__(self, name):
        # Only implemented for trees, but we'll let the object raise the exception.
        return self._object[name] # type: ignore

    def __contains__(self, name):
        return name in self._object

    def __str__(self):
        return f"{self.entry_long} {self.name}"

    def __repr__(self):
        return f"GitTreeEntry({self.name!r}, {self.entry_long!r})"

    def __format__(self, fmt: str):
        return f"{self.entry_long.__format__(fmt)}"

    def _repr_pretty_(self, p: RepresentationPrinter, cycle: bool):
        if cycle:
            p.text("GitTreeEntry(...)")
        else:
            with p.group(4, "GitTreeEntry(", ')'):
                p.breakable()
                p.pretty(self._object)
                p.text(',')
                p.breakable()
                p.text(f'mode{self.mode!r},')
                p.breakable()
                p.text(f'name={self.name!r}')
