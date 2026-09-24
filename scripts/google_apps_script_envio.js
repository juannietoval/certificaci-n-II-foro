/**
 * ====================================================================================
 * SISTEMA INSTITUCIONAL DE ENVÍO DE CERTIFICADOS Y GRABACIÓN
 * II FORO DE EDITORES DE REVISTAS CIENTÍFICAS 2026
 * UNIMINUTO • IBERO • UTP
 * ====================================================================================
 * 
 * CARACTERÍSTICAS FORMALES:
 * 1. Tratamiento personalizado por género formal: "Estimado [Nombre]" / "Estimada [Nombre]".
 * 2. Cero emojis o stickers: Redacción y diseño 100% académico, sobrio y profesional.
 * 3. Certificado oficial en formato PDF adjunto directamente en el correo.
 * 4. Botones institucionales limpios para verificación web y grabación de la sesión.
 * 5. Registro automático de estado de envío para evitar duplicidades.
 */

// ================= CONFIGURACIÓN GLOBAL =================
const CONFIG = {
  // Enlace oficial de la grabación (SharePoint UNIMINUTO)
  LINK_GRABACION: "https://uniminuto0-my.sharepoint.com/personal/felix_duenas_uniminuto_edu/_layouts/15/stream.aspx?id=%2Fpersonal%2Ffelix%5Fduenas%5Funiminuto%5Fedu%2FDocuments%2FGrabaciones%2FII%20FORO%20DE%20EDITORES%20DE%20REVISTAS%20CIENT%C3%8DFICAS%2D20260911%5F080635%2DGrabaci%C3%B3n%20de%20la%20reuni%C3%B3n%2Emp4&ga=1&referrer=StreamWebApp%2EWeb&referrerScenario=AddressBarCopied%2Eview%2E692c7bc5%2Df83b%2D4dbf%2D905d%2D7cb360d59b9e",
  
  // Nombre oficial del remitente
  NOMBRE_REMITENTE: "Comité Organizador - II Foro de Editores 2026",
  
  // URL base del repositorio para obtener los PDFs automáticamente
  BASE_PDF_URL: "https://raw.githubusercontent.com/juannietoval/certificaci-n-II-foro/main/output/pdf/",

  // ID opcional de carpeta de Google Drive si prefieres que busque ahí (opcional)
  ID_CARPETA_DRIVE: "",
  
  // Nombres de las hojas
  HOJA_PILOTO: "Piloto_Ponentes",
  HOJA_PRUEBA: "Prueba_Envio",
  HOJA_ASISTENTES: "Asistentes",
  HOJA_PONENTES: "Ponentes"
};

// ================= MENÚ SUPERIOR EN GOOGLE SHEETS =================
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu("Envío de Certificados")
    .addItem("1. Ejecutar PILOTO: Enviar 12 Ponentes a mi correo UTP", "enviarPilotoPonentes")
    .addItem("2. Enviar prueba específica (Juan UTP y Erika Gmail)", "enviarPruebaDosDestinatarios")
    .addSeparator()
    .addItem("3. Enviar a Ponentes (Correos reales pendientes)", "enviarPonentes")
    .addItem("4. Enviar a Asistentes (Correos reales pendientes)", "enviarAsistentes")
    .addSeparator()
    .addItem("5. Enviar a TODOS los pendientes", "enviarTodos")
    .addToUi();
}

// ================= DETECCIÓN DE GÉNERO (ESTIMADO / ESTIMADA) =================
function obtenerTratamiento(nombre) {
  if (!nombre) return "Estimado(a)";
  const nmLower = nombre.toString().trim().toLowerCase();
  
  if (nmLower.startsWith("dra.") || nmLower.startsWith("doctora")) return "Estimada";
  if (nmLower.startsWith("dr.") || nmLower.startsWith("doctor")) return "Estimado";

  const nombresFemeninos = [
    "erika", "maria", "maría", "nohelia", "zahira", "yesenia", "katherine",
    "elena", "ana", "lady", "veronica", "verónica", "carolina", "julia",
    "liseth", "melissa", "ester", "dahiana", "lina", "celina", "cinthya",
    "fátima", "fatima", "jorgelina", "dorelys", "doris", "fabiola", "mayra",
    "belkis", "katty", "eva", "diana", "andrea", "bertha", "giovana",
    "montserrat", "antonia", "myriam", "laura", "cristina", "araceli",
    "marcelina", "thailing", "alba", "elisa", "angie", "emma", "mariana",
    "isela", "ligia", "mariela", "cassandra", "karina", "wendolyne", "rocio",
    "rocío", "consuelo", "gloria", "patricia", "sandra", "claudia", "monica",
    "mónica", "paola", "martha", "marta", "luz", "carmen", "pilar", "mercedes",
    "guadalupe", "rosario", "concepcion", "concepción", "beatriz", "raquel",
    "ines", "inés", "astrid", "vanessa", "vanesa", "tatiana", "stephanie",
    "stefany", "natalia", "ximena", "sheyla", "nancy", "margarita", "leidy",
    "analia", "analía", "camila", "moncerrath"
  ];

  const limpio = nmLower.replace(/^(dr\.|dra\.|ing\.|lic\.|prof\.|profesor|profesora)\s+/, "");
  const partes = limpio.split(/\s+/);
  const primerNombre = partes[0] || "";
  
  if (nombresFemeninos.includes(primerNombre)) return "Estimada";
  if (partes.length > 1 && nombresFemeninos.includes(partes[1])) return "Estimada";
  
  if (primerNombre.endsWith("a") && !["alain", "alaín", "josue", "josué"].includes(primerNombre)) {
    return "Estimada";
  }
  
  return "Estimado";
}

// ================= ENVÍO DE PRUEBA A LOS 2 DESTINATARIOS =================
function enviarPruebaDosDestinatarios() {
  const ui = SpreadsheetApp.getUi();
  const resp = ui.alert(
    "Confirmación de Envío de Prueba",
    "Se enviarán 2 correos institucionales de prueba con el certificado PDF adjunto:\n\n" +
    "1. Asistente: juan.nieto2@utp.edu.co (Juan Esteban Nieto Valencia)\n" +
    "2. Ponente: juanestebannietovalencia@gmail.com (Erika Betancourt)\n\n" +
    "¿Desea proceder con el envío de prueba?",
    ui.ButtonSet.YES_NO
  );

  if (resp !== ui.Button.YES) return;

  let exitos = 0;
  let errores = [];

  // 1. Asistente: Juan Esteban Nieto Valencia
  try {
    const datosAsistente = {
      id: "FORO26-ASI-012",
      nombre: "Juan Esteban Nieto Valencia",
      email: "juan.nieto2@utp.edu.co",
      rol: "ASISTENTE",
      asunto: "Certificado Oficial de Asistencia y Grabación - II Foro de Editores de Revistas Científicas 2026",
      tema: "Gestión editorial en tiempos de inteligencia artificial",
      urlVerificacion: "https://juannietoval.github.io/certificaci-n-II-foro/?id=FORO26-ASI-012"
    };
    enviarCorreo(datosAsistente);
    exitos++;
  } catch (e) {
    errores.push("juan.nieto2@utp.edu.co: " + e.message);
  }

  // 2. Ponente: Erika Betancourt
  try {
    const datosPonente = {
      id: "FORO26-PON-006",
      nombre: "Erika Betancourt",
      email: "juanestebannietovalencia@gmail.com",
      rol: "PONENTE",
      asunto: "Certificado Oficial de Ponente y Grabación - II Foro de Editores de Revistas Científicas 2026",
      ponencia: "Presentación de la Revista Miradas",
      eje: "Socialización de Revistas Científicas",
      institucion: "Universidad Tecnológica de Pereira",
      urlVerificacion: "https://juannietoval.github.io/certificaci-n-II-foro/?id=FORO26-PON-006"
    };
    enviarCorreo(datosPonente);
    exitos++;
  } catch (e) {
    errores.push("juanestebannietovalencia@gmail.com: " + e.message);
  }

  if (errores.length === 0) {
    ui.alert(
      "Prueba Completada",
      "Los dos correos fueron enviados exitosamente con su archivo PDF adjunto:\n\n" +
      "- juan.nieto2@utp.edu.co (Estimado Juan Esteban Nieto Valencia)\n" +
      "- juanestebannietovalencia@gmail.com (Estimada Erika Betancourt)\n\n" +
      "Por favor verifique las bandejas de entrada correspondientes.",
      ui.ButtonSet.OK
    );
  } else {
    ui.alert("Aviso de Envío", "Enviados: " + exitos + "\nErrores:\n" + errores.join("\n"), ui.ButtonSet.OK);
  }
}

// ================= ENVÍOS MASIVOS Y PILOTO POR PESTAÑAS =================
function enviarPilotoPonentes() {
  procesarHoja(CONFIG.HOJA_PILOTO || "Piloto_Ponentes", "PONENTE");
}

function enviarAsistentes() {
  procesarHoja(CONFIG.HOJA_ASISTENTES, "ASISTENTE");
}

function enviarPonentes() {
  procesarHoja(CONFIG.HOJA_PONENTES, "PONENTE");
}

function enviarTodos() {
  procesarHoja(CONFIG.HOJA_PONENTES, "PONENTE");
  procesarHoja(CONFIG.HOJA_ASISTENTES, "ASISTENTE");
}

function procesarHoja(nombreHoja, tipoRol) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(nombreHoja);
  const ui = SpreadsheetApp.getUi();
  
  if (!sheet) {
    ui.alert("No se encontró la pestaña llamada '" + nombreHoja + "'.");
    return;
  }

  const data = sheet.getDataRange().getValues();
  if (data.length <= 1) {
    ui.alert("La hoja '" + nombreHoja + "' no contiene registros.");
    return;
  }

  const headers = data[0];
  const colId = headers.indexOf("Código Certificado");
  const colNombre = headers.indexOf("Nombre Completo") !== -1 ? headers.indexOf("Nombre Completo") : headers.indexOf("Nombre Ponente");
  let colEmail = headers.indexOf("Correo Envío Piloto (Prueba)");
  if (colEmail === -1) {
    colEmail = headers.indexOf("Correo Electrónico") !== -1 ? headers.indexOf("Correo Electrónico") : headers.indexOf("Correo");
  }
  const colVerif = headers.indexOf("Enlace Verificación QR") !== -1 ? headers.indexOf("Enlace Verificación QR") : headers.indexOf("Enlace Validación Web (QR)");
  const colPonencia = headers.indexOf("Ponencia Magistral Presentada");
  const colEje = headers.indexOf("Eje Temático");
  
  let colEstado = headers.indexOf("Estado Envío");
  if (colEstado === -1) {
    colEstado = headers.length;
    sheet.getRange(1, colEstado + 1).setValue("Estado Envío").setFontWeight("bold");
  }

  let pendientes = 0;
  for (let i = 1; i < data.length; i++) {
    const estado = data[i][colEstado] || "";
    const email = colEmail !== -1 ? data[i][colEmail] : "";
    if (!estado.toString().startsWith("ENVIADO") && email && email.toString().includes("@")) {
      pendientes++;
    }
  }

  if (pendientes === 0) {
    ui.alert("Todos los correos de '" + nombreHoja + "' ya están registrados como enviados.");
    return;
  }

  const confirmacion = ui.alert(
    "Confirmación de Envío - " + nombreHoja,
    "Se enviarán " + pendientes + " correos institucionales con certificado PDF adjunto en '" + nombreHoja + "'.\n\n¿Desea iniciar el proceso?",
    ui.ButtonSet.YES_NO
  );
  if (confirmacion !== ui.Button.YES) return;

  let enviados = 0;
  let errores = 0;

  for (let i = 1; i < data.length; i++) {
    const fila = data[i];
    const estadoActual = fila[colEstado] || "";
    const email = colEmail !== -1 ? fila[colEmail].toString().trim() : "";
    const id = colId !== -1 ? fila[colId].toString().trim() : "";
    const nombre = colNombre !== -1 ? fila[colNombre].toString().trim() : "";
    const urlVerif = colVerif !== -1 ? fila[colVerif].toString().trim() : "";
    const ponencia = colPonencia !== -1 ? fila[colPonencia].toString().trim() : "";
    const eje = colEje !== -1 ? fila[colEje].toString().trim() : "";

    if (estadoActual.toString().startsWith("ENVIADO") || !email || !email.includes("@")) {
      continue;
    }

    const asunto = (tipoRol === "PONENTE")
      ? "Certificado Oficial de Ponente y Grabación - II Foro de Editores de Revistas Científicas 2026"
      : "Certificado Oficial de Asistencia y Grabación - II Foro de Editores de Revistas Científicas 2026";

    const payload = {
      id: id,
      nombre: nombre,
      email: email,
      rol: tipoRol,
      asunto: asunto,
      ponencia: ponencia,
      eje: eje,
      urlVerificacion: urlVerif || ("https://juannietoval.github.io/certificaci-n-II-foro/?id=" + id)
    };

    try {
      enviarCorreo(payload);
      const timestamp = Utilities.formatDate(new Date(), "GMT-5", "yyyy-MM-dd HH:mm");
      sheet.getRange(i + 1, colEstado + 1).setValue("ENVIADO (" + timestamp + ")").setFontColor("#059669");
      enviados++;
    } catch (e) {
      sheet.getRange(i + 1, colEstado + 1).setValue("ERROR: " + e.message).setFontColor("#dc2626");
      errores++;
    }

    Utilities.sleep(300);
  }

  ui.alert("Proceso Finalizado", "Enviados: " + enviados + "\nErrores: " + errores, ui.ButtonSet.OK);
}

// ================= CONSTRUCTOR Y ENVÍO DE CORREO =================
function enviarCorreo(datos) {
  const esPonente = (datos.rol === "PONENTE");
  const asunto = datos.asunto || "Certificado Oficial y Grabación - II Foro de Editores de Revistas Científicas 2026";
  const tratamiento = obtenerTratamiento(datos.nombre);

  let bloqueRol = "";
  if (esPonente) {
    bloqueRol = `
      <p style="font-size: 15px; color: #334155; line-height: 1.6; margin: 0 0 16px 0;">
        Agradecemos profundamente su valiosa contribución como <strong>Ponente</strong> con la presentación de la conferencia magistral:
      </p>
      <div style="background-color: #f8fafc; border-left: 4px solid #b89047; padding: 14px 18px; margin: 18px 0; border-radius: 4px;">
        <p style="margin: 0; font-size: 15px; font-weight: 600; color: #0b223d; font-style: italic;">
          &laquo;${datos.ponencia || 'Ponencia Magistral'}&raquo;
        </p>
        ${datos.eje ? `<p style="margin: 6px 0 0 0; font-size: 13px; color: #64748b;">Eje Temático: <strong>${datos.eje}</strong></p>` : ''}
        ${datos.institucion ? `<p style="margin: 2px 0 0 0; font-size: 13px; color: #64748b;">${datos.institucion}</p>` : ''}
      </div>
    `;
  } else {
    bloqueRol = `
      <p style="font-size: 15px; color: #334155; line-height: 1.6; margin: 0 0 16px 0;">
        Agradecemos sinceramente su asistencia y participación en el <strong>II Foro de Editores de Revistas Científicas: <em>«Gestión editorial en tiempos de inteligencia artificial»</em></strong>, llevado a cabo el pasado 11 de septiembre de 2026.
      </p>
    `;
  }

  const htmlBody = `
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 24px; background-color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 620px; background-color: #ffffff; border-radius: 6px; overflow: hidden; box-shadow: 0 4px 14px rgba(11, 34, 61, 0.08); border: 1px solid #e2e8f0;">
        
        <!-- ENCABEZADO INSTITUCIONAL -->
        <tr>
          <td style="background-color: #0b223d; padding: 30px 24px; text-align: center; border-bottom: 3px solid #b89047;">
            <div style="font-size: 11px; font-weight: 700; color: #b89047; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px;">
              CONSTANCIA OFICIAL DE PARTICIPACIÓN
            </div>
            <h1 style="color: #ffffff; font-size: 20px; margin: 0; font-weight: 700; line-height: 1.3;">
              II FORO DE EDITORES DE REVISTAS CIENTÍFICAS
            </h1>
            <p style="color: #cbd5e1; font-size: 14px; font-style: italic; margin: 6px 0 0 0;">
              &laquo;Gestión editorial en tiempos de inteligencia artificial&raquo;
            </p>
          </td>
        </tr>

        <!-- CUERPO PRINCIPAL -->
        <tr>
          <td style="padding: 32px 30px;">
            <p style="font-size: 16px; color: #0b223d; font-weight: 700; margin: 0 0 16px 0;">
              ${tratamiento} ${datos.nombre}:
            </p>

            ${bloqueRol}

            <p style="font-size: 15px; color: #334155; line-height: 1.6; margin: 0 0 18px 0;">
              Adjunto a este correo encontrará su <strong>certificado oficial en formato PDF</strong> debidamente emitido con código de registro alfanumérico y código QR de validación institucional.
            </p>

            <!-- CAJA DE DOCUMENTO ADJUNTO -->
            <div style="background-color: #fdfaf3; border: 1px solid #b89047; border-radius: 4px; padding: 14px 18px; margin: 0 0 20px 0;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="vertical-align: middle;">
                    <div style="font-size: 10.5px; font-weight: 700; color: #8C6D3B; text-transform: uppercase; letter-spacing: 1px;">
                      DOCUMENTO ADJUNTO (PDF)
                    </div>
                    <div style="font-size: 14px; font-weight: 700; color: #0b223d; margin-top: 2px;">
                      certificado - ${datos.nombre}.pdf
                    </div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 2px;">
                      Código Único: <strong>${datos.id}</strong>
                    </div>
                  </td>
                  <td style="text-align: right; vertical-align: middle;">
                    <a href="${datos.urlVerificacion}" target="_blank" style="display: inline-block; background-color: #0b223d; color: #ffffff; text-decoration: none; padding: 9px 16px; font-size: 12px; font-weight: 600; border-radius: 3px;">
                      Consultar en Portal Web
                    </a>
                  </td>
                </tr>
              </table>
            </div>

            <p style="font-size: 15px; color: #334155; line-height: 1.6; margin: 0 0 16px 0;">
              Asimismo, ponemos a su disposición el enlace oficial para consultar la <strong>grabación completa de la jornada académica</strong> en Microsoft Stream:
            </p>

            <!-- BOTÓN DE GRABACIÓN -->
            <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 4px; padding: 16px 18px; margin: 0 0 24px 0; text-align: center;">
              <div style="font-size: 10.5px; font-weight: 700; color: #0b223d; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">
                MEMORIAS EN VIDEO • SESIÓN COMPLETA
              </div>
              <a href="${CONFIG.LINK_GRABACION}" target="_blank" style="display: inline-block; background-color: #059669; color: #ffffff; text-decoration: none; padding: 11px 24px; font-size: 13.5px; font-weight: 600; border-radius: 3px;">
                Acceder a la Grabación de la Reunión
              </a>
            </div>

            <!-- NOTA DE SEGURIDAD -->
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 14px 18px; margin: 0 0 20px 0;">
              <p style="margin: 0; font-size: 12.5px; color: #64748b; line-height: 1.5;">
                <strong>Verificación de autenticidad:</strong> Su certificado puede ser validado en cualquier momento escaneando el código QR incorporado en el documento o ingresando al enlace directo:<br>
                <a href="${datos.urlVerificacion}" style="color: #0b223d; word-break: break-all;">${datos.urlVerificacion}</a>
              </p>
            </div>

            <!-- FIRMA INSTITUCIONAL -->
            <div style="margin-top: 28px; border-top: 1px solid #e2e8f0; padding-top: 20px; text-align: center;">
              <p style="margin: 0; font-size: 13.5px; font-style: italic; color: #64748b;">Atentamente,</p>
              <p style="margin: 4px 0 2px 0; font-size: 14px; font-weight: 700; color: #0b223d; letter-spacing: 0.5px;">
                COMITÉ ORGANIZADOR
              </p>
              <p style="margin: 0; font-size: 12px; color: #64748b;">
                Coordinación General del Evento
              </p>
              <p style="margin: 6px 0 0 0; font-size: 12px; font-weight: 700; color: #b89047; letter-spacing: 1px;">
                UNIMINUTO &bull; IBERO &bull; UTP
              </p>
            </div>

          </td>
        </tr>

        <!-- PIE DE PÁGINA -->
        <tr>
          <td style="background-color: #f8fafc; padding: 16px 20px; text-align: center; border-top: 1px solid #e2e8f0;">
            <p style="margin: 0; font-size: 11.5px; color: #94a3b8; line-height: 1.4;">
              Mensaje oficial emitido por la Coordinación General del II Foro de Editores de Revistas Científicas 2026.<br>
              Pereira, Colombia — Viernes 11 de septiembre de 2026.
            </p>
          </td>
        </tr>

      </table>
    </body>
    </html>
  `;

  const plainText = `${tratamiento} ${datos.nombre}:\n\n` +
    `Adjunto a este correo encontrará su certificado oficial en formato PDF para el II Foro de Editores de Revistas Científicas 2026.\n\n` +
    `Código de verificación: ${datos.id}\n` +
    `Verificación en portal web: ${datos.urlVerificacion}\n` +
    `Grabación oficial de la reunión: ${CONFIG.LINK_GRABACION}\n\n` +
    `Atentamente,\nCOMITÉ ORGANIZADOR\nCoordinación General del Evento\nUNIMINUTO • IBERO • UTP`;

  const emailOptions = {
    htmlBody: htmlBody,
    name: CONFIG.NOMBRE_REMITENTE,
    attachments: []
  };

  // Obtener y adjuntar el archivo PDF automáticamente
  try {
    const cleanName = datos.nombre.replace(/[\/\\:\*\?"<>\|]/g, '').trim().replace(/\s+/g, '_');
    const remotePdfUrl = CONFIG.BASE_PDF_URL + encodeURIComponent(datos.id + "_" + cleanName + ".pdf");
    
    const resp = UrlFetchApp.fetch(remotePdfUrl, { muteHttpExceptions: true });
    if (resp.getResponseCode() === 200) {
      const pdfBlob = resp.getBlob().setName(`certificado - ${datos.nombre}.pdf`);
      emailOptions.attachments.push(pdfBlob);
    } else if (CONFIG.ID_CARPETA_DRIVE) {
      const carpeta = DriveApp.getFolderById(CONFIG.ID_CARPETA_DRIVE);
      const archivos = carpeta.getFilesByName(`certificado - ${datos.nombre}.pdf`);
      if (archivos.hasNext()) {
        emailOptions.attachments.push(archivos.next().getAs(MimeType.PDF));
      }
    }
  } catch (e) {
    Logger.log("Aviso en adjunto de PDF: " + e.message);
  }

  GmailApp.sendEmail(datos.email, asunto, plainText, emailOptions);
}
