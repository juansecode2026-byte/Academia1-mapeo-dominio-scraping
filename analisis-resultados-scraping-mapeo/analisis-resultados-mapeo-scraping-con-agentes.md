# Análisis de los resultados: mapeo y scraping con agentes

Registro de lo que sale al repetir el mismo ejercicio con agentes de IA (Claude API). Se hace después de las otras dos formas, con las mismas etapas y métricas, para poder comparar.

**Versión** v3 · **Fecha** 10 de octubre de 2026 · **Estado** Plan, sin resultados todavía

> Fuente original: `analisis-resultados-mapeo-scraping-con-agentes_2026-10-10_v3.html` (respaldo, no leer). Este `.md` es la copia para leer y actualizar.

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
- [ ] **Pieza 2. Selector** — IA (modelo rápido) · Elige cuáles merecen lectura · Equivale a la etapa 3. Entra donde las reglas del paso 8 se quedan cortas.
- [ ] **Pieza 3. Lector** — Código · Descarga y limpia el texto · Equivale a la etapa 4.
- [ ] **Pieza 4. Analista** — IA (modelo mejor) · Extrae datos y resume con palabras propias · Equivale a las etapas 4 y 5. Entra en lugar del paso 9 del manual (inspeccionar el HTML).
- [ ] **Pieza 5. Archivo** — Código · Guarda con fuente y fecha · Equivale a la etapa 5.
- [ ] **Pieza 6. Revisión** — Tú · Apruebas o descartas cada ficha.

> **Antes de empezar** Terminan primero el manual con código y DevTools. Los permisos (etapa 1) y el mapa del sitio salen de esos ejercicios; aquí se reutilizan y se registra solo lo nuevo.


## Dónde entra el agente: el paso 9 del manual y por qué

En el ejercicio manual, el **paso 9** consiste en abrir un artículo, inspeccionar su HTML y descubrir en qué etiqueta vive cada dato (el título, el autor, la fecha, los párrafos) para poder escribir código que los saque. Aquí es donde, con lo visto en el ejercicio, **entra el agente**. Esta sección explica el motivo.

**Qué se hace a mano en el paso 9 y por qué es el cuello de botella:**

| Lo que se vio | De dónde sale |
|---|---|
| Cada sitio arma su HTML distinto, así que las reglas de «dónde está el título» o «dónde están los párrafos» hay que descubrirlas y escribirlas **una por sitio**. | Guía 1, paso 3: los selectores como `article p` «no escalan». |
| Si el sitio cambia su diseño, el código se rompe y hay que repararlo. | Guía 2, tabla de la comparación: el manual «se rompe y hay que reparar»; el agente «sigue funcionando porque lee contenido, no etiquetas». |
| El HTML crudo de la portada pesa unos 240 KB y empieza con comentarios para Internet Explorer, metadatos y scripts: el texto del artículo está enterrado en medio. | Paso 5 del manual (descargar una página). |
| Las reglas por el nombre de la dirección descartaron series enteras y artículos prácticos, y no ven los que hablan de Colombia sin nombrarla. | Paso 8 del manual (filtrado). |

**Qué hace el agente en lugar de eso:** no necesita saber dónde está cada dato dentro del HTML. Recibe el texto ya limpio de la página y devuelve los datos que se le piden, en una ficha con campos fijos (título, autor, fecha, lugares, costos, resumen con palabras propias). Lo que no está en el texto, lo devuelve vacío en vez de inventarlo.

| Tarea | A mano (pasos 9 y 10) | Con el agente |
|---|---|---|
| Encontrar el título, el autor y la fecha | Inspeccionar el HTML y escribir un selector para cada dato, en cada sitio. | Los lee en el texto y los devuelve en la ficha. |
| Sacar los párrafos del artículo | Selectores o una librería (`trafilatura`). | Recibe el texto ya limpio por el código. |
| Decidir si un artículo habla de Colombia | Reglas por palabras en la dirección: ven solo el nombre. | Lee el contenido y juzga con criterio, incluso si la dirección no nombra el país. |
| Extraer datos como lugares o costos | Muy difícil: cada artículo los cuenta de otra forma. | Los extrae en la ficha, con `null` si faltan. |
| Resumir con palabras propias y citar la fuente | Lo hace una persona, artículo por artículo. | Propone el resumen y la persona lo revisa. |
| Si el sitio cambia su diseño | Hay que reparar los selectores. | Sigue funcionando, porque lee contenido y no etiquetas. |
| Costo | Casi nulo. | Se pagan tokens por cada página analizada. |

**Dónde entra en las piezas de la guía 2:**

| Pieza | Qué hace el agente aquí | Qué sustituye del manual |
|---|---|---|
| Pieza 2. Selector | Elige cuáles de las 292 direcciones merecen lectura, juzgando título y tema. | Las reglas del paso 8, que se quedaron cortas. |
| Pieza 4. Analista | Extrae los datos de cada página y escribe un resumen propio con su fuente. | El paso 9 (inspeccionar el HTML) y la reescritura del paso 11 hecha a mano. |

> **Dónde NO hace falta un agente** Sacar el texto limpio de un artículo no necesita inteligencia artificial: `trafilatura` (paso 10 del manual) lo hace gratis y de forma repetible. La regla de oro de la guía 2 es «usa código para lo mecánico y el modelo solo para lo que requiere criterio». Por eso el agente se justifica en juzgar y estructurar, no en descargar ni en limpiar. Si el objetivo fuera solo el texto, el manual alcanza.

**Qué se medirá en este ejercicio** (para la comparación de las tres formas):

- Cuántos artículos de Colombia encuentra el agente que las reglas del paso 8 no vieron (las **omisiones** de las reglas).
- Cuántas de las 8 marcadas por las reglas descarta el agente como no útiles (los **falsos positivos** de las reglas).
- Qué porcentaje de las fichas sale con todos los campos completos, y si inventa algún dato.
- Cuántos tokens y cuántos dólares cuesta, frente al costo casi nulo del manual.

Todo esto sigue pendiente: esta sección es el plan y el motivo, no un resultado.


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
| Muestra de la etapa 4 | 3 páginas y luego las 8 marcadas de Colombia. |
| Filtro elegido | Opciones A, B, C y D: mapa de origen, palabras de Colombia en la dirección, familia por el nombre y carpeta `/paises/`. Cuentan todos los lugares de Colombia; no cuentan los vídeos; solo información tipo blog. |
| Tema inicial | Colombia: el filtro del paso 8 busca el material que sirva para un artículo sobre ese tema. |
| Direcciones | Se guardan todas (292) y se marcan; no se borra nada. Las guías por país cuentan como material. |
| Contenido de terceros | El informe lleva cifras y citas cortas, nunca el texto completo de los artículos. |


## Versiones de este archivo

| Versión | Fecha | Archivo | Qué contiene |
|---|---|---|---|
| v1 | 9 de octubre de 2026 | `analisis-resultados-mapeo-scraping-con-agentes_2026-10-09_v1.html` | Plan: checklist de piezas de la guía 2, esqueleto, métricas, resultados pendientes y tabla de comparación vacía. |
| v2 | 9 de octubre de 2026 | `analisis-resultados-mapeo-scraping-con-agentes_2026-10-09_v2.html` | Agrega la tercera forma (DevTools): tabla de las tres formas y comparación con tres columnas. |
| v3 | 10 de octubre de 2026 | `analisis-resultados-mapeo-scraping-con-agentes_2026-10-10_v3.html` | Agrega la sección «Dónde entra el agente»: por qué hace falta un agente en el paso 9 del manual (en lugar de inspeccionar el HTML), qué sustituye, dónde no hace falta y qué se medirá. |

Cada vez que se cierre un paso o una etapa se actualiza este informe y se guarda una versión nueva con la fecha en el nombre.

