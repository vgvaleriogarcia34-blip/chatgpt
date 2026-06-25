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

## Activación — estado real (2026-06-25)
- **Make:** organización `My Organization` (id 1657100), equipo `My Team` (id 549343), plan **Free**.
- **App oficial:** `whatsapp-business-cloud` — el conector **oficial de Meta** ("WhatsApp
  Business Cloud"). Conexión tipo `account:whatsapp-business-cloud`.
- **Requisitos de Meta (una vez):** cuenta de Facebook, **Meta Business Suite** con un *business
  portfolio*, y un **número de WhatsApp Business** válido. Importante: **desactivar la
  verificación en dos pasos** del número si la tienes activa.
- **Solicitud de conexión creada por Charly** (módulos: enviar mensaje, plantilla, recibir eventos):
  - Estado: **pendiente de que Valerio la autorice**.
  - 🔗 Enlace: https://eu2.make.com/549343/credentials-requests/inbox?requestId=666e84a4-4421-4bc5-ab8e-db86aef630f1
- **Lo que tú haces (una vez):** abrir el enlace → iniciar sesión en **Meta**, elegir tu *business
  portfolio* y tu *cuenta de WhatsApp Business* (o crearla en el momento) y confirmar. No se pega
  ningún token: es el login de Meta. Charly no puede hacerlo por ti (es tu identidad de Meta).
- **Cuando esté autorizada, dime "activa el canal WhatsApp"** y Charly construye los 2 escenarios
  (envío de propuestas + recogida de tu respuesta) y los deja en pausa para que los revises.
- ⚠️ **Nota plan Free:** límite de 2 escenarios activos y 1.000 operaciones/mes. Si hace falta,
  valoramos consolidar escenarios o subir de plan.

## Mientras tanto
El becario entrega las propuestas aquí, en el chat, con el mismo formato numerado para que el
salto a WhatsApp sea inmediato cuando conectes el número.
