# WordExcelTools

A tool for quickly operating on Excel files and generating Word documents based on docx, python-docx and openpyxl.

> The current version 1.0.6 is quite different from the previous version, so please note before you update it.

## Install

```sh
pip install wordexceltools
```

## Main Functions

```sh
1: word_docxinitial, Parameters: ['doc', 'text_font_type', 'text_font_size', 'text_font_line_spacing', 'text_header', 'text_footer']
2: word_setsectionformat, Parameters: ['doc']
3: word_add_figure_caption, Parameters: ['document', 'caption_text']
4: word_add_custom_heading, Parameters: ['document', 'level', 'text']
5: word_add_custom_paragraph, Parameters: ['document', 'text', 'style']
6: word_add_custom_table, Parameters: ['document', 'row_count', 'column_count', 'style', 'font_size', 'spacing_before']
7: word_add_indented_paragraph, Parameters: ['document', 'text']
8: word_add_ordered_list, Parameters: ['document', 'items', 'index_style', 'indentation']
9: word_add_table_caption, Parameters: ['document', 'caption_text']
10: excel_get_sheet_cell_value, Parameters: ['sheet', 'row', 'column']
11: excel_get_sheet_cell_date_value, Parameters: ['sheet', 'row', 'column']
12: excel_get_column_keyword_count, Parameters: ['sheet', 'column_name', 'keyword']
13: excel_get_column_len, Parameters: ['sheet', 'column_name']
14: excel_get_column_list, Parameters: ['sheet', 'column_name']
15: excel_get_column_str_custom, Parameters: ['sheet', 'column_name', 'separator', 'end_mark']
16: excel_get_columns_keyword_counts, Parameters: ['sheet', 'platform_prefix', 'result_suffix']
17: word_get_section_number, Parameters: ['paragraph_text']
18: word_get_table_cell_text, Parameters: ['table', 'row_index', 'column_index']
19: excel_get_sheets_name_row, Parameters: ['source_excel']
20: excel_get_sheet, Parameters: ['source_excel', 'sheet_index']
21: excel_get_sheet_row_values, Parameters: ['sheet', 'row_index']
22: excel_get_sheet_col_values, Parameters: ['sheet', 'col_index']
23: excel_get_sheet_name, Parameters: ['sheet_data', 'sheet_index']
24: excel_get_sheet_row_col, Parameters: ['sheet']
25: excel_insert_sheet_columns, Parameters: ['source_excel', 'sheet_index', 'target_column_index', 'number_of_columns']
26: excel_insert_sheet_rows, Parameters: ['source_excel', 'sheet_index', 'target_row_index', 'number_of_rows']
27: excel_set_sheet_cell_value, Parameters: ['source_excel', 'sheet_index', 'row', 'column', 'value']
28: excel_delete_sheet_rows, Parameters: ['source_excel', 'sheet_index', 'target_row_index', 'number_of_rows']
29: excel_delete_sheet_columns, Parameters: ['source_excel', 'sheet_index', 'target_column_index', 'number_of_columns']
30: excel_add_sheet, Parameters: ['source_excel', 'new_sheet_name']
31: excel_delete_sheet_by_index, Parameters: ['source_excel', 'sheet_index']
32: word_merge_cells, Parameters: ['table', 'start_row', 'start_column', 'end_row', 'end_column']
33: word_merge_cells_by_column, Parameters: ['table', 'column_index']
34: word_set_number_to_roman, Parameters: ['number']
35: word_set_table_cell_text, Parameters: ['table', 'row_index', 'column_index', 'text']
36: word_set_table_alignment, Parameters: ['table', 'start_row', 'start_column', 'end_row', 'end_column', 'horizontal_alignment', 'vertical_alignment']
37: word_set_table_style, Parameters: ['table', 'font_size', 'spacing_before']
38: word_get_platform_results, Parameters: ['list_test_objs', 'platform_prefix', 'result_suffix']
```

## Example

```python
from docx import Document
import openpyxl
import wordexceltools

soucrce_excel = "./test.xlsx"
sheet0 = excel_get_sheet(source_excel, 0)
print(sheet0.max_column)
print(sheet0.max_row)
print(excel_get_sheet_cell_value(sheet0, 2, 2))
print('========================')
print(excel_get_sheet_row_col(sheet0))
print('========================')

print(excel_get_sheet_row_values(sheet0, 1))
print(excel_get_sheet_col_values(sheet0, 1))
print('========================')

excel_insert_sheet_columns(source_excel, 0, 1, 2)

excel_insert_sheet_rows(source_excel, 0, 2, 3)

for i in range(3,6):
    for j in range(2,4):
        excel_set_sheet_cell_value(source_excel,0,i,j,f"{i}x{j}")
#
excel_delete_sheet_columns(source_excel, 0,2,1)
excel_delete_sheet_rows(source_excel, 0,2,2)
excel_add_sheet(source_excel,"test1")
excel_add_sheet(source_excel,"test2")
print(excel_get_sheets_name_row(source_excel))
excel_delete_sheet_by_index(source_excel,3)
excel_delete_sheet_by_index(source_excel,2)
```