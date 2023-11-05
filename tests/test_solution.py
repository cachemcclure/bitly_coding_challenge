import unittest
from solutions.comprehensive import (
    interpret_file,
    build_bitlink_dict,
    process_click_data,
)
from pathlib import Path


class MyTestCase(unittest.TestCase):
    """
    Rather than separating these into multiple tests, it was simpler for this exercise to include all basic test
    cases for each function in each test. While not strictly best practice, it serves the function of test coverage.
    """

    def test_interpret_file_1(self):
        """
        Unit test for interpret_file function in comprehensive solution
        """
        fp = Path("tests").joinpath("test_data_1.json")
        test_dict = {
            "http://bit.ly/test1": 0,
            "http://bit.ly/test2": 0,
            "http://bit.ly/test3": 0,
        }
        test_out = interpret_file(fp=fp, count_dict=test_dict, timestamp_filter=2021)
        self.assertEqual(test_out["http://bit.ly/test1"], 1)
        self.assertEqual(test_out["http://bit.ly/test2"], 3)
        self.assertEqual(test_out["http://bit.ly/test3"], 1)
        self.assertEqual("http://bit.ly/test4" not in test_out, True)

    def test_build_dict(self):
        """
        Unit test for build_bitlink_dict function in comprehensive solution
        """
        fp = Path("tests").joinpath("test_data_2.csv")
        test_out = build_bitlink_dict(fp=fp)
        self.assertEqual("http://bit.ly/test1" in test_out, True)
        self.assertEqual(test_out["http://bit.ly/test1"] == "https://test1.com/", True)
        self.assertEqual("http://bit.ly/test2" in test_out, True)
        self.assertEqual(test_out["http://bit.ly/test2"] == "https://test2.com/", True)
        self.assertEqual("http://bit.ly/test3" in test_out, True)
        self.assertEqual(test_out["http://bit.ly/test3"] == "https://test3.com/", True)
        self.assertEqual("http://bit.ly/bitlink" in test_out, True)
        self.assertEqual(test_out["http://bit.ly/bitlink"] == "https://link.com/", True)
        self.assertEqual(len(list(test_out.keys())) == 4, True)

    def test_process_click_data(self):
        """
        Unit test for process_click_data function in comprehensive solution
        """
        encode_fp = Path("tests").joinpath("test_data_2.csv")
        decode_fp = Path("tests").joinpath("test_data_1.json")
        test_out = process_click_data(encode_fp=encode_fp, decode_fp=decode_fp)
        self.assertEqual("https://test1.com/" in test_out, True)
        self.assertEqual(test_out["https://test1.com/"] == 1, True)
        self.assertEqual("https://test2.com/" in test_out, True)
        self.assertEqual(test_out["https://test2.com/"] == 3, True)
        self.assertEqual("https://test3.com/" in test_out, True)
        self.assertEqual(test_out["https://test3.com/"] == 1, True)


if __name__ == "__main__":
    unittest.main()
