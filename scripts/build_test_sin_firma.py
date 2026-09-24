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

DEFAULT_EVENT_TITLE = "II FORO DE EDITORES DE REVISTAS CIENTÍFICAS"
DEFAULT_EVENT_SUBTITLE = "Gestión editorial en tiempos de inteligencia artificial"
DEFAULT_FECHA = "Viernes 11 de septiembre de 2026"
DEFAULT_HORARIO = "8:00 a 12:00 m. (hora Colombia)"
DEFAULT_INTENSIDAD = "4 horas"
DEFAULT_MODALIDAD = "Virtual"
DEFAULT_CIUDAD = "Pereira, Colombia"

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
    prefixes = ("C.C.", "CC", "D.I.", "DI", "DNI", "PASAPORTE", "PAS.", "PAS", "C.E.", "CE")
    for pfx in prefixes:
        if upper_s.startswith(pfx):
            return s
    if s.isdigit():
        num = int(s)
        return f"C.C. {num:,}".replace(",", ".")
    return f"D.I. {s}"

def title_case_ponencia(titulo):
    if not titulo:
        return ""
    parts = titulo.split(": ")
    result = []
    for i, part in enumerate(parts):
        if i == 0:
            result.append(part[0].upper() + part[1:].lower() if len(part) > 1 else part.upper())
        else:
            result.append(part[0].upper() + part[1:].lower() if len(part) > 1 else part.upper())
    return ": ".join(result)

def build_tests():
    with open(os.path.join(BASE, "templates", "master_template.html"), "r", encoding="utf-8") as f:
        tpl_pon = f.read()

    with open(os.path.join(BASE, "templates", "master_asistente_template.html"), "r", encoding="utf-8") as f:
        tpl_asi = f.read()

    with open(os.path.join(BASE, "data", "participantes.json"), "r", encoding="utf-8") as f:
        participantes = json.load(f)

    p_pon = [p for p in participantes if p["id"] == "FORO26-PON-001"][0]
    p_asi = [p for p in participantes if p["id"] == "FORO26-ASI-001"][0]

    # 1. OPTION 1: Pure Typographic Endorsement (Atentamente, + Comité Organizador + Coordinación General del Evento + UNIMINUTO • IBERO • UTP)
    # We replace the rubric & line with .sign-atentamente and .sig-accent
    old_sig_html = '''    <!-- SIGNATURE -->
    <div class="signatures-block">
      <div class="sig-col">
        <svg class="sig-rubric" viewBox="0 0 160 38" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 28 C28 12, 38 6, 48 22 C55 32, 60 14, 72 18 C84 22, 80 34, 94 25 C106 16, 118 20, 130 14 C136 11, 146 10, 150 14" stroke="#0b223d" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.82"/>
          <path d="M26 25 C46 34, 88 35, 144 19" stroke="#0b223d" stroke-width="1.2" stroke-linecap="round" opacity="0.7"/>
          <path d="M50 14 C58 5, 68 3, 70 12 C72 19, 66 26, 60 30" stroke="#8C6D3B" stroke-width="1.0" stroke-linecap="round" opacity="0.55"/>
        </svg>
        <div class="sig-line"></div>
        <div class="sig-accent"></div>
        <div class="sig-name">{{COORDINACION}}</div>
        <div class="sig-role">Coordinaci&oacute;n General del Evento</div>
        <div class="sig-univs">UNIMINUTO &bull; IBERO &bull; UTP</div>
      </div>
    </div>'''

    new_sig_opt1 = '''    <!-- CONSTANCIA INSTITUCIONAL (SIN FIRMA MANUSCRITA) -->
    <div class="signatures-block">
      <div class="sig-col">
        <div class="sign-atentamente">Atentamente,</div>
        <div class="sig-accent"></div>
        <div class="sig-name">{{COORDINACION}}</div>
        <div class="sig-role">Coordinaci&oacute;n General del Evento</div>
        <div class="sig-univs">UNIMINUTO &bull; IBERO &bull; UTP</div>
      </div>
    </div>'''

    # Additional CSS for .sign-atentamente and improved .sig-name
    opt1_css = '''
    .sign-atentamente {
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 13.5pt;
      font-style: italic;
      font-weight: 500;
      color: #8C6D3B;
      letter-spacing: 0.6px;
      margin-bottom: 3px;
      line-height: 1;
    }
    .sig-accent {
      width: 44px;
      height: 1.6px;
      background: #8C6D3B;
      margin: 0 auto 5px auto;
      border-radius: 1px;
    }
    .sig-name {
      font-family: 'Cinzel', serif;
      font-size: 10.5pt;
      font-weight: 700;
      color: #0b223d;
      text-transform: uppercase;
      letter-spacing: 1.2px;
      margin-bottom: 2px;
    }
    .sig-role {
      font-size: 8pt;
      color: #64748b;
      margin-top: 1px;
      letter-spacing: 0.4px;
    }
    .sig-univs {
      font-size: 8.2pt;
      font-weight: 700;
      color: #8C6D3B;
      letter-spacing: 0.8px;
      margin-top: 3px;
    }
'''

    # OPTION 2: Tripartite Seal on Left, Constancia in Center, QR on Right!
    seal_svg = '''<svg class="seal-emblem" viewBox="0 0 100 100" width="80" height="80" xmlns="http://www.w3.org/2000/svg">
      <circle cx="50" cy="50" r="47" fill="none" stroke="#8C6D3B" stroke-width="1.3" opacity="0.85"/>
      <circle cx="50" cy="50" r="43.5" fill="none" stroke="#0b223d" stroke-width="0.8" stroke-dasharray="2 2" opacity="0.6"/>
      <circle cx="50" cy="50" r="31" fill="none" stroke="#8C6D3B" stroke-width="0.9" opacity="0.75"/>
      <path id="seal-top" d="M 16,50 A 34,34 0 1,1 84,50" fill="none"/>
      <path id="seal-bot" d="M 84,50 A 34,34 0 0,1 16,50" fill="none"/>
      <text font-family="'Cinzel', serif" font-size="5.8" font-weight="700" fill="#0b223d" letter-spacing="1.2">
        <textPath href="#seal-top" startOffset="50%" text-anchor="middle">COMIT&#201; ORGANIZADOR</textPath>
      </text>
      <text font-family="'Montserrat', sans-serif" font-size="4.6" font-weight="600" fill="#8C6D3B" letter-spacing="0.8">
        <textPath href="#seal-bot" startOffset="50%" text-anchor="middle">&#8226; II FORO 2026 &#8226;</textPath>
      </text>
      <g transform="translate(50, 50) scale(0.66)" opacity="0.85">
        <path d="M-18,2 C-14,-10 0,-14 0,-2 C0,-14 14,-10 18,2 C12,12 0,14 0,14 C0,14 -12,12 -18,2 Z" fill="none" stroke="#8C6D3B" stroke-width="1.8" stroke-linejoin="round"/>
        <path d="M0,-12 L0,14" stroke="#8C6D3B" stroke-width="1.4"/>
        <path d="M-12,-3 C-8,5 0,7 0,7" stroke="#0b223d" stroke-width="1.2" fill="none"/>
        <path d="M12,-3 C8,5 0,7 0,7" stroke="#0b223d" stroke-width="1.2" fill="none"/>
        <circle cx="0" cy="-17" r="2.2" fill="#8C6D3B"/>
      </g>
    </svg>'''

    new_sig_opt2 = f'''    <!-- SEAL EMBLEM (LEFT) -->
    <div class="seal-frame">
      {seal_svg}
      <div class="seal-caption">UNIMINUTO &bull; IBERO &bull; UTP</div>
    </div>

    <!-- CONSTANCIA INSTITUCIONAL (CENTER) -->
    <div class="signatures-block">
      <div class="sig-col">
        <div class="sign-atentamente">Atentamente,</div>
        <div class="sig-accent"></div>
        <div class="sig-name">{{{{COORDINACION}}}}</div>
        <div class="sig-role">Coordinaci&oacute;n General del Evento</div>
        <div class="sig-univs">UNIMINUTO &bull; IBERO &bull; UTP</div>
      </div>
    </div>'''

    opt2_css = opt1_css + '''
    .seal-frame {
      position: absolute;
      bottom: 42px;
      left: 55px;
      display: flex;
      flex-direction: column;
      align-items: center;
      z-index: 2;
    }
    .seal-caption {
      font-size: 6.8pt;
      font-weight: 600;
      color: #8C6D3B;
      letter-spacing: 0.8px;
      margin-top: 4px;
      text-transform: uppercase;
    }
'''

    # Build Ponente Opt 1
    html_pon_opt1 = tpl_pon.replace(old_sig_html, new_sig_opt1)
    html_pon_opt1 = html_pon_opt1.replace("</style>", opt1_css + "\n  </style>")
    # Fill Ponente Data
    cert_id = p_pon["id"]
    nombre = p_pon["nombre"]
    rol = p_pon.get("rol", "PONENTE").upper()
    qr_url = f"{BASE_WEB_URL}/?id={cert_id}"
    fecha = p_pon.get("fecha", DEFAULT_FECHA)
    horario = p_pon.get("horario", DEFAULT_HORARIO)
    modalidad = p_pon.get("modalidad", DEFAULT_MODALIDAD)
    ciudad = p_pon.get("ciudad", DEFAULT_CIUDAD)
    institucion = p_pon.get("institucion", "")
    intensidad = p_pon.get("intensidad", DEFAULT_INTENSIDAD)
    ciudad_disp = f"{ciudad} (Modalidad {modalidad})" if modalidad else ciudad
    location_date = f"{ciudad_disp} &mdash; {clean_val(fecha)}"
    doc_line = format_doc(p_pon.get("cedula", ""))
    titulo_raw = p_pon.get("titulo", "")
    titulo_display = title_case_ponencia(titulo_raw)

    html_pon_opt1 = html_pon_opt1.replace("{{ID}}", cert_id)
    html_pon_opt1 = html_pon_opt1.replace("{{NOMBRE}}", clean_val(nombre))
    doc_block = f'<div class="doc-line">{clean_val(doc_line)}</div>' if doc_line else ''
    html_pon_opt1 = html_pon_opt1.replace("{{DOCUMENTO_LINE}}", doc_block)
    html_pon_opt1 = html_pon_opt1.replace("{{ROL}}", clean_val(rol))
    html_pon_opt1 = html_pon_opt1.replace("{{TITULO}}", clean_val(titulo_display))
    html_pon_opt1 = html_pon_opt1.replace("{{EJE}}", clean_val(p_pon.get("eje", "")))
    html_pon_opt1 = html_pon_opt1.replace("{{INTENSIDAD}}", clean_val(intensidad))
    html_pon_opt1 = html_pon_opt1.replace("{{HORARIO}}", clean_val(horario))
    html_pon_opt1 = html_pon_opt1.replace("{{INSTITUCION}}", clean_val(institucion))
    html_pon_opt1 = html_pon_opt1.replace("{{PAIS}}", clean_val(p_pon.get("pais", "")))
    html_pon_opt1 = html_pon_opt1.replace("{{LOCATION_DATE}}", location_date)
    html_pon_opt1 = html_pon_opt1.replace("{{COORDINACION}}", clean_val(p_pon.get("coordinacion", "Comité Organizador")))
    html_pon_opt1 = html_pon_opt1.replace("{{QR_URL}}", qr_url)

    # Build Ponente Opt 2
    html_pon_opt2 = tpl_pon.replace(old_sig_html, new_sig_opt2)
    html_pon_opt2 = html_pon_opt2.replace("</style>", opt2_css + "\n  </style>")
    html_pon_opt2 = html_pon_opt2.replace("{{ID}}", cert_id)
    html_pon_opt2 = html_pon_opt2.replace("{{NOMBRE}}", clean_val(nombre))
    html_pon_opt2 = html_pon_opt2.replace("{{DOCUMENTO_LINE}}", doc_block)
    html_pon_opt2 = html_pon_opt2.replace("{{ROL}}", clean_val(rol))
    html_pon_opt2 = html_pon_opt2.replace("{{TITULO}}", clean_val(titulo_display))
    html_pon_opt2 = html_pon_opt2.replace("{{EJE}}", clean_val(p_pon.get("eje", "")))
    html_pon_opt2 = html_pon_opt2.replace("{{INTENSIDAD}}", clean_val(intensidad))
    html_pon_opt2 = html_pon_opt2.replace("{{HORARIO}}", clean_val(horario))
    html_pon_opt2 = html_pon_opt2.replace("{{INSTITUCION}}", clean_val(institucion))
    html_pon_opt2 = html_pon_opt2.replace("{{PAIS}}", clean_val(p_pon.get("pais", "")))
    html_pon_opt2 = html_pon_opt2.replace("{{LOCATION_DATE}}", location_date)
    html_pon_opt2 = html_pon_opt2.replace("{{COORDINACION}}", clean_val(p_pon.get("coordinacion", "Comité Organizador")))
    html_pon_opt2 = html_pon_opt2.replace("{{QR_URL}}", qr_url)

    # Build Asistente Opt 1
    html_asi_opt1 = tpl_asi.replace(old_sig_html, new_sig_opt1)
    html_asi_opt1 = html_asi_opt1.replace("</style>", opt1_css + "\n  </style>")
    cert_id_asi = p_asi["id"]
    nombre_asi = p_asi["nombre"]
    doc_line_asi = format_doc(p_asi.get("cedula", ""))
    intensidad_asi = p_asi.get("intensidad", DEFAULT_INTENSIDAD)
    horario_asi = p_asi.get("horario", DEFAULT_HORARIO)
    ciudad_disp_asi = f"{ciudad} (Modalidad {modalidad})" if modalidad else ciudad
    location_date_asi = f"{ciudad_disp_asi} &mdash; {clean_val(fecha)}"
    qr_url_asi = f"{BASE_WEB_URL}/?id={cert_id_asi}"

    html_asi_opt1 = html_asi_opt1.replace("{{ID}}", cert_id_asi)
    html_asi_opt1 = html_asi_opt1.replace("{{NOMBRE}}", clean_val(nombre_asi))
    html_asi_opt1 = html_asi_opt1.replace("{{DOCUMENTO_LINE}}", clean_val(doc_line_asi))
    html_asi_opt1 = html_asi_opt1.replace("{{ROL}}", "ASISTENTE")
    html_asi_opt1 = html_asi_opt1.replace("{{INTENSIDAD}}", clean_val(intensidad_asi))
    html_asi_opt1 = html_asi_opt1.replace("{{HORARIO}}", clean_val(horario_asi))
    html_asi_opt1 = html_asi_opt1.replace("{{AFFILIATION_BLOCK}}", "")
    html_asi_opt1 = html_asi_opt1.replace("{{LOCATION_DATE}}", location_date_asi)
    html_asi_opt1 = html_asi_opt1.replace("{{COORDINACION}}", clean_val(p_asi.get("coordinacion", "Comité Organizador")))
    html_asi_opt1 = html_asi_opt1.replace("{{QR_URL}}", qr_url_asi)

    # Build Asistente Opt 2
    html_asi_opt2 = tpl_asi.replace(old_sig_html, new_sig_opt2)
    # Adjust seal-frame bottom for asistente since signatures-block is at bottom: 110px
    opt2_css_asi = opt2_css.replace("bottom: 42px;", "bottom: 85px;")
    html_asi_opt2 = html_asi_opt2.replace("</style>", opt2_css_asi + "\n  </style>")
    html_asi_opt2 = html_asi_opt2.replace("{{ID}}", cert_id_asi)
    html_asi_opt2 = html_asi_opt2.replace("{{NOMBRE}}", clean_val(nombre_asi))
    html_asi_opt2 = html_asi_opt2.replace("{{DOCUMENTO_LINE}}", clean_val(doc_line_asi))
    html_asi_opt2 = html_asi_opt2.replace("{{ROL}}", "ASISTENTE")
    html_asi_opt2 = html_asi_opt2.replace("{{INTENSIDAD}}", clean_val(intensidad_asi))
    html_asi_opt2 = html_asi_opt2.replace("{{HORARIO}}", clean_val(horario_asi))
    html_asi_opt2 = html_asi_opt2.replace("{{AFFILIATION_BLOCK}}", "")
    html_asi_opt2 = html_asi_opt2.replace("{{LOCATION_DATE}}", location_date_asi)
    html_asi_opt2 = html_asi_opt2.replace("{{COORDINACION}}", clean_val(p_asi.get("coordinacion", "Comité Organizador")))
    html_asi_opt2 = html_asi_opt2.replace("{{QR_URL}}", qr_url_asi)

    # Targets to render
    targets = [
        ("TEST_PONENTE_sin_firma_opt1", html_pon_opt1),
        ("TEST_PONENTE_sin_firma_opt2", html_pon_opt2),
        ("TEST_ASISTENTE_sin_firma_opt1", html_asi_opt1),
        ("TEST_ASISTENTE_sin_firma_opt2", html_asi_opt2)
    ]

    for name, content in targets:
        html_path = os.path.abspath(os.path.join(BASE, "templates", f"{name}.html"))
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)

        pdf_path = os.path.abspath(os.path.join(BASE, "output", "pdf", f"{name}.pdf"))
        cmd_pdf = [
            BROWSER,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            f"file:///{html_path}"
        ]
        subprocess.run(cmd_pdf, capture_output=True, text=True)

        png_path = os.path.abspath(os.path.join(BASE, "output", "preview", f"{name}.png"))
        doc = pymupdf.open(pdf_path)
        page = doc[0]
        pix = page.get_pixmap(dpi=150)
        pix.save(png_path)
        doc.close()

        print(f"[OK] Generated {name} -> {pdf_path} and preview -> {png_path}")

if __name__ == "__main__":
    build_tests()
