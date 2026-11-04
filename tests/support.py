"""Repository-contained scratch directories compatible with Windows sandbox ACLs."""

import shutil
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4


@contextmanager
def scratch_directory() -> Iterator[str]:
    """Create and remove only this test's uniquely owned workspace directory."""
    root = Path(__file__).resolve().parent.parent
    path = root / ".runs" / f"test-{uuid4()}"
    path.mkdir(parents=True)
    try:
        yield str(path)
    finally:
        if not path.resolve().is_relative_to(root / ".runs"):
            raise RuntimeError("Refusing cleanup outside the test workspace.")
        shutil.rmtree(path)
