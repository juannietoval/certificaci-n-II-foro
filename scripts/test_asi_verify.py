# -*- coding: utf-8 -*-
import os
import subprocess
import pymupdf

BASE = r'c:\Users\Lenovo\Desktop\Juan\sistema_certificados'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
BROWSER = CHROME if os.path.exists(CHROME) else EDGE

with open(os.path.join(BASE, 'templates', 'master_asistente_template.html'), 'r', encoding='utf-8') as f:
    tpl = f.read()

tpl = tpl.replace('{{ID}}', 'FORO26-ASI-001')
tpl = tpl.replace('{{NOMBRE}}', 'Cristian Yasser Martínez Rodríguez')
tpl = tpl.replace('{{DOCUMENTO_LINE}}', 'C.C. 1.014.246.761')
tpl = tpl.replace('{{ROL}}', 'ASISTENTE')
tpl = tpl.replace('{{INTENSIDAD}}', '4 horas')
tpl = tpl.replace('{{HORARIO}}', '8:00 a. m. a 12:00 m. (hora Colombia)')
tpl = tpl.replace('{{AFFILIATION_BLOCK}}', '<div class="affiliation">Universidad de Los Andes &bull; Colombia</div>')
tpl = tpl.replace('{{LOCATION_DATE}}', 'Pereira, Colombia (Modalidad Virtual) &mdash; Viernes 11 de septiembre de 2026')
tpl = tpl.replace('{{COORDINACION}}', 'Comité Organizador')

html_test = os.path.join(BASE, 'templates', 'test_asi_verify.html')
with open(html_test, 'w', encoding='utf-8') as f:
    f.write(tpl)

pdf_test = os.path.join(BASE, 'output', 'pdf', 'test_asi_verify.pdf')
png_test = os.path.join(BASE, 'output', 'preview', 'test_asi_verify.png')

subprocess.run([BROWSER, '--headless', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={pdf_test}', f'file:///{html_test}'], check=True)

doc = pymupdf.open(pdf_test)
page = doc[0]
pix = page.get_pixmap(dpi=150)
pix.save(png_test)
doc.close()
print('Test asistente successfully rendered to PDF and PNG!')
