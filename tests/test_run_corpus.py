import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run_corpus as rc  # noqa: E402


def wrap(text, notes="- için → üçin"):
    return "%s\n%s\n%s\n\n%s\n" % (rc.START, text, rc.END, notes)


class TestRunCorpus(unittest.TestCase):
    def test_final_text_is_taken_from_between_the_markers(self):
        self.assertEqual(rc.final_text("x\n<<<TEXT\nSalam.\nTEXT>>>\nnotes"), "Salam.")
        self.assertIsNone(rc.final_text("Salam."))
        self.assertIsNone(rc.final_text("<<<TEXT\nSalam."))

    def test_reference_answers_pass_and_notes_are_not_graded(self):
        # The notes after the text name the removed Turkish word; that must not fail the case.
        for case in rc.cases():
            with self.subTest(case=case):
                ref = rc.read(os.path.join(rc.CORPUS, case, "reference.txt"))
                self.assertEqual(rc.check(case, wrap(ref)), [])

    def test_answer_without_markers_fails(self):
        case = rc.cases()[0]
        ref = rc.read(os.path.join(rc.CORPUS, case, "reference.txt"))
        self.assertEqual(len(rc.check(case, ref)), 1)

    def test_system_prompt_holds_every_reference(self):
        for variant, first in (("skill", "SKILL.md"), ("prompt", "prompts/system-prompt.md")):
            s = rc.system_prompt(variant)
            self.assertIn("<file name='%s'>" % first, s)
            for name in os.listdir(os.path.join(rc.ROOT, "references")):
                self.assertIn("references/%s" % name, s)
            self.assertTrue(s.endswith(rc.HARNESS_NOTE))

    def test_saved_answers_mode(self):
        tmp = tempfile.mkdtemp()
        try:
            good, bad = os.path.join(tmp, "good"), os.path.join(tmp, "bad")
            for case in rc.cases():
                for folder, name in ((good, "reference.txt"), (bad, "input.txt")):
                    os.makedirs(os.path.join(folder, case))
                    text = rc.read(os.path.join(rc.CORPUS, case, name))
                    for n in (1, 2):
                        with open(os.path.join(folder, case, "%d.txt" % n), "w", encoding="utf-8") as fh:
                            fh.write(wrap(text))
            out = os.path.join(tmp, "out")
            with open(os.devnull, "w") as null:
                stdout, sys.stdout = sys.stdout, null
                try:
                    ok = rc.main(["--answers", good, "--runs", "2", "--out", out])
                    fail = rc.main(["--answers", bad, "--runs", "2", "--out", out])
                finally:
                    sys.stdout = stdout
            self.assertEqual((ok, fail), (0, 1))
            self.assertIn("FAIL", rc.read(os.path.join(out, "report.md")))
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
