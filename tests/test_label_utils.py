import unittest
from src.label_utils import (
    process_skip_labels_input,
    get_num_from_cell,
    get_row_col,
    convert_skip_range_to_list,
    get_skips_dict
)

class TestLabelUtils(unittest.TestCase):

    def test_process_skip_labels_input(self):
        input_text = "1: A1, B2, C3\n2: D4, E5"
        expected_output = [
            (1, ["A1", "B2", "C3"]),
            (2, ["D4", "E5"])
        ]
        self.assertEqual(process_skip_labels_input(input_text), expected_output)

    def test_get_num_from_cell(self):
        cols = 5
        self.assertEqual(get_num_from_cell("A1", cols), 1)  # A1 → 1
        self.assertEqual(get_num_from_cell("B3", cols), 12)  # B3 → 8
        self.assertEqual(get_num_from_cell("D5", cols), 24)  # D5 → 20

    def test_get_row_col(self):
        self.assertEqual(get_row_col(1, 5), (1, 1))  # First cell
        self.assertEqual(get_row_col(8, 5), (2, 3))  # Second row, 3rd column
        self.assertEqual(get_row_col(20, 5), (4, 5))  # Fourth row, last column

    def test_convert_skip_range_to_list(self):
        cell_ranges = ["A1-C2"] 
        expected_output = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 2), (2, 3)]
        rows = 17
        cols = 5
        self.assertCountEqual(convert_skip_range_to_list(cell_ranges, rows, cols), expected_output)

        cell_ranges = ["B3"]  # Single cell
        self.assertEqual(convert_skip_range_to_list(cell_ranges, rows, cols), [(3, 2)])

        cell_ranges = ["Z99"]  # Out of range, should return empty
        self.assertEqual(convert_skip_range_to_list(cell_ranges, rows, cols), [])

    def test_get_skips_dict(self):

        skip_input = "1: A3-C4\n2: D4, E4"
        start_label = "B2"
        expected_skips_dict = {
            1: [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (4, 1), (4, 2), (4, 3)],
            2: [(4, 4), (4, 5)]
        }
        result = get_skips_dict(skip_input, "LCRY-1700", start_label)
        for key in expected_skips_dict:
            self.assertCountEqual(result[key], expected_skips_dict[key])

if __name__ == "__main__":
    unittest.main()
