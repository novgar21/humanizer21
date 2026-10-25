import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

import barla  # noqa: E402


def cats(text):
    return [f["category"] for f in barla.run(text)["findings"]]


def sample(name):
    with open(os.path.join(HERE, "samples", name), encoding="utf-8") as fh:
        return fh.read()


class TestLetters(unittest.TestCase):
    def test_turkish_letters(self):
        self.assertIn("turkish-letter", cats("Bu ýıl gowy geçdi."))

    def test_y_before_vowel(self):
        result = barla.run("Mekdep 960 okuwçy üçin niyetlenen.")
        fixes = [f.get("suggestion") for f in result["findings"] if f["category"] == "y-vs-ý"]
        self.assertEqual(fixes, ["niýetlenen"])

    def test_y_after_vowel_before_consonant(self):
        fixes = [f.get("suggestion") for f in barla.run("Bu örän peydaly, bay obada.")["findings"]
                 if f["category"] == "y-vs-ý"]
        self.assertEqual(fixes, ["peýdaly", "baý"])

    def test_correct_y_words_are_clean(self):
        self.assertNotIn("y-vs-ý", cats("Köp ýöreýän adamlar baý obada çaý içýärler. Goýy gök. Taýyn."))

    def test_mixed_script(self):
        # Cyrillic small a (U+0430) inside a Latin word
        self.assertIn("mixed-script", cats("Aşg\u0430bat"))

    def test_foreign_name_is_only_a_note(self):
        f = barla.run("Vladimir geldi.")["findings"]
        self.assertTrue(all(x["severity"] == "info" for x in f if x["category"] == "foreign-letter"))


class TestWords(unittest.TestCase):
    def test_turkish_words(self):
        found = [f["text"] for f in barla.run("Bu çok önemli ve gerekli.")["findings"]
                 if f["category"] == "turkish-word"]
        self.assertEqual(found, ["çok", "önemli", "ve"])

    def test_harmony(self):
        self.assertIn("harmony", cats("Täze kompýuterlar geldi."))
        self.assertNotIn("harmony", cats("Täze kompýuterler we kitaplar geldi."))

    def test_genitive_n(self):
        self.assertIn("n-vs-ň", cats("Türkmenistanyn paýtagty"))


class TestNumbers(unittest.TestCase):
    def test_ordinals(self):
        bad = [f["suggestion"] for f in barla.run("2025-njy ýyl, 10-nji synp, 6-nci gezek")["findings"]
               if f["category"] == "ordinal"]
        self.assertEqual(bad, ["2025-nji", "10-njy", "6-njy"])

    def test_correct_ordinals(self):
        self.assertNotIn("ordinal", cats("2026-njy ýyl, 2025-nji ýyl, 30-njy oktýabr, 20-nji, 9-njy, 1-nji"))

    def test_plural_after_number(self):
        self.assertIn("plural-after-number", cats("Topara 40 talyplar gatnaşdy."))
        self.assertNotIn("plural-after-number", cats("Topara 40 talyp gatnaşdy. Bahasy 100 dollar."))

    def test_plural_after_number_with_adjectives(self):
        found = [f["text"] for f in barla.run("6 täze mikrofonlar we 12 sany häzirki zaman kompýuterler")["findings"]
                 if f["category"] == "plural-after-number"]
        self.assertEqual(found, ["mikrofonlar", "kompýuterler"])
        self.assertNotIn("plural-after-number", cats("5 ýyldan bäri adamlar gelýär."))


class TestPhrasesAndPunctuation(unittest.TestCase):
    def test_chatbot_residue(self):
        c = cats("Gowy sorag! Geliň, bu meselä seredeliň.\n\nUmyt edýärin, bu size kömek eder!")
        self.assertGreaterEqual(c.count("chatbot-residue"), 2)
        self.assertIn("staged-opener", c)
        self.assertIn("staged-opener", cats("Geliň, sagdyn durmuş barada gürleşeliň."))

    def test_dashes_in_short_text(self):
        self.assertIn("dashes", cats("Işe pyýada gidiň \u2014 basgançakdan peýdalanyň \u2014 agşamlar gezelenç ediň."))

    def test_quotes(self):
        self.assertIn("quotes", cats('Ol "Watan" kinoteatryna gitdi.'))
        self.assertNotIn("quotes", cats("Ol «Watan» kinoteatryna gitdi."))

    def test_invisible(self):
        self.assertIn("invisible-char", cats("Salam\u200b dünýä"))

    def test_urls_are_skipped(self):
        self.assertEqual(cats("Serediň: https://enedilim.com/sozluk/soz/ve"), [])


class TestSamples(unittest.TestCase):
    def test_ai_sample_has_many_findings(self):
        self.assertGreaterEqual(len(barla.run(sample("01-ai-habar.txt"))["findings"]), 10)

    def test_human_sample_is_clean(self):
        self.assertEqual(barla.run(sample("02-adam-yazgysy.txt"))["findings"], [])

    def test_chatbot_post(self):
        c = cats(sample("03-chatbot-post.txt"))
        for expected in ("chatbot-residue", "turkish-word", "formatting"):
            self.assertIn(expected, c)


if __name__ == "__main__":
    unittest.main()
