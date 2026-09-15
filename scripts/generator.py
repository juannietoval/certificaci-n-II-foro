# -*- coding: utf-8 -*-
import os
import json
import subprocess

BASE = r"c:\Users\Lenovo\Desktop\Juan\sistema_certificados"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BROWSER = CHROME if os.path.exists(CHROME) else EDGE
BASE_WEB_URL = "https://juannietoval.github.io/certificaci-n-II-foro"

def escape_html(text):
    if not isinstance(text, str):
        return str(text)
    return (text.replace("&", "&amp;")
                .replace("?", "&aacute;").replace("?", "&eacute;").replace("?", "&iacute;").replace("?", "&oacute;").replace("?", "&uacute;")
                .replace("?", "&Aacute;").replace("?", "&Eacute;").replace("?", "&Iacute;").replace("?", "&Oacute;").replace("?", "&Uacute;")
                .replace("?", "&ntilde;").replace("?", "&Ntilde;"))

def generate_all():
    with open(os.path.join(BASE, "templates", "master_template.html"), "r", encoding="utf-8") as f:
        template = f.read()

    with open(os.path.join(BASE, "data", "participantes.json"), "r", encoding="utf-8") as f:
        participantes = json.load(f)

    for p in participantes:
        cert_id = p["id"]
        nombre = p["nombre"]
        clean_name = nombre.replace(" ", "_")
        qr_url = f"{BASE_WEB_URL}/?id={cert_id}"

        cert_html = template
        cert_html = cert_html.replace("{{ID}}", cert_id)
        cert_html = cert_html.replace("{{NOMBRE}}", escape_html(nombre))
        cert_html = cert_html.replace("{{ROL}}", escape_html(p.get("rol", "PONENTE")))
        cert_html = cert_html.replace("{{TITULO}}", escape_html(p.get("titulo", "")))
        cert_html = cert_html.replace("{{EJE}}", escape_html(p.get("eje", "")))
        cert_html = cert_html.replace("{{INSTITUCION}}", escape_html(p.get("institucion", "")))
        cert_html = cert_html.replace("{{PAIS}}", escape_html(p.get("pais", "")))
        cert_html = cert_html.replace("{{CIUDAD}}", escape_html(p.get("ciudad", "")))
        cert_html = cert_html.replace("{{FECHA}}", escape_html(p.get("fecha", "")))
        cert_html = cert_html.replace("{{MODERADOR}}", escape_html(p.get("moderador", "Comit? Organizador")))

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
        cmd_png = [
            BROWSER,
            "--headless",
            "--disable-gpu",
            "--window-size=1414,1000",
            "--hide-scrollbars",
            f"--screenshot={png_file}",
            f"file:///{html_file}"
        ]
        subprocess.run(cmd_png, capture_output=True, text=True)
        print(f"Generated Vector Certificate: {cert_id} - {nombre}")

if __name__ == "__main__":
    generate_all()
