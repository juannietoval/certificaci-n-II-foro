import os, json

root = r'c:\Users\Lenovo\Desktop\Juan\sistema_certificados'
json_path = os.path.join(root, 'data', 'participantes.json')

with open(json_path, 'r', encoding='utf-8') as f:
    participantes = json.load(f)

print(f"Auditing documents for all {len(participantes)} participants...")

for p in participantes:
    cert_id = p.get('id')
    nombre = p.get('nombre')
    cedula = p.get('cedula')
    tipo_doc = p.get('tipo_doc', '')
    doc_raw = p.get('doc_raw', '')
    pais = p.get('pais', '') or p.get('pais_ciudad', '')
    
    # Check if foreign country has C.C.
    is_colombia = 'colombia' in str(pais).lower()
    has_cc = str(cedula).startswith('C.C.')
    
    # Flags
    issues = []
    if has_cc and not is_colombia and pais:
        issues.append(f"Foreign country '{pais}' but document labeled as '{cedula}' (raw: '{tipo_doc}' '{doc_raw}')")
    
    # Check if doc_raw doesn't match numbers in cedula
    clean_raw = "".join(c for c in str(doc_raw) if c.isalnum())
    clean_ced = "".join(c for c in str(cedula) if c.isalnum())
    if clean_raw and clean_raw.lower() not in clean_ced.lower() and clean_ced.lower() not in clean_raw.lower():
        issues.append(f"Raw doc '{doc_raw}' does not match formatted cedula '{cedula}'")

    if issues:
        print(f"\n[{cert_id}] {nombre} ({pais}):")
        for iss in issues:
            print(f"   -> {iss}")
