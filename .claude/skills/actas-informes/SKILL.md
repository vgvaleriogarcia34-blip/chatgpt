---
name: actas-informes
description: Genera actas de reunión e informes profesionales a partir de los datos del jefe. Úsalo cuando pida "haz el acta de la reunión", "pásame a limpio esta reunión de Plaud", "genérame un informe de X", "resume estos documentos", o tras detectar una reunión sin acta. Toma transcripciones (Plaud), notas o datos (Drive, CRM) y produce documentos claros, accionables y presentables (Canva si hace falta).
---

# 📝 Actas e informes

Convierte conversaciones y datos en documentos útiles: actas accionables e informes con criterio.

## A) Actas de reunión

### Fuente
- Transcripción de **Plaud** (`get_transcript` / `get_note`), notas del jefe, o el evento de Calendar.

### Estructura del acta
1. **Encabezado:** título, fecha, asistentes, objetivo de la reunión.
2. **Resumen ejecutivo:** 3–5 líneas con lo esencial.
3. **Temas tratados:** por bloques.
4. **Decisiones tomadas.**
5. **Tareas / próximos pasos:** responsable + fecha (formato accionable).
6. **Puntos abiertos / a seguir.**

### Tras aprobación
- Guarda el acta en Drive (`create_file`).
- Crea las tareas/eventos de seguimiento en Calendar.
- Si hay acuerdos con un cliente, refleja el cambio en HubSpot.

## B) Informes

### Tipos habituales
- Informe de cliente (estado, histórico, oportunidades).
- Informe de competencia (apóyate en `analisis-competencia`).
- Informe de actividad / resultados (cruza CRM + Calendar + Gmail).

### Principios
- **Empieza por la conclusión** (qué significan los datos, no solo los datos).
- Apoya cada afirmación en un dato real y su fuente.
- Termina con **recomendaciones accionables**.

### Entregable
- Markdown en `propuestas/` o Drive por defecto.
- Si el jefe quiere algo presentable (cliente/dirección), genera versión en **Canva**.

## Reglas
- Fiel a la fuente: no pongas en boca de nadie lo que no dijo. Marca lo dudoso.
- Accionable siempre: un acta sin "próximos pasos" está incompleta.
- Confidencialidad de lo tratado.
