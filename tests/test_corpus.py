import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import barla  # noqa: E402
import grade  # noqa: E402

CORPUS = os.path.join(HERE, "corpus")
CASES = sorted(d for d in os.listdir(CORPUS) if os.path.isdir(os.path.join(CORPUS, d)))


def read(case, name):
    with open(os.path.join(CORPUS, case, name), encoding="utf-8") as fh:
        return fh.read()


class TestCorpus(unittest.TestCase):
    def test_reference_results_pass_every_check(self):
        for case in CASES:
            with self.subTest(case=case):
                failed = [n for n, ok in grade.grade(os.path.join(CORPUS, case), read(case, "reference.txt")) if not ok]
                self.assertEqual(failed, [])

    def test_inputs_fail_the_checks(self):
        # Each input must break several checks, or the case tests nothing.
        for case in CASES:
            with self.subTest(case=case):
                failed = [n for n, ok in grade.grade(os.path.join(CORPUS, case), read(case, "input.txt")) if not ok]
                self.assertGreaterEqual(len(failed), 5)

    def test_barla_flags_every_input(self):
        for case in CASES:
            with self.subTest(case=case):
                s = barla.run(read(case, "input.txt"))["summary"]
                self.assertGreaterEqual(s["error"] + s["warn"], 5)


if __name__ == "__main__":
    unittest.main()
