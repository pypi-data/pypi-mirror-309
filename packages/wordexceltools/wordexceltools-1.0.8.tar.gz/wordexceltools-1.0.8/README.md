# WordExcelTools

A tool for quickly operating on Excel files and generating Word documents based on docx, python-docx and openpyxl.

> The current version 1.0.8 is quite different from the previous version, so please note before you update it.

## Install

```sh
pip install wordexceltools
```

## Main Functions

```sh
1: excel_add_sheet(source_excel, new_sheet_name)
2: excel_copy_file(source_excel, target_excel)
3: excel_delete_file(target_excel)
4: excel_delete_sheet_by_index(source_excel, sheet_index)
5: excel_delete_sheet_columns(source_excel, sheet_index, target_column_index, number_of_columns)
6: excel_delete_sheet_rows(source_excel, sheet_index, target_row_index, number_of_rows)
7: excel_freeze_panes(source_excel, sheet_index, cell_reference, output_file)
8: excel_get_column_keyword_count(sheet, column_name, keyword)
9: excel_get_column_len(sheet, column_name)
10: excel_get_column_list(sheet, column_name)
11: excel_get_column_str_custom(sheet, column_name, separator, end_mark)
12: excel_get_columns_keyword_counts(sheet, platform_prefix, result_suffix)
13: excel_get_sheet(source_excel, sheet_index)
14: excel_get_sheet_cell_date_value(sheet, row, column)
15: excel_get_sheet_cell_value(sheet, row, column)
16: excel_get_sheet_col_values(sheet, col_index)
17: excel_get_sheet_name(sheet_data, sheet_index)
18: excel_get_sheet_row_col(sheet)
19: excel_get_sheet_row_values(sheet, row_index)
20: excel_get_sheets_name_row(source_excel)
21: excel_insert_sheet_columns(source_excel, sheet_index, target_column_index, number_of_columns)
22: excel_insert_sheet_rows(source_excel, sheet_index, target_row_index, number_of_rows)
23: excel_merge_cells(source_excel, sheet_index, ranges_to_merge, output_file)
24: excel_replace_content(source_excel, sheet_index, target_text, replacement_text, output_file, rows, cols)
25: excel_set_alignment(source_excel, sheet_index, ranges, horizontal, vertical, output_file)
26: excel_set_bold(source_excel, sheet_index, ranges, bold, output_file)
27: excel_set_fill_color(source_excel, sheet_index, ranges, color, output_file)
28: excel_set_font_color(source_excel, sheet_index, ranges, color, output_file)
29: excel_set_font_size(source_excel, sheet_index, ranges, font_size, output_file)
30: excel_set_sheet_cell_value(source_excel, sheet_index, row, column, value)
31: excel_unmerge_cells(source_excel, sheet_index, ranges_to_unmerge, output_file)
32: word_add_custom_heading(document, level, text)
33: word_add_custom_paragraph(document, text, style)
34: word_add_custom_table(document, row_count, column_count, style, font_size, spacing_before)
35: word_add_figure_caption(document, caption_text)
36: word_add_indented_paragraph(document, text)
37: word_add_ordered_list(document, items, index_style, indentation)
38: word_add_table_caption(document, caption_text)
39: word_docxinitial(doc, text_font_type, text_font_size, text_font_line_spacing, text_header, text_footer)
40: word_get_platform_results(list_test_objs, platform_prefix, result_suffix)
41: word_get_section_number(paragraph_text)
42: word_get_table_cell_text(table, row_index, column_index)
43: word_merge_cells(table, start_row, start_column, end_row, end_column)
44: word_merge_cells_by_column(table, column_index)
45: word_set_number_to_roman(number)
46: word_set_table_alignment(table, start_row, start_column, end_row, end_column, horizontal_alignment, vertical_alignment)
47: word_set_table_cell_text(table, row_index, column_index, text)
48: word_set_table_style(table, font_size, spacing_before)
49: word_setsectionformat(doc)
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