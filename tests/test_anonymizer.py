import unittest
import difflib
from core.anonymizer import anonymize_text
from interfaces.file_io import read_file

class TestAnonymizer(unittest.TestCase):

    def setUp(self):
        """Wczytanie dokumentu testowego przed każdym testem."""
        self.test_text = read_file("tests/test_document.txt")
        self.maxDiff = None

    def _assert_text_equals(self, actual, expected, actual_path):
        """Asserts that two texts are equal, providing a detailed diff on failure."""
        if actual.strip() != expected.strip():
            with open(actual_path, "w", encoding="utf-8") as f:
                f.write(actual)
            
            diff = difflib.unified_diff(
                expected.strip().splitlines(keepends=True),
                actual.strip().splitlines(keepends=True),
                fromfile='expected.txt',
                tofile='actual.txt',
            )
            
            diff_str = ''.join(diff)
            self.fail(f"Anonymized text does not match expected text. Diff:\n{diff_str}")

    def test_pseudonymization_profile(self):
        """Testuje profil 'pseudonymized' z użyciem subtestów."""
        anonymized_text, sub_map = anonymize_text(self.test_text, profile="pseudonymized")
        
        assertions = {
            "Should contain PERSON token": ("__PERSON_0__", anonymized_text),
            "Should contain PESEL token": ("__PESEL_0__", anonymized_text),
            "Should contain ORGANIZATION token": ("__ORGANIZATION_0__", anonymized_text),
            "Should contain NIP token": ("__NIP_0__", anonymized_text),
            "Should contain KW token": ("__KW_0__", anonymized_text),
            "Should contain POST_CODE token": ("__POST_CODE_0__", anonymized_text),
            "Should contain STREET_ADDRESS token": ("__STREET_ADDRESS_0__", anonymized_text),
            "Should contain LAND_PLOT token": ("__LAND_PLOT_0__", anonymized_text),
        }
        
        for msg, (expected, actual) in assertions.items():
            with self.subTest(msg=msg):
                self.assertIn(expected, actual)

        with self.subTest(msg="Should remove original name"):
            self.assertNotIn("Jan Kowalski", anonymized_text)
        
        with self.subTest(msg="Should have original PESEL in sub_map"):
            self.assertIn("82031212345", sub_map.values())

    def test_gdpr_profile(self):
        """Testuje profil 'gdpr' (anonimizacja) z użyciem subtestów."""
        anonymized_text, sub_map = anonymize_text(self.test_text, profile="gdpr")

        with self.subTest(msg="Should generalize money"):
            self.assertIn("około 520 tys. PLN", anonymized_text)
        
        with self.subTest(msg="Should generalize date"):
            self.assertIn("Q1 2023", anonymized_text)
            
        with self.subTest(msg="Should not contain PERSON token"):
            self.assertNotIn("__PERSON_0__", anonymized_text)
            
        with self.subTest(msg="Should not contain original name"):
            self.assertNotIn("Jan Kowalski", anonymized_text)
            
        with self.subTest(msg="Substitution map should be empty"):
            self.assertEqual(len(sub_map), 0)

    def test_custom_classes(self):
        """Testuje anonimizację z niestandardową listą klas z użyciem subtestów."""
        custom_classes = ["PESEL", "MONEY"]
        
        anonymized_text, sub_map = anonymize_text(
            self.test_text,
            profile="pseudonymized",
            custom_classes=custom_classes
        )

        with self.subTest(msg="Should contain PESEL token"):
            self.assertIn("__PESEL_0__", anonymized_text)
        
        with self.subTest(msg="Should not contain NIP token"):
            self.assertNotIn("__NIP_0__", anonymized_text)
            
        with self.subTest(msg="Should contain original name"):
            self.assertIn("Jan Kowalski", anonymized_text)

    def test_anonymization_on_big_file(self):
        """Testuje anonimizację na dużym pliku i porównuje z oczekiwanym wynikiem."""
        big_text = read_file("tests/test_document-big.source.txt")
        expected_text = read_file("tests/test_document-big.expected.txt")
        anonymized_text, _ = anonymize_text(big_text, profile="pseudonymized")

        self.assertNotIn('<_<', anonymized_text, "Detected obsolete nested substitution token '<_<'")
        self.assertNotIn('__<', anonymized_text, "Detected nested substitution token '__<'")
        self.assertNotIn('<__', anonymized_text, "Detected nested substitution token '<__'")
        
        self._assert_text_equals(
            anonymized_text,
            expected_text,
            "tests/test_document-big.actual.txt"
        )

    def test_anonymization_on_area_file(self):
        """Testuje anonimizację na pliku z danymi o powierzchni i porównuje z oczekiwanym wynikiem."""
        area_text = read_file("tests/test_document_area.source.txt")
        expected_text = read_file("tests/test_document_area.expected.txt")
        anonymized_text, _ = anonymize_text(area_text, profile="pseudonymized")
        
        self._assert_text_equals(
            anonymized_text,
            expected_text,
            "tests/test_document_area.actual.txt"
        )
        
if __name__ == '__main__':
    unittest.main()