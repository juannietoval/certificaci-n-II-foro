# -*- coding: utf-8 -*-
"""
Script de envío de prueba en Python usando SMTP (Gmail o institucional UTP).
Permite adjuntar directamente los archivos PDF desde tu disco local.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

BASE = r"c:\Users\Lenovo\Desktop\Juan\sistema_certificados"

LINK_GRABACION = "https://uniminuto0-my.sharepoint.com/personal/felix_duenas_uniminuto_edu/_layouts/15/stream.aspx?id=%2Fpersonal%2Ffelix%5Fduenas%5Funiminuto%5Fedu%2FDocuments%2FGrabaciones%2FII%20FORO%20DE%20EDITORES%20DE%20REVISTAS%20CIENT%C3%8DFICAS%2D20260911%5F080635%2DGrabaci%C3%B3n%20de%20la%20reuni%C3%B3n%2Emp4&ga=1&referrer=StreamWebApp%2EWeb&referrerScenario=AddressBarCopied%2Eview%2E692c7bc5%2Df83b%2D4dbf%2D905d%2D7cb360d59b9e"

DESTINATARIOS_PRUEBA = [
    {
        "id": "FORO26-ASI-012",
        "nombre": "Juan Esteban Nieto Valencia",
        "email": "juan.nieto2@utp.edu.co",
        "rol": "ASISTENTE",
        "asunto": "Certificado Oficial de Asistencia y Grabación - II Foro de Editores de Revistas Científicas 2026",
        "tema": "Gestión editorial en tiempos de inteligencia artificial",
        "urlVerificacion": "https://juannietoval.github.io/certificaci-n-II-foro/?id=FORO26-ASI-012",
        "pdf_path": os.path.join(BASE, "certificados", "asistentes", "certificado - Juan Esteban Nieto Valencia.pdf")
    },
    {
        "id": "FORO26-PON-006",
        "nombre": "Erika Betancourt",
        "email": "juanestebannietovalencia@gmail.com",
        "rol": "PONENTE",
        "asunto": "Certificado Oficial de Ponente y Grabación - II Foro de Editores de Revistas Científicas 2026",
        "ponencia": "Presentación de la Revista Miradas",
        "eje": "Socialización de Revistas Científicas",
        "institucion": "Universidad Tecnológica de Pereira",
        "urlVerificacion": "https://juannietoval.github.io/certificaci-n-II-foro/?id=FORO26-PON-006",
        "pdf_path": os.path.join(BASE, "certificados", "ponentes", "certificado - Erika Betancourt.pdf")
    }
]

def construir_html(datos):
    es_ponente = (datos["rol"] == "PONENTE")
    
    if es_ponente:
        bloque_rol = f"""
          <p style="font-size: 15px; color: #334155; line-height: 1.6; margin: 0 0 16px 0;">
            Agradecemos profundamente su valiosa contribución como <strong>Ponente</strong> con la presentación de la conferencia magistral:
          </p>
          <div style="background-color: #f8fafc; border-left: 4px solid #b89047; padding: 14px 18px; margin: 18px 0; border-radius: 4px;">
            <p style="margin: 0; font-size: 15px; font-weight: 600; color: #0b223d; font-style: italic;">
              &laquo;{datos.get('ponencia', 'Ponencia Magistral')}&raquo;
            </p>
            <p style="margin: 6px 0 0 0; font-size: 13px; color: #64748b;">Eje Temático: <strong>{datos.get('eje', '')}</strong></p>
            <p style="margin: 2px 0 0 0; font-size: 13px; color: #64748b;">{datos.get('institucion', '')}</p>
          </div>
        """
    else:
        bloque_rol = """
          <p style="font-size: 15px; color: #334155; line-height: 1.6; margin: 0 0 16px 0;">
            Agradecemos sinceramente su asistencia y participación en el <strong>II Foro de Editores de Revistas Científicas: <em>«Gestión editorial en tiempos de inteligencia artificial»</em></strong>, llevado a cabo con gran éxito el pasado 11 de septiembre de 2026.
          </p>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="margin: 0; padding: 20px; background-color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 620px; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(11, 34, 61, 0.08); border: 1px solid #e2e8f0;">
        <tr>
          <td style="background: linear-gradient(135deg, #071628 0%, #0b223d 100%); padding: 32px 28px; text-align: center; border-bottom: 3px solid #b89047;">
            <span style="display: inline-block; font-size: 11px; font-weight: 700; color: #b89047; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px;">
              CONSTANCIA OFICIAL DE PARTICIPACIÓN
            </span>
            <h1 style="color: #ffffff; font-size: 20px; margin: 0; font-weight: 700; line-height: 1.3;">
              II FORO DE EDITORES DE REVISTAS CIENTÍFICAS
            </h1>
            <p style="color: #cbd5e1; font-size: 14px; font-style: italic; margin: 6px 0 0 0;">
              &laquo;Gestión editorial en tiempos de inteligencia artificial&raquo;
            </p>
          </td>
        </tr>
        <tr>
          <td style="padding: 32px 30px;">
            <p style="font-size: 16px; color: #0b223d; font-weight: 700; margin: 0 0 16px 0;">
              Estimado(a) {datos['nombre']}:
            </p>
            {bloque_rol}
            <p style="font-size: 15px; color: #334155; line-height: 1.6; margin: 0 0 24px 0;">
              Ponemos a su disposición su <strong>certificado digital oficial</strong> adjunto a este mensaje y con validación mediante código QR y serial único de registro, así como el acceso a la <strong>grabación íntegra</strong> de la jornada académica:
            </p>
            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 24px 0;">
              <tr>
                <td style="padding-bottom: 14px;">
                  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #fdfaf3; border: 1.5px solid #b89047; border-radius: 6px; padding: 16px 20px;">
                    <tr>
                      <td>
                        <span style="font-size: 11px; font-weight: 700; color: #8C6D3B; text-transform: uppercase; letter-spacing: 1px;">
                          Acreditación Oficial • Código: {datos['id']}
                        </span>
                        <div style="margin-top: 10px;">
                          <a href="{datos['urlVerificacion']}" target="_blank" style="display: inline-block; background-color: #0b223d; color: #ffffff; text-decoration: none; padding: 11px 22px; font-size: 14px; font-weight: 600; border-radius: 4px;">
                            📄 Ver y Descargar Certificado Oficial en Portal Web
                          </a>
                        </div>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
              <tr>
                <td>
                  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f0fdf4; border: 1.5px solid #86efac; border-radius: 6px; padding: 16px 20px;">
                    <tr>
                      <td>
                        <span style="font-size: 11px; font-weight: 700; color: #15803d; text-transform: uppercase; letter-spacing: 1px;">
                          Memorias en Video • Sesión Completa (Microsoft Stream)
                        </span>
                        <div style="margin-top: 10px;">
                          <a href="{LINK_GRABACION}" target="_blank" style="display: inline-block; background-color: #059669; color: #ffffff; text-decoration: none; padding: 11px 22px; font-size: 14px; font-weight: 600; border-radius: 4px;">
                            🎥 Ver Grabación Oficial de la Reunión
                          </a>
                        </div>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 14px 18px; margin: 24px 0 16px 0;">
              <p style="margin: 0; font-size: 13px; color: #64748b; line-height: 1.5;">
                🔒 <strong>Verificación de autenticidad:</strong> Su certificado puede ser validado en cualquier momento escaneando el código QR incorporado en el documento o ingresando a: <br>
                <a href="{datos['urlVerificacion']}" style="color: #0b223d; word-break: break-all;">{datos['urlVerificacion']}</a>
              </p>
            </div>
            <div style="margin-top: 32px; border-top: 1px solid #e2e8f0; padding-top: 20px; text-align: center;">
              <p style="margin: 0; font-size: 13.5px; font-style: italic; color: #64748b;">Atentamente,</p>
              <p style="margin: 4px 0 2px 0; font-size: 14.5px; font-weight: 700; color: #0b223d; letter-spacing: 0.5px;">
                COMITÉ ORGANIZADOR
              </p>
              <p style="margin: 0; font-size: 12.5px; color: #64748b;">
                Coordinación General del Evento
              </p>
              <p style="margin: 6px 0 0 0; font-size: 12px; font-weight: 700; color: #b89047; letter-spacing: 1px;">
                UNIMINUTO &bull; IBERO &bull; UTP
              </p>
            </div>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

def enviar_correos_smtp(remitente_email, remitente_password, servidor_smtp="smtp.gmail.com", puerto=587):
    print("Iniciando conexión con servidor SMTP...")
    server = smtplib.SMTP(servidor_smtp, puerto)
    server.starttls()
    server.login(remitente_email, remitente_password)
    print("Autenticación exitosa.")

    for d in DESTINATARIOS_PRUEBA:
        msg = MIMEMultipart()
        msg['From'] = f"Comité Organizador - II Foro de Editores 2026 <{remitente_email}>"
        msg['To'] = d['email']
        msg['Subject'] = d['asunto']

        html_content = construir_html(d)
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))

        # Adjuntar PDF local
        if os.path.exists(d['pdf_path']):
            with open(d['pdf_path'], 'rb') as f_pdf:
                part = MIMEApplication(f_pdf.read(), Name=os.path.basename(d['pdf_path']))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(d["pdf_path"])}"'
            msg.attach(part)
            print(f"  [OK] PDF adjunto: {os.path.basename(d['pdf_path'])}")
        else:
            print(f"  [AVISO] No se encontró el archivo: {d['pdf_path']}")

        server.send_message(msg)
        print(f"  [ENVIADO] -> {d['email']} ({d['rol']} - {d['nombre']})")

    server.quit()
    print("Todos los correos de prueba fueron enviados con éxito.")

if __name__ == "__main__":
    import getpass
    print("=== ENVÍO DE PRUEBA DE CERTIFICADOS ===")
    user = input("Ingresa tu correo de Gmail o UTP remitente: ").strip()
    pwd = getpass.getpass("Ingresa tu contraseña o contraseña de aplicación: ").strip()
    if user and pwd:
        enviar_correos_smtp(user, pwd)
    else:
        print("Datos incompletos. Se canceló el envío.")
