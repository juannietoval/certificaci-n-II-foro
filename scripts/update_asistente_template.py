# -*- coding: utf-8 -*-
import os
import re

base = r"c:\Users\Lenovo\Desktop\Juan\sistema_certificados"

# Read master_template.html to extract the base64 logo and the inlined QRCode library
with open(os.path.join(base, "templates", "master_template.html"), "r", encoding="utf-8") as f:
    master_pon = f.read()

# Extract logo img src
logo_match = re.search(r'<img [^>]*src="(data:image/png;base64,[^"]+)"', master_pon)
if not logo_match:
    raise Exception("Could not find base64 logo in master_template.html")
logo_data_uri = logo_match.group(1)

# Extract QRCode inline library
qr_lib_match = re.search(r'(<script>var QRCode;!function\(\).*?</script>)', master_pon, re.DOTALL)
if not qr_lib_match:
    raise Exception("Could not find inline QRCode script in master_template.html")
qr_lib_script = qr_lib_match.group(1)

# Read master_asistente_template.html
asistente_path = os.path.join(base, "templates", "master_asistente_template.html")
with open(asistente_path, "r", encoding="utf-8") as f:
    asistente_content = f.read()

# 1. Replace logo src
asistente_content = re.sub(
    r'<img class="logos-img" src="[^"]*" alt="Logos Revistas Científicas">',
    f'<img class="logos-img" src="{logo_data_uri}" alt="Logos Revistas Científicas">',
    asistente_content
)

# 2. Replace signatures block HTML
old_sig_block_pattern = r'<!-- SIGNATURE -->\s*<div class="signatures-block">.*?</div>\s*</div>'
new_sig_block = '''<!-- CONSTANCIA INSTITUCIONAL (SIN FIRMA MANUSCRITA) -->
    <div class="signatures-block">
      <div class="sig-col">
        <div class="sign-atentamente">Atentamente,</div>
        <div class="sig-accent"></div>
        <div class="sig-name">{{COORDINACION}}</div>
        <div class="sig-role">Coordinaci&oacute;n General del Evento</div>
        <div class="sig-univs">UNIMINUTO &bull; IBERO &bull; UTP</div>
      </div>
    </div>'''

asistente_content = re.sub(old_sig_block_pattern, new_sig_block, asistente_content, flags=re.DOTALL)

# 3. Replace CSS for signatures
old_sig_css_pattern = r'/\* SIGNATURES SECTION - HARMONIOUS ELEVATION AS PEDESTAL \*/\s*\.signatures-block \{.*?\.sig-divider \{.*?\}(?=\s*/\* QR CODE)'
new_sig_css = '''/* CONSTANCIA INSTITUCIONAL (SIN FIRMA MANUSCRITA) */
    .signatures-block {
      position: absolute;
      bottom: 105px;
      left: 0;
      right: 0;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      z-index: 2;
    }
    .sig-col {
      width: 320px;
      text-align: center;
      position: relative;
    }
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
    }'''

asistente_content = re.sub(old_sig_css_pattern, new_sig_css, asistente_content, flags=re.DOTALL)

# 4. Replace external QRCode script with inlined script
asistente_content = re.sub(
    r'<script src="\.\./assets/qrcode\.min\.js"></script>',
    qr_lib_script,
    asistente_content
)

# 5. Fix QR text URL in script to match standard
asistente_content = re.sub(
    r'text:\s*"\{\{QR_URL\}\}"',
    'text: "https://juannietoval.github.io/certificaci-n-II-foro/?id={{ID}}"',
    asistente_content
)

# Save updated template
with open(asistente_path, "w", encoding="utf-8") as f:
    f.write(asistente_content)

print("master_asistente_template.html successfully updated!")
