import unittest
from unittest.mock import MagicMock, patch
from src.label_maker import LabelMaker
from reportlab.pdfbase.ttfonts import TTFont

class TestLabelMaker(unittest.TestCase):
    @patch('src.label_maker.labels.Sheet')
    @patch('src.label_maker.labels.Specification')
 
    def test_initialization(self, mock_spec, mock_sheet):
        with patch.dict('src.label_maker.sheet_types', {
            "custom_type": {
                'cols': 2,
                'rows': 4,
                'sheet_width': 200,
                'sheet_height': 100,
                'label_width': 50,
                'label_height': 25,
                'column_gap': 2,
                'row_gap': 2,
                'x_margin': 1,
                'top_margin': 1,
                'corner_radius': 0
            }
        }):
            mock_spec.return_value = MagicMock()
            l = LabelMaker(sheet_type='custom_type')
            mock_spec.assert_called_once_with(
                200, 100, 2, 4, 50, 25, column_gap=2, row_gap=2, left_margin=1,
                top_margin=1, corner_radius=0, left_padding=1.75, top_padding=1.75,
                bottom_padding=1.75, right_padding=1.75
            )


    @patch('src.label_maker.labels.Sheet')
    def test_write_multiline_text_to_label(self, mock_sheet):
        label = MagicMock()
        text = "Line 1\nLine 2\nLine 3"
        l = LabelMaker(input_labels=[text])
        l._write_multiline_text_to_label(label, 100, 50, text)
 
        # Assert label.add was called, indicating lines were processed and added
        self.assertTrue(label.add.called)

    @patch('src.label_maker.labels.Sheet')
    def test_save(self, mock_sheet):
        mock_sheet_instance = MagicMock()
        mock_sheet.return_value = mock_sheet_instance
        l = LabelMaker()
        l.save("test.pdf")
        # Verify if save method of the Sheet class was called
        mock_sheet_instance.save.assert_called_once_with("test.pdf")

if __name__ == '__main__':
    unittest.main()
