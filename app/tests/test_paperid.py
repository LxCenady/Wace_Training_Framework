"""Paper recognition rules come from the subject pack: SCSA wording by default, another board's wording when the
pack names it (pack.json "recognise")."""
import os, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import paperid  # noqa: E402

SCSA = {"recognise": {"title": ["accounting and finance"],
                      "kinds": {"InformationBooklet": ["information booklet"]}}}
CAMBRIDGE = {"recognise": {"title": ["mathematics 9709"], "exam": ["question paper"], "key": ["mark scheme"],
                           "report": ["principal examiner report"], "year": [r"(?:may/june|october/november|february/march) (20\d\d)"],
                           "sample": [r"specimen paper", r"specimen mark scheme"], "sample_year": "2020Specimen"}}


class Recognise(unittest.TestCase):
    def test_scsa_defaults(self):
        kind, m = paperid.kind_of("atar course examination, 2024 question/answer booklet accounting and finance", SCSA)
        self.assertEqual((kind, m.group(1)), ("Exam", "2024"))
        kind, m = paperid.kind_of("2023 atar course examination report accounting and finance marking key", SCSA)
        self.assertEqual((kind, m.group(1)), ("ExamReport", "2023"))
        kind, m = paperid.kind_of("atar course examination, 2025 accounting and finance information booklet", SCSA)
        self.assertEqual((kind, m.group(1)), ("InformationBooklet", "2025"))

    def test_another_board_names_its_own_wording(self):
        kind, m = paperid.kind_of("mathematics 9709/11 paper 1 pure mathematics 1 may/june 2024 mark scheme", CAMBRIDGE)
        self.assertEqual((kind, m.group(1)), ("MarkingKey", "2024"))
        kind, m = paperid.kind_of("mathematics 9709/31 question paper october/november 2023", CAMBRIDGE)
        self.assertEqual((kind, m.group(1)), ("Exam", "2023"))
        self.assertIsNone(paperid.kind_of("mathematics 9709 question/answer booklet", CAMBRIDGE))  # not SCSA's words


if __name__ == "__main__":
    unittest.main()
