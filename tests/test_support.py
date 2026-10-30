"""Repository-contained scratch directories compatible with Windows sandbox ACLs."""

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
import shutil
from uuid import uuid4


@contextmanager
def scratch_directory() -> Iterator[str]:
    """Create and remove only this test's uniquely owned workspace directory."""
    root = Path.cwd().resolve()
    path = root / ".runs" / f"test-{uuid4()}"
    path.mkdir(parents=True)
    try:
        yield str(path)
    finally:
        if not path.resolve().is_relative_to(root / ".runs"):
            raise RuntimeError("Refusing cleanup outside the test workspace.")
        shutil.rmtree(path)
