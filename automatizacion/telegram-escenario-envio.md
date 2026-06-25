# 🤖 Telegram — Escenario A (Envío de propuestas) · Especificación de construcción

> Plan de Charly para montar el escenario en cuanto la API de Make deje de bloquear.
> Equipo Make: 549343 · Conexión: `Telegram Bot — Charly` (creada por Valerio).

## Objetivo (Nivel 1)
Charly envía las propuestas del día al bot de Telegram de Valerio. La aprobación y ejecución se
siguen gestionando en el chat con Charly (el lazo automático es el Nivel 2, futuro).

## Pasos de construcción (orden exacto)
1. `connections_list` (team 549343, type `telegram`) → obtener el **connectionId** del bot.
2. **Obtener el chat ID** de Valerio:
   - Valerio envía cualquier mensaje al bot (ej. "hola").
   - Charly ejecuta el módulo `getUpdates` (o un escenario temporal `watchUpdates`) → lee
     `message.chat.id`. Guardarlo en `perfil/sobre-mi.md` (campo Telegram chat ID).
3. `scenarios_create` (team 549343) con blueprint mínimo:
   - **Trigger:** *Schedule* (diario, hora a definir; sugerido 08:00 Europe/Madrid).
   - **Módulo 1 (opcional):** fuente de propuestas (lectura de `propuestas/` o webhook de Charly).
   - **Módulo 2:** Telegram `sendMessage` → chat ID de Valerio, texto = resumen del día.
4. Dejar el escenario **en pausa** (no activar) hasta que Valerio lo revise.
5. **Mensaje de prueba:** ejecutar una vez `sendMessage` con un texto de test para confirmar
   que llega al móvil.

## Formato del mensaje (Telegram)
```
🧠 Charly · Propuestas del {fecha}

Top {n} por impacto:
1️⃣ {título} — 💡 {beneficio}
2️⃣ {título} — 💡 {beneficio}
3️⃣ {título} — 💡 {beneficio}

Aprueba: responde "1 sí, 3 sí" (o "todo sí").
```

## Límite plan Free (vigilar)
2 escenarios activos · 1.000 operaciones/mes. Un envío diario = ~30 operaciones/mes: holgado.

## Estado
- ⏳ **Bloqueado temporalmente:** la API de Make devuelve `requires approval` en las lecturas.
  En cuanto se estabilice, Charly ejecuta los pasos 1-5 de arriba.
