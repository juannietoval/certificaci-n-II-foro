import os, glob, openpyxl

root = r'c:\Users\Lenovo\Desktop\Juan'
asist_file = glob.glob(os.path.join(root, '*Registro de Asistencia*.xlsx'))[0]
wb = openpyxl.load_workbook(asist_file)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))

target_rows = [62, 70, 87, 95, 100, 101, 104, 113]
for tr in target_rows:
    r = rows[tr - 1] # 1-indexed row in Excel
    print(f"\n--- EXCEL ROW {tr} ---")
    print(f"Timestamp: {r[0]}")
    print(f"Email: {r[1]}")
    print(f"Name: {r[2]}")
    print(f"Tipo Doc: {r[3]}")
    print(f"Num Doc: {r[4]}")
    print(f"Institucion: {r[5]}")
    print(f"Pais/Ciudad: {r[6]}")
    print(f"Rol: {r[7]}")
