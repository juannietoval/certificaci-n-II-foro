import os
import json
import pymupdf

BASE = r"c:\Users\Lenovo\Desktop\Juan\sistema_certificados"
json_path = os.path.join(BASE, "data", "participantes.json")

with open(json_path, "r", encoding="utf-8") as f:
    participantes = json.load(f)

asistentes = [p for p in participantes if p.get("rol") == "ASISTENTE"]
print(f"Total Asistentes in DB: {len(asistentes)}")

missing_pdf_output = []
missing_pdf_carpeta = []
missing_preview = []
corrupted_pdf = []
missing_email = []
doc_issues = []

for idx, a in enumerate(asistentes, 1):
    cid = a["id"]
    nom = a["nombre"]
    em = a.get("email", "")
    pdf_rel = a.get("pdf", "")
    preview_rel = a.get("preview", "")
    carpeta_rel = a.get("archivo_carpeta", "")
    
    # 1. Email check
    if not em or "@" not in em:
        missing_email.append((cid, nom, em))
        
    # 2. PDF output check
    pdf_path = os.path.join(BASE, pdf_rel)
    if not os.path.exists(pdf_path):
        missing_pdf_output.append((cid, nom, pdf_path))
    else:
        # Check integrity
        try:
            doc = pymupdf.open(pdf_path)
            if len(doc) == 0:
                corrupted_pdf.append((cid, nom, "0 pages"))
            else:
                txt = doc[0].get_text()
                if "ASISTENTE" not in txt and "asistencia" not in txt.lower():
                    corrupted_pdf.append((cid, nom, "Text does not contain ASISTENTE"))
        except Exception as e:
            corrupted_pdf.append((cid, nom, str(e)))

    # 3. PDF carpeta check
    carpeta_path = os.path.join(BASE, carpeta_rel)
    if not os.path.exists(carpeta_path):
        missing_pdf_carpeta.append((cid, nom, carpeta_path))
        
    # 4. Preview check
    prev_path = os.path.join(BASE, preview_rel)
    if not os.path.exists(prev_path):
        missing_preview.append((cid, nom, prev_path))

print("\n=== AUDIT RESULTS ===")
print(f"1. Asistentes with missing or invalid email: {len(missing_email)}")
for m in missing_email:
    print(f"   -> {m}")

print(f"2. Missing PDFs in output/pdf/: {len(missing_pdf_output)}")
for m in missing_pdf_output:
    print(f"   -> {m}")

print(f"3. Missing PDFs in certificados/asistentes/: {len(missing_pdf_carpeta)}")
for m in missing_pdf_carpeta:
    print(f"   -> {m}")

print(f"4. Missing Preview PNGs in output/preview/: {len(missing_preview)}")
for m in missing_preview:
    print(f"   -> {m}")

print(f"5. Corrupted or unreadable PDFs: {len(corrupted_pdf)}")
for m in corrupted_pdf:
    print(f"   -> {m}")
