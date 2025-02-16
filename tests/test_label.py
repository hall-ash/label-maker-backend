import unittest
from src.label import Label, LabelList, Aliquot  

class TestLabel(unittest.TestCase):

    def test_label_without_aliquots(self):
        label = Label(name="Sample Label", use_aliquots=False, count=3)
        self.assertEqual(label.get_text(), ["Sample Label", "Sample Label", "Sample Label"])

    def test_label_with_aliquots(self):
        aliquots = [{"text": "Aliquot A", "number": 2}, {"text": "Aliquot B", "number": 3}]
        label = Label(name="Test Label", use_aliquots=True, aliquots=aliquots)

        expected_output = [
            "Test Label\nAliquot A 1 of 2",
            "Test Label\nAliquot A 2 of 2",
            "Test Label\nAliquot B 1 of 3",
            "Test Label\nAliquot B 2 of 3",
            "Test Label\nAliquot B 3 of 3"
        ]
        self.assertEqual(label.get_text(), expected_output)

    def test_label_with_empty_aliquots(self):
        label = Label(name="Empty Aliquot Label", use_aliquots=True, aliquots=[])
        self.assertEqual(label.get_text(), [])

    def test_label_with_invalid_count(self):
        label = Label(name="Test Label", use_aliquots=False, count="5")
        self.assertEqual(label.get_text(), ["Test Label"] * 5)


class TestAliquot(unittest.TestCase):

    def test_aliquot_initialization(self):
        aliquot = Aliquot(text="Test Aliquot", number=3)
        self.assertEqual(aliquot.text, "Test Aliquot")
        self.assertEqual(aliquot.number, 3)

    def test_aliquot_number_conversion(self):
        aliquot = Aliquot(text="Aliquot 1", number="4")  # Ensure conversion from string to int
        self.assertEqual(aliquot.number, 4)


class TestLabelList(unittest.TestCase):

    def test_label_list_initialization(self):
        labels = [
            {"name": "Label 1", "use_aliquots": False, "aliquots": [], "count": 2},
            {"name": "Label 2", "use_aliquots": True, "aliquots": [{"text": "Aliquot X", "number": 1}], "count": 0}
        ]
        label_list = LabelList(labels)
        expected_output = ["Label 1", "Label 1", "Label 2\nAliquot X 1 of 1"]
        self.assertEqual(label_list.get_label_texts(), expected_output)

    def test_label_list_with_empty_labels(self):
        label_list = LabelList([])
        self.assertEqual(label_list.get_label_texts(), [])

if __name__ == "__main__":
    unittest.main()
