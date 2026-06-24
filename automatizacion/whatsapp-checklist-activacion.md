# ✅ Checklist de activación del canal WhatsApp

Sigue estos pasos en orden. Cuando los marques todos, dime **"activa el canal WhatsApp"** y
construyo los escenarios en Make.

## Bloque 1 — Acceso a Make desde Claude (lo habilitas tú)
- [ ] Las herramientas de Make (`mcp__…Make…`) requieren aprobación. Acéptalas en los permisos
      de la sesión, **o** ejecuta este paso desde Claude Code en tu equipo (donde aparece el
      diálogo de aprobación de MCP).
- [ ] Verifica que el Becario puede listar tus conexiones de Make sin error.

## Bloque 2 — Conexión de WhatsApp Business (lo haces tú una vez)
- [ ] Tener una **cuenta de WhatsApp Business** y acceso a **Meta for Developers**.
- [ ] Activar **WhatsApp Business Cloud API** y obtener: `Phone Number ID` + `Access Token`.
- [ ] En **Make → Connections**, crear conexión **WhatsApp Business Cloud** con esos datos.
- [ ] Anotar tu **número de destino** (tu móvil) en `perfil/sobre-mi.md`.

## Bloque 3 — Construcción (lo hago yo, con tu OK)
- [ ] El Becario crea el **Escenario A** (envío de propuestas, programado).
- [ ] El Becario crea el **Escenario B** (recepción y lectura de tu respuesta).
- [ ] Prueba de humo: te llega un mensaje de test y tu "1 sí" se registra bien.
- [ ] Pones la hora de entrega diaria (p.ej. 08:00) y activas los escenarios.

## Alternativa más rápida (si no quieres la Cloud API de Meta)
Si montar la Cloud API se te hace cuesta arriba, hay dos atajos:
- **Make + Twilio (WhatsApp)**: conexión más sencilla, mismo flujo. *(De pago por mensaje.)*
- **Telegram en vez de WhatsApp**: conector directo y gratuito en Make; si te vale Telegram,
  el canal se activa en minutos. Dímelo y adapto el diseño.

---
> Mientras esto no esté, el Becario te entrega las propuestas **aquí en el chat** con el mismo
> formato numerado (ver `whatsapp-plantilla-mensaje.md`), así que no pierdes nada de tiempo.
