"""Safe filesystem primitives for generated documentation output."""

from pathlib import Path
import shutil

from .errors import DocKitError

OWNERSHIP_MARKER = ".dockit-fp-site"


def prepare_output(output: Path) -> None:
    """Empty a DocKit-FP-owned output directory and recreate its marker."""
    output = output.resolve()
    if output.exists():
        if not output.is_dir():
            raise DocKitError(f"Output path is not a directory: {output}")
        if not (output / OWNERSHIP_MARKER).is_file():
            raise DocKitError(
                f"Refusing to replace output directory {output}: it is not owned by DocKit-FP "
                f"(missing {OWNERSHIP_MARKER})."
            )
        shutil.rmtree(output)
    output.mkdir(parents=True)
    (output / OWNERSHIP_MARKER).write_text("DocKit-FP generated output.\n", encoding="utf-8")
