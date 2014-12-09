from xlrd import open_workbook,cellname
book = open_workbook('agro.xlsx')
sheet = book.sheet_by_name('Resultado')

print 'Nome', '\t\tNota 1B', 'Nota 2B', 'Nota 3B', 'Nota 4B', 'PF'
for row_index in range(12, 60):
  try: 
    row = int(sheet.cell(row_index, 0).value)
    sheet1b = book.sheet_by_name('Nota 1B') # 45 AT
    sheet2b = book.sheet_by_name('Nota 2B')
    sheet3b = book.sheet_by_name('Nota 3B')
    sheet4b = book.sheet_by_name('Nota 4B')
    
    ft1b = sheet1b.cell(row_index, 45).value
    ft2b = sheet2b.cell(row_index, 45).value
    ft3b = sheet3b.cell(row_index, 45).value
    ft4b = sheet4b.cell(row_index, 45).value




    if len(sheet.cell(row_index, 2).value) < 3:
      continue
 
    print sheet.cell(row_index, 2).value,'ft', int(ft1b),  'nt', sheet.cell(row_index, 21).value,'ft:', ft2b,  sheet.cell(row_index, 24).value,'ft', ft3b,  sheet.cell(row_index, 27).value, 'ft', ft4b,  sheet.cell(row_index,30).value, sheet.cell(row_index,39).value 
  except: 
    print "Err"

