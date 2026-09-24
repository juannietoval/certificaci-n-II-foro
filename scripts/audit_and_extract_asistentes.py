# -*- coding: utf-8 -*-
import openpyxl
import re
import json

excel_path = r'c:\Users\Lenovo\Desktop\Juan\Registro de Asistencia - II Foro de Editores de Revistas Científicas 2026 (respuestas).xlsx'
wb = openpyxl.load_workbook(excel_path)
ws = wb.active

ponente_emails = {
    'noheliay@gmail.com',
    'zahirasilano28@gmail.com',
    'fabian.zarta@uniminuto.edu',
    'fgalvez175@gmail.com',
    'profesorayeseniacenteno@gmail.com',
    'profe.reisner@gmail.com'
}

raw_rows = []
for r in range(2, ws.max_row + 1):
    timestamp = ws.cell(r, 1).value
    email = str(ws.cell(r, 2).value or '').strip()
    nombre = str(ws.cell(r, 3).value or '').strip()
    tipo_doc = str(ws.cell(r, 4).value or '').strip()
    doc_raw = str(ws.cell(r, 5).value or '').strip()
    institucion = str(ws.cell(r, 6).value or '').strip()
    pais_ciudad = str(ws.cell(r, 7).value or '').strip()
    rol = str(ws.cell(r, 8).value or '').strip()
    if doc_raw.endswith('.0'):
        doc_raw = doc_raw[:-2]
    
    # Exclude ponentes who registered in the attendance form
    if email.lower() in ponente_emails:
        continue
    
    # Handle known email in name anomaly (row 2)
    if '@' in nombre:
        nombre = 'Cristian Yasser Martínez Rodríguez'
        
    raw_rows.append({
        'row': r,
        'timestamp': timestamp,
        'email': email,
        'nombre': nombre,
        'tipo_doc': tipo_doc,
        'doc': doc_raw,
        'institucion': institucion,
        'pais_ciudad': pais_ciudad,
        'rol': rol
    })

# Deduplicate by email keeping the latest (most recent submission)
by_email = {}
for r in raw_rows:
    em = r['email'].lower()
    by_email[em] = r

unique_102 = list(by_email.values())
print(f"Total unique attendees: {len(unique_102)}")

# Check duplicate docs
doc_map = {}
for u in unique_102:
    d = u['doc']
    if d and d != 'None':
        doc_map.setdefault(d, []).append(u)

dup_docs = {k: v for k, v in doc_map.items() if len(v) > 1}
print(f"Duplicate docs among unique attendees: {len(dup_docs)}")
for d, rows in dup_docs.items():
    print(f"  Doc {d}:")
    for r in rows:
        print(f"    Row {r['row']}: {r['nombre']} ({r['email']})")

# Check duplicate names
name_map = {}
for u in unique_102:
    n = re.sub(r'\s+', ' ', u['nombre']).strip().lower()
    name_map.setdefault(n, []).append(u)

dup_names = {k: v for k, v in name_map.items() if len(v) > 1}
print(f"Duplicate names among unique attendees: {len(dup_names)}")
for n, rows in dup_names.items():
    print(f"  Name {n}:")
    for r in rows:
        print(f"    Row {r['row']}: {r['nombre']} ({r['email']})")

# Save the 102 attendees to json for review
with open(r'c:\Users\Lenovo\Desktop\Juan\sistema_certificados\data\asistentes_raw.json', 'w', encoding='utf-8') as f:
    json.dump(unique_102, f, ensure_ascii=False, indent=2, default=str)
print("Saved asistentes_raw.json successfully!")
