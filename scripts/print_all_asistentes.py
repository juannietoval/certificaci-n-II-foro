import os, json

root = r'c:\Users\Lenovo\Desktop\Juan\sistema_certificados'
json_path = os.path.join(root, 'data', 'participantes.json')

with open(json_path, 'r', encoding='utf-8') as f:
    participantes = json.load(f)

print(f"{'ID':15} | {'NOMBRE':32} | {'DOCUMENTO':24} | {'PAIS / CIUDAD':30} | {'INSTITUCION'}")
print("-" * 140)

for p in participantes:
    if p.get('rol') == 'ASISTENTE':
        cid = p.get('id')
        nom = p.get('nombre')
        doc = p.get('cedula')
        pais = p.get('pais_ciudad') or p.get('pais', '')
        inst = p.get('institucion', '')
        print(f"{cid:15} | {nom[:32]:32} | {doc[:24]:24} | {pais[:30]:30} | {inst[:40]}")
