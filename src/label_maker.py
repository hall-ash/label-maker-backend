import labels
from reportlab.graphics import shapes
from reportlab.pdfbase.pdfmetrics import stringWidth, registerFont
from reportlab.pdfbase.ttfonts import TTFont
from static.sheet_types import sheet_types
import os


MU = "µ"

class LabelMaker:
    '''
    used_label_dict is a dict of key: pg_no, list of used_labels 1-indexed row, col
    '''
    def __init__(self, input_labels=[], used_label_dict={}, border=False, sheet_type="LCRY-1700", padding_value=1.75, font_size=12, text_anchor="middle"):
     
        sheet_type = sheet_types[sheet_type]
        
        self.cols = sheet_type['cols']
        self.rows = sheet_type['rows']
       
        self.font_size = font_size
        self.text_anchor = text_anchor

        self.font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../static/Arial-Bold.ttf"))

        specs = labels.Specification(sheet_type['sheet_width'], 
                                     sheet_type['sheet_height'], 
                                     self.cols, 
                                     self.rows, 
                                     sheet_type['label_width'], 
                                     sheet_type['label_height'], 
                                     column_gap=sheet_type['column_gap'], 
                                     row_gap=sheet_type['row_gap'], 
                                     left_margin=sheet_type['x_margin'], 
                                     top_margin=sheet_type['top_margin'], 
                                     corner_radius=sheet_type['corner_radius'], 
                                     left_padding=padding_value, 
                                     top_padding=padding_value, 
                                     bottom_padding=padding_value, 
                                     right_padding=padding_value) 
        # Create the sheet.
        self.sheet = labels.Sheet(specs, self._write_multiline_text_to_label, border=border)

        for page, used_labels in used_label_dict.items():
            self.sheet.partial_page(page, used_labels)
        
        self.sheet.add_labels(input_labels)


    def save(self, dest_path):
        self.sheet.save(dest_path)


    def _write_multiline_text_to_label(self, label, width, height, text):
        registerFont(TTFont("Arial-Bold", self.font_path))
        
        # Split the multiline text into individual lines
        text = str(text)
        lines = text.split('\n')
        font_size = self.font_size
        
        # Measure the width of each line and shrink the font size until all lines fit within the width
        font_name = "Arial-Bold" 
        max_line_width = max(stringWidth(line, font_name, font_size) for line in lines)
        
        while max_line_width > width:
            font_size *= 0.95
            max_line_width = max(stringWidth(line, font_name, font_size) for line in lines)

        # Calculate the total height of the text block 
        line_height = font_size * 1.25  # Add spacing between lines
        total_text_height = len(lines) * line_height
   
        # fit text height to the label
        while total_text_height > height:
            font_size *= 0.95
            line_height = font_size * 1.25
            total_text_height = len(lines) * line_height

        # Add each line to the label
        if self.text_anchor == 'start':
            start_x = 0
        elif self.text_anchor == 'end':
            start_x = width
        else:
            start_x = width / 2.0
        start_y = (height + total_text_height) / 2 - font_size 
        for i, line in enumerate(lines):
            line_y = start_y - i * line_height
            s = shapes.String(start_x, line_y, line, textAnchor=self.text_anchor)
            s.fontName = font_name
            s.fontSize = font_size
            label.add(s)


    