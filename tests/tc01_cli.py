import unittest
import os
import subprocess

class TestCLI(unittest.TestCase):

    def setUp(self):
        """Reference fixed test input file and expected outputs"""
        self.input_filename = "tests/tc01_cli_input.txt"
        self.default_output_filename = "tests/tc01_cli_input.anon.txt"
        self.default_output_json = "tests/tc01_cli_input.anon.map.json"

    def tearDown(self):
        """Clean up generated output files"""
        if os.path.exists(self.default_output_filename):
            os.remove(self.default_output_filename)
        if os.path.exists(self.default_output_json):
            os.remove(self.default_output_json)

    def run_cli_command(self, command):
        """Run the CLI command and return the result."""
        full_command = ["python3", "janusz-cli.py"]
        full_command.extend(command)
        result = subprocess.run(full_command, capture_output=True, text=True)
        return result

    def assert_pseudonyms_in_output(self, output_file):
        """Assert that the output file contains expected pseudonyms"""
        self.assertTrue(
            os.path.exists(output_file),
            f"Output file {output_file} does not exist"
        )
        with open(output_file, "r") as f:
            content = f.read()
        self.assertIn("__PERSON_0__", content, "Person pseudonym missing")
        self.assertIn("__PESEL_0__", content, "PESEL pseudonym missing")

    def test_default_output_file_read_only(self):
        """Verify default output creation with existing predefined input"""
        input_file = self.input_filename
        command = ["-i", input_file]
        result = self.run_cli_command(command)
        self.assertEqual(
            result.returncode,
            0,
            f"CLI command failed with: {result.stderr}"
        )

        # Verify CLI did not modify original input file
        self.assertFalse(
            os.stat(input_file).st_mtime > os.path.getmtime(self.default_output_filename),
            "Test input should not have been modified"
        )
        
        self.assert_pseudonyms_in_output(self.default_output_filename)

if __name__ == '__main__':
    unittest.main()