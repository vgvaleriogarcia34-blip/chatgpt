# Agentes del proyecto

El proyecto incluye tres subagentes de Claude Code que orquestan el flujo
completo de producción de reels. Viven en `.claude/agents/` y se invocan
automáticamente cuando el texto del usuario encaja con la descripción de
cada uno, o manualmente con `@nombre`.

## `reel-producer`

Project manager. Es el punto de entrada cuando el usuario da una orden de
alto nivel como *"organiza esto hasta que tenga los reels"*. Hace los
chequeos previos (env, ffmpeg, disco), delega en `reel-orchestrator`,
espera los resultados y encadena con `reel-qa`. Devuelve un resumen
ejecutivo.

## `reel-orchestrator`

Ejecuta el pipeline real: resuelve la fuente (local o URL), transcribe,
selecciona highlights con Claude, renderiza los mp4 con ffmpeg y escribe
`manifest.json`. No publica nada.

## `reel-qa`

Audita los outputs: ejecuta `ffprobe`, valida duración, resolución, fps,
codec, audio, tamaño y chequea las captions en el manifest. Produce una
tabla con veredicto por reel y acciones concretas si hay problemas.

## Reglas compartidas

1. **Nunca publican en redes** en esta fase. La parte de publicadores
   (`src/publishers/`) queda inerte hasta que se añadan credenciales.
2. **Nunca borran fuentes ni renders** sin confirmación del usuario.
3. Cada agente reporta en ≤ 5 líneas al terminar.
4. Cualquier error debe indicar causa probable + acción sugerida.

## Flujo típico

```
Usuario: "procesa inbox/podcast.mp4 a 5 reels B2B"
   │
   ▼
reel-producer
   ├─ pre-flight checks
   ├─ delega ► reel-orchestrator (ejecuta make_reels.py)
   │            └─ devuelve manifest.json
   ├─ delega ► reel-qa (audita mp4s + manifest)
   │            └─ devuelve tabla con veredicto
   └─ informe final al usuario
```

## Ampliarlos

Cuando llegue la fase 2 (publicación) crearemos:

- `reel-publisher-ig` — Instagram Graph API (Reels).
- `reel-publisher-li` — LinkedIn UGC video.
- `reel-scheduler` — decide slots óptimos por canal.

Todos compartirán las mismas reglas de seguridad (no publicar sin
confirmación explícita la primera vez, log de cada post).
