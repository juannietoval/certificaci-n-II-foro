import os
import json
import openpyxl

BASE = r"c:\Users\Lenovo\Desktop\Juan\sistema_certificados"

new_emails = {
    "FORO26-PON-003": "jorgehhoyos@gmail.com",       # Jorge Hernán Hoyos Rentería
    "FORO26-PON-006": "erbetancourt@utp.edu.co",      # Erika Betancourt
    "FORO26-PON-008": "ksantiana@bolivariano.edu.ec"  # Katherine Santiana Rosado
}

# 1. Update data/participantes.json
json_path = os.path.join(BASE, "data", "participantes.json")
with open(json_path, "r", encoding="utf-8") as f:
    participantes = json.load(f)

for p in participantes:
    if p["id"] in new_emails:
        p["email"] = new_emails[p["id"]]
        print(f"Updated JSON for {p['id']} ({p['nombre']}): {p['email']}")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(participantes, f, ensure_ascii=False, indent=2)

# 2. Update master Excel registro_certificados_foro_2026.xlsx
excel_master = os.path.join(BASE, "registro_certificados_foro_2026.xlsx")
wb_m = openpyxl.load_workbook(excel_master)
ws_m = wb_m["Ponentes"]
for row in ws_m.iter_rows(min_row=2):
    cid = row[0].value
    if cid in new_emails:
        row[8].value = new_emails[cid]
        print(f"Updated Master Excel Ponentes for {cid}: {new_emails[cid]}")
wb_m.save(excel_master)

# 3. Update piloto_envio_ponentes.xlsx in both locations
for path in [
    os.path.join(BASE, "piloto_envio_ponentes.xlsx"),
    r"c:\Users\Lenovo\Desktop\Juan\piloto_envio_ponentes.xlsx"
]:
    if os.path.exists(path):
        wb_p = openpyxl.load_workbook(path)
        ws_p = wb_p["Piloto_Ponentes"]
        for row in ws_p.iter_rows(min_row=2):
            cid = row[0].value
            if cid in new_emails:
                row[4].value = new_emails[cid] # Column 5: Correo Real del Ponente
                # If it's Erika Betancourt, configure the special destination
                if cid == "FORO26-PON-006":
                    # Keep Correo Envío Piloto as Juan or her email if requested
                    pass
        wb_p.save(path)
        print(f"Updated {path} successfully!")

# 4. Update index.html DEFAULT_CERTS
html_path = os.path.join(BASE, "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

start_marker = "const DEFAULT_CERTS = ["
start_idx = html_content.find(start_marker)
end_idx = html_content.find("];", start_idx)
if start_idx != -1 and end_idx != -1:
    json_formatted = json.dumps(participantes, ensure_ascii=False, indent=6)
    new_certs_block = f"const DEFAULT_CERTS = {json_formatted}"
    updated_html = html_content[:start_idx] + new_certs_block + html_content[end_idx + 1:]
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(updated_html)
    print("Updated index.html DEFAULT_CERTS successfully!")

print("\nAll database and Excel records updated!")
