# Análisis de los resultados: mapeo y scraping con DevTools

Registro de lo que sale al hacer a mano el mismo ejercicio con las herramientas del navegador (DevTools, tecla F12), sin escribir un programa. Entra en la comparación con el manual con código y con los agentes.

**Versión** v1 · **Fecha** 9 de octubre de 2026 · **Estado** Plan, sin resultados todavía

> Fuente original: `analisis-resultados-mapeo-scraping-con-devtools_2026-10-09_v1.html` (respaldo, no leer). Este `.md` es la copia para leer y actualizar.

## Para qué sirve este informe

Es la forma con DevTools de un ejercicio con tres formas. Se hace a mano en el navegador, sin escribir un programa: sirve para ver el sitio como lo ve el código y para comparar su resultado con el del manual y el de agentes.

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


## Cómo trabajamos

El proceso es guiado, igual que el manual: Claude indica el paso, tú lo haces en el navegador y cuentas qué viste. Claude no avanza al siguiente paso hasta tener tu resultado, y marca el paso en el checklist.

| Quién | Qué hace |
|---|---|
| Claude | Explica qué se va a entender, entrega la línea de consola cuando haga falta e indica en qué pestaña de DevTools se ejecuta y qué debería verse. |
| Tú | Abres DevTools con F12, ejecutas o miras lo indicado y reportas lo que apareció, incluidos los errores completos o una captura. |
| Claude | Anota tu resultado en este informe, marca el paso como hecho, explica en CONCEPTOS lo nuevo y da el siguiente paso. |

> **Nota sobre las reglas** Abrir el sitio con tu navegador es una visita humana. Aun así, para que la comparación sea justa y respetuosa, se usa la misma muestra que en las otras formas (3 páginas y luego 10) y un ritmo tranquilo. Los permisos (robots.txt y términos de uso) se reutilizan del informe manual.


## Checklist de pasos

Los pasos 2 a 4 son el mapeo; el 5, el filtrado; del 6 al 8, el scraping; el 9 y el 10 cierran con la ficha y la muestra.

- [ ] **Paso 1. Abrir DevTools y reconocer sus pestañas** *(en curso)* — Navegador (F12) · Etapa 0 · Qué muestran Elements, Console, Network y Sources.
- [ ] **Paso 2. Leer los enlaces de la portada con la consola** — Navegador · Etapa 2 · Cómo se lista lo que enlaza una página.
- [ ] **Paso 3. Recorrer una categoría y un artículo** — Navegador · Etapa 2 · Cómo se descubre el sitio de página en página (el rastreo a mano).
- [ ] **Paso 4. Comparar con el sitemap** — Navegador · Etapa 2 · Qué páginas aparecen en un mapa y no en el otro.
- [ ] **Paso 5. Elegir a mano los artículos útiles** — Navegador · Etapa 3 · Cómo filtra una persona: leyendo y juzgando.
- [ ] **Paso 6. Inspeccionar el HTML de un artículo con Elements** — Navegador (F12) · Etapa 4 · Dónde viven el título, el autor, la fecha y el texto.
- [ ] **Paso 7. Extraer título, autor, fecha y párrafos con la consola** — Navegador · Etapa 4 · Cómo se lee una página con selectores.
- [ ] **Paso 8. Ver lo que descarga el navegador con Network** — Navegador · Etapa 4 · Cuántas peticiones genera una sola página.
- [ ] **Paso 9. Guardar la ficha y la cita** — Etapa 5 · Cómo queda un dato citable cuando se guarda a mano.
- [ ] **Paso 10. Muestra de 3 y luego 10 páginas** — Navegador · Etapas 4 y 5 · Qué pasa al repetir a escala, con ritmo tranquilo.


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

> **Ojo con las peticiones** En DevTools una sola página dispara muchas peticiones (imágenes, scripts, anuncios). Se registran las que muestra la pestaña Network, y no son comparables una a una con las del código, que descarga solo el HTML.

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


### Etapa 0. Preparación

| Bloque | Registro |
|---|---|
| Qué se hizo | Paso 1: abrir DevTools y reconocer sus pestañas. No hay que instalar nada: viene en Chrome. |
| Resultado | Pendiente. |
| Costo (tiempo, peticiones, tokens) | Pendiente. |
| Qué falló o sorprendió | Pendiente. |
| Conclusión | Pendiente. |


### Etapa 1. Permisos (reutiliza el manual)

| Bloque | Registro |
|---|---|
| Qué se hizo | Se reutiliza la etapa 1 del informe manual: robots.txt verificado y términos de uso revisados el 9 oct 2026. |
| Resultado | Ver el informe manual, etapa 1. Resumen: luz verde con 6 rutas prohibidas y `Crawl-delay: 10`; los términos no prohíben expresamente el scraping, pero rigen los derechos de autor. |
| Costo (tiempo, peticiones, tokens) | Pendiente. |
| Qué falló o sorprendió | Pendiente. |
| Conclusión | Pendiente. |


### Etapa 2. Mapeo

| Bloque | Registro |
|---|---|
| Qué se hizo | Pasos 2 a 4: enlaces de la portada, recorrido de una categoría y un artículo, y comparación con el sitemap. |
| Resultado | Pendiente. |
| Costo (tiempo, peticiones, tokens) | Pendiente. |
| Qué falló o sorprendió | Pendiente. |
| Conclusión | Pendiente. |


### Etapa 3. Filtrado

| Bloque | Registro |
|---|---|
| Qué se hizo | Paso 5: elegir a mano los artículos útiles. |
| Resultado | Pendiente. |
| Costo (tiempo, peticiones, tokens) | Pendiente. |
| Qué falló o sorprendió | Pendiente. |
| Conclusión | Pendiente. |


### Etapa 4. Scraping

| Bloque | Registro |
|---|---|
| Qué se hizo | Pasos 6, 7, 8 y 10: inspección del HTML, extracción con la consola, Network y muestra de 3 y luego 10 páginas. |
| Resultado | Pendiente. |
| Costo (tiempo, peticiones, tokens) | Pendiente. |
| Qué falló o sorprendió | Pendiente. |
| Conclusión | Pendiente. |


### Etapa 5. Archivo y reescritura

| Bloque | Registro |
|---|---|
| Qué se hizo | Paso 9: ficha con cita. El artículo propio va aparte, no dentro del informe. |
| Resultado | Pendiente. |
| Costo (tiempo, peticiones, tokens) | Pendiente. |
| Qué falló o sorprendió | Pendiente. |
| Conclusión | Pendiente. |


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
| v1 | 9 de octubre de 2026 | `analisis-resultados-mapeo-scraping-con-devtools_2026-10-09_v1.html` | Plan: modo de trabajo, checklist de 10 pasos, esqueleto, métricas, resultados pendientes y sección CONCEPTOS (qué es DevTools, la consola y la lectura de enlaces). |

Cada vez que se cierre un paso o una etapa se actualiza este informe y se guarda una versión nueva con la fecha en el nombre.


---

# CONCEPTOS DEL PROCESO IMPORTANTES PARA ENTENDER

Esta sección es para aprender, no para registrar resultados. Está escrita para alguien que empieza, con palabras simples y ejemplos. Crece con cada paso. Los conceptos de permisos (robots.txt, términos de uso, derechos de autor) están explicados en el informe manual y valen igual aquí. La etiqueta amarilla al frente de cada título indica a qué etapa y paso del proceso pertenece: haz clic en ella para ir a esa etapa, y el recuadro «Para qué» explica por qué se hizo eso y cuál es su objetivo.


## [Etapa 0 · Paso 1] 1. Qué es DevTools

> **Para qué:** Ver por dentro cómo está hecha una página, sin escribir un programa.

**DevTools** (herramientas para desarrolladores) es un panel que trae el navegador Chrome. Se abre con la tecla **F12** (o clic derecho sobre la página y «Inspeccionar»). Muestra por dentro cómo está hecha la página que estás viendo: su código, lo que descarga y los mensajes que genera.

Analogía: una página web es como una casa vista desde la calle; DevTools son los rayos X que dejan ver las paredes, las tuberías y los cables. No cambia la casa: solo la muestra.

| Pestaña | Qué muestra | Para qué la usamos |
|---|---|---|
| **Elements** | El HTML de la página, ordenado como un árbol de etiquetas. | Encontrar dónde vive el título, el autor, la fecha y el texto de un artículo. |
| **Console** | Una línea de comandos donde se escribe JavaScript que se ejecuta sobre la página abierta, y los mensajes de error o aviso de la página. | Leer datos de la página con una línea de código, por ejemplo la lista de enlaces. |
| **Network** | Cada archivo que el navegador descarga al cargar la página: HTML, imágenes, scripts, anuncios. | Ver cuántas peticiones genera una sola página. |
| **Sources** | Los archivos de código de la página. | No la usamos por ahora. |


## [Etapa 2 · Paso 2] 2. Qué es la consola y cómo leer los enlaces de una página

> **Para qué:** Sacar la lista de enlaces de una página con una sola línea: es mapear a mano.

La consola recibe una línea de JavaScript y la ejecuta sobre la página que tienes abierta. Esta lista los enlaces internos de la página:

```
const enlaces = [...new Set(
  [...document.querySelectorAll('a[href]')]
    .map(a => a.href.split('#')[0])
    .filter(h => new URL(h).hostname.endsWith('viviendoporelmundo.com'))
)].sort();
console.log(enlaces.length);
console.table(enlaces);
```

Cómo se lee, de adentro hacia afuera:

| Parte | Qué hace |
|---|---|
| `document.querySelectorAll('a[href]')` | Toma todos los enlaces de la página (`a` es la etiqueta de enlace y `href` es la dirección a la que apunta). |
| `a.href.split('#')[0]` | Quita lo que va después de `#` (el ancla), porque apunta al mismo lugar de la misma página. |
| `.filter(... endsWith('viviendoporelmundo.com'))` | Se queda solo con los enlaces **internos** y descarta los de afuera (YouTube, redes, Amazon). |
| `new Set(...)` | Elimina los repetidos. |
| `.sort()` | Los ordena alfabéticamente. |
| `console.log(enlaces.length)` | Imprime cuántos hay. |
| `console.table(enlaces)` | Los muestra en una tabla. |

> **Aviso de seguridad** Chrome bloquea el pegado en la consola como protección: si sale un aviso, hay que escribir `allow pasting` y pulsar Enter. Solo se pega código cuya lógica se entienda. Este solo lee la página, no modifica nada.


## [Etapa 2 · Paso 3] 3. Por qué DevTools mapea una página y no todo el dominio

> **Para qué:** Entender el límite de esta forma de mapear y por qué conviene compararla con el sitemap.

Cada ejecución de la línea anterior devuelve los enlaces de **la página que tienes abierta**. Para cubrir el sitio tendrías que repetirla en cada página que descubras. Eso es exactamente lo que hace un rastreo («crawl»): seguir enlaces de página en página. Con DevTools lo haces tú a mano; con código se automatiza.

| Forma de mapear | Alcance | Qué ve |
|---|---|---|
| Sitemap | Todo el dominio de una vez | La lista oficial que el dueño decidió publicar. |
| DevTools | Una página por vez | Lo que el sitio muestra: menús, categorías, pie de página. |
| Rastreo con código | Cientos de páginas, con espera | Lo mismo que DevTools, automático. |

Por eso conviene **comparar** el resultado de DevTools con el del sitemap: una página puede estar enlazada pero no aparecer en el sitemap, o al revés.


## [Etapa 1 · Permisos] 4. Una visita tuya no es una visita de un bot

> **Para qué:** Saber qué reglas aplican cuando entra una persona y por qué aun así se mantiene un ritmo tranquilo.

Abrir el sitio con tu navegador y mirar su código es una visita humana normal. El robots.txt y la espera de 10 segundos son reglas para **programas**. Aun así, para que la comparación entre las tres formas sea justa y respetuosa, aquí se usa la misma muestra (3 páginas y luego 10) y un ritmo tranquilo. Si algún paso se automatizara, volverían a regir las reglas del robots.txt.


## [Etapa 0 · Paso 1] 5. Los mensajes de error en rojo de la consola

> **Para qué:** No asustarse con mensajes que no tienen que ver con lo que hacemos.

Al abrir la consola en una página con publicidad aparecen errores en rojo y avisos en amarillo (por ejemplo `ERR_NAME_NOT_RESOLVED` o `generate_204`). Son de los scripts de terceros de la propia página (anuncios, YouTube, estadísticas). No tienen que ver con lo que hacemos y se ignoran.

