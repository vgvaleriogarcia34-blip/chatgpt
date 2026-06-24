# ⚙️ Capa de automatización (Make)

El cerebro del becario vive en Claude Code, pero para que trabaje **por ti 24/7** —sin que tú
abras nada— usamos **Make** como motor de disparadores y de mensajería.

## Qué automatizamos

| Escenario | Disparador | Acción |
|---|---|---|
| **Propuestas diarias por WhatsApp** | Cada mañana a una hora fija | El becario genera propuestas y te envía el resumen por WhatsApp. Ver [`canal-whatsapp.md`](./canal-whatsapp.md). |
| **Alerta de oportunidad** | Email entrante de un lead / cliente clave | El becario analiza y te avisa con la acción sugerida. |
| **Reunión sin acta** | Fin de evento de Calendar con grabación Plaud | El becario prepara el borrador de acta. |
| **Renovación próxima** | Deal de HubSpot con fecha cercana | El becario te propone el plan de renovación. |

## Principio de seguridad
Todos los escenarios respetan **propone, tú apruebas**: Make entrega *propuestas* y *borradores*;
el envío/cierre real solo ocurre tras tu OK (por WhatsApp o en el chat).

## Estado
- **Diseño:** listo (en este directorio).
- **Activación:** requiere conectar en Make tus cuentas (WhatsApp Business, Gmail, HubSpot…).
  El becario no activa ningún escenario sin tu confirmación de conexiones.

## Cómo activarlos
Dile al becario *"activa el escenario de propuestas por WhatsApp"* una vez tengas conectado tu
número en Make. El becario construirá el escenario (vía las herramientas de Make) y te pedirá
revisar antes de ponerlo en marcha.
