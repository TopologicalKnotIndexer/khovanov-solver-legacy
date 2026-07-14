# khovanov-solver-legacy

`khovanov-solver-legacy` is a small Python wrapper around the original bundled
JavaKh v2 class files. It accepts a planar diagram (PD) code and prints integral
Khovanov homology in the familiar `q^...*t^...*Z[...]` format.

This repository is retained for reproducibility and compatibility testing. New
C++ applications should generally use
[`cppkh`](https://github.com/TopologicalKnotIndexer/cppkh), which is faster and
has a broader maintained interface.

## Requirements

- Python 3.9 or newer.
- A Java runtime. The default command is `java` from `PATH`; pass `--java` or
  set `JAVAKH_JAVA` to select an ordinary Java executable on another system.

The wrapper does not use Bash, symbolic links, WSL paths, or machine-specific
URIs. The JavaKh classes and their historical JAR dependencies are tracked as
ordinary files under `src/javakh_ori_temp`.

## Usage

Read from stdin:

```sh
echo "[[1,5,2,4],[3,1,4,6],[5,3,6,2]]" | python src/main.py
```

Or pass the PD code directly:

```sh
python src/main.py "[[1,5,2,4],[3,1,4,6],[5,3,6,2]]"
```

Select Java and resource limits explicitly:

```sh
python src/main.py --java /path/to/java --max-memory 2g --timeout 120 "[[1,1,2,2]]"
```

`--timeout 0` disables the subprocess timeout.

## Validation and Reduction

Input is parsed with `ast.literal_eval`; arbitrary Python expressions are never
executed. Every crossing must have four positive integer labels, and each label
must occur exactly twice.

The original JavaKh build returns an empty result for diagrams containing R1
crossings, so the wrapper removes R1 crossings before calculation. It does not
apply the historical `de_k8` heuristic by default: that routine assumes a
single-component knot and is not a safe general simplification for links.

A completely reduced `PD[]` is reported as the standard unknot homology. Plain
PD notation cannot record the number of components that have no crossings, so
inputs consisting only of several disconnected R1 components remain outside
this legacy wrapper's representable contract.

## Tests

```sh
python -m unittest discover -s tests -v
```

The integration tests exercise the bundled JavaKh classes on the unknot,
trefoil, Hopf link, R1 reduction, input rejection, and an explicit Java path.

## Provenance

See [Third-party components](THIRD_PARTY.md) for the bundled JavaKh and JAR
provenance. No package is published as part of repository maintenance.

## Citation

If you use this repository in academic work, please cite it as:

```bibtex
@software{topologicalknotindexer_khovanov_solver_legacy,
  author = {{TopologicalKnotIndexer contributors}},
  title = {{khovanov-solver-legacy}},
  year = {2026},
  url = {https://github.com/TopologicalKnotIndexer/khovanov-solver-legacy}
}
```
