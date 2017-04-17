import xlsxwriter

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('bals.xls')
worksheet = workbook.add_worksheet()

# Add a bold format to use to highlight cells.
bold = workbook.add_format({'bold': True})

# Add a number format for cells with money.

# Write some data headers.
worksheet.write('B13', 'Item', bold)
