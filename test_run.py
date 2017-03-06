import unittest
import re
import run
class TestRegexStuff(unittest.TestCase):
    def test_get_file_with_output_name_input_with_int_regex(self):
        run.UNIQUE_ID_PATTERN = "(\d+?)"
        run.IN_FILE_PATTERN=re.compile("test" + run.UNIQUE_ID_PATTERN + ".in")
        run.OUT_FILE_PATTERN = re.compile("test" + run.UNIQUE_ID_PATTERN + ".out")

        self.assertEqual(run.get_file_with_output_name("test1.in"),"test1.out")

    def test_get_file_with_output_name_input_with_str_regex(self):
        run.UNIQUE_ID_PATTERN = "(.+?)"
        run.IN_FILE_PATTERN = re.compile("test" + run.UNIQUE_ID_PATTERN + ".in")
        run.OUT_FILE_PATTERN = re.compile("test" + run.UNIQUE_ID_PATTERN + ".out")

        self.assertEqual(run.get_file_with_output_name("testABC123.in"), "testABC123.out")
    def test_get_file_with_output_name_regex_that_allows_0_chars(self):
        run.UNIQUE_ID_PATTERN = "(.*?)"
        run.IN_FILE_PATTERN = re.compile("test" + run.UNIQUE_ID_PATTERN + ".in")
        run.OUT_FILE_PATTERN = re.compile("test" + run.UNIQUE_ID_PATTERN + ".out")

        self.assertEqual(run.get_file_with_output_name("test.in"), "test.out")
        self.assertEqual(run.get_file_with_output_name("testABC123.in"), "testABC123.out")
if __name__ == '__main__':
    unittest.main()