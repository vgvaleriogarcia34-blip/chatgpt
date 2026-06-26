# 06 · Política de Cookies (LSSI-CE, art. 22.2)

> Solo aplica si la web usa cookies/rastreadores. Si la web aún no existe o es estática sin
> analítica, este documento queda en espera. Sustituye `[CORCHETES]`.

---

## 1. Reglas clave (criterio AEPD vigente)

- Las cookies **no necesarias** (analítica, marketing) requieren **consentimiento previo**.
- El banner debe permitir **Aceptar**, **Rechazar** (con la misma facilidad) y **Configurar**.
- **No** se pueden usar muros de cookies que obliguen a aceptar para navegar (salvo alternativa).
- **No** se instalan cookies no necesarias hasta que el usuario acepte.
- Debe poder **retirarse** el consentimiento tan fácilmente como se dio.

---

## 2. Banner (texto modelo)

> *Usamos cookies propias y de terceros para fines técnicos y, con tu permiso, de analítica.
> Puedes aceptar todas, rechazarlas o configurarlas.*
> **[Aceptar todas] [Rechazar todas] [Configurar]**

---

## 3. Tabla de cookies (rellenar con las reales)

| Cookie | Tipo | Finalidad | Titular | Duración |
|---|---|---|---|---|
| `[nombre]` | Técnica (necesaria) | Funcionamiento del sitio | Propia | Sesión |
| `_ga` `[VERIFICAR]` | Analítica | Medir audiencia (Google Analytics) | Google (terceros) | `[plazo]` |
| `[…]` | Marketing | `[…]` | `[…]` | `[…]` |

> ⚠️ **Acción:** auditar la web real con una herramienta (escáner de cookies) para listar
> exactamente las que se cargan. No publicar tablas inventadas.

---

## 4. Cómo gestionar/retirar el consentimiento

Explicar que el usuario puede cambiar su elección desde el **icono/enlace de configuración de
cookies** y desde la configuración de su navegador.

---

## 5. Estado

🔴 **Pendiente de la web.** Cuando exista dominio y analítica, se completa la tabla real y se
implanta un gestor de consentimiento (CMP) conforme.
