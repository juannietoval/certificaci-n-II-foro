# -*- coding: utf-8 -*-
import os
import re
import json
import html
import subprocess
import pymupdf

BASE = r"c:\Users\Lenovo\Desktop\Juan\sistema_certificados"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BROWSER = CHROME if os.path.exists(CHROME) else EDGE
BASE_WEB_URL = "https://juannietoval.github.io/certificaci-n-II-foro"

# OFFICIAL EVENT DEFAULTS
DEFAULT_EVENT_TITLE = "II FORO DE EDITORES DE REVISTAS CIENTÍFICAS"
DEFAULT_EVENT_SUBTITLE = "Gestión editorial en tiempos de inteligencia artificial"
DEFAULT_FECHA = "Viernes 11 de septiembre de 2026"
DEFAULT_HORARIO = "8:00 a. m. a 12:00 m. (hora Colombia)"
DEFAULT_INTENSIDAD = "4 horas"
DEFAULT_MODALIDAD = "Virtual"
DEFAULT_CIUDAD = "Pereira, Colombia"
DEFAULT_INSTITUCION = ""

def clean_val(val, default=""):
    if val is None:
        return default
    text = str(val).strip()
    return html.escape(text)

def format_doc(doc_str):
    if not doc_str:
        return ""
    s = str(doc_str).strip()
    upper_s = s.upper()
    prefixes = ("C.C.", "CC", "D.I.", "DI", "DNI", "PASAPORTE", "PAS.", "PAS", "C.E.", "CE", "C.I.", "CI", "INE", "DUI", "CURP", "CREDENCIAL")
    for pfx in prefixes:
        if upper_s.startswith(pfx):
            return s
    if s.isdigit():
        num = int(s)
        return f"C.C. {num:,}".replace(",", ".")
    return f"D.I. {s}"

def format_title_display(titulo):
    """Preserve mixed-case acronyms; convert ALL-CAPS titles to sentence case."""
    if not titulo:
        return ""
    if titulo.isupper():
        parts = titulo.split(": ")
        result = []
        for i, part in enumerate(parts):
            result.append(part[0].upper() + part[1:].lower() if len(part) > 1 else part.upper())
        return ": ".join(result)
    return titulo

def safe_filename(name):
    """Sanitize string for cross-platform safe filenames."""
    # Replace spaces with underscores and remove problematic punctuation
    s = re.sub(r'[\/\\:\*\?"<>\|]', '', name)
    s = re.sub(r'\s+', '_', s.strip())
    return s

def generate_all():
    template_ponente_path = os.path.join(BASE, "templates", "master_template.html")
    with open(template_ponente_path, "r", encoding="utf-8") as f:
        template_ponente = f.read()

    template_asistente_path = os.path.join(BASE, "templates", "master_asistente_template.html")
    with open(template_asistente_path, "r", encoding="utf-8") as f:
        template_asistente = f.read()

    data_path = os.path.join(BASE, "data", "participantes.json")
    with open(data_path, "r", encoding="utf-8") as f:
        participantes = json.load(f)

    web_certs = []

    for p in participantes:
        cert_id = p["id"]
        nombre = p["nombre"]
        clean_name = safe_filename(nombre)
        rol = p.get("rol", "PONENTE").upper()
        qr_url = f"{BASE_WEB_URL}/?id={cert_id}"

        fecha = p.get("fecha", DEFAULT_FECHA)
        horario = p.get("horario", DEFAULT_HORARIO)
        modalidad = p.get("modalidad", DEFAULT_MODALIDAD)
        ciudad = p.get("ciudad", DEFAULT_CIUDAD)
        institucion = p.get("institucion", DEFAULT_INSTITUCION)

        pdf_rel = f"output/pdf/{cert_id}_{clean_name}.pdf"
        preview_rel = f"output/preview/{cert_id}_preview.png"

        if rol == "ASISTENTE":
            cert_html = template_asistente
            doc_line = format_doc(p.get("cedula", ""))
            intensidad = p.get("intensidad", DEFAULT_INTENSIDAD)
            horario = p.get("horario", DEFAULT_HORARIO)
            ciudad_disp = f"{ciudad} (Modalidad {modalidad})" if modalidad else ciudad
            location_date = f"{ciudad_disp} &mdash; {clean_val(fecha)}"

            cert_html = cert_html.replace("{{ID}}", cert_id)
            cert_html = cert_html.replace("{{NOMBRE}}", clean_val(nombre))
            cert_html = cert_html.replace("{{DOCUMENTO_LINE}}", clean_val(doc_line))
            cert_html = cert_html.replace("{{ROL}}", "ASISTENTE")
            cert_html = cert_html.replace("{{INTENSIDAD}}", clean_val(intensidad))
            cert_html = cert_html.replace("{{HORARIO}}", clean_val(horario))
            if institucion:
                aff_block = f'<div class="affiliation">{clean_val(institucion)}</div>'
            else:
                aff_block = ''
            cert_html = cert_html.replace("{{AFFILIATION_BLOCK}}", aff_block)
            cert_html = cert_html.replace("{{LOCATION_DATE}}", location_date)
            cert_html = cert_html.replace("{{COORDINACION}}", clean_val(p.get("coordinacion", "Comité Organizador")))
            cert_html = cert_html.replace("{{QR_URL}}", qr_url)
        else:
            cert_html = template_ponente
            doc_line = format_doc(p.get("cedula", ""))
            intensidad = p.get("intensidad", DEFAULT_INTENSIDAD)
            horario = p.get("horario", DEFAULT_HORARIO)
            ciudad_disp = f"{ciudad} (Modalidad {modalidad})" if modalidad else ciudad
            location_date = f"{ciudad_disp} &mdash; {clean_val(fecha)}"
            titulo_raw = p.get("titulo", "")
            titulo_display = format_title_display(titulo_raw)

            cert_html = cert_html.replace("{{ID}}", cert_id)
            cert_html = cert_html.replace("{{NOMBRE}}", clean_val(nombre))
            if doc_line:
                doc_block = f'<div class="doc-line">{clean_val(doc_line)}</div>'
            else:
                doc_block = ''
            cert_html = cert_html.replace("{{DOCUMENTO_LINE}}", doc_block)
            cert_html = cert_html.replace("{{ROL}}", clean_val(p.get("rol", "PONENTE")))
            cert_html = cert_html.replace("{{TITULO}}", clean_val(titulo_display))
            cert_html = cert_html.replace("{{EJE}}", clean_val(p.get("eje", "")))
            cert_html = cert_html.replace("{{INTENSIDAD}}", clean_val(intensidad))
            cert_html = cert_html.replace("{{HORARIO}}", clean_val(horario))
            cert_html = cert_html.replace("{{INSTITUCION}}", clean_val(institucion))
            cert_html = cert_html.replace("{{PAIS}}", clean_val(p.get("pais", "")))
            cert_html = cert_html.replace("{{LOCATION_DATE}}", location_date)
            cert_html = cert_html.replace("{{COORDINACION}}", clean_val(p.get("coordinacion", "Comité Organizador")))
            cert_html = cert_html.replace("{{QR_URL}}", qr_url)

        # Write HTML for individual cert
        html_file = os.path.abspath(os.path.join(BASE, "templates", f"{cert_id}.html"))
        with open(html_file, "w", encoding="utf-8") as f_out:
            f_out.write(cert_html)

        # Generate PDF
        pdf_file = os.path.abspath(os.path.join(BASE, pdf_rel))
        cmd_pdf = [
            BROWSER,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_file}",
            f"file:///{html_file}"
        ]
        subprocess.run(cmd_pdf, capture_output=True, text=True)

        # Generate PNG preview (150 DPI)
        png_file = os.path.abspath(os.path.join(BASE, preview_rel))
        try:
            doc = pymupdf.open(pdf_file)
            page = doc[0]
            pix = page.get_pixmap(dpi=150)
            pix.save(png_file)
            doc.close()
        except Exception as e:
            print(f"Warning: Could not render PDF preview with PyMuPDF: {e}")

        # Record for index.html dataset
        record = dict(p)
        record["pdf"] = pdf_rel
        record["preview"] = preview_rel
        web_certs.append(record)

        print(f"[OK] {cert_id} - {nombre} -> {pdf_rel}")

    # Update index.html embedded dataset
    update_index_html(web_certs)

def update_index_html(web_certs):
    index_path = os.path.join(BASE, "index.html")
    if not os.path.exists(index_path):
        return

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    json_str = json.dumps(web_certs, ensure_ascii=False, indent=6)
    pattern = r"const DEFAULT_CERTS = \[.*?\];"
    replacement = f"const DEFAULT_CERTS = {json_str};"

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Successfully updated index.html with {len(web_certs)} certificates!")

if __name__ == "__main__":
    generate_all()
