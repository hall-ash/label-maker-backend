import unittest
import json
from io import BytesIO
from src.app import app  # Import the Flask app

class TestPDFGenerationAPI(unittest.TestCase):

    def setUp(self):
        """Set up the Flask test client before each test."""
        self.client = app.test_client()
        self.client.testing = True

    def test_generate_pdf_success(self):
        """Test if the API successfully generates a PDF."""
        data = {
            "labels": [
                {"name": "Label 1\nmore text\n3rd line very long long long", "use_aliquots": False, "aliquots": [], "count": 10},
                {"name": "Label 2", "use_aliquots": True, "aliquots": [{"text": "A\n", "number": 5}], "count": 0}
            ],
            "sheet_type": "LCRY-1700",
            "skip_labels": "1: A5-C5\n2: D2-E5",
            "start_label": "C3",
            "border": True,
            "font_size": 20,
            "padding": 1.75,
            "file_name": "test_labels",
            "text_anchor": "start"
        }

        response = self.client.post('/api/generate_pdf', data=json.dumps(data), content_type='application/json')

        # Check for successful response
        self.assertEqual(response.status_code, 200, f"API Error: {response.data}")

        # Check if the response contains a valid PDF
        content_type = response.headers.get("Content-Type", "")
        self.assertIn("application/pdf", content_type, "Response is not a PDF")

        # Ensure the PDF is not empty
        pdf_data = BytesIO(response.data)
        pdf_data.seek(0, 2)  # Move to the end of the buffer
        self.assertGreater(pdf_data.tell(), 100, "PDF file seems empty")

    def test_generate_pdf_no_labels(self):
        """Test API response when no labels are provided."""
        data = {
            "labels": [],  # Empty labels
            "sheet_type": "LCRY-1700"
        }

        response = self.client.post('/api/generate_pdf', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_generate_pdf_invalid_json(self):
        """Test API response when sending invalid JSON."""
        response = self.client.post('/api/generate_pdf', data="Invalid JSON", content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_generate_pdf_missing_fields(self):
        """Test API with missing optional fields."""
        data = {
            "labels": [
                {"name": "Label Only", "use_aliquots": False, "aliquots": [], "count": 1}
            ]
        }  # Missing sheet_type, font_size, padding, etc.

        response = self.client.post('/api/generate_pdf', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_generate_pdf_invalid_font_size(self):
        """Test API response when an invalid font_size is provided."""
        data = {
            "labels": [{"name": "Label 1", "use_aliquots": False, "aliquots": [], "count": 1}],
            "font_size": "invalid"  # Invalid font size (should be a number)
        }

        response = self.client.post('/api/generate_pdf', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()

