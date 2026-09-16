# -*- coding: utf-8 -*-
import os
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
DEFAULT_HORARIO = "8:00 a 12:00 m. (hora Colombia)"
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
    if s.isdigit():
        num = int(s)
        return f"C.C. {num:,}".replace(",", ".")
    return f"Doc. {s}"

def title_case_ponencia(titulo):
    """Convert ALL CAPS title to sentence case for readability."""
    if not titulo:
        return ""
    # Convert to sentence case: first letter uppercase, rest lowercase
    # But preserve uppercase after colon
    parts = titulo.split(": ")
    result = []
    for i, part in enumerate(parts):
        if i == 0:
            result.append(part[0].upper() + part[1:].lower() if len(part) > 1 else part.upper())
        else:
            result.append(part[0].upper() + part[1:].lower() if len(part) > 1 else part.upper())
    return ": ".join(result)

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

    for p in participantes:
        cert_id = p["id"]
        nombre = p["nombre"]
        clean_name = nombre.replace(" ", "_")
        rol = p.get("rol", "PONENTE").upper()
        qr_url = f"{BASE_WEB_URL}/?id={cert_id}"

        fecha = p.get("fecha", DEFAULT_FECHA)
        horario = p.get("horario", DEFAULT_HORARIO)
        modalidad = p.get("modalidad", DEFAULT_MODALIDAD)
        ciudad = p.get("ciudad", DEFAULT_CIUDAD)
        institucion = p.get("institucion", DEFAULT_INSTITUCION)

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
            titulo_display = title_case_ponencia(titulo_raw)

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

        html_file = os.path.abspath(os.path.join(BASE, "templates", f"{cert_id}.html"))
        with open(html_file, "w", encoding="utf-8") as f_out:
            f_out.write(cert_html)

        pdf_file = os.path.abspath(os.path.join(BASE, "output", "pdf", f"{cert_id}_{clean_name}.pdf"))
        cmd_pdf = [
            BROWSER,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_file}",
            f"file:///{html_file}"
        ]
        subprocess.run(cmd_pdf, capture_output=True, text=True)

        png_file = os.path.abspath(os.path.join(BASE, "output", "preview", f"{cert_id}_preview.png"))
        try:
            doc = pymupdf.open(pdf_file)
            page = doc[0]
            pix = page.get_pixmap(dpi=150)
            pix.save(png_file)
            doc.close()
        except Exception as e:
            print(f"Warning: Could not render PDF preview with PyMuPDF: {e}")

        print(f"Generated Vector Certificate & Exact Preview: {cert_id} - {nombre}")

if __name__ == "__main__":
    generate_all()
