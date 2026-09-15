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

def clean_val(val, default=""):
    if val is None:
        return default
    text = str(val).strip()
    return html.escape(text)

def generate_all():
    template_path = os.path.join(BASE, "templates", "master_template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    data_path = os.path.join(BASE, "data", "participantes.json")
    with open(data_path, "r", encoding="utf-8") as f:
        participantes = json.load(f)

    for p in participantes:
        cert_id = p["id"]
        nombre = p["nombre"]
        clean_name = nombre.replace(" ", "_")
        qr_url = f"{BASE_WEB_URL}/?id={cert_id}"

        cert_html = template
        cert_html = cert_html.replace("{{ID}}", cert_id)
        cert_html = cert_html.replace("{{NOMBRE}}", clean_val(nombre))
        cert_html = cert_html.replace("{{ROL}}", clean_val(p.get("rol", "PONENTE")))
        cert_html = cert_html.replace("{{TITULO}}", clean_val(p.get("titulo", "")))
        cert_html = cert_html.replace("{{EJE}}", clean_val(p.get("eje", "")))
        cert_html = cert_html.replace("{{INSTITUCION}}", clean_val(p.get("institucion", "")))
        cert_html = cert_html.replace("{{PAIS}}", clean_val(p.get("pais", "")))
        cert_html = cert_html.replace("{{CIUDAD}}", clean_val(p.get("ciudad", "")))
        cert_html = cert_html.replace("{{FECHA}}", clean_val(p.get("fecha", "")))
        cert_html = cert_html.replace("{{MODERADOR}}", clean_val(p.get("moderador", "Comité Organizador")))

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

        # Generate exact high-resolution preview directly from the generated PDF
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
