import os, glob, openpyxl, json
from collections import Counter

root = r'c:\Users\Lenovo\Desktop\Juan'
prog_file = glob.glob(os.path.join(root, '*Programacion*.xlsx'))[0]
asist_file = glob.glob(os.path.join(root, '*Registro de Asistencia*.xlsx'))[0]

wb_prog = openpyxl.load_workbook(prog_file)
wb_asist = openpyxl.load_workbook(asist_file)

# 1. Inspect Programacion
print("=== PROGRAMACION SHEETS DETAIL ===")
for sname in wb_prog.sheetnames:
    ws = wb_prog[sname]
    print(f"\n--- Sheet: {sname} ---")
    for r in ws.iter_rows(values_only=True):
        if any(r):
            print(r)

# 2. Inspect Asistencia
print("\n=== ASISTENCIA DETAIL ===")
ws_asist = wb_asist.active
asist_rows = list(ws_asist.iter_rows(values_only=True))
header = asist_rows[0]
data_rows = asist_rows[1:]
print(f"Total response rows in Asistencia form: {len(data_rows)}")

# Roles declared in Asistencia
roles_declared = [r[7] for r in data_rows]
print("Roles declared in form:", Counter(roles_declared))

# Duplicates by email or doc or name
emails = [str(r[1]).strip().lower() if r[1] else '' for r in data_rows]
docs = [str(r[4]).strip() if r[4] else '' for r in data_rows]
names = [str(r[2]).strip().lower() if r[2] else '' for r in data_rows]

print("\nDuplicate emails in Asistencia:")
for email, count in Counter(emails).items():
    if count > 1 and email:
        print(f"  {email}: {count}")

print("\nDuplicate docs in Asistencia:")
for doc, count in Counter(docs).items():
    if count > 1 and doc:
        print(f"  {doc}: {count}")

print("\nDuplicate names in Asistencia:")
for name, count in Counter(names).items():
    if count > 1 and name:
        print(f"  {name}: {count}")
