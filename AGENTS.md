# Reglas del Sistema de Automatizacion de Certificados

## 1. Identidad Visual y Estandares de Diseno
- Formato: A4 Horizontal (Landscape) - 297mm x 210mm (proporcion 1.414).
- Referencia Maestra: La plantilla aprobada en assets/template.jpg.
- Logos Institucionales: Inclusion y Desarrollo, Horizontes Pedagogicos, Miradas (UTP). No alterar ni mover.
- Paleta de Colores:
  - Azul Institucional / Indigo: #0f2b48 / #16325c
  - Acento Dorado / Mostaza: #b89047 / #c49a45
  - Fondo Marfil: Textura natural del diseno master
  - Texto Secundario / Cuerpo: #2c3e50 / #333333

## 2. Campos Dinamicos
- id: Codigo alfanumerico unico (ej. FORO26-PON-001).
- nombre: Nombre completo del ponente o asistente.
- rol: Rol en el evento (PONENTE, ASISTENTE, MODERADOR, ORGANIZADOR).
- titulo: Titulo de la ponencia academica.
- eje: Eje tematico del foro.
- institucion: Universidad o institucion de afiliacion.
- pais: Pais de origen.
- fecha: Fecha de emision.
- ciudad: Ciudad sede.

## 3. Codigo QR y Verificacion
- Todo certificado debe portar su codigo QR en el recuadro inferior derecho.
- El QR debe codificar una URL valida y escaneable al endpoint publico de verificacion.
- Bajo el recuadro debe indicarse el ID legible.

## 4. Control de Calidad
- Sin desbordamiento: Ajuste automatico de tamano de fuente para nombres o titulos extensos.
- Salida: Archivos PDF individuales A4 listos para impresion a 300 DPI y nombramiento estandarizado.
