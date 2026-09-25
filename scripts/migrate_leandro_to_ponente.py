import os
import json
import re

BASE = r"c:\Users\Lenovo\Desktop\Juan\sistema_certificados"
json_path = os.path.join(BASE, "data", "participantes.json")

with open(json_path, "r", encoding="utf-8") as f:
    participantes = json.load(f)

# Separate existing ponentes and asistentes
ponentes = [p for p in participantes if p.get("rol") == "PONENTE"]
asistentes = [p for p in participantes if p.get("rol") == "ASISTENTE"]

print(f"Initial: {len(ponentes)} Ponentes, {len(asistentes)} Asistentes")

# Find Leandro in asistentes
leandro = None
new_asistentes = []
for a in asistentes:
    if "ceballos" in a.get("nombre", "").lower():
        leandro = a
    else:
        new_asistentes.append(a)

if not leandro:
    raise ValueError("Leandro Ceballos not found in asistentes!")

print(f"Found Leandro: {leandro['nombre']}, doc: {leandro['cedula']}")

# Convert Leandro to Ponente
leandro_ponente = {
    "id": "FORO26-PON-013",
    "nombre": "Leandro Ceballos Henao",
    "cedula": leandro.get("cedula", "C.C. 1.039.447.159"),
    "rol": "PONENTE",
    "titulo": "Publicación científica para todas las personas: accesibilidad e inclusividad como criterios de calidad editorial",
    "eje": "Ética y buenas prácticas editoriales",
    "institucion": "Corporación Universitaria Minuto de Dios - UNIMINUTO",
    "pais": "Colombia",
    "intensidad": "4 horas",
    "modalidad": "Virtual",
    "fecha": "Viernes 11 de septiembre de 2026",
    "horario": "8:00 a. m. a 12:00 m. (hora Colombia)",
    "ciudad": "Pereira, Colombia",
    "email": "tiflo.ceballos@gmail.com",
    "pdf": "output/pdf/FORO26-PON-013_Leandro_Ceballos_Henao.pdf",
    "preview": "output/preview/FORO26-PON-013_preview.png",
    "archivo_carpeta": "certificados/ponentes/certificado - Leandro Ceballos Henao.pdf"
}

ponentes.append(leandro_ponente)

# Renumber new_asistentes from 1 to len(new_asistentes)
def clean_filename(name):
    s = re.sub(r'[\/\\:\*\?"<>\|]', '', name)
    return re.sub(r'\s+', '_', s.strip())

for idx, a in enumerate(new_asistentes, start=1):
    new_id = f"FORO26-ASI-{idx:03d}"
    a["id"] = new_id
    nom = a["nombre"]
    safe_nm = clean_filename(nom)
    a["pdf"] = f"output/pdf/{new_id}_{safe_nm}.pdf"
    a["preview"] = f"output/preview/{new_id}_preview.png"
    a["archivo_carpeta"] = f"certificados/asistentes/certificado - {nom}.pdf"

# Combine back
all_updated = ponentes + new_asistentes
print(f"Updated: {len(ponentes)} Ponentes (001-013), {len(new_asistentes)} Asistentes (001-101). Total: {len(all_updated)}")

# Save to participantes.json
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(all_updated, f, ensure_ascii=False, indent=2)

print("Saved updated participantes.json successfully!")
