# Sistema de Certificaci?n Acad?mica y Portal de Verificaci?n Digital
### II Foro de Editores de Revistas Cient?ficas

Plataforma integral y automatizada para la emisi?n, validaci?n y consulta de certificados acad?micos con c?digo QR verificable en tiempo real.

---

## ?? Portal de Verificaci?n en L?nea (GitHub Pages)

El portal de verificaci?n oficial se encuentra disponible p?blicamente en:
?? **[https://juannietoval.github.io/certificaci-n-II-foro/](https://juannietoval.github.io/certificaci-n-II-foro/)**

### ?C?mo funciona la verificaci?n?
1. Cada participante cuenta con un certificado oficial en formato PDF A4 horizontal con un c?digo QR ?nico (ej. `FORO26-PON-001`).
2. Al escanear el c?digo QR con cualquier smartphone o acceder al enlace con el par?metro `?id=FORO26-PON-001`:
   - El sistema valida inmediatamente la autenticidad en la base institucional.
   - Presenta el escudo de verificaci?n: **? CERTIFICADO OFICIAL V?LIDO Y AUT?NTICO**.
   - Muestra todos los datos acreditados: Nombre, Rol (Ponente/Asistente), Ponencia magistral, Eje tem?tico, Universidad de origen y Fecha.
   - Permite visualizar o descargar el certificado oficial original en PDF.

---

## ?? Estructura del Repositorio

```text
.
??? index.html               # Portal web p?blico de verificaci?n (GitHub Pages)
??? AGENTS.md                # Est?ndares de dise?o y reglas del sistema
??? assets/
?   ??? template.jpg         # Plantilla visual maestra de referencia
?   ??? qrcode.min.js        # Librer?a aut?noma para generaci?n de QR offline
??? data/
?   ??? participantes.json   # Base de datos de asistentes y ponentes
??? output/
?   ??? pdf/                 # Certificados individuales en PDF listos para imprimir
?   ??? preview/             # Vistas previas en alta resoluci?n
??? scripts/
?   ??? generator.py         # Motor de renderizado automatizado
??? templates/               # Plantillas HTML/CSS por participante
```

---

## ?? Generaci?n de Certificados

Para generar o actualizar certificados:
```bash
python scripts/generator.py
```
El motor genera en segundos los archivos PDF vectoriales en `output/pdf/` y actualiza los c?digos QR con redirecci?n autom?tica al portal web.
