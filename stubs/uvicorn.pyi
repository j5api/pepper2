"""
Type stubs for uvicorn.

This only covers the functions that we used, and may not reflect the
actual structure of the uvicorn module, just the interface that it exposes.
"""

from typing import Optional


def run(
    app: str,
    *,
    host: Optional[str],
    port: Optional[int],
    debug: Optional[bool],
    reload: Optional[bool],
    workers: Optional[int],
) -> None: ...
