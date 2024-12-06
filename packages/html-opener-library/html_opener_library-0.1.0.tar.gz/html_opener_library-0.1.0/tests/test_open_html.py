
import unittest
from html_opener_library import open_html_periodically

class TestHtmlOpener(unittest.TestCase):
    def test_file_exists(self):
        try:
            open_html_periodically("sample.html", interval=5)
        except FileNotFoundError:
            self.fail("open_html_periodically raised FileNotFoundError unexpectedly!")

if __name__ == "__main__":
    unittest.main()
