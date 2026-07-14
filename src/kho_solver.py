"""Portable wrapper around the bundled original JavaKh class files."""

from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess
import tempfile


SOURCE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SOURCE_DIR / "javakh_ori_temp"
JARS = (
    "log4j-1.2.12.jar",
    "commons-io-1.2.jar",
    "commons-cli-1.0.jar",
    "commons-logging-1.1.jar",
)
RESULT_RE = re.compile(r'"(q\^[^"]*)"')


class JavaKhError(RuntimeError):
    """Raised when the bundled JavaKh process cannot produce a result."""


def _pd_code_wrapper(pd_code: list[list[int]]) -> str:
    return "PD[" + ", ".join("X" + str(crossing) for crossing in pd_code) + "]"


def _classpath() -> str:
    entries = [TEMPLATE_DIR, *(TEMPLATE_DIR / "jars" / name for name in JARS)]
    missing = [path for path in entries if not path.exists()]
    if missing:
        raise JavaKhError("bundled JavaKh files are missing: " + ", ".join(map(str, missing)))
    return os.pathsep.join(str(path) for path in entries)


def kho_solver(
    pd_code: list[list[int]],
    *,
    java_path: str | os.PathLike[str] | None = None,
    max_memory: str = "2g",
    timeout: float | None = 120,
) -> str:
    """Compute integral Khovanov homology with the bundled JavaKh classes."""

    java = str(java_path or os.environ.get("JAVAKH_JAVA") or "java")
    if not max_memory or any(character.isspace() for character in max_memory):
        raise ValueError("max_memory must be one Java -Xmx value such as '2g' or '1024m'")

    with tempfile.TemporaryDirectory(prefix="khovanov_solver_legacy_") as tmp:
        workdir = Path(tmp)
        (workdir / "PD.txt").write_text(_pd_code_wrapper(pd_code) + "\n", encoding="ascii")
        try:
            result = subprocess.run(
                [
                    java,
                    f"-Xmx{max_memory}",
                    "-classpath",
                    _classpath(),
                    "org.katlas.JavaKh.JavaKh",
                ],
                cwd=workdir,
                text=True,
                encoding="utf-8",
                errors="replace",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
                check=False,
            )
        except FileNotFoundError as exc:
            raise JavaKhError(
                f"Java executable not found: {java!r}; pass --java or set JAVAKH_JAVA"
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise JavaKhError(f"JavaKh timed out after {timeout} seconds") from exc

    matches = RESULT_RE.findall(result.stdout)
    if result.returncode != 0 or not matches:
        details = (result.stderr.strip() or result.stdout.strip() or "no output")[-2000:]
        raise JavaKhError(
            f"JavaKh failed with exit code {result.returncode}: {details}"
        )
    return matches[-1].strip()


if __name__ == "__main__":
    print(kho_solver([[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]))
