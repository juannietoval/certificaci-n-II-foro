# -*- coding: utf-8 -*-
import json
import re

def title_case_name(name):
    if not name:
        return ""
    lowers = {'de', 'del', 'la', 'las', 'el', 'los', 'y', 'e', 'en', 'da', 'do', 'dos'}
    
    custom_fixes = {
        'MARIA ESTER GONZALEZ': 'María Ester González',
        'CAMILO CORCHUELO': 'Camilo Corchuelo',
        'ENRIQUE BLANCARTE FUENTES': 'Enrique Blancarte Fuentes',
        'MARIA GUADALUPE RODRIGUEZ OLIVA': 'María Guadalupe Rodríguez Oliva',
        'CORINA ECHAVARRIA': 'Corina Echavarría',
        'BERTHA JACQUELINE CONTLA RAMIREZ': 'Bertha Jacqueline Contla Ramírez',
        'MARCELINA SOYDETH JIMENEZ AVILA': 'Marcelina Soydeth Jiménez Ávila',
        'THAILING NUNEZ BETANCOURT': 'Thailing Núñez Betancourt',
        'BAYRON STEVEN LOPEZ JAUREUI': 'Bayron Steven López Jáuregui',
        'Fabiola Nez Pastrana': 'Fabiola Núñez Pastrana',
        'Fabiola N?ez Pastrana': 'Fabiola Núñez Pastrana'
    }
    
    clean_n = re.sub(r'\s+', ' ', name).strip()
    if clean_n in custom_fixes:
        return custom_fixes[clean_n]
    if clean_n.upper() in custom_fixes:
        return custom_fixes[clean_n.upper()]
        
    if clean_n.isupper():
        words = clean_n.split()
        res = []
        for i, w in enumerate(words):
            wl = w.lower()
            if i > 0 and wl in lowers:
                res.append(wl)
            else:
                res.append(w.capitalize())
        return " ".join(res)
    return clean_n

def format_doc_asistente(tipo_doc, doc_str):
    if not doc_str:
        return ""
    s = str(doc_str).strip()
    if s.upper() in ('NA', 'N/A', 'NONE', 'NO', '-', '.', ''):
        return ""
        
    upper_s = s.upper()
    
    # Specific known formats
    if upper_s.startswith("IDMEX"):
        return f"INE {s}"
        
    prefixes = ("C.C.", "CC", "D.I.", "DI", "DNI", "PASAPORTE", "PAS.", "PAS", "C.E.", "CE", "C.I.", "CI", "INE", "CURP", "RUT")
    for pfx in prefixes:
        if upper_s.startswith(pfx):
            return s
            
    upper_td = str(tipo_doc or '').upper()
    if 'CIUDADAN' in upper_td or 'C.C' in upper_td:
        if s.isdigit():
            num = int(s)
            return f"C.C. {num:,}".replace(",", ".")
        return f"C.C. {s}"
    elif 'EXTRANJER' in upper_td or 'C.E' in upper_td:
        return f"C.E. {s}"
    elif 'IDENTIDAD' in upper_td or 'C.I' in upper_td or 'DNI' in upper_td:
        if 'DNI' in upper_td:
            return f"DNI {s}"
        return f"C.I. {s}"
    elif 'PASAPORTE' in upper_td:
        return f"Pasaporte {s}"
    elif 'INE' in upper_td:
        return f"INE {s}"
        
    if s.isdigit():
        num = int(s)
        return f"C.C. {num:,}".replace(",", ".")
    return f"D.I. {s}"

with open(r'c:\Users\Lenovo\Desktop\Juan\sistema_certificados\data\asistentes_raw.json', 'r', encoding='utf-8') as f:
    attendees = json.load(f)

lines = []
for i, a in enumerate(attendees):
    nm_formatted = title_case_name(a['nombre'])
    doc_formatted = format_doc_asistente(a['tipo_doc'], a['doc'])
    inst = a['institucion'].strip()
    pc = a['pais_ciudad'].strip()
    lines.append(f"{i+1:3d}. FORO26-ASI-{i+1:03d} | {nm_formatted} | Doc: {doc_formatted} | {inst} | {pc}")

with open(r'c:\Users\Lenovo\Desktop\Juan\sistema_certificados\data\audit_102_asistentes.txt', 'w', encoding='utf-8') as f_out:
    f_out.write("\n".join(lines))

print(f"Written all {len(lines)} records to audit_102_asistentes.txt!")
