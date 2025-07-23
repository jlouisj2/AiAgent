import unittest
import sys
import os
sys.path.insert(0, os.path.abspath("../functions"))

from run_python import run_python_file

class TestRunPythonFile(unittest.TestCase):
    def test_main_usage(self):
        result = run_python_file("calculator", "main.py")
        self.assertIn("Hello from aiagent", result)

    def test_main_with_args(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        self.assertIn("Hello from aiagent", result)

    def test_nonexistent_file(self):
        result = run_python_file("calculator", "nonexistent.py")
        self.assertIn("not found", result)

    def test_invalid_path(self):
        result = run_python_file("calculator", "../main.py")
        self.assertIn("outside the permitted working directory", result)

    def test_read_lorem_txt(self):
        result = run_python_file("calculator", "main.py", ["get the contents of lorem.txt"])
        self.assertIn("wait, this isn't lorem ipsum", result)

    def test_create_readme(self):
        result = run_python_file("calculator", "main.py", ["create a new README.md file with the contents '# calculator'"])
        self.assertTrue(os.path.exists("calculator/README.md"))

    def test_list_root_files(self):
        result = run_python_file("calculator", "main.py", ["what files are in the root?"])
        self.assertIn("lorem.txt", result)
        self.assertIn("README.md", result)

    def test_write_file(self):
        result = run_python_file("calculator", "main.py", ["write file 'test.txt' with contents 'hello world'"])
        self.assertTrue(os.path.exists("calculator/test.txt"))

    def test_run_self(self):
        result = run_python_file("calculator", "tests.py")
        self.assertIn("Ran 9 tests", result)
if __name__ == "__main__":
    unittest.main()