from static.sheet_types import sheet_types


def process_skip_labels_input(input_text):
    labels_skipped_by_pg = []
    pages = input_text.strip().split('\n')
    for pg in pages:
        pg_no, skips = pg.split(':')
        pg_no = int(pg_no.strip())
        skips = [skip.replace(' ', '') for skip in skips.strip().split(',')]
        labels_skipped_by_pg.append((pg_no, skips))
    return labels_skipped_by_pg

def get_num_from_cell(cell, max_cols):
    letter = cell[0]
    row = int(cell[1:])
    col = int(ord(letter.upper()) - ord('A') + 1)
    return col + (row - 1) * max_cols


def get_row_col(num, max_cols):
    row = num // max_cols + 1
    col = num % max_cols
    if col == 0:
        col = max_cols
        row -= 1
    return row, col

def convert_skip_range_to_list(cell_ranges, max_rows, max_cols):
    '''
    example cell_range = "A1-C4" 
    cell_ranges = ["A1-C4", "D10-G1"]
    '''

    skips = set()
    
    max_pos = max_rows * max_cols

    for cell_range in cell_ranges:

        cell_range_split = cell_range.split("-")
        
        if len(cell_range_split) == 2:
            first_pos, last_pos = [get_num_from_cell(cell, max_cols) for cell in cell_range_split]
        elif len(cell_range_split) == 1:
            first_pos = get_num_from_cell(cell_range_split[0], max_cols)
            last_pos = first_pos
        else: # invalid input
            continue 
            
        if not (0 < first_pos <= last_pos and last_pos <= max_pos): # invalid cell range
            continue
            
        if first_pos == last_pos:
            skips.add(get_row_col(first_pos, max_cols))
        else:
            skips.update([get_row_col(pos, max_cols) for pos in range(first_pos, last_pos + 1)])

    return list(skips)


def get_skips_dict(skip_input, sheet_type, start_label):

    sheet = sheet_types.get(sheet_type)
    rows = sheet.get('rows')
    cols = sheet.get('cols')

    if skip_input:
        processed_input = process_skip_labels_input(skip_input)
        skips_dict = {pg_no: convert_skip_range_to_list(skip_range, rows, cols) for pg_no, skip_range in processed_input}
    else:
        skips_dict = {}
        
    if start_label:
        last_pos = get_num_from_cell(start_label, cols)
        labels_to_skip = [get_row_col(pos, cols) for pos in range(1, last_pos)]
        if 1 in skips_dict: #first page
            for skip in labels_to_skip:
                if skip not in skips_dict[1]:
                    skips_dict[1].append(skip)
        else:
            skips_dict[1] = labels_to_skip
            
    return skips_dict