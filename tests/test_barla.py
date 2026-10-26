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

    def test_harmony_after_plural(self):
        self.assertIn("harmony", cats("Ähli mekdeplerda Wi-Fi bar."))
        self.assertIn("harmony", cats("Kitaplerde ýazylan."))
        self.assertNotIn("harmony", cats("Ähli mekdeplerde we kitaplarda bar."))

    def test_knowledge_limit(self):
        self.assertIn("knowledge-limit", cats("Elimdäki maglumatlara görä, takyk bahasy ýok."))

    def test_title_case_heading(self):
        self.assertIn("formatting", cats("## Sanly Bilimiň Täze Döwri\nTekst."))
        self.assertNotIn("formatting", cats("## Sanly bilimiň täze döwri\nAşgabat şäheri."))

    def test_russian_calques_and_wrong_reader(self):
        c = cats("Taslamanyň çäklerinde studiýa guruldy. Bäsleşik iki tapgyry öz içine alýar.")
        self.assertEqual(c.count("calque"), 2)
        self.assertIn("wrong-reader", cats("Siziň bilşiňiz ýaly, kanal açyldy. Siz bu barada ýygnakda hem aýtdyňyz."))

    def test_turkish_abilir(self):
        self.assertIn("turkish-word", cats("Görkezijiler gowulaşabilir."))
        self.assertNotIn("turkish-word", cats("Görkezijiler gowulaşyp biler. Ol kabil adam."))

    def test_apostrophe_before_ending(self):
        self.assertIn("apostrophe", cats("Kanal YouTube'da açyldy, Aşgabat'da hem."))
        self.assertNotIn("apostrophe", cats("Kanal Aşgabatda açyldy."))

    def test_genitive_n(self):
        self.assertIn("n-vs-ň", cats("Türkmenistanyn paýtagty"))


class TestForms(unittest.TestCase):
    def test_dropped_vowel(self):
        found = [f["text"] for f in barla.run("Ogulynyň toýy. Agyzy açyk. Ogly geldi, oglunyň toýy, ogullar, agzy.")["findings"]
                 if f["category"] == "dropped-vowel"]
        self.assertEqual(found, ["Ogulynyň", "Agyzy"])

    def test_consonant_change(self):
        fixes = [f.get("suggestion") for f in barla.run("Agaçyň gabygy, kitapy okady.")["findings"]
                 if f["category"] == "consonant-change"]
        self.assertEqual(fixes, ["Agajyň", "kitaby"])
        self.assertNotIn("consonant-change", cats("Agajyň gabygy, kitaby, kitaphana, mekdepler, toprakda."))

    def test_month_capital(self):
        found = [f["text"] for f in barla.run("Ol 5-nji Maý geldi. Biz 1-nji Oktýabrdan başladyk.")["findings"]
                 if f["category"] == "capital-letter"]
        self.assertEqual(found, ["Maý", "Oktýabrdan"])
        self.assertNotIn("capital-letter", cats("Maý aýy gowy. Maýa Ataýewa geldi.\n## Oktýabr\n5-nji maý."))

    def test_place_word_capital(self):
        self.assertIn("capital-letter", cats("Aşgabat Şäherindäki muzeý."))
        self.assertNotIn("capital-letter", cats("Aşgabat şäherindäki muzeý. Ol Oba hojalyk ministrligi."))

    def test_question_particle_and_turkish_iyor(self):
        self.assertIn("question-particle", cats("Siz gördüňiz mi?"))
        self.assertNotIn("question-particle", cats("Siz gördüňizmi?"))
        self.assertIn("turkish-word", cats("Olar geliyorlar."))


class TestWordList(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.words = barla.WordList()

    def test_known_and_unknown_forms(self):
        for w in ("oglunyň", "agajyň", "welaýatynda", "kompýuterler", "mekdeplerde", "Türkmenistanyň", "düwni"):
            self.assertTrue(self.words.known(w), w)
        for w in ("ogulynyň", "agaçyň", "welaýatyda", "kompýuterlar", "mekdeplerda", "niyet", "sadece"):
            self.assertFalse(self.words.known(w), w)

    def test_additions(self):
        for w in ("tanalypmyş", "meýilleşdirýäris", "olimpiadasy", "goşundyda", "jikme-jik"):
            self.assertTrue(self.words.known(w), w)

    def test_dict_mode_skips_names_numbers_and_quotes_marks(self):
        r = barla.run("Gülşat Amanowa geldi. 1 200-si täze. Ahal welaýatyda ýa-da gije-gündiz.", words=self.words)
        found = [f["text"] for f in r["findings"] if f["category"] == "unknown-word"]
        self.assertEqual(found, ["welaýatyda"])
        self.assertTrue(all(f["severity"] == "info" for f in r["findings"] if f["category"] == "unknown-word"))

    def test_dict_mode_is_off_by_default(self):
        self.assertNotIn("unknown-word", cats("Ahal welaýatyda."))


class TestCompare(unittest.TestCase):
    SRC = ("Muzeýde 2 müň haly bar. Direktor Gülşat Amanowa: «Her bir haly — bu bir kitap».\n"
           "| Önüm | Sany |\n|---|---|\n| Haly | 4 800 |\n| Torba | 3 100 |\n- birinji\n- ikinji\n")

    def test_nothing_lost(self):
        self.assertEqual(barla.compare(self.SRC, self.SRC), [])

    def test_lost_number_quote_name_row_and_item(self):
        res = ("Muzeýde iki müň haly bar. Direktor: «Her bir haly, bu bir kitap».\n"
               "| Önüm | Sany |\n|---|---|\n| Haly | 4 800 |\n- birinji\n")
        kinds = {i["kind"]: i["items"] for i in barla.compare(self.SRC, res)}
        self.assertEqual(kinds["number"], ["3100"])
        self.assertEqual(kinds["quote"], ["Her bir haly — bu bir kitap"])
        self.assertIn("Amanowa", kinds["name"])
        self.assertIn("table", kinds)
        self.assertIn("list", kinds)

    def test_translation_compares_numbers_only(self):
        src = "Директор Арслан Мурадов сказал: «Мы ждём всех — от первоклассников до ветеранов». Пришли 15 тыс. человек."
        res = "Direktor Arslan Myradow: «Biz hemmä garaşýarys – birinji synp okuwçylaryndan weteranlara çenli» diýdi. 15 müň adam geldi."
        self.assertEqual(barla.compare(src, res), [])


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

    def test_plural_after_number_with_long_phrase(self):
        found = [f["text"] for f in barla.run(
            "Kompaniýanyň 3 radio kanallary işleýär. 2 täze göçme telewizion stansiýalar alyndy. "
            "5 daşary ýurt media guramalary bilen ylalaşyk baglaşyldy. 9 sany uly baýramçylyk konsertleri guraldy."
        )["findings"] if f["category"] == "plural-after-number"]
        self.assertEqual(found, ["kanallary", "stansiýalar", "guramalary", "konsertleri"])

    def test_number_phrase_stops_at_verbs_cases_and_compounds(self):
        clean = ("320 orunlyk iki çagalar bagy açyldy. 5 ýyldan bäri adamlar gelýär. 3 gezek ýaryşlara gatnaşdy. "
                 "12 kamera we kompýuterler alyndy. 960 okuwçy okap biler. 35 ýaşdan ýaş adamlar.")
        self.assertNotIn("plural-after-number", cats(clean))
        self.assertIn("plural-after-number", cats("2 çagalar geldi."))

    def test_bir_in_set_phrases_is_not_a_number(self):
        self.assertNotIn("plural-after-number", cats("Olar diňe bir meseleleri çözmekde däl. Her bir okuwçylaryň işi."))
        self.assertIn("plural-after-number", cats("Bir kitaplar."))


class TestPhrasesAndPunctuation(unittest.TestCase):
    def test_chatbot_residue(self):
        c = cats("Gowy sorag! Geliň, bu meselä seredeliň.\n\nUmyt edýärin, bu size kömek eder!")
        self.assertGreaterEqual(c.count("chatbot-residue"), 2)
        self.assertIn("staged-opener", c)
        self.assertIn("staged-opener", cats("Geliň, sagdyn durmuş barada gürleşeliň."))

    def test_phrases_inside_quotes_are_skipped(self):
        quoted = "Ol şeýle diýdi: «Olar diňe bir meseleleri çözmekde däl, eýsem düşündirmekde hem ökde»."
        self.assertNotIn("not-x-but-y", cats(quoted))
        self.assertIn("not-x-but-y", cats("Bu diňe bir bina däl, eýsem merkez."))

    def test_dashes_in_quotes_ranges_and_dialogue_are_not_counted(self):
        text = ("Ol şeýle diýdi: «Biz gelýäris \u2014 hemmämiz \u2014 ertir». Sagat 7:00\u20139:00 aralygynda.\n"
                "\u2014 Haçan?\n\u2014 Ertir.")
        self.assertNotIn("dashes", cats(text))

    def test_roman_numerals_and_brands(self):
        c = cats("XIX we XX asyrlar. YouTube kanaly.")
        self.assertNotIn("foreign-letter", c)
        self.assertNotIn("y-vs-ý", c)
        self.assertIn("foreign-letter", cats("Ol vagt geldi."))

    def test_hope_this_helps_variants(self):
        for t in ("Umyt edýärin, bu maglumatlar size ýarar.", "Umyt edýärin, ol size gerek bolar:"):
            self.assertIn("chatbot-residue", cats(t))
        self.assertNotIn("chatbot-residue", cats("Ol ýeňjekdigine umyt edýärin, bu ýyl."))

    def test_dashes_in_short_text(self):
        self.assertIn("dashes", cats("Işe pyýada gidiň \u2014 basgançakdan peýdalanyň \u2014 agşamlar gezelenç ediň."))

    def test_quotes(self):
        self.assertIn("quotes", cats('Ol "Watan" kinoteatryna gitdi.'))
        self.assertNotIn("quotes", cats("Ol «Watan» kinoteatryna gitdi."))

    def test_invisible(self):
        self.assertIn("invisible-char", cats("Salam\u200b dünýä"))

    def test_urls_are_skipped(self):
        self.assertEqual(cats("Serediň: https://enedilim.com/sozluk/soz/ve"), [])


class TestFix(unittest.TestCase):
    def test_clean_text_removes_hidden_characters(self):
        dirty = ("Salam" + chr(0x200B) + " dünýä." + chr(0xA0) + "Kitap" + chr(0xAD) + "hana"
                 + chr(0xE0041) + chr(0x202E) + "." + chr(0x2028) + "12" + chr(0x2009) + "km")
        clean, counts = barla.clean_text(dirty)
        self.assertEqual(clean, "Salam dünýä. Kitaphana.\n12 km")
        self.assertEqual(counts, {"invisible": 4, "tag": 1, "spaces": 2})

    def test_clean_text_keeps_normal_text(self):
        text = "Aşgabat şäheri, «Watan» kinoteatry – 2026-njy ýyl.\nTäze setir."
        self.assertEqual(barla.clean_text(text), (text, {"invisible": 0, "tag": 0, "spaces": 0}))

    def test_fix_from_stdin(self):
        import subprocess
        script = os.path.join(HERE, "..", "scripts", "barla.py")
        r = subprocess.run([sys.executable, script, "-", "--fix"], input="Aşgabat" + chr(0xA0) + "şäheri",
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.stdout, "Aşgabat şäheri")
        self.assertIn("1 unusual space", r.stderr)


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
