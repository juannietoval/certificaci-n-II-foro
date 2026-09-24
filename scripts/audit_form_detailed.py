import os, glob, openpyxl, json

root = r'c:\Users\Lenovo\Desktop\Juan'
asist_file = glob.glob(os.path.join(root, '*Registro de Asistencia*.xlsx'))[0]
wb_asist = openpyxl.load_workbook(asist_file)
ws_asist = wb_asist.active
asist_rows = list(ws_asist.iter_rows(values_only=True))[1:]

json_path = os.path.join(root, 'sistema_certificados', 'data', 'participantes.json')
with open(json_path, 'r', encoding='utf-8') as f:
    participantes = json.load(f)

print(f"Total rows in Asistencia form: {len(asist_rows)}")
print(f"Total records in participantes.json: {len(participantes)}")

# Build lookup by email and by raw doc
p_by_email = {}
p_by_doc = {}
p_by_name = {}

for p in participantes:
    em = (p.get('email') or '').strip().lower()
    if em:
        p_by_email[em] = p
    doc = str(p.get('doc_raw') or '').strip().lower()
    if doc:
        p_by_doc[doc] = p
    # also normalized name
    nm = "".join(c for c in p.get('nombre', '').lower() if c.isalnum())
    p_by_name[nm] = p

print("\n--- DETAILED STATUS OF EVERY FORM RESPONSE ---")
stats = {
    'asistente_ok': 0,
    'ponente_ok': 0,
    'duplicate_skipped': 0,
    'special_case': 0,
    'unmatched': 0
}

seen_form_emails = {}

for idx, r in enumerate(asist_rows, start=2):
    email = str(r[1] or '').strip().lower()
    raw_name = str(r[2] or '').strip()
    tipo_doc = str(r[3] or '').strip()
    raw_doc = str(r[4] or '').strip()
    if raw_doc.endswith('.0'):
        raw_doc = raw_doc[:-2]
    inst = str(r[5] or '').strip()
    pais = str(r[6] or '').strip()
    rol_form = str(r[7] or '').strip()

    # Is it duplicate?
    if email in seen_form_emails:
        prev_row = seen_form_emails[email]
        print(f"Row {idx:3d}: [DUPLICADO OMITIDO] {raw_name} ({email}) -> Ya registrado en Fila {prev_row}")
        stats['duplicate_skipped'] += 1
        continue
    else:
        seen_form_emails[email] = idx

    # Match in participantes
    matched_p = None
    match_reason = ""
    if email in p_by_email:
        matched_p = p_by_email[email]
        match_reason = "Email"
    elif raw_doc and raw_doc.lower() in p_by_doc:
        matched_p = p_by_doc[raw_doc.lower()]
        match_reason = "Documento"
    else:
        norm_nm = "".join(c for c in raw_name.lower() if c.isalnum())
        if norm_nm in p_by_name:
            matched_p = p_by_name[norm_nm]
            match_reason = "Nombre"

    if matched_p:
        p_id = matched_p.get('id')
        p_rol = matched_p.get('rol')
        p_nom = matched_p.get('nombre')
        p_doc = matched_p.get('cedula')
        
        if p_rol == 'PONENTE':
            stats['ponente_ok'] += 1
            print(f"Row {idx:3d}: [PONENTE {p_id}] {p_nom} (Form: '{raw_name}') | Doc: {p_doc} | Email: {email}")
        else:
            stats['asistente_ok'] += 1
            # Check for any discrepancies in doc, name, inst
            discrepancy = []
            if raw_name.lower() != p_nom.lower():
                discrepancy.append(f"Nombre en form '{raw_name}' -> certificado '{p_nom}'")
            if raw_doc and raw_doc not in str(p_doc):
                discrepancy.append(f"Doc en form '{raw_doc}' vs cert '{p_doc}'")
            
            if discrepancy:
                print(f"Row {idx:3d}: [ASISTENTE {p_id}] {p_nom} (Coincidencia {match_reason}) -> Discrepancias: {'; '.join(discrepancy)}")
    else:
        stats['unmatched'] += 1
        print(f"Row {idx:3d}: [NO ENCONTRADO EN CERTIFICADOS] {raw_name} | Doc: {tipo_doc} {raw_doc} | Inst: {inst} | Email: {email}")

print("\n--- RESUMEN DE CONCILIACIÓN FORMULARIO ASISTENCIA ---")
for k, v in stats.items():
    print(f"{k}: {v}")
print(f"Total procesadas: {sum(stats.values())} (debería ser {len(asist_rows)})")
