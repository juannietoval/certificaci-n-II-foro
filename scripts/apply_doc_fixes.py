import os, json, openpyxl

root = r'c:\Users\Lenovo\Desktop\Juan\sistema_certificados'
json_path = os.path.join(root, 'data', 'participantes.json')

with open(json_path, 'r', encoding='utf-8') as f:
    participantes = json.load(f)

# Apply fixes to the specific records
fixes_count = 0
for p in participantes:
    cid = p.get('id')
    
    if cid == 'FORO26-ASI-059': # Itzel Miranda Lopez
        p['cedula'] = 'INE 2156919108'
        p['doc_raw'] = '2156919108'
        fixes_count += 1
        
    elif cid == 'FORO26-ASI-066': # Bertha Jacqueline Contla Ramirez
        p['cedula'] = 'INE 0069010511866'
        p['tipo_doc'] = 'Credencial para Votar (INE)'
        fixes_count += 1
        
    elif cid == 'FORO26-ASI-092': # Daniel Neftali Ramirez Salazar
        p['cedula'] = 'DUI 00707384-2'
        p['tipo_doc'] = 'DUI'
        fixes_count += 1
        
    elif cid == 'FORO26-ASI-094': # Napoleon Ernesto Lopez Espinoza
        p['cedula'] = 'DUI 01343533-7'
        p['tipo_doc'] = 'DUI'
        fixes_count += 1
        
    elif cid == 'FORO26-ASI-045': # Fatima Mayerli Fuentes
        p['cedula'] = 'DUI 06909511-9'
        p['tipo_doc'] = 'DUI'
        fixes_count += 1
        
    elif cid == 'FORO26-ASI-102': # Maria del Rosario Rodriguez Leon
        p['cedula'] = 'Credencial UNAM 826091'
        p['tipo_doc'] = 'Credencial Institucional UNAM'
        fixes_count += 1
        
    elif cid == 'FORO26-ASI-010': # Carlos Javier Lizcano Chapeta
        p['cedula'] = 'C.I. 1759650623'
        p['tipo_doc'] = 'Cédula de residente de Ecuador'
        fixes_count += 1

    elif cid == 'FORO26-ASI-095': # Ligia Marcela Lazo Majano
        p['cedula'] = 'DUI 01267274-0'
        fixes_count += 1

    elif cid == 'FORO26-ASI-096': # Mariela Vanessa Melendez Ascencio
        p['cedula'] = 'DUI 02300379-2'
        fixes_count += 1

    elif cid == 'FORO26-ASI-086': # Alain Garcia Penaloza
        p['cedula'] = 'CURP GRPLAL84090315H000'
        p['tipo_doc'] = 'CURP'
        fixes_count += 1

print(f"Applied {fixes_count} surgical fixes.")

# Save back to participantes.json
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(participantes, f, ensure_ascii=False, indent=2)
print("Updated participantes.json successfully.")
