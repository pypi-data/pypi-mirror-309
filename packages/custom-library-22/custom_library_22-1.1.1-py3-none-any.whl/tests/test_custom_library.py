
import unittest
from custom_library import HelperFunctions

class TestHelperFunctions(unittest.TestCase):
    def test_allowed_file_extension(self):
        result = HelperFunctions.allowed_file_extension("file.txt", {"txt", "jpg"})
        self.assertTrue(result)
        result = HelperFunctions.allowed_file_extension("file.exe", {"txt", "jpg"})
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
