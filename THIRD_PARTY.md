# Third-Party Components

The `src/javakh_ori_temp` directory contains the historical JavaKh v2 compiled
classes and the JAR files required by that build. JavaKh originated in the Knot
Atlas ecosystem; the corresponding source lineage is available from
[`geometer/JavaKh-v2`](https://github.com/geometer/JavaKh-v2).

Bundled support libraries include historical versions of Apache Commons CLI,
Apache Commons IO, Apache Commons Logging, Log4j 1.x, GNU Trove classes, and
MallardSoft tuple classes. These files are retained to reproduce the legacy
solver and are not fetched or modified at runtime.

For a maintained source-level port and detailed JavaKh comparison notes, see
[`TopologicalKnotIndexer/cppkh`](https://github.com/TopologicalKnotIndexer/cppkh).
