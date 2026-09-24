import os, json

root = r'c:\Users\Lenovo\Desktop\Juan\sistema_certificados'
json_path = os.path.join(root, 'data', 'participantes.json')

with open(json_path, 'r', encoding='utf-8') as f:
    participantes = json.load(f)

print("=== CHECKING FOR ANY NULL, NONE, UNDEFINED OR EMPTY STRINGS ===")
for p in participantes:
    cid = p.get('id')
    rol = p.get('rol')
    nom = p.get('nombre')
    
    # Required fields for everyone
    for field in ['id', 'nombre', 'rol', 'fecha', 'ciudad']:
        val = p.get(field)
        if not val or val in ['None', 'null', 'undefined', 'NaN']:
            print(f"[{cid}] Missing required field '{field}': {repr(val)}")
            
    if rol == 'PONENTE':
        for field in ['titulo', 'eje', 'institucion', 'pais']:
            val = p.get(field)
            if not val or val in ['None', 'null', 'undefined', 'NaN']:
                print(f"[PONENTE {cid}] Missing field '{field}': {repr(val)}")
                
    if rol == 'ASISTENTE':
        for field in ['tema_central', 'intensidad', 'modalidad']:
            val = p.get(field)
            if not val or val in ['None', 'null', 'undefined', 'NaN']:
                print(f"[ASISTENTE {cid}] Missing field '{field}': {repr(val)}")

print("Verification done.")
