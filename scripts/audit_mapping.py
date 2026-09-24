import os, glob, openpyxl, json

root = r'c:\Users\Lenovo\Desktop\Juan'
asist_file = glob.glob(os.path.join(root, '*Registro de Asistencia*.xlsx'))[0]
wb_asist = openpyxl.load_workbook(asist_file)
ws_asist = wb_asist.active
asist_rows = list(ws_asist.iter_rows(values_only=True))[1:]

master_file = os.path.join(root, 'sistema_certificados', 'registro_certificados_foro_2026.xlsx')
wb_master = openpyxl.load_workbook(master_file)
master_asi = list(wb_master['Asistentes'].iter_rows(values_only=True))[1:]
master_pon = list(wb_master['Ponentes'].iter_rows(values_only=True))[1:]

master_asi_names = [str(r[1]).strip().lower() for r in master_asi]
master_pon_names = [str(r[1]).strip().lower() for r in master_pon]

print(f"Total raw form rows: {len(asist_rows)}")

# Track how each row in raw form maps
mapped_to_asi = []
mapped_to_pon = []
duplicate_in_form = []
unmapped = []

seen_emails = {}
seen_docs = {}

for idx, r in enumerate(asist_rows):
    row_num = idx + 2
    email = str(r[1]).strip().lower() if r[1] else ''
    name = str(r[2]).strip()
    tipo_doc = str(r[3]).strip()
    doc_num = str(r[4]).strip()
    inst = str(r[5]).strip()
    pais = str(r[6]).strip()
    rol = str(r[7]).strip()

    # Check duplicate
    is_dup = False
    if email in seen_emails:
        is_dup = True
        duplicate_in_form.append((row_num, name, email, f"Duplicate of row {seen_emails[email]}"))
    else:
        seen_emails[email] = row_num

    # Check if in ponentes
    is_pon = False
    for p_name in master_pon_names:
        if name.lower() in p_name or p_name in name.lower():
            is_pon = True
            break
    
    # Check if in asistentes
    is_asi = False
    for a_name in master_asi_names:
        if name.lower() in a_name or a_name in name.lower():
            is_asi = True
            break

    if is_pon and not is_dup:
        mapped_to_pon.append((row_num, name, email, rol))
    elif is_asi and not is_dup:
        mapped_to_asi.append((row_num, name, email, rol))
    elif not is_dup:
        unmapped.append((row_num, name, email, rol, inst, pais))

print(f"\nMapped to Asistentes: {len(mapped_to_asi)}")
print(f"Mapped to Ponentes: {len(mapped_to_pon)}")
for p in mapped_to_pon:
    print(f"   {p}")

print(f"Duplicates skipped: {len(duplicate_in_form)}")
for d in duplicate_in_form:
    print(f"   {d}")

print(f"Unmapped: {len(unmapped)}")
for u in unmapped:
    print(f"   {u}")
