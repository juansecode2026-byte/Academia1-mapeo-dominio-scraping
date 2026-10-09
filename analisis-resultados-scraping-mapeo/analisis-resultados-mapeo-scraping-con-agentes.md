# Análisis de los resultados: mapeo y scraping con agentes

Registro de lo que sale al repetir el mismo ejercicio con agentes de IA (Claude API). Se hace después de las otras dos formas, con las mismas etapas y métricas, para poder comparar.

**Versión** v2 · **Fecha** 9 de octubre de 2026 · **Estado** Plan, sin resultados todavía

> Fuente original: `analisis-resultados-mapeo-scraping-con-agentes_2026-10-09_v2.html` (respaldo, no leer). Este `.md` es la copia para leer y actualizar.

## Para qué sirve este informe

Es la forma con agentes de un ejercicio con tres formas. El manual se hace primero para entender cada eslabón; aquí se repite con agentes y se compara con las otras dos.

| Forma | Cómo se hace | Informe |
|---|---|---|
| Manual con código | Tú, con Python escrito paso a paso y guiado. | `analisis-resultados-mapeo-scraping-manual` |
| Con DevTools | Tú, a mano en el navegador (F12), sin programa. | `analisis-resultados-mapeo-scraping-con-devtools` |
| Con agentes | Agentes de IA con la API de Claude. | `analisis-resultados-mapeo-scraping-con-agentes` |

| Documento | Papel |
|---|---|
| Guía 1 / Guía 2 (`documentacion/`) | El **cómo**: pasos y código. No se tocan. |
| `FUENTES.md` | La **ficha del sitio**: reglas, ritmo y estado de cada etapa. |
| Este informe | El **qué salió**: cifras, tiempos, fallos y conclusiones de cada etapa. Es el único lugar donde se registran los resultados. |

Sitio del ejercicio: `https://www.viviendoporelmundo.com/`. Antes de tocarlo rige su ficha en `FUENTES.md`.


## Checklist de piezas (guía 2)

Son las seis piezas de la guía 2. Cada una hace una sola cosa; se detalla paso a paso cuando terminen las otras dos formas.

- [ ] **Pieza 1. Mapa** — Código · Lista las URLs del dominio · Equivale a la etapa 2 del manual.
- [ ] **Pieza 2. Selector** — IA (modelo rápido) · Elige cuáles merecen lectura · Equivale a la etapa 3.
- [ ] **Pieza 3. Lector** — Código · Descarga y limpia el texto · Equivale a la etapa 4.
- [ ] **Pieza 4. Analista** — IA (modelo mejor) · Extrae datos y resume con palabras propias · Equivale a las etapas 4 y 5.
- [ ] **Pieza 5. Archivo** — Código · Guarda con fuente y fecha · Equivale a la etapa 5.
- [ ] **Pieza 6. Revisión** — Tú · Apruebas o descartas cada ficha.

> **Antes de empezar** Terminan primero el manual con código y DevTools. Los permisos (etapa 1) y el mapa del sitio salen de esos ejercicios; aquí se reutilizan y se registra solo lo nuevo.


## Esqueleto de cada etapa

Cada etapa del informe lleva los mismos cinco bloques:

| Bloque | Qué va |
|---|---|
| 1. Qué se hizo | Dos líneas. |
| 2. Resultado | Cifras y, si aplica, una muestra corta (nunca el texto completo de un artículo). |
| 3. Costo | Tiempo de ejecución, peticiones al sitio y tokens (en manual es cero). |
| 4. Qué falló o sorprendió | Errores, casos raros, cosas que no esperábamos. |
| 5. Conclusión | Qué se aprendió y qué se haría distinto. |


## Métricas a registrar

Las mismas en los tres informes. Al final del informe de agentes se comparan las tres formas, una junto a otra.

| Métrica | Cómo se mide |
|---|---|
| URLs encontradas / elegidas | Cuántas hay en el mapa y cuántas pasan el filtro. |
| Páginas leídas | Cuántas se descargaron y procesaron. |
| Tiempo total de ejecución | De pared, con la espera de 10 s incluida. |
| Peticiones al sitio | Debe respetar el `Crawl-delay`. |
| Costo en tokens (USD) | Manual: 0. Agentes: lo que marque la consola de la API. |
| Campos completos por ficha (%) | Título, autor, fecha y texto presentes. |
| Páginas que no eran artículo y se colaron | Falsos positivos del filtro. |
| Tiempo humano | Escribir código o prompts, y revisar el resultado. |


## Resultados por etapa


### Etapa 1. Permisos (reutiliza el manual)

| Bloque | Registro |
|---|---|
| Qué se hizo | Pendiente de hacer, después del manual. |
| Resultado | Pendiente. |
| Costo (tiempo, peticiones, tokens) | Pendiente. |
| Qué falló o sorprendió | Pendiente. |
| Conclusión | Pendiente. |


### Etapa 2. Mapa

| Bloque | Registro |
|---|---|
| Qué se hizo | Pendiente de hacer, después del manual. |
| Resultado | Pendiente. |
| Costo (tiempo, peticiones, tokens) | Pendiente. |
| Qué falló o sorprendió | Pendiente. |
| Conclusión | Pendiente. |


### Etapa 3. Selector

| Bloque | Registro |
|---|---|
| Qué se hizo | Pendiente de hacer, después del manual. |
| Resultado | Pendiente. |
| Costo (tiempo, peticiones, tokens) | Pendiente. |
| Qué falló o sorprendió | Pendiente. |
| Conclusión | Pendiente. |


### Etapa 4. Lector y analista

| Bloque | Registro |
|---|---|
| Qué se hizo | Pendiente de hacer, después del manual. |
| Resultado | Pendiente. |
| Costo (tiempo, peticiones, tokens) | Pendiente. |
| Qué falló o sorprendió | Pendiente. |
| Conclusión | Pendiente. |


### Etapa 5. Archivo y revisión

| Bloque | Registro |
|---|---|
| Qué se hizo | Pendiente de hacer, después del manual. |
| Resultado | Pendiente. |
| Costo (tiempo, peticiones, tokens) | Pendiente. |
| Qué falló o sorprendió | Pendiente. |
| Conclusión | Pendiente. |


## Comparación de las tres formas

Se llena al cerrar las tres formas.

| Métrica | Manual con código | DevTools | Agentes | Lectura |
|---|---|---|---|---|
| URLs encontradas / elegidas | — | — | — | — |
| Páginas leídas | — | — | — | — |
| Tiempo total de ejecución | — | — | — | — |
| Peticiones al sitio | — | — | — | — |
| Costo en tokens (USD) | — | — | — | — |
| Campos completos por ficha (%) | — | — | — | — |
| Páginas que no eran artículo y se colaron | — | — | — | — |
| Tiempo humano | — | — | — | — |


## Decisiones del plan

| Decisión | Valor |
|---|---|
| Tres formas | Manual con código, DevTools y agentes: mismo sitio, mismas etapas y mismas métricas, para comparar. |
| Etapa 1 reabierta | Sí: los términos de uso pendientes se cierran antes de extraer contenido. |
| Etapa 0 de preparación | Es un paso propio. |
| Ubicación | `analisis-resultados-scraping-mapeo/`, con copia en `.md`. |
| Muestra de la etapa 4 | 3 páginas y luego 10. |
| Contenido de terceros | El informe lleva cifras y citas cortas, nunca el texto completo de los artículos. |


## Versiones de este archivo

| Versión | Fecha | Archivo | Qué contiene |
|---|---|---|---|
| v1 | 9 de octubre de 2026 | `analisis-resultados-mapeo-scraping-con-agentes_2026-10-09_v1.html` | Plan: checklist de piezas de la guía 2, esqueleto, métricas, resultados pendientes y tabla de comparación vacía. |
| v2 | 9 de octubre de 2026 | `analisis-resultados-mapeo-scraping-con-agentes_2026-10-09_v2.html` | Agrega la tercera forma (DevTools): tabla de las tres formas y comparación con tres columnas. |

Cada vez que se cierre un paso o una etapa se actualiza este informe y se guarda una versión nueva con la fecha en el nombre.

