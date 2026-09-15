# -*- coding: utf-8 -*-
import os
import json
import subprocess
import base64

BASE = r"c:\Users\Lenovo\Desktop\Juan\sistema_certificados"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BROWSER = CHROME if os.path.exists(CHROME) else EDGE

# GitHub Pages URL requested by user
BASE_WEB_URL = "https://juannietoval.github.io/certificaci-n-II-foro"

def generate_all():
    with open(os.path.join(BASE, "data", "participantes.json"), "r", encoding="utf-8") as f:
        participantes = json.load(f)

    with open(os.path.join(BASE, "assets", "template.jpg"), "rb") as img_f:
        bg_b64 = base64.b64encode(img_f.read()).decode("utf-8")
    with open(os.path.join(BASE, "assets", "qrcode.min.js"), "r", encoding="utf-8") as qr_f:
        qr_js = qr_f.read()

    amp = "&"
    font_link = f"https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700{amp}family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,400;1,600{amp}family=Montserrat:wght@300;400;500;600;700{amp}display=swap"

    for p in participantes:
        cert_id = p["id"]
        nombre = p["nombre"]
        clean_name = nombre.replace(" ", "_")
        qr_target_url = f"{BASE_WEB_URL}/?id={cert_id}"
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Certificado - {nombre}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{font_link}" rel="stylesheet">
  <style>
    @page {{
      size: 297mm 210mm;
      margin: 0;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    html, body {{
      margin: 0;
      padding: 0;
      width: 297mm;
      height: 210mm;
      background: #f7f5ef;
      font-family: 'Montserrat', sans-serif;
    }}
    .cert-page {{
      position: relative;
      width: 297mm;
      height: 210mm;
      margin: 0 auto;
      background-image: url('data:image/jpeg;base64,{bg_b64}');
      background-size: 100% 100%;
      background-repeat: no-repeat;
      overflow: hidden;
    }}
    
    /* RECIPIENT NAME BLOCK - HERO */
    .recipient-block {{
      position: absolute;
      top: 33.2%;
      left: 14%;
      right: 14%;
      height: 8.8%;
      display: flex;
      align-items: flex-end;
      justify-content: center;
      text-align: center;
    }}
    .recipient-name {{
      font-family: 'Cinzel', 'Playfair Display', Georgia, serif;
      font-size: 25pt;
      font-weight: 700;
      color: #0b223d;
      letter-spacing: 2px;
      text-transform: uppercase;
      line-height: 1.1;
      white-space: nowrap;
    }}

    /* BODY TEXT */
    .body-block {{
      position: absolute;
      top: 44.0%;
      left: 15%;
      right: 15%;
      text-align: center;
      color: #2b3a4a;
    }}
    .lead-text {{
      font-size: 11.5pt;
      font-weight: 400;
      color: #4a5568;
      letter-spacing: 0.5px;
      margin-bottom: 5px;
    }}
    .role-highlight {{
      font-weight: 700;
      color: #0b223d;
      letter-spacing: 1.5px;
    }}
    .event-title {{
      font-family: 'Cinzel', 'Playfair Display', serif;
      font-size: 13pt;
      font-weight: 700;
      color: #0b223d;
      letter-spacing: 1px;
      margin-bottom: 7px;
    }}
    .thematic-axis {{
      font-size: 10pt;
      color: #718096;
      margin-bottom: 8px;
      font-style: italic;
    }}
    .thematic-axis strong {{
      color: #334155;
      font-style: normal;
      font-weight: 600;
    }}
    .presentation-box {{
      margin: 4px auto 8px auto;
      max-width: 90%;
    }}
    .presentation-intro {{
      font-size: 9pt;
      text-transform: uppercase;
      letter-spacing: 1.2px;
      color: #8c733e;
      font-weight: 600;
      margin-bottom: 2px;
    }}
    .presentation-title {{
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 14pt;
      font-weight: 600;
      font-style: italic;
      color: #111827;
      line-height: 1.25;
      padding: 0 10px;
    }}
    .affiliation {{
      font-size: 10pt;
      font-weight: 500;
      color: #475569;
      margin-top: 6px;
    }}
    .location-date {{
      font-size: 9.5pt;
      color: #64748b;
      margin-top: 8px;
      letter-spacing: 0.5px;
    }}

    /* SIGNATURES */
    .signatures-block {{
      position: absolute;
      top: 85.2%;
      left: 17%;
      right: 23%;
      display: flex;
      justify-content: space-between;
    }}
    .sig-col {{
      width: 44%;
      text-align: center;
    }}
    .sig-name {{
      font-size: 8.5pt;
      font-weight: 600;
      color: #0b223d;
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }}
    .sig-role {{
      font-size: 7.5pt;
      color: #64748b;
      margin-top: 2px;
    }}

    /* QR BOX */
    .qr-box {{
      position: absolute;
      top: 77.1%;
      left: 84.7%;
      width: 78px;
      height: 78px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    #qrcode img, #qrcode canvas {{
      width: 66px !important;
      height: 66px !important;
    }}
    .cert-id {{
      position: absolute;
      top: 89.2%;
      left: 81%;
      width: 15%;
      text-align: center;
      font-size: 6.8pt;
      font-weight: 600;
      color: #0b223d;
      letter-spacing: 0.5px;
      font-family: monospace;
    }}
  </style>
</head>
<body>
  <div class="cert-page">
    <div class="recipient-block">
      <div class="recipient-name">{nombre}</div>
    </div>

    <div class="body-block">
      <div class="lead-text">
        Por su destacada participaci&oacute;n en calidad de <span class="role-highlight">{p['rol']}</span> en el
      </div>
      <div class="event-title">
        II FORO DE EDITORES DE REVISTAS CIENT&Iacute;FICAS
      </div>
      <div class="thematic-axis">
        Eje tem&aacute;tico: <strong>{p['eje']}</strong>
      </div>
      <div class="presentation-box">
        <div class="presentation-intro">Ponencia magistral:</div>
        <div class="presentation-title">
          &laquo;{p['titulo']}&raquo;
        </div>
      </div>
      <div class="affiliation">
        {p['institucion']} &bull; {p['pais']}
      </div>
      <div class="location-date">
        {p['ciudad']} &mdash; {p['fecha']}
      </div>
    </div>

    <div class="signatures-block">
      <div class="sig-col">
        <div class="sig-name">Comit&eacute; Editorial</div>
        <div class="sig-role">Revistas Cient&iacute;ficas UTP</div>
      </div>
      <div class="sig-col">
        <div class="sig-name">{p.get('moderador', 'Comit? Organizador')}</div>
        <div class="sig-role">Moderador de Eje / Coordinaci&oacute;n</div>
      </div>
    </div>

    <div class="qr-box">
      <div id="qrcode"></div>
    </div>
    <div class="cert-id">{cert_id}</div>
  </div>

  <script>{qr_js}</script>
  <script>
    new QRCode(document.getElementById("qrcode"), {{
      text: "{qr_target_url}",
      width: 66,
      height: 66,
      colorDark : "#0b223d",
      colorLight : "#ffffff",
      correctLevel : QRCode.CorrectLevel.M
    }});
  </script>
</body>
</html>"""

        html_file = os.path.abspath(os.path.join(BASE, "templates", f"{cert_id}.html"))
        with open(html_file, "w", encoding="utf-8") as f_out:
            f_out.write(html)
        
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
        print(f"Generated with QR to {qr_target_url}: {cert_id} - {nombre}")

if __name__ == "__main__":
    generate_all()
