import os, glob, openpyxl, json

root = r'c:\Users\Lenovo\Desktop\Juan'
asist_file = glob.glob(os.path.join(root, '*Registro de Asistencia*.xlsx'))[0]
wb_asist = openpyxl.load_workbook(asist_file)
ws_asist = wb_asist.active
asist_rows = list(ws_asist.iter_rows(values_only=True))[1:]

json_path = os.path.join(root, 'sistema_certificados', 'data', 'participantes.json')
with open(json_path, 'r', encoding='utf-8') as f:
    participantes = json.load(f)

p_by_email = {p.get('email', '').strip().lower(): p for p in participantes if p.get('email')}

print("=== COMPARING NAMES: RAW FORM vs CERTIFICATE ===")
for r in asist_rows:
    em = str(r[1] or '').strip().lower()
    raw_name = str(r[2] or '').strip()
    if em in p_by_email:
        p = p_by_email[em]
        cert_name = p.get('nombre')
        # Normalize simple case & whitespace
        if raw_name.strip() != cert_name.strip():
            # Check if it's just title-case or accents added
            print(f"[{p.get('id')}] Raw: '{raw_name}'\n       Cert: '{cert_name}'\n       Email: {em}")
