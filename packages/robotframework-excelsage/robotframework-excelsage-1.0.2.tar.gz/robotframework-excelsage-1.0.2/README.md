# ExcelSage Library
ExcelSage is a Python-based library designed for interacting with Excel 2010 and above files in automation testing environments, specifically built for use with Robot Framework. The library provides comprehensive methods for manipulating Excel sheets, cells, rows, columns, and workbooks. This includes reading and writing data, modifying formatting, sheet protection, and more.

## Features
- Excel Workbook Manipulation: Open, create, save, and close workbooks, with options for sheet creation, deletion, renaming, and more.
- Cell and Sheet Operations: Read and write to specific cells, manage rows and columns, format cells, and fetch sheet data in various formats (list, dict, or pandas DataFrame).
- Data Management: Sort, find, and replace values, search for duplicates, and merge data from multiple Excel files.
- Security Features: Protect/unprotect sheets and workbooks with passwords.
- Integration with Robot Framework: Easily use the library in Robot Framework for automated testing scenarios.

## Installation
You can install the ExcelSage library using pip:
```
pip install robotframework-excelsage
```

## Documentation
You can find the keyword documentation [here](https://deekshith-poojary98.github.io/robotframework-excelsage/).

## Python Usage
Here’s a brief guide on how to use the library in your Python projects.
#### Opening and Creating Workbooks
```py
# Open an existing workbook
excel_sage.open_workbook(workbook_name="path/to/excel.xlsx")

# Create a new workbook
excel_sage.create_workbook(workbook_name="new_excel.xlsx", overwrite_if_exists=True, sheet_data=[['Name', 'Age'], ['Alice', 25]])
```

#### Fetching Sheet Data
```py
# Fetch data from a specific sheet
data = excel_sage.fetch_sheet_data(sheet_name="Sheet1", starting_cell="D6", output_format="dataframe")
```

#### Working with Sheets
```py
# Add a new sheet
excel_sage.add_sheet(sheet_name="NewSheet", sheet_pos=1)

# Delete an existing sheet
excel_sage.delete_sheet(sheet_name="Sheet2")

# Rename a sheet
excel_sage.rename_sheet(old_name="OldSheet", new_name="NewSheetName")
```

#### Writing to Cells
```py
# Write a value to a specific cell
excel_sage.write_to_cell(cell_name="A1", cell_value="Test Data", sheet_name="Sheet1")

# Fetch a value from a specific cell
value = excel_sage.get_cell_value(cell_name="B2", sheet_name="Sheet1")
```

#### Managing Rows and Columns
```py
# Append a row to the sheet
excel_sage.append_row(row_data=["Mark", "Engineer", 36], sheet_name="Sheet1")

# Insert a column at a specific position
excel_sage.insert_column(col_data=["Name", "John", "Dean", "Sam"], col_index=2, sheet_name="Sheet1")

# Delete a row
excel_sage.delete_row(row_index=5, sheet_name="Sheet1")
```

#### Formatting Cells
```py
# Format cell A1 in Sheet1
excel_sage.format_cell(cell_name="A1", font_size=12, font_color="#FF0000", sheet_name="Sheet1", bold=True, bg_color="#FFFF00")
```

#### Searching and Replacing
```py
# Find value in a sheet
excel_sage.find_value(value="search_term", sheet_name="Sheet1", occurence="first")

# Find and replace a value in a sheet
excel_sage.find_and_replace(old_value="old_term", new_value="new_term", sheet_name="Sheet1", occurence="all")
```

#### Merging and Comparing Excel Files
```py
# Merge multiple Excel files
excel_sage.merge_excels(file_list=["file1.xlsx", "file2.xlsx"], output_filename="merged_output.xlsx", merge_type="multiple_sheets")

# Compare two Excel files
comparison = excel_sage.compare_excels(source_excel="file1.xlsx", target_excel="file2.xlsx", source_excel_config={'sheet_name': 'Sheet1','columns': ['Name', 'Age']}, target_excel_config={'sheet_name': 'Sheet2', 'starting_cell': 'D8', 'columns': ['Name', 'Age']})
```

#### Security Features
```py
# Protect a sheet with a password
excel_sage.protect_sheet(password="mypassword", sheet_name="Sheet1")

# Unprotect a workbook
excel_sage.unprotect_workbook(password="mypassword", unprotect_sheets=True)
```

#### CSV Export
```py
# Export a sheet to CSV
excel_sage.export_to_csv(filename="source.xlsx", sheet_name="Sheet1", output_filename="output.csv
```

## Robot Framework Usage
To use ExcelSage in Robot Framework, first add it to your test suite using the Library keyword.

```robot
*** Settings ***
Library    ExcelSage

*** Variables ***
${EXCEL_PATH}    path/to/excel.xlsx

*** Test Cases ***
Test Opening Workbook
    Open Workbook    ${EXCEL_PATH}

Test Fetching Sheet Data
    ${data}=    Fetch Sheet Data    sheet_name=Sheet1    output_format=dataframe
    Log    ${data}

Test Writing to Cell
    Write To Cell    A1    Test Data    Sheet1

Test Appending Row
    Append Row    row_data=["John", 28, "Engineer"]    sheet_name=Sheet1

Test Formatting Cell
    Format Cell    A1    font_size=12    font_color=FF0000    sheet_name=Sheet1    bold=True    bg_color=FFFF00

Test Protecting Sheet
    Protect Sheet    password=my_password    sheet_name=Sheet1
```

#### Opening and Creating Workbooks
```robot
*** Test Cases ***
Open Existing Workbook
    Open Workbook    workbook_name=${EXCEL_PATH}

Create New Workbook
    Create Workbook    workbook_name=new_excel.xlsx    overwrite_if_exists=True    sheet_data=[[Name, Age], [Alice, 25]]
```

#### Fetching Sheet Data
```robot
*** Test Cases ***
Fetch Data From Sheet
    ${data}=    Fetch Sheet Data    sheet_name=Sheet1    output_format=dataframe    starting_cell=A1
    Log    ${data}
```

#### Working with Sheets
```robot
*** Test Cases ***
Add New Sheet
    Add Sheet    sheet_name=NewSheet    sheet_pos=1    sheet_data=[[ID, Name], [1, John]]

Delete Existing Sheet
    Delete Sheet    sheet_name=Sheet2

Rename Sheet
    Rename Sheet    old_name=OldSheet    new_name=NewSheet
```

#### Writing to Cells
```robot
*** Test Cases ***
Write Data to a Cell
    Write To Cell    A1    Test Value    sheet_name=Sheet1

Get Data from a Cell
    ${value}=    Get Cell Value    A1    sheet_name=Sheet1
    Log    ${value}
```

#### Managing Rows and Columns
```robot
*** Test Cases ***
Append a Row to a Sheet
    Append Row    row_data=["John", 30]    sheet_name=Sheet1

Insert a Row at Specific Index
    Insert Row    row_data=["Jane", 28]    row_index=2    sheet_name=Sheet1

Delete a Row
    Delete Row    row_index=4    sheet_name=Sheet1

Append a Column
    Append Column    col_data=["New Column", "Data 1", "Data 2"]    sheet_name=Sheet1

Insert a Column at Specific Position
    Insert Column    col_data=["Col Header", "Val 1", "Val 2"]    col_index=2    sheet_name=Sheet1

Delete a Column
    Delete Column    col_index=3    sheet_name=Sheet1
```

#### Formatting Cells
```robot
*** Test Cases ***
Format a Cell
    Format Cell    A1    font_size=14    font_color=#0000FF    sheet_name=Sheet1    bold=True    italic=True    bg_color=#FFFFAA
```

#### Searching and Replacing
```robot
*** Test Cases ***
Find a Value
    ${location}=    Find Value    value=search_term    sheet_name=Sheet1    occurence=first
    Log    ${location}

Find and Replace a Value
    Find And Replace    old_value=old_term    new_value=new_term    sheet_name=Sheet1    occurence=all
```

#### Merging and Comparing Excel Files
```robot
*** Test Cases ***
Merge Excel Files
    Merge Excels    file_list=[file1.xlsx, file2.xlsx]    output_filename=merged_output.xlsx    merge_type=sheet_wise

Compare Two Excel Files
    ${comparison}    Compare Excels    source_excel=file1.xlsx    target_excel=file2.xlsx
    Log    ${comparison}
```

#### Protecting and Unprotecting Sheets and Workbooks
```robot
*** Test Cases ***
Protect a Sheet
    Protect Sheet    password=my_password    sheet_name=Sheet1

Unprotect a Workbook
    Unprotect Workbook    password=my_password    unprotect_sheets=True
```

#### CSV Export
```robot
*** Test Cases ***
Export Sheet Data to CSV
    Export To CSV    filename=source.xlsx    sheet_name=Sheet1    output_filename=output.csv    overwrite_if_exists=True
```

#### Miscellaneous Features
```robot
*** Test Cases ***
Clear a Sheet
    Clear Sheet    sheet_name=Sheet1

Copy a Sheet
    Copy Sheet    source_sheet_name=Sheet1    new_sheet_name=Sheet_Copy

Sort a Column
    Sort Column    column_name_or_letter=A    asc=True    sheet_name=Sheet1

Find Duplicates
    ${duplicates}=    Find Duplicates    column_names_or_letters=[A, B]    output_format=list    starting_cell=A1    sheet_name=Sheet1
    Log    ${duplicates}
```

## API Reference
#### Private Helper Methods
- `__get_active_sheet_name(self, sheet_name)` – Fetches the name of the active sheet.
- `__argument_type_checker(self, arg_list)` – Validates the types of provided arguments.

#### Public Methods
- `open_workbook(self, workbook_name)` – Opens an existing Excel workbook.
- `create_workbook(self, workbook_name, overwrite_if_exists, sheet_data)` – Creates a new workbook.
- `get_sheets(self)` – Retrieves a list of all sheets in the workbook.
- `add_sheet(self, sheet_name, sheet_pos, sheet_data)` – Adds a new sheet.
- `delete_sheet(self, sheet_name)` – Deletes the specified sheet.
- `fetch_sheet_data(self, sheet_name, ignore_empty_rows, ignore_empty_columns, starting_cell, output_format)` – Retrieves sheet data in the specified format (list, dict, or DataFrame).
- `rename_sheet(self, old_name, new_name)` – Renames an existing sheet.
- `get_cell_value(self, cell_name, sheet_name)` – Retrieves the value of a specified cell.
- `close_workbook(self)` – Closes the active workbook.
- `save_workbook(self)` – Saves the active workbook.
- `set_active_sheet(self, sheet_name)` – Sets the active sheet.
- `write_to_cell(self, cell_name, cell_value, sheet_name)` – Writes a value to a specific cell.
- `get_column_count(self, starting_cell, ignore_empty_columns, sheet_name)` – Returns the count of columns in the sheet.
- `get_row_count(self, sheet_name, starting_cell, include_header, ignore_empty_rows)` – Returns the count of rows in the sheet, optionally excluding the header.
- `append_row(self, row_data, sheet_name)` – Appends a row to the specified sheet.
- `insert_row(self, row_data, row_index, sheet_name)` – Inserts a row at a specific index.
- `delete_row(self, row_index, sheet_name)` – Deletes a row at a specific index.
- `append_column(self, col_data, sheet_name)` – Appends a column to the specified sheet.
- `insert_column(self, col_data, col_index, sheet_name)` – Inserts a column at a specific index.
- `delete_column(self, col_index, sheet_name)` – Deletes a column at a specific index.
- `get_column_values(self, column_names_or_letters, output_format, sheet_name, starting_cell)` – Retrieves values from the specified columns.
- `get_row_values(self, row_indices, output_format, sheet_name)` – Retrieves values from the specified rows.
- `protect_sheet(self, password, sheet_name)` – Protects the specified sheet with a password.
- `unprotect_sheet(self, password, sheet_name)` – Unprotects the specified sheet.
- `protect_workbook(self, password, protect_sheets)` – Protects the workbook with a password.
- `unprotect_workbook(self, unprotect_sheets)` – Unprotects the workbook.
- `clear_sheet(self, sheet_name)` – Clears the contents of the specified sheet.
- `copy_sheet(self, source_sheet_name, new_sheet_name)` – Copies a sheet to a new sheet with a different name.
- `find_value(self, value, sheet_name, occurence)` – Finds the occurrence of a value in the specified sheet.
- `find_and_replace(self, old_value, new_value, sheet_name, occurence)` – Finds and replaces values in the specified sheet.
- `format_cell(self, cell_name, font_size, font_color, sheet_name, alignment, wrap_text, bg_color, etc.)` – Formats the specified cell with various styling options.
- `merge_excels(self, file_list, output_filename, merge_type, skip_bad_rows)` – Merges multiple Excel files.
- `merge_cells(self, cell_range, sheet_name)` – Merges a range of cells in the specified sheet.
- `unmerge_cells(self, cell_range, sheet_name)` – Unmerges a range of cells in the specified sheet.
- `sort_column(self, column_name_or_letter, asc, starting_cell, output_format, sheet_name)` – Sorts a column based on values.
- `find_duplicates(self, column_names_or_letters, output_format, starting_cell, sheet_name)` – Finds duplicate values in the specified columns.
- `compare_excels(self, source_excel, target_excel, source_excel_config, target_excel_config)` – Compares two Excel files.
- `export_to_csv(self, filename, sheet_name, output_filename, overwrite_if_exists)` – Exports sheet data to a CSV file.
- `get_column_headers(self, starting_cell, sheet_name)` – Fetches the column headers starting from the specified cell.

## License
This project is licensed under the [Apache-2.0 License](https://github.com/Deekshith-07/robotframework-excelsage?tab=Apache-2.0-1-ov-file).
