# 📱 Canal WhatsApp — Recibir y aprobar propuestas

Quieres recibir las propuestas del becario **por WhatsApp** y poder aprobarlas desde ahí.
No existe un conector directo de WhatsApp, así que el canal se monta con **Make + WhatsApp
Business Cloud API**. Aquí está el diseño y los pasos de activación.

## Cómo funcionará (flujo)

```
  ┌─────────────┐   genera     ┌──────────────┐   envía WhatsApp   ┌──────────┐
  │  Becario    │ ───────────▶ │  propuestas/ │ ─────────────────▶ │   Tú     │
  │  (proponer- │   resumen    │  (archivo)   │   resumen + "1 sí" │ (móvil)  │
  │   tareas)   │              └──────────────┘                    └────┬─────┘
  └─────────────┘                                                       │ respondes
        ▲                                                               │ "1 sí"
        │            ejecuta lo aprobado y confirma por WhatsApp        ▼
        └───────────────────────────────────────────────── Make recoge respuesta
```

1. El becario genera las propuestas del día y un **resumen corto** (top 3–5).
2. Make envía ese resumen a tu WhatsApp, cada propuesta numerada.
3. Tú respondes (ej. `1 sí`, `2 no`, `3 sí`).
4. Make recoge la respuesta y el becario **ejecuta lo aprobado** y te confirma por WhatsApp.

## Lo que necesitas conectar (una vez)

1. **WhatsApp Business** con acceso a la **WhatsApp Business Cloud API** (vía Meta) o un número
   de WhatsApp Business conectado en Make.
2. En **Make**: crear una conexión de WhatsApp Business Cloud (token + número).
3. Confirmar tu número de destino en `perfil/sobre-mi.md`.

> Sin estos pasos, el canal queda en diseño y el becario entrega las propuestas en el chat de
> Claude Code mientras tanto.

## Diseño del escenario en Make

**Escenario A — Envío de propuestas (programado):**
- **Trigger:** *Schedule* (ej. cada día a las 08:00).
- **Módulo 1:** disparar el ciclo del becario (webhook a Claude Code / lectura del último
  archivo de `propuestas/`).
- **Módulo 2:** *WhatsApp Business › Send a Message* con el resumen y la numeración.

**Escenario B — Recoger la aprobación (en tiempo real):**
- **Trigger:** *WhatsApp Business › Watch Messages* (mensaje entrante tuyo).
- **Router:** interpreta `N sí` / `N no`.
- **Acción:** marca la propuesta N como aprobada/rechazada y notifica al becario para ejecutar.

## Activación
Cuando tengas la conexión lista, dime: **"activa el canal WhatsApp"**. Construiré ambos
escenarios en tu cuenta de Make con las herramientas disponibles y te los dejaré en pausa para
que los revises antes de encenderlos.

## Mientras tanto
El becario entrega las propuestas aquí, en el chat, con el mismo formato numerado para que el
salto a WhatsApp sea inmediato cuando conectes el número.
