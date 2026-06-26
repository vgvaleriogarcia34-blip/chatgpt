# 03 · Medidas de seguridad técnicas y organizativas

> El art. 32 RGPD obliga a aplicar medidas **apropiadas al riesgo**. Dado que se tratan datos
> financieros y grabaciones (riesgo alto), las medidas deben ser **reforzadas**. Este documento
> es a la vez el **Documento de Seguridad** de referencia (buena práctica, heredada de la antigua
> LOPD) y la base del cumplimiento del principio de **integridad y confidencialidad** (art. 5.1.f).

---

## 1. Medidas ORGANIZATIVAS

| Medida | Estado | Responsable |
|---|---|---|
| Designar Responsable Interno de Privacidad | `[PENDIENTE]` | Valerio |
| Deber de secreto firmado por todo el que accede a datos | `[PENDIENTE]` (doc. 10) | Valerio |
| Política de mesas limpias y bloqueo de sesión | A implantar | Todos |
| Política de contraseñas robustas + gestor de contraseñas | `[VERIFICAR]` | Todos |
| Formación básica en protección de datos | `[PENDIENTE]` (doc. 10) | Valerio |
| Procedimiento de altas/bajas de accesos | A implantar | Valerio |
| Inventario de dispositivos que acceden a datos | `[PENDIENTE]` | Valerio |
| Revisión anual del plan | Anual | Valerio |

---

## 2. Medidas TÉCNICAS

### Control de acceso
- **Autenticación multifactor (MFA/2FA)** en Google Workspace, HubSpot, Plaud, Make, Canva.
- **Mínimo privilegio:** cada persona accede solo a las carpetas/expedientes que necesita.
- Permisos de **Google Drive por carpeta de cliente** (no compartir carpetas raíz).
- Cuentas **nominativas** (no compartir usuario/contraseña).

### Cifrado
- **Cifrado de disco** en todos los equipos (BitLocker/FileVault).
- Datos en tránsito siempre por **HTTPS/TLS**.
- Cifrar/proteger con contraseña los ficheros financieros especialmente sensibles.

### Copias de seguridad y continuidad
- Google Workspace mantiene redundancia; aun así, **exportación periódica** de expedientes
  críticos. `[VERIFICAR política de backup]`
- Verificar que las copias **se pueden restaurar** (prueba periódica).

### Trazabilidad
- Activar **registros de actividad/auditoría** en Google Workspace y HubSpot.
- Revisar accesos sospechosos periódicamente.

### Dispositivos y red
- Antivirus/EDR actualizado, sistema operativo y apps al día.
- Bloqueo automático de pantalla y borrado remoto en móviles/portátiles.
- Evitar redes WiFi públicas sin VPN para acceder a datos.

---

## 3. Medidas específicas por foco de riesgo

### Datos financieros de personas físicas (Tratamiento 01)
- Acceso restringido al mínimo de personas.
- Carpeta dedicada con permisos cerrados; no compartir por email sin cifrar.
- Borrado seguro al cumplir el plazo de conservación.

### Grabaciones Plaud (Tratamiento 03)
- **Informar/consentir antes de grabar** (cláusula doc. 05).
- Borrar el **audio original** una vez generada el acta (minimización).
- Acceso a transcripciones restringido al equipo del proyecto.

### Encargados / IA
- No introducir en herramientas de IA datos identificables que no sean necesarios.
- Verificar garantías de cada proveedor (doc. 09).

---

## 4. Verificación

Checklist de seguridad a revisar **cada 6–12 meses**; cualquier hallazgo se trata como mejora o,
si implica acceso indebido, como posible **brecha** (doc. 08).
