import os, glob, openpyxl, json

root = r'c:\Users\Lenovo\Desktop\Juan'
prog_file = glob.glob(os.path.join(root, '*Programacion*.xlsx'))[0]
asist_file = glob.glob(os.path.join(root, '*Registro de Asistencia*.xlsx'))[0]

wb_prog = openpyxl.load_workbook(prog_file)
wb_asist = openpyxl.load_workbook(asist_file)

ws_prog = wb_prog['Programa ponencias']
ws_asist = wb_asist.active

json_path = os.path.join(root, 'sistema_certificados', 'data', 'participantes.json')
with open(json_path, 'r', encoding='utf-8') as f:
    participantes = json.load(f)

asist_rows = list(ws_asist.iter_rows(values_only=True))[1:]

print("=== CHECKING ALL PARTICIPANTES AGAINST RAW EXCEL ===")
discrepancies = []

for p in participantes:
    cert_id = p.get('id')
    rol = p.get('rol')
    p_name = p.get('nombre')
    p_doc = p.get('cedula')
    p_inst = p.get('institucion')
    p_email = p.get('email')
    
    if rol == 'PONENTE':
        # Check against Programacion or Asistencia
        # Find if name appears in Programacion
        found_in_prog = False
        for r in ws_prog.iter_rows(values_only=True):
            row_str = " ".join([str(c) for c in r if c])
            # Check last name or first name
            for token in p_name.split():
                if len(token) > 4 and token.lower() in row_str.lower():
                    found_in_prog = True
                    break
            if found_in_prog:
                break
        
        # Also check if they submitted Asistencia form
        found_in_asist = False
        asist_match = None
        for ar in asist_rows:
            ar_name = str(ar[2] or '')
            for token in p_name.split():
                if len(token) > 4 and token.lower() in ar_name.lower():
                    found_in_asist = True
                    asist_match = ar
                    break
            if found_in_asist:
                break
                
        print(f"\nPONENTE {cert_id}: {p_name}")
        print(f"   In Programacion: {found_in_prog} | In Asistencia form: {found_in_asist}")
        if asist_match:
            print(f"   Form Name: {asist_match[2]} | Form Doc: {asist_match[3]} {asist_match[4]} | Email: {asist_match[1]}")
            print(f"   JSON Doc: {p_doc} | JSON Email: {p_email}")
        else:
            print(f"   No form submitted. JSON Doc: {p_doc} | JSON Email: {p_email}")

    elif rol == 'ASISTENTE':
        # Find corresponding row in Asistencia form
        # We can match by email, doc_raw, or name
        match = None
        for ar in asist_rows:
            form_email = str(ar[1] or '').strip().lower()
            form_name = str(ar[2] or '').strip()
            form_doc = str(ar[4] or '').strip()
            if form_email and form_email == (p_email or '').strip().lower():
                match = ar
                break
            # Or match by doc
            if p.get('doc_raw') and p.get('doc_raw') in form_doc:
                match = ar
                break
            # Or match by name
            if p_name.lower() in form_name.lower() or form_name.lower() in p_name.lower():
                match = ar
                break
        
        if not match:
            discrepancies.append((cert_id, p_name, "NOT FOUND IN RAW ASISTENCIA FORM!"))
        else:
            form_name = str(match[2] or '').strip()
            form_tipo_doc = str(match[3] or '').strip()
            form_doc = str(match[4] or '').strip()
            form_inst = str(match[5] or '').strip()
            form_pais = str(match[6] or '').strip()
            form_email = str(match[1] or '').strip()
            
            # Check name difference
            if p_name.lower() != form_name.lower():
                discrepancies.append((cert_id, "NAME_DIFF", f"JSON: '{p_name}' vs FORM: '{form_name}' (Email: {form_email})"))
            
            # Check doc
            # Did JSON invent or alter doc?
            # Check institution
            if p_inst != form_inst and (p_inst or form_inst):
                discrepancies.append((cert_id, "INST_DIFF", f"JSON: '{p_inst}' vs FORM: '{form_inst}'"))

print("\n\n=== DISCREPANCIES FOUND IN ASISTENTES ===")
for d in discrepancies:
    print(d)
