from xlrd import open_workbook,cellname
book = open_workbook('agro.xlsx')
sheet = book.sheet_by_name('Resultado')

print 'Nome', '\t\tNota 1B', 'Nota 2B', 'Nota 3B', 'Nota 4B', 'PF'
for row_index in range(12, 47):
  print sheet.cell(row_index,2).value,  sheet.cell(row_index,21).value, sheet.cell(row_index,24).value, sheet.cell(row_index,27).value, sheet.cell(row_index,30).value, sheet.cell(row_index,39).value 

