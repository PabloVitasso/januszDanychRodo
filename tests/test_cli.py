import unittest
import os
import subprocess

class TestCLI(unittest.TestCase):

    def setUp(self):
        """Set up a test input file."""
        self.input_filename = "test_input.txt"
        self.output_filename = "test_output.txt"
        self.default_output_filename = "test_input.anon.txt"
        with open(self.input_filename, "w") as f:
            f.write("Jan Kowalski PESEL 82031212345")

    def tearDown(self):
        """Clean up created files."""
        for f in [self.input_filename, self.output_filename, self.default_output_filename, "test_output_map.json", "test_input.anon_map.json"]:
            if os.path.exists(f):
                os.remove(f)

    def test_short_aliases(self):
        """Test using -i and -o aliases."""
        command = [
            "python3", "januszdanych.py",
            "-i", self.input_filename,
            "-o", self.output_filename,
            "--profile", "pseudonymized"
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"CLI command failed with output: {result.stderr}")
        self.assertTrue(os.path.exists(self.output_filename))
        with open(self.output_filename, "r") as f:
            content = f.read()
        self.assertIn("__PERSON_0__", content)
        self.assertIn("__PESEL_0__", content)

    def test_default_output_file(self):
        """Test default output file creation."""
        command = [
            "python3", "januszdanych.py",
            "-i", self.input_filename,
            "--profile", "pseudonymized"
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"CLI command failed with output: {result.stderr}")
        self.assertTrue(os.path.exists(self.default_output_filename))
        with open(self.default_output_filename, "r") as f:
            content = f.read()
        self.assertIn("__PERSON_0__", content)
        self.assertIn("__PESEL_0__", content)

if __name__ == '__main__':
    unittest.main()