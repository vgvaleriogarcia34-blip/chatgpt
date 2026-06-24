---
name: radar-agenda-email
description: Escanea la agenda (Google Calendar) y la bandeja de entrada (Gmail) del jefe para detectar oportunidades, urgencias, seguimientos pendientes y cosas que se le escapan. Úsalo cuando el jefe pida "revisa mi agenda", "qué tengo pendiente", "algo urgente en el correo", "prepárame el día/la semana", o como parte del ciclo de proponer-tareas.
---

# 📡 Radar de agenda y email

Detecta lo que importa en la agenda y la bandeja del jefe, sin que él tenga que mirar.

## Proceso

### Agenda (Google Calendar — solo lectura)
1. Lista los eventos próximos (hoy / esta semana).
2. Para cada reunión, detecta:
   - ¿Está **preparada**? (¿hay agenda, documentos, contexto del asistente?)
   - ¿Es con un **cliente/prospecto** de `perfil/clientes.md`? → cruza datos.
   - ¿Requiere un **seguimiento posterior** (acta, propuesta, email)?
3. Detecta **huecos** aprovechables y **conflictos** o solapamientos.

### Email (Gmail — solo lectura)
1. Revisa la bandeja reciente y los hilos sin responder.
2. Clasifica por:
   - 🔴 **Urgente / requiere respuesta** (cliente esperando, deadline).
   - 🟡 **Oportunidad** (interés comercial, lead, petición que se puede convertir).
   - 🟢 **Seguimiento** (algo que prometiste y no cerraste).
   - ⚪ **Ruido** (ignorable).
3. Cruza remitentes con `perfil/clientes.md` para detectar clientes que se han enfriado.

## Salida
Entrega un resumen priorizado:
- **Urgente hoy:** …
- **Oportunidades a convertir:** …
- **Seguimientos pendientes:** …
- **Reuniones a preparar:** …

Para cada punto, propón la acción concreta (ej. "borrador de respuesta a X", "preparar reunión
con Y"). Si el jefe aprueba, ejecuta: redacta borradores en Gmail (`create_draft`) — **nunca
envíes sin aprobación** — y prepara los materiales de reunión.

## Reglas
- Borradores sí, envíos no (sin aprobación explícita).
- No marques, archives ni etiquetes correos sin permiso.
- Protege la privacidad: no expongas contenido sensible fuera de lo necesario.
