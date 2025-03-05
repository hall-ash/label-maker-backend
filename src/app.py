from flask import Flask, request, send_file, jsonify
from src.label_maker import LabelMaker
from src.label import LabelList
from flask_cors import CORS
from io import BytesIO
from src.label_utils import get_skips_dict
import os
import logging
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Handle CORS 
allowed_origin = os.getenv("CORS_ALLOWED_ORIGINS")  
CORS(app, resources={r"/api/*": {"origins": allowed_origin}})

# Configure logging
logging.basicConfig(filename='./tests/error.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Log each request
@app.before_request
def log_request():
    logging.info(f"Request received: {request.method} {request.path} from {request.remote_addr}")

# Custom error handling
@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Error: {str(e)}") 
    if isinstance(e, HTTPException):
        return jsonify({"error": e.description}), e.code
    return jsonify({"error": "Something went wrong. Please try again later."}), 500  

def validate_payload(data):
    """Validates the incoming JSON payload, allowing empty/None fields."""
    expected_fields = {
        "labels": list,
        "sheet_type": (str, type(None)),
        "skip_labels": (str, type(None)),
        "start_label": (str, type(None)),
        "border": (bool, type(None)),
        "font_size": (int, float, type(None)),
        "padding": (int, float, type(None)),
        "file_name": (str, type(None)),
        "text_anchor": (str, type(None))
    }

    if not isinstance(data, dict):
        return "Invalid payload: Data must be a JSON object."
    
    if not data.get('labels'):
        return "No labels provided."

    for field, expected_type in expected_fields.items():
        if field in data and not isinstance(data[field], expected_type):
            return f"Invalid type for '{field}': Expected {expected_type}, got {type(data[field])}"

    return None  # No errors

@app.route('/api/generate_pdf', methods=['POST'])
def generate_pdf():
    try:
        # Handle invalid JSON requests
        try:
            data = request.get_json(force=True)  # Ensures JSON is parsed correctly
        except Exception:
            return jsonify({"error": "Invalid JSON payload"}), 400  

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate data
        error_message = validate_payload(data)
        if error_message:
            return jsonify({"error": error_message}), 400

        labels = data.get('labels')
        sheet_type = data.get('sheet_type', "LCRY-1700")
        skip_labels = data.get('skip_labels', None)
        start_label = data.get('start_label', None)
        border = data.get('border', False)
        font_size = data.get('font_size', 12)
        padding = data.get('padding', 1.75)
        file_name = data.get('file_name', 'labels')
        text_anchor = data.get('text_anchor', 'middle')
        
        if len(labels) <= 0:
            raise ValueError("No labels provided")

        input_labels = LabelList(labels).get_label_texts()
        used_label_dict = get_skips_dict(skip_labels, sheet_type, start_label)

        label_maker = LabelMaker(
            input_labels=input_labels,
            used_label_dict=used_label_dict,
            sheet_type=sheet_type, border=border,
            padding_value=padding, font_size=font_size,
            text_anchor=text_anchor)

        pdf_buffer = BytesIO()
        label_maker.save(pdf_buffer)
        pdf_buffer.seek(0)

        return send_file(pdf_buffer, as_attachment=True, download_name=f'{file_name}.pdf', mimetype='application/pdf')

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({'error': "Something went wrong. Please try again later."}), 500  

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  
    app.run(host='0.0.0.0', port=port)




