# 09 · Encargados del tratamiento y transferencias internacionales

> Todo proveedor que **trata datos personales por cuenta** de Familias Empresarias es un
> **Encargado del Tratamiento** y requiere un **contrato de encargo (art. 28 RGPD)**, normalmente
> el **DPA** (Data Processing Agreement) del propio proveedor. Si el proveedor está fuera del EEE
> (p. ej. EE. UU.), además hay que garantizar la **transferencia internacional** (arts. 44-49).

---

## 1. Inventario de encargados

| Proveedor | Servicio | ¿Datos personales? | Ubicación | DPA disponible | Estado |
|---|---|---|---|---|---|
| **Google (Workspace)** | Email, Drive, Calendar | Sí (todos) | UE/EE. UU. | Sí (Google Cloud/Workspace DPA) | 🟡 Aceptar/archivar DPA |
| **HubSpot** | CRM | Sí (clientes/prospectos) | EE. UU. | Sí (HubSpot DPA) | 🟡 Aceptar/archivar |
| **Plaud** | Grabación/transcripción | Sí (voz) | EE. UU. `[VERIFICAR]` | `[VERIFICAR]` | 🔴 Revisar urgente |
| **Make** | Automatización | Sí (los que pasen por flujos) | UE/EE. UU. | Sí (Make DPA) | 🟡 Aceptar/archivar |
| **Canva** | Diseño | Sí (si hay datos personales en diseños) | EE. UU. | Sí (Canva DPA) | 🟡 Aceptar/archivar |
| **Asistente IA (Anthropic/Claude)** | Análisis y redacción | Depende del input | EE. UU. | `[VERIFICAR]` | 🔴 Revisar |
| **Asesoría/gestoría** | Contabilidad/fiscal | Sí | España `[VERIFICAR]` | Contrato encargo | 🟡 Firmar |
| **Hosting web** | Web/formularios | Sí | `[PENDIENTE]` | `[VERIFICAR]` | 🔴 Pendiente |

> ⚠️ **Prioridad:** Plaud (grabaciones de voz) y el proveedor de IA, por ser los de mayor riesgo
> y donde más conviene confirmar garantías. Y el hosting de la web cuando exista.

---

## 2. Transferencias internacionales (EE. UU. y otros)

Para proveedores en EE. UU., la transferencia debe ampararse en una de estas garantías:

1. **EU-US Data Privacy Framework (DPF):** que el proveedor esté **certificado** en el marco
   UE-EE. UU. (verificable en la lista oficial del DPF). Es la vía más simple si está adherido.
2. **Cláusulas Contractuales Tipo (SCC)** de la Comisión Europea, incluidas en el DPA del proveedor.
3. **Evaluación de impacto de la transferencia (TIA)** si el riesgo lo requiere.

> **Acción:** por cada proveedor de EE. UU., comprobar si está **adherido al DPF** o si su DPA
> incorpora **SCC**, y **archivar la evidencia**. Casi todos los grandes (Google, HubSpot, Make,
> Canva) lo cumplen; **Plaud y el proveedor de IA** son los que hay que verificar expresamente.

---

## 3. Contenido mínimo del contrato de encargo (art. 28.3)

Todo DPA/contrato debe recoger que el encargado:
- Trata los datos **solo siguiendo instrucciones** del responsable.
- Garantiza el **deber de confidencialidad** de su personal.
- Aplica las **medidas de seguridad** del art. 32.
- No **subcontrata** sin autorización (y traslada las mismas obligaciones).
- **Asiste** al responsable con los derechos de los interesados y las brechas.
- **Suprime o devuelve** los datos al final del servicio.
- Permite **auditorías** y pone a disposición la información para demostrar cumplimiento.

---

## 4. Familias Empresarias como ENCARGADO de sus clientes

Cuando un cliente entrega a Familias Empresarias datos personales de terceros (p. ej. sus
empleados, su base de clientes), **es el cliente quien debe firmar con Familias Empresarias** un
contrato de encargo. En `plantillas/` se incluye un **modelo de contrato de encargo (art. 28)**
listo para ofrecer al cliente y dejar la relación cubierta.

---

## 5. Estado y siguiente paso

- Recopilar y **archivar el DPA** de cada proveedor (la mayoría se aceptan en su panel/condiciones).
- **Verificar Plaud, IA y hosting** (los 🔴).
- Firmar el contrato de encargo **con cada cliente** del que se reciban datos personales.
- Guardar todo en una carpeta `proteccion-datos/contratos/` (o en Drive).
