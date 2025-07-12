import unittest
from core.anonymizer import anonymize_text
from interfaces.file_io import read_file

class TestAnonymizer(unittest.TestCase):

    def setUp(self):
        """Wczytanie dokumentu testowego przed każdym testem."""
        self.test_text = read_file("tests/test_document.txt")

    def test_pseudonymization_profile(self):
        """Testuje profil 'pseudonymized' z użyciem subtestów."""
        anonymized_text, sub_map = anonymize_text(self.test_text, profile="pseudonymized")
        
        assertions = {
            "Should contain PERSON token": ("<PERSON_0>", anonymized_text),
            "Should contain PESEL token": ("<PESEL_0>", anonymized_text),
            "Should contain ORGANIZATION token": ("<ORGANIZATION_0>", anonymized_text),
            "Should contain NIP token": ("<NIP_0>", anonymized_text),
            "Should contain KW token": ("<KW_0>", anonymized_text),
        }
        
        for msg, (expected, actual) in assertions.items():
            with self.subTest(msg=msg):
                self.assertIn(expected, actual)

        with self.subTest(msg="Should remove original name"):
            self.assertNotIn("Jan Kowalski", anonymized_text)
        
        with self.subTest(msg="Should have original PESEL in sub_map"):
            # To jest zła asercja, w mapie powinien być ztokenizowany pesel jako klucz
            # Sprawdzam, czy oryginalny PESEL jest jedną z wartości w mapie
            self.assertIn("82031212345", sub_map.values())

    def test_gdpr_profile(self):
        """Testuje profil 'gdpr' (anonimizacja) z użyciem subtestów."""
        anonymized_text, sub_map = anonymize_text(self.test_text, profile="gdpr")

        with self.subTest(msg="Should generalize money"):
            self.assertIn("około 520 tys. PLN", anonymized_text)
        
        with self.subTest(msg="Should generalize date"):
            self.assertIn("Q1 2023", anonymized_text)
            
        with self.subTest(msg="Should not contain PERSON token"):
            self.assertNotIn("<PERSON_0>", anonymized_text)
            
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
            self.assertIn("<PESEL_0>", anonymized_text)
        
        with self.subTest(msg="Should not contain NIP token"):
            self.assertNotIn("<NIP_0>", anonymized_text)
            
        with self.subTest(msg="Should contain original name"):
            self.assertIn("Jan Kowalski", anonymized_text)

    def test_anonymization_on_big_file(self):
        """Testuje anonimizację na dużym pliku i porównuje z oczekiwanym wynikiem."""
        big_text = read_file("tests/test_document-big.txt")
        expected_text = read_file("tests/test_document-big.expected.txt")
        anonymized_text, _ = anonymize_text(big_text, profile="pseudonymized")
        
        self.assertEqual(anonymized_text.strip(), expected_text.strip())

if __name__ == '__main__':
    unittest.main()