# 00 · Diagnóstico y alcance del tratamiento

> Punto de partida del plan: **qué datos personales trata Familias Empresarias, de quién, para
> qué y con qué herramientas.** De aquí se deriva todo lo demás (RAT, riesgos, medidas).

---

## 1. El Responsable del Tratamiento

| Campo | Valor |
|---|---|
| Razón social | **Familias Empresarias SL** `[VERIFICAR razón social exacta]` |
| Nombre comercial / marca | Familias Empresarias · *Arquitectos de Claridad* |
| CIF / NIF | `[PENDIENTE]` |
| Domicilio social | `[PENDIENTE]` |
| Email de contacto en privacidad | `[PENDIENTE — sugerido: privacidad@familiasempresarias.xxx]` |
| Email operativo actual | familiasempresarias2080@gmail.com |
| Representante legal | Valerio García `[VERIFICAR cargo: administrador único]` |
| Web | `[PENDIENTE: dominio]` |
| Nº de personas en plantilla | `[PENDIENTE]` (define si aplica registro de jornada, canal interno, etc.) |

> **Rol RGPD:** Familias Empresarias actúa principalmente como **Responsable del Tratamiento**
> de sus propios datos (clientes, prospectos, contactos, personal). Respecto a algunos datos de
> los *clientes finales* podría actuar como **Encargado** (si trata datos de terceros por cuenta
> de un cliente) — ver §4.

---

## 2. ¿De quién se tratan datos? (categorías de interesados)

1. **Clientes** (personas de contacto de empresas familiares: socios, administradores, gerentes).
2. **Prospectos / leads** (contactos comerciales captados por LinkedIn, referidos, web).
3. **Proveedores y colaboradores** (autónomos, partners).
4. **Personal interno** (empleados / colaboradores como Cecilia Torralba — agenda) `[VERIFICAR]`.
5. **Asistentes a reuniones** grabadas con Plaud (voz e imagen si hay vídeo).
6. **Personas físicas dentro de los datos de cliente** (p. ej. **datos económicos familiares**
   en proyectos tipo "Familia España 2025": ingresos, gastos, ahorro de personas físicas).

---

## 3. ¿Qué categorías de datos se tratan?

| Categoría | Ejemplos en el negocio | ¿Riesgo? |
|---|---|---|
| Identificativos | Nombre, cargo, empresa, email, teléfono | Estándar |
| Comerciales / CRM | Etapa de pipeline, valor de deal, notas (HubSpot) | Estándar |
| **Económico-financieros** | Cuentas, márgenes, precios, **finanzas familiares** (ingresos/gastos de personas físicas) | **Alto** |
| **Grabaciones de voz** | Reuniones grabadas y transcritas con Plaud | **Alto** |
| Datos de negocio del cliente | Catálogos, proveedores, SKUs (mayoría datos de empresa, no personales) | Bajo-Medio |
| Categorías especiales (art. 9) | **No previstas** de forma habitual `[VERIFICAR que no haya salud/ideología/etc.]` | — |

> ⚠️ **Punto crítico 1 — Datos financieros de personas físicas.** En proyectos como "Familia
> España 2025" se tratan datos económicos de una familia (personas físicas). Aunque no son
> "categoría especial" del art. 9, sí son datos de **alto riesgo** que exigen base jurídica
> clara, contrato y medidas reforzadas.
>
> ⚠️ **Punto crítico 2 — Grabaciones Plaud.** Grabar y transcribir reuniones implica tratar la
> **voz** (dato personal) de todos los asistentes. Exige **informar y/o recabar consentimiento**
> antes de grabar (ver cláusula en doc. 05).

---

## 4. ¿Responsable o Encargado? (doble rol)

- Cuando Familias Empresarias gestiona **sus propios** clientes, prospectos y personal →
  es **Responsable**.
- Cuando **trata datos personales que le entrega un cliente** para prestarle el servicio
  (p. ej. una base de contactos del cliente, nóminas, datos de los empleados del cliente) →
  actúa como **Encargado del Tratamiento de ese cliente**, y se necesita un **contrato de
  encargo (art. 28)** firmado *con el cliente* (ver doc. 09, modelo incluido).

> **Acción:** revisar cliente por cliente si Valerio recibe datos personales de terceros. En la
> mayoría de proyectos parece tratar **datos de empresa** (catálogos, SKUs, finanzas de la
> sociedad), que no son datos personales — pero "Familia España" sí lo es. `[VERIFICAR por cliente]`

---

## 5. Sistemas y herramientas (dónde viven los datos)

| Sistema | Uso | Rol | Ubicación datos |
|---|---|---|---|
| **Google Workspace** (Gmail, Drive, Calendar) | Email, expedientes, agenda | Encargado | UE/EE. UU. |
| **HubSpot** | CRM, pipeline | Encargado | EE. UU. |
| **Plaud** | Grabación + transcripción de reuniones | Encargado | EE. UU. `[VERIFICAR]` |
| **Make** | Automatizaciones | Encargado | UE/EE. UU. |
| **Canva** | Diseño de entregables | Encargado | EE. UU. |
| **Asistente IA (Claude / Anthropic)** | Análisis y generación de documentos | Encargado `[VERIFICAR]` | EE. UU. |

> Todos son **encargados de tratamiento** y varios implican **transferencia internacional** de
> datos (EE. UU.). Detalle y garantías en **doc. 09**.

---

## 6. Conclusiones del diagnóstico

1. El negocio **trata datos personales** (clientes, prospectos, personal, asistentes a reuniones)
   y, en algunos casos, **datos económicos de personas físicas** → cumplimiento RGPD obligatorio.
2. Hay **grabaciones de voz** (Plaud): tratamiento que exige información/consentimiento específico.
3. Hay **múltiples encargados** y **transferencias internacionales** → contratos y garantías.
4. **DPO:** probablemente **no obligatorio** (ver análisis en doc. 02), pero conviene **designar
   un responsable interno de privacidad**.
5. **EIPD:** a valorar por el uso de **IA + perfilado financiero + grabaciones** (criterio en doc. 02).
