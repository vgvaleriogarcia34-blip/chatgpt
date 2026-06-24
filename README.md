# 🧠 Becario Máster — Tu agente de agentes

Este repositorio es el **Centro de Mando** de tu becario proactivo: un agente que te conoce,
mira por tu beneficio, analiza tu negocio (agenda, emails, CRM, clientes, competencia) y
**te propone tareas concretas** que quiere ejecutar por y para ti. Tú apruebas; él ejecuta.

## Cómo funciona

- **El cerebro** vive en [`CLAUDE.md`](./CLAUDE.md): la identidad, la misión y las reglas del becario.
- **Lo que sabe de ti** vive en [`perfil/`](./perfil/): tu negocio, tus clientes, tu competencia, tus objetivos.
- **Lo que sabe hacer** vive en [`.claude/skills/`](./.claude/skills/): sus capacidades especializadas.
- **Lo que te propone** aparece en [`propuestas/`](./propuestas/): tareas con su beneficio concreto.

## Modo actual: *Propone, tú apruebas*

El becario puede **observar y analizar** todo libremente, y **dejar propuestas**. No ejecuta
ninguna acción de cara al exterior (emails, CRM, publicaciones) sin tu visto bueno.

## Para empezar a usarlo

1. **Rellena tu perfil.** Abre los archivos de [`perfil/`](./perfil/) y complétalos (o pídele al
   becario que los rellene investigando tus cuentas conectadas).
2. **Pide propuestas.** Dile: *"Lanza el ciclo de propuestas"* o invoca la skill `proponer-tareas`.
   El becario analizará tu contexto y dejará una lista priorizada en `propuestas/`.
3. **Aprueba y ejecuta.** Marca las que quieras y el becario las ejecuta y te reporta.

## Skills disponibles

| Skill | Qué hace |
|---|---|
| `proponer-tareas` | El ciclo proactivo: analiza todo y propone tareas con beneficio. |
| `radar-agenda-email` | Detecta oportunidades y urgencias en tu agenda y bandeja. |
| `prospeccion-clientes` | Analiza y prepara el acercamiento a potenciales clientes. |
| `actas-informes` | Genera actas (desde Plaud) e informes a partir de tus datos. |
| `analisis-competencia` | Investiga competidores y detecta brechas no explotadas. |
| `crear-skill` | El becario diseña y crea nuevas skills cuando detecta una necesidad. |

## Integraciones conectadas

Gmail · Google Calendar · Google Drive · HubSpot (CRM) · Plaud · Canva · Make · Búsqueda web.
