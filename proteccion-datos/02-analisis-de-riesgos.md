# 02 · Análisis de riesgos, EIPD y DPO

> El RGPD exige un enfoque de **responsabilidad proactiva** (art. 24) basado en el **riesgo**.
> Aquí se valora el riesgo de cada tratamiento, si procede una **Evaluación de Impacto (EIPD,
> art. 35)** y si es obligatorio un **Delegado de Protección de Datos (DPO, art. 37)**.

---

## 1. Metodología

Riesgo = **Probabilidad × Impacto** sobre los derechos y libertades de las personas.
Escala: Bajo 🟢 · Medio 🟡 · Alto 🔴.

---

## 2. Mapa de riesgos por tratamiento

| Tratamiento | Datos sensibles | Probabilidad | Impacto | Riesgo |
|---|---|---|---|---|
| 01 Clientes | Económico-financieros de personas físicas | Media | Alto | 🔴 Alto |
| 02 Prospectos | Profesionales | Media | Bajo | 🟢 Bajo |
| 03 Grabaciones Plaud | Voz + contenido | Media | Alto | 🔴 Alto |
| 04 Personal | Laborales/pago | Baja | Medio | 🟡 Medio |
| 05 Proveedores | Bancarios | Baja | Medio | 🟡 Medio |
| 06 Web/cookies | Navegación | Media | Bajo | 🟢 Bajo |

**Focos rojos:** (1) datos financieros de familias y (2) grabaciones de reuniones.

---

## 3. Principales riesgos identificados y mitigación

| Riesgo | Mitigación (ver doc. 03) |
|---|---|
| Acceso no autorizado a expedientes financieros en Drive | Permisos por carpeta, MFA, cifrado, mínimo privilegio |
| Fuga por dispositivo perdido/robado | Cifrado de disco, bloqueo, borrado remoto |
| Grabar a asistentes sin informarles | Cláusula y aviso **antes** de grabar (doc. 05) |
| Transferencia internacional sin garantías | Verificar DPA + cláusulas tipo de cada proveedor (doc. 09) |
| Conservación excesiva (audios, leads viejos) | Política de borrado y minimización |
| Suplantación al ejercer derechos | Verificación de identidad (doc. 07) |
| Brecha no notificada en plazo | Procedimiento de 72 h (doc. 08) |
| Encargado sin contrato (art. 28) | Recopilar/firmar DPA de cada proveedor (doc. 09) |
| IA: datos enviados a terceros sin control | Revisar políticas del proveedor IA; no introducir datos identificables innecesarios |

---

## 4. ¿Hace falta una Evaluación de Impacto (EIPD)?

La EIPD es obligatoria cuando el tratamiento **probablemente entrañe un alto riesgo** (art. 35).
La **AEPD** publica una lista de tratamientos que la requieren. Señales en este negocio:

- ✅ **Evaluación/scoring o perfilado** con efectos sobre las personas → análisis financiero de
  familias con apoyo de **IA**.
- ✅ **Tratamiento a gran escala** de datos de naturaleza sensible/altamente personal
  (financieros) — *a valorar según volumen real*. `[VERIFICAR volumen]`
- ✅ Uso de **nuevas tecnologías** (IA) para tratar datos personales.
- ✅ **Grabaciones sistemáticas** de reuniones.

> **Conclusión:** es **recomendable realizar una EIPD** centrada en el tratamiento de **datos
> financieros de personas físicas con apoyo de IA** y, secundariamente, en las **grabaciones
> Plaud**. No es un trámite menor: conviene apoyarse en plantilla AEPD (herramienta *Gestiona
> EIPD* / *Facilita RGPD*) y validación jurídica.
> **Acción en checklist.** Marcado como entregable a desarrollar si confirmas el volumen.

---

## 5. ¿Hace falta un Delegado de Protección de Datos (DPO)?

El DPO es obligatorio (art. 37 RGPD + art. 34 LOPDGDD) si:
- Es una autoridad/organismo público → **No**.
- La actividad principal es **observación habitual y sistemática a gran escala** → **No**.
- La actividad principal es el tratamiento **a gran escala de categorías especiales** (art. 9)
  o datos penales → **No** (no se tratan categorías especiales como núcleo).

> **Conclusión:** el DPO **no parece obligatorio**. No obstante, dada la sensibilidad financiera
> y el uso de IA, se **recomienda designar un Responsable Interno de Privacidad** (puede ser
> Valerio) y, opcionalmente, contar con asesor externo de protección de datos. Si se designa,
> debe constar y comunicarse a la AEPD.

---

## 6. Revisión

Este análisis se revisa **anualmente** y ante cualquier cambio relevante (nueva herramienta,
nuevo tipo de proyecto con datos sensibles, incidente de seguridad).
