from flask import Flask, request, send_file, jsonify
from label_maker import LabelMaker
from label import LabelList
from flask_cors import CORS
from io import BytesIO
import os
from api_logic import get_skips_dict


app = Flask(__name__)
#CORS(app, resources={r"/*": {"origins": "http://192.168.134.118:3000"}})
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

@app.route('/api/generate_pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.get_json()

        if not data:
            raise ValueError("No data provided")

        labels = data.get('labels')
        sheet_type = data.get('sheet_type')
        skip_labels = data.get('skip_labels', None)
        start_label = data.get('start_label', None)
        border = data.get('border', False)
        font_size = data.get('font_size', 12)
        padding = data.get('padding', 1.75)
        file_name = data.get('file_name', 'labels')
        
        input_labels = LabelList(labels).get_label_texts()

        used_label_dict = get_skips_dict(skip_labels, sheet_type, start_label) 
        label_maker = LabelMaker(input_labels=input_labels, used_label_dict=used_label_dict, sheet_type=sheet_type, border=border, padding_value=padding, font_size=font_size)
        
        pdf_buffer = BytesIO()
        label_maker.save(pdf_buffer)
        pdf_buffer.seek(0)

        return send_file(pdf_buffer, as_attachment=True, download_name=f'{file_name}.pdf', mimetype='application/pdf')

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    #app.run(debug=True)
    host = "192.168.4.112"
    workhost = "192.168.134.118"
    app.run(host=workhost, port=5000, debug=True)