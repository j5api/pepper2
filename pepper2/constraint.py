"""
USB Constraint.

Defines a set of parameters that a USB / Folder can conform to.
"""
from abc import ABCMeta, abstractmethod
from pathlib import Path


class Constraint(metaclass=ABCMeta):
    """A constraint that a path can match."""

    @abstractmethod
    def matches(self, path: Path) -> bool:
        """Return true if path matches the constraint."""
        raise NotImplementedError  # pragma: nocover


class FilePresentConstraint(Constraint):
    """Ensure that a file is present."""

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def matches(self, path: Path) -> bool:
        """Check if the path contains the file."""
        return all([
            path.exists(),
            path.is_dir(),
            path.joinpath(self.filename).exists(),
        ])


class NumberOfFilesConstraint(Constraint):
    """Ensure that n files are present."""

    def __init__(self, n: int):
        self.n = n

    def matches(self, path: Path) -> bool:
        """Check that the path contains n files."""
        if all([
            path.exists(),
            path.is_dir(),
        ]):
            return self.n == len(list(path.iterdir()))
        else:
            return False


class OrConstraint(Constraint):
    """Ensure that either of the constraints match."""

    def __init__(self, a: Constraint, b: Constraint) -> None:
        self.a = a
        self.b = b

    def matches(self, path: Path) -> bool:
        """Check if either of the constraints match."""
        return any([
            self.a.matches(path),
            self.b.matches(path),
        ])


class AndConstraint(Constraint):
    """Ensure that both of the constraints match."""

    def __init__(self, a: Constraint, b: Constraint) -> None:
        self.a = a
        self.b = b

    def matches(self, path: Path) -> bool:
        """Check that both of the constraints match."""
        return all([
            self.a.matches(path),
            self.b.matches(path),
        ])


class NotConstraint(Constraint):
    """Ensure that the constraint does not match."""

    def __init__(self, a: Constraint):
        self.a = a

    def matches(self, path: Path) -> bool:
        """Check that the constraint does not match."""
        return not self.a.matches(path)


class TrueConstraint(Constraint):
    """A constraint that is always true."""

    def matches(self, _: Path) -> bool:
        """Always return true."""
        return True
