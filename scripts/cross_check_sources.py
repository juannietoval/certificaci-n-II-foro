import os, glob, openpyxl, json

root = r'c:\Users\Lenovo\Desktop\Juan'
prog_file = glob.glob(os.path.join(root, '*Programacion*.xlsx'))[0]
asist_file = glob.glob(os.path.join(root, '*Registro de Asistencia*.xlsx'))[0]
master_file = os.path.join(root, 'sistema_certificados', 'registro_certificados_foro_2026.xlsx')
json_path = os.path.join(root, 'sistema_certificados', 'data', 'participantes.json')

with open(json_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

wb_master = openpyxl.load_workbook(master_file)
ws_master_pon = wb_master['Ponentes']
ws_master_asi = wb_master['Asistentes']

wb_asist = openpyxl.load_workbook(asist_file)
ws_asist = wb_asist.active
asist_rows = list(ws_asist.iter_rows(values_only=True))[1:]

print("=== CHECKING 12 PONENTES IN MASTER vs JSON vs SOURCE PROGRAM ===")
for r in list(ws_master_pon.iter_rows(values_only=True))[1:]:
    cert_id = r[0]
    nombre = r[1]
    doc = r[2]
    inst = r[3]
    pais = r[4]
    ponencia = r[5]
    eje = r[6]
    email = r[8]
    print(f"[{cert_id}] {nombre} | Doc: {doc} | Inst: {inst} | Pais: {pais} | Email: {email}")
    print(f"      Ponencia: {ponencia[:60]}... | Eje: {eje}")

print("\n=== PONENTES IN ASISTENCIA FORM? ===")
# Check which ponentes also submitted attendance form
for p_idx, r in enumerate(asist_rows):
    nombre_form = str(r[2]).strip()
    rol_form = str(r[7]).strip()
    email_form = str(r[1]).strip()
    doc_form = str(r[4]).strip()
    tipo_doc = str(r[3]).strip()
    if 'ponente' in rol_form.lower() or any(w in nombre_form.lower() for w in ['alfonzo', 'silano', 'hoyos', 'zarta', 'galvez', 'gonzalez', 'centeno', 'santiana', 'tolozano', 'orellana', 'ravelo', 'baron', 'betancourt']):
        print(f"Row {p_idx+2}: {nombre_form} | Rol: {rol_form} | Doc: {tipo_doc} {doc_form} | Email: {email_form}")

print("\n=== CHECKING ASISTENTES COUNT AND MASTER CONSISTENCY ===")
print(f"Master Asistentes rows: {ws_master_asi.max_row - 1}")
print(f"JSON Asistentes count: {len([p for p in json_data if p.get('rol') == 'ASISTENTE'])}")
