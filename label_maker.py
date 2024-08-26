import labels
from reportlab.graphics import shapes
from reportlab.pdfbase.pdfmetrics import stringWidth
from sample import Sample
from lots import lots
from label import LabelList

MU = "µ"

class LabelMaker:
    '''
    used_label_dict is a dict of key: pg_no, list of used_labels 1-indexed row, col
    '''
    def __init__(self, input_labels=[], used_label_dict={}, border=False, sheet_type="LCRY-1700"):
        
        # Dimensions here
        # https://www.divbio.com/content/files/laser_instructions/laser_cryo-tag_instructions_1.pdf
     
        if sheet_type == "LCRY-1700": 
            column_gap = 3 #3.2
            row_gap = 3 #3.49
            cols = 5
            rows = 17
            label_width = 32.62 #33.65 #33 or 32.512 (1.28in)
            label_height = 12.88 #13 or 12.7 (0.5 in)
            sheet_width = 214
            sheet_height = 279 #279
            x_margin = 19.5#15 # 0.77 in, looks like 20
            top_margin = 6.1 #0.24 in; was 0
            corner_radius = 3
        
        self.cols = cols
        self.rows = rows
        # specs = labels.Specification(sheet_width, sheet_height, cols, rows, label_width, label_height, left_margin=x_margin, column_gap=gap, right_margin=x_margin, top_margin=y_margin, row_gap=gap, bottom_margin=y_margin, left_padding=PADDING, right_padding=PADDING, top_padding=PADDING, bottom_padding=PADDING, corner_radius=2, padding_radius=2)

        #specs = labels.Specification(sheet_width, sheet_height, cols, rows, label_width, label_height, left_margin=x_margin, column_gap=x_gap, top_margin=top_margin, row_gap=y_gap, corner_radius=2) # top_padding=2, bottom_padding=1, left_padding=1, right_padding=1, padding_radius=1)

        padding_value = 1.75
        specs = labels.Specification(sheet_width, sheet_height, self.cols, self.rows, label_width, label_height, column_gap=column_gap, row_gap=row_gap, left_margin=x_margin, top_margin=top_margin, corner_radius=corner_radius, left_padding=padding_value, top_padding=padding_value, bottom_padding=padding_value, right_padding=padding_value) if padding_value \
            else labels.Specification(sheet_width, sheet_height, self.cols, self.rows, label_width, label_height, column_gap=column_gap, row_gap=row_gap, left_margin=x_margin, top_margin=top_margin, corner_radius=corner_radius)

        # Create the sheet.
        self.sheet = labels.Sheet(specs, self._write_multiline_text_to_label, border=border)


      
        # if start_label:
        #     if used_label_dict:
        #         used_label_dict[1].extend(self.start_on_label(start_label))
        #     else:
        #         used_label_dict = {1: self.start_on_label(start_label)}

        # self.start_label = start_label

        # if used_label_dict:
        #     validated_skipped_labels = self._get_validated_skipped_labels(self.rows, self.cols, used_label_dict)
        #     for page, used_labels in validated_skipped_labels.items():
        #         self.sheet.partial_page(page, used_labels)


        # if samples:
        #     for sample in samples:
        #         sample_labels = self._add_sample_labels(sample)
        #         input_labels.extend(sample_labels)

        for page, used_labels in used_label_dict.items():
            self.sheet.partial_page(page, used_labels)
        
        self.sheet.add_labels(input_labels)



    def save(self, dest_path):
        # for page in range(1, self.sheet.page_count + 1):
        #     self.sheet.preview(page, f'preview{page}.png')
       
        self.sheet.save(dest_path)
        print("{0:d} label(s) output on {1:d} page(s).".format(self.sheet.label_count, self.sheet.page_count))


    # TAKE INTO ACCOUNT ANY SKIPPED LABELS!!!!!!
    # MAKE SKIPPED LABELS AN ATTRIBUTE?
    def find_next_start_label(self):

        labels_per_sheet = self.rows * self.cols
        num_used_labels = len(self.start_on_label(self.start_label))
        num_labels_remaining = self.sheet.label_count - labels_per_sheet - num_used_labels
        num_labels_last_pg = num_labels_remaining % labels_per_sheet

        start_col = num_labels_last_pg % self.cols + 1
        start_row = num_labels_last_pg / self.cols + 1

        to_letter = lambda col : chr(col + 64) 
        # start_label = A17
        return to_letter(start_col) + str(start_row)


    # def _add_sample_labels(self, sample):
    #     aliquots = sample.aliquots
    #     label_text = sample.name + "\n" + str(round(sample.concentration, 1)) + " " + sample.concentration_unit + " in water\n" 
    #     sample_labels = []

    #     for a in aliquots:
    #         sample_labels.extend([f'{label_text}{a['volume']}{a['volume_unit']}, {a['mass']}{a['mass_unit']} {i} of {a['number']}' for i in range(1, a['number'] + 1)])

    #     return sample_labels


    def _write_multiline_text_to_label(self, label, width, height, text):
        # Split the multiline text into individual lines
        text = str(text)
        lines = text.split('\n')
        
        # Measure the width of each line and shrink the font size until all lines fit within the width
        font_size = 12
        # text_width = width - 6
        font_name = "Helvetica" # "Bahnschrift"
        max_line_width = max(stringWidth(line, font_name, font_size) for line in lines)
        
        while max_line_width > width:
            font_size *= 0.95
            max_line_width = max(stringWidth(line, font_name, font_size) for line in lines)

        # Calculate the total height of the text block to fit and center it vertically
        line_height = font_size * 1.25  # Add some space between lines
        total_text_height = len(lines) * line_height
        # text_height = height - 3
        while total_text_height > height:
            font_size *= 0.95
            line_height = font_size * 1.25
            total_text_height = len(lines) * line_height

        start_y = (height + total_text_height) / 2 - font_size 
        
        # Add each line to the label, centered horizontally and vertically
        for i, line in enumerate(lines):
            line_y = start_y - i * line_height
            line_width = stringWidth(line, font_name, font_size)
            s = shapes.String(width / 2.0, line_y, line, textAnchor="middle")
            s.fontName = font_name
            s.fontSize = font_size
            label.add(s)


    def _get_validated_skipped_labels(self, rows, cols, skipped_labels):
        '''
        used_label_dict = {
        1: [(1, 1), (2, 6)],
        2: [(3, 3), (1, 1)],
        }
        '''
        
        validated_skipped_labels = {page: [] for page in skipped_labels.keys()}
        for page, skipped_labels in skipped_labels.items():
            for row, col in skipped_labels:
                if 0 < row <= rows and 0 < col <= cols:
                    validated_skipped_labels[page].append((row, col))

        return validated_skipped_labels


    @staticmethod
    def skip_multiple(max_row, max_col, other_skips=None):
        skips = []
        for row in range(1, max_row + 1):
            for col in range(1, max_col + 1):
                skips.append((row, col))
                
        if other_skips:
            skips.extend(other_skips)
        
        return skips


    @staticmethod
    def skip_all_but(rows, cols, dont_skip=None):
        skips = set()
        for row in range(1, rows + 1):
            for col in range(1, cols + 1):
                skips.add((row, col))
        
        return skips - set(dont_skip)

    @staticmethod
    def skip_by_cell_range(page_no, cell_ranges, max_cols=5):
        '''
        example cell_range = "A1-C4" 
        cell_ranges = ["A1-C4", "D10-G1"]
        '''

        # REWRITE FOR CASE A1-A3
        col_num = lambda letter : ord(letter.upper()) - ord('A') + 1 

        skips = set()
        
        for cell_range in cell_ranges:
         
            single_cell = "-" not in cell_range
            split = cell_range.split("-")
            
            first_cell = split[0]
            last_cell = first_cell if single_cell else split[1]
            start_col = col_num(first_cell[0])
            end_col = col_num(last_cell[0])
            start_row = int(first_cell[1:])
            end_row = int(last_cell[1:])


            if single_cell:
                skips.add((start_row, start_col))
            else:
                if start_col == end_col:
                    skips.update({(row, start_col) for row in range(start_row, end_row + 1)})
                else:
                    skips.update({(start_row, col) for col in range(start_col, max_cols + 1)})
                    for row in range(start_row + 1, end_row):
                        for col in range(1, max_cols + 1):
                            skips.add((row, col))

                    skips.update({(end_row, col) for col in range(1, end_col + 1)})
            
        return {page_no: list(skips)}


    def start_on_label(self, label):
        col_num = lambda letter : ord(letter.upper()) - ord('A') + 1 
        end_row = int(label[1:])
        end_col = col_num(label[0])

        skipped_labels = []

        for row in range(1, end_row):
            for col in range(1, self.cols + 1):
                skipped_labels.append((row, col))

        skipped_labels.extend([(end_row, col) for col in range(1, end_col)])

        return skipped_labels


# Save the file and we are done.
if __name__ == "__main__":


    # used_label_dict_ibpl = {
    #     #1: LabelMaker.skip_all_but(17, 5, dont_skip=dont_skip)
    #     1: LabelMaker.skip_multiple(14, 5, other_skips)
    # }

    used_labels = LabelMaker.skip_by_cell_range(1, ['A1-E15'])

    

    # samples_ivt = [
    #     Sample('Klebsiella KPO1 OPS B4\nLot IVT-KPO1-004', 1589.92337164751 / 1000, 'mg/mL', aliquots=kpo4_aliquots),
    # ]



   
    #samples_ibpl = [Sample(lot['name'], lot['concentration'] / 1000, 'mg/mL', aliquots=lot['aliquots']) for lot in lots]


    
    input_labels = [
        f'Klebsiella KPK149 CPS B2\nLot IVT-K149-002\n19.3 mg/mL in water\n5mg, 258{MU}L',
        f'Klebsiella KPK62 CPS B1\nLot IVT-K62-001\n6.6 mg/mL in water\n5mg, 757{MU}L',
        f'Klebsiella KPK102 CPS B3\nLot IVT-K102-003\n12.2 mg/mL in water\n1g, 81.8mL',
        f'Klebsiella KPK25 CPS B2\nLot IVT-K25-002\n18.7 mg/mL in water\n1g, 53.6mL',
        f'Klebsiella KPK2 CPS B2\nLot IVT-K2-002\n2.7 mg/mL in water\n1g, 336.1mL',
    ]

    PRINT_BLANKS = False

    if PRINT_BLANKS:
        used_labels = LabelMaker.skip_by_cell_range(1, ['A1-E15'])
        print('used', str(used_labels))
        input_labels = ['blank']
        input_labels.extend(["  " for i in range(84)])
        label_maker = LabelMaker(input_labels=input_labels, border=True, used_label_dict=used_labels)
        label_maker.save('blanks.pdf')
    else:
        label_maker = LabelMaker(input_labels=input_labels, used_label_dict=used_labels)
        label_maker.save('aliquots for drew and dimple.pdf')
  