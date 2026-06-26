# 08 · Procedimiento de gestión de brechas de seguridad

> Una "violación de la seguridad de los datos" (brecha) es cualquier incidente que provoque
> destrucción, pérdida, alteración o acceso/comunicación no autorizada de datos personales.
> El RGPD obliga a **notificar a la AEPD en 72 h** (art. 33) y, si hay alto riesgo para las
> personas, **comunicárselo a los afectados** (art. 34).

---

## 1. Qué hacer cuando se detecta una brecha (cronómetro: 72 h)

1. **Contener** (paso 0, inmediato): cortar el acceso, cambiar contraseñas, aislar el equipo.
2. **Registrar** el incidente (§4) con hora de detección.
3. **Evaluar el riesgo** para los derechos de las personas (¿qué datos?, ¿cuántos?, ¿sensibles?,
   ¿cifrados?, ¿quién accedió?).
4. **Decidir notificación:**
   - **A la AEPD** (sede electrónica) en **≤ 72 h** desde que se tiene constancia, **salvo** que
     sea **improbable** que suponga un riesgo. Si se pasa de 72 h, justificar el retraso.
   - **A los afectados** "sin dilación indebida" si el riesgo es **alto** (p. ej. fuga de datos
     financieros sin cifrar).
5. **Mitigar y documentar** medidas correctoras.
6. **Registrar** todo el proceso (obligatorio aunque no se notifique).

---

## 2. Criterio rápido de notificación

| Situación | ¿Notificar AEPD? | ¿Avisar afectados? |
|---|---|---|
| Datos cifrados/anonimizados perdidos | Probablemente no | No |
| Acceso no autorizado a expedientes financieros | **Sí** | **Probablemente sí** |
| Email con datos enviado a destinatario erróneo (pocos datos) | Valorar | Según riesgo |
| Pérdida de portátil con disco cifrado y bloqueo | Probablemente no | No |
| Ransomware con datos personales | **Sí** | Según riesgo |

> Ante la duda, **documentar siempre** y consultar el criterio de la AEPD / asesor.

---

## 3. Contactos de emergencia

| Rol | Persona | Contacto |
|---|---|---|
| Responsable interno de privacidad | `[Valerio García]` | `[contacto]` |
| Asesor externo / DPO | `[PENDIENTE]` | `[contacto]` |
| Soporte IT | `[PENDIENTE]` | `[contacto]` |
| AEPD (sede electrónica) | — | sede.aepd.gob.es |

---

## 4. Registro de brechas (obligatorio — art. 33.5)

| Fecha detección | Descripción | Datos/afectados | Riesgo | ¿Notificada AEPD? | ¿Afectados? | Medidas |
|---|---|---|---|---|---|---|
| | | | | | | |

> Este registro debe mantenerse **aunque la brecha no se notifique**, para poder demostrar la
> decisión ante la AEPD.
