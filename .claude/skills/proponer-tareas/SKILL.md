---
name: proponer-tareas
description: El ciclo proactivo del Becario Máster. Úsalo cuando el jefe pida "propón tareas", "qué puedo hacer hoy", "lanza el ciclo de propuestas", "qué oportunidades ves", o al empezar una sesión sin instrucción concreta. Analiza todo el contexto del jefe (agenda, emails, CRM, clientes, competencia, objetivos) y genera una lista priorizada de tareas con su beneficio concreto, que el jefe aprueba antes de ejecutar.
---

# 🫀 Proponer tareas — El ciclo proactivo

Esta es la skill central del Becario Máster. Convierte el conocimiento del jefe en una lista
de tareas accionables, priorizadas por beneficio, listas para aprobar.

## Cuándo se activa
- El jefe lo pide explícitamente.
- Al inicio de una sesión sin instrucción concreta.
- De forma periódica (diaria/semanal) si así se ha acordado.

## Proceso

### 1. Cárgate el contexto (lee siempre primero)
- `perfil/sobre-mi.md`, `perfil/objetivos.md`, `perfil/clientes.md`, `perfil/competidores.md`.
- Revisa `propuestas/` para no repetir lo ya propuesto/aprobado/rechazado.

### 2. Observa las señales (usa las integraciones, solo lectura)
- **Calendar:** reuniones próximas sin preparar, huecos, conflictos, seguimientos pendientes.
- **Gmail:** emails sin responder, oportunidades, urgencias, clientes que enfriaron.
- **HubSpot:** deals estancados, renovaciones próximas, contactos sin actividad, up-sell.
- **Drive / Plaud:** reuniones recientes sin acta, documentos que pidan seguimiento.
- **Web:** novedades relevantes de competidores o mercado (si aplica).

### 3. Detecta beneficio
Para cada señal, pregúntate: *¿qué acción concreta genera beneficio para el jefe?*
Beneficio = tiempo ganado, dinero ganado, cliente ganado/retenido, o riesgo evitado.

### 4. Prioriza
Ordena por **Impacto × Urgencia**, alineado con `perfil/objetivos.md`.
No más de 5–8 propuestas por ciclo. Calidad sobre cantidad.

### 5. Escribe la propuesta
Crea/actualiza un archivo en `propuestas/` con la fecha (ej. `propuestas/2026-06-24.md`),
siguiendo la plantilla `propuestas/PLANTILLA.md`. Cada tarea lleva:

- **Título** claro y específico.
- **Beneficio concreto:** la frase que justifica hacerlo.
- **Qué haría yo (el becario):** los pasos exactos a ejecutar.
- **Skill / herramientas:** qué usaría.
- **Riesgo / requiere aprobación:** sí/no y por qué.
- **Casilla de aprobación:** `[ ]`.

### 6. Entrega y espera aprobación
Presenta al jefe un resumen corto (las 3–5 más importantes) y dile que el detalle está en
`propuestas/`. **No ejecutes nada de cara al exterior hasta que apruebe.**

### 7. Ejecuta lo aprobado y cierra el bucle
- Ejecuta cada tarea aprobada (invocando la skill que corresponda).
- Marca `[x]` y anota el resultado en la propuesta.
- Si aprendes algo del jefe/negocio/mercado, **actualiza `perfil/`**.

## Reglas
- Nunca propongas algo vago. Si no puedes nombrar el beneficio concreto, no es una propuesta.
- Respeta `perfil/objetivos.md` → "Qué NO es prioridad ahora".
- Si detectas una necesidad recurrente sin skill que la cubra, invoca `crear-skill`.
