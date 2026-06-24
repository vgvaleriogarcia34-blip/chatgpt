---
name: crear-skill
description: Meta-skill. Permite al Becario Máster diseñar y crear nuevas skills cuando detecta una necesidad recurrente sin cubrir. Úsalo cuando el jefe pida "créate una skill para X", "automatiza esto que hacemos siempre", o cuando el propio becario identifique un patrón repetitivo que merezca su propia capacidad. El becario propone la skill; el jefe la aprueba antes de que pase a estar activa.
---

# 🛠️ Crear skill — El sistema crece solo

Esta es la capacidad que hace del Becario Máster un verdadero "agente de agentes": cuando una
necesidad se repite, no la resuelve a mano cada vez — **se construye una herramienta**.

## Cuándo crear una skill nueva
- Una tarea aparece **3+ veces** o claramente se va a repetir.
- El jefe lo pide explícitamente.
- Detectas un proceso valioso que merece estandarizarse y automatizarse.

## Proceso

### 1. Define la necesidad
- ¿Qué problema resuelve? ¿Con qué frecuencia aparece? ¿Qué beneficio aporta automatizarlo?

### 2. Diseña la skill
- **Nombre:** corto, en kebab-case (ej. `seguimiento-impagos`).
- **Descripción (`description`):** clave para que se active sola. Describe *cuándo* usarla,
  con las frases reales que diría el jefe. Es lo que el sistema lee para decidir invocarla.
- **Proceso:** pasos claros y numerados.
- **Integraciones:** qué herramientas MCP usa.
- **Salida:** qué entrega.
- **Reglas:** límites de seguridad (qué requiere aprobación).

### 3. Escribe el archivo
Crea `.claude/skills/<nombre>/SKILL.md` con este formato:

```markdown
---
name: <nombre-en-kebab-case>
description: <Cuándo usarla, con frases reales del jefe. Específico y orientado a activación.>
---

# <Título>

<Propósito en una frase.>

## Proceso
1. ...

## Salida
...

## Reglas
- Nada de cara al exterior sin aprobación.
```

### 4. Propón antes de activar
Presenta la nueva skill al jefe: qué hace, por qué la creaste, qué beneficio da.
Solo se considera "activa" tras su OK. Registra el alta en el README si procede.

### 5. Mantén la coherencia
- Toda skill nueva respeta el principio **propone, tú apruebas**.
- Reutiliza las skills existentes en vez de duplicar lógica.
- Si una skill queda obsoleta, propón retirarla.

## Reglas
- Una skill = una responsabilidad clara. Nada de skills "cajón de sastre".
- La `description` es lo más importante: si está mal escrita, la skill nunca se activará sola.
- No crees skills que ejecuten acciones externas automáticas sin checkpoint de aprobación.
