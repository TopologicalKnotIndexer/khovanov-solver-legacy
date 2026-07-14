from pathlib import Path
import shutil
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from de_r1 import de_r1
from input_sanity import input_sanity
from kho_solver import kho_solver


TREFOIL = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
TREFOIL_RESULT = (
    "q^1*t^0*Z[0] + q^3*t^0*Z[0] + q^5*t^2*Z[0] + "
    "q^7*t^3*Z[2] + q^9*t^3*Z[0]"
)
HOPF = [[2, 3, 1, 4], [4, 1, 3, 2]]
HOPF_RESULT = "q^-6*t^-2*Z[0] + q^-4*t^-2*Z[0] + q^-2*t^0*Z[0] + q^0*t^0*Z[0]"


@unittest.skipUnless(shutil.which("java"), "java is required for the legacy integration tests")
class JavaKhIntegrationTests(unittest.TestCase):
    def test_known_trefoil_and_hopf_results(self):
        self.assertEqual(kho_solver(TREFOIL), TREFOIL_RESULT)
        self.assertEqual(kho_solver(HOPF), HOPF_RESULT)

    def test_cli_handles_r1_and_explicit_java(self):
        java = shutil.which("java")
        result = subprocess.run(
            [sys.executable, str(SRC / "main.py"), "--java", java, "[[1,1,2,2]]"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        self.assertEqual(result.stdout.strip(), "q^-1*t^0*Z[0] + q^1*t^0*Z[0]")


class ValidationTests(unittest.TestCase):
    def test_r1_splices_and_renumbers(self):
        trefoil_with_r1 = [
            [1, 5, 2, 4],
            [3, 7, 4, 6],
            [5, 3, 6, 2],
            [1, 8, 7, 8],
        ]
        self.assertEqual(de_r1(trefoil_with_r1), TREFOIL)

    def test_literal_input_validation(self):
        self.assertEqual(input_sanity(str(TREFOIL)), TREFOIL)
        for bad in ("__import__('os').system('echo bad')", "[[True,1,2,2]]", "[[1,2,3,4]]"):
            with self.assertRaises(ValueError):
                input_sanity(bad)


if __name__ == "__main__":
    unittest.main()
