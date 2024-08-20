from flask import Flask, request, send_file, jsonify
from label_maker import LabelMaker
from label import LabelList
from flask_cors import CORS
import os
from api_logic import get_skips_dict

app = Flask(__name__)
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
        border = data.get('border')

        print('labels', labels)
        print('sheet_type', sheet_type)
        print('skip_labels', skip_labels)
        print('start_label', start_label)

        input_labels = LabelList(labels).get_label_texts()

        used_label_dict = get_skips_dict(skip_labels, sheet_type, start_label) 
        label_maker = LabelMaker(input_labels=input_labels, used_label_dict=used_label_dict, sheet_type=sheet_type, border=border)
        
        # Path to save the PDF file
        file_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'demo.pdf')
        label_maker.save(file_path)
        
        # Send the file back to the client
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
