"""
Core operations for the API.

Essentially just miscellaneous things that don't fit better
elsewhere, but are still important.
"""

from fastapi import APIRouter

from pepper2 import __version__

router = APIRouter()


@router.get(
    "/version",
    tags=["version"],
    summary="Daemon Version",
    response_description="Version number of the daemon.",
)
def version() -> str:
    """
    Get the version of the pepper2 daemon.

    This will match the version number on the Python package.

    It should conform to the numbering standards in PEP440.
    """
    return __version__
