import unittest

from helper import extract_skills


class ExtractSkillsTests(unittest.TestCase):
    def test_does_not_match_single_letter_skill_inside_cpp(self):
        text = "I have experience with C++ and SQL."
        self.assertEqual(extract_skills(text), ["c++", "sql"])


if __name__ == "__main__":
    unittest.main()
