# Análisis de los resultados: mapeo y scraping manual

Registro de lo que sale en cada etapa del ejercicio sobre viviendoporelmundo.com, hecho a mano con Python y guiado paso a paso.

**Versión** v5 · **Fecha** 10 de octubre de 2026 · **Estado** Etapas 0 a 3 hechas

> Fuente original: `analisis-resultados-mapeo-scraping-manual_2026-10-10_v5.html` (respaldo, no leer). Este `.md` es la copia para leer y actualizar.

## Para qué sirve este informe

Es la forma manual con código de un ejercicio con tres formas: el mismo sitio, las mismas etapas y las mismas métricas. Se hace primero, a mano, para entender cada eslabón del proceso; las otras dos formas (DevTools y agentes) se comparan contra esta.

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

El proceso es guiado: Claude indica el paso, tú lo ejecutas y cuentas qué viste. Claude no avanza al siguiente paso hasta tener tu resultado, y marca el paso en el checklist.

| Quién | Qué hace |
|---|---|
| Claude | Explica qué se va a entender, genera el código cuando haga falta e indica en qué archivo va, dónde se ejecuta y qué debería verse. |
| Tú | Ejecutas en la terminal (PowerShell, en la raíz del proyecto, con `(.venv)` activo) o en el navegador, y reportas lo que apareció, incluidos los errores completos. |
| Claude | Anota tu resultado en este informe, marca el paso como hecho, explica en la sección CONCEPTOS los conceptos nuevos y da el siguiente paso. |

> **Objetivo** Entender el scraping y el mapeo en detalle. La velocidad llega después, con los agentes.


## Checklist de pasos

Los pasos 1 a 7 son el mapeo; del 9 al 11, el scraping. El filtrado (paso 8) es el puente entre los dos.

- [x] **Paso 1. Preparar el entorno** — Terminal · Etapa 0 · Se entiende por qué se aísla un proyecto Python.
- [x] **Paso 2. Leer los términos de uso** — Navegador · Etapa 1 · Qué permiso hay más allá del robots.txt.
- [x] **Paso 3. Leer el robots.txt con código** — Terminal · Etapa 1 · Cómo un programa pregunta si puede entrar.
- [x] **Paso 4. Abrir el `sitemap_index.xml`** — Navegador · Etapa 2 · Cómo se ve un índice de mapas.
- [x] **Paso 5. Descargar una página con código** — Terminal · Etapa 2 · Qué es una petición HTTP y el HTML crudo.
- [x] **Paso 6. Leer el índice y los mapas hijos** — Terminal · Etapa 2 · Cómo se pasa de un índice a la lista de URLs.
- [x] **Paso 7. Guardar las URLs en SQLite** — Terminal · Etapa 2 · Qué es una base de datos y cómo se evita duplicar.
- [x] **Paso 8. Filtrar las URLs** — Terminal · Etapa 3 · Dónde fallan las reglas fijas.
- [ ] **Paso 9. Inspeccionar el HTML de un artículo** *(en curso)* — Navegador (F12) · Etapa 4 · La estructura de una página.
- [ ] **Paso 10. Extraer el texto de una página** — Terminal · Etapa 4 · Qué hacen BeautifulSoup y trafilatura.
- [ ] **Paso 11. Guardar la ficha y la cita** — Terminal · Etapa 5 · Cómo queda un dato citable.
- [ ] **Paso 12. Muestra de 3 y luego las 8 de Colombia** — Terminal · Etapas 4 y 5 · Qué pasa al repetir a escala.


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


### Etapa 0. Preparación

| Bloque | Registro |
|---|---|
| Qué se hizo | Paso 1 hecho (9 oct 2026): se creó el entorno virtual `.venv` y se instalaron las librerías de la guía 1. `scraper.py` se crea en el paso 3 y `datos/scraping.db` en el paso 7. |
| Resultado | Python 3.12.10. Instalado: `requests` 2.34.2, `beautifulsoup4` 4.15.0, `lxml` 6.1.3 y `trafilatura` 2.3.1. La prueba de importación imprimió `Todo instalado`. La carpeta `.venv` queda fuera de git. |
| Costo (tiempo, peticiones, tokens) | 0 peticiones al sitio, 0 tokens. Tiempo no medido. |
| Qué falló o sorprendió | Nada falló. `pip` avisó de que hay una versión nueva (25.0.1 → 26.2.1); es solo un aviso y no hace falta actualizar. |
| Conclusión | El entorno está listo. Lo instaló Claude por petición del usuario, que no sabía dónde ejecutar los comandos; para los pasos con código se explicará cómo abrir la terminal. |


### Etapa 1. Permisos

| Bloque | Registro |
|---|---|
| Qué se hizo | Cerrada el 9 oct: el robots.txt está leído en el navegador, paso 2 (términos de uso) y paso 3 (robots.txt leído con código: `scraper.py` y `probar_robots.py`). |
| Resultado | Robots.txt (9 oct 2026): idéntico al del 8 oct, con y sin `www`; luz verde con 6 rutas prohibidas y `Crawl-delay: 10`. Términos de uso (aviso legal, leído el 9 oct): el texto recibido no menciona bots, scraping ni reproducción de contenido, pero sí tiene una cláusula general (1.7) que anuncia acciones civiles y penales contra «cualquier utilización indebida». El titular es una persona natural, el sitio se financia con afiliación y publicidad, y rige la ley española. La sección 1.4 no existe: la página del sitio salta de la 1.3 a la 1.4.2 (verificado con captura de pantalla el 9 oct). Conclusión del paso 2: no hay prohibición expresa de scraping; sí hay una cláusula general y rigen los derechos de autor por defecto. Lectura con código (paso 3): con la función de la guía tal cual, tres rutas prohibidas (`/xmlrpc.php`, `/readme.html`, `/wp-content/plugins/`) salían como permitidas; la causa es la línea en blanco tras `Crawl-delay`. Corregido: ahora las nueve rutas de prueba dan lo esperado, la espera es 10 s y se detecta el sitemap. |
| Costo (tiempo, peticiones, tokens) | Pendiente. |
| Qué falló o sorprendió | Lo más importante: el lector de robots.txt de Python (`urllib.robotparser`) descarta las reglas que vienen después de una línea en blanco; la guía 1 decía que daba `False` en esas rutas y no es cierto con este archivo. Además, el aviso legal salta de la sección 1.3 a la 1.4.2: faltan la 1.4 y la 1.4.1 en la propia página, no fue un error de copia. No sabemos qué decían, y justo ahí suelen ir las condiciones de uso de los contenidos. |
| Conclusión | El permiso existe, con límites claros. La lectura con código tiene una trampa: no se debe confiar en el lector de Python sin comprobarlo con las rutas prohibidas. El sitio no prohíbe expresamente el scraping, pero tampoco lo autoriza: que no diga nada no es un permiso. Se avanza con prudencia: muestra mínima, 10 s de espera, palabras propias y citas cortas con enlace. |


### Etapa 2. Mapeo

| Bloque | Registro |
|---|---|
| Qué se hizo | Etapa cerrada. Pasos 4 a 7 hechos (9 y 10 oct 2026): el sitemap visto en el navegador; la portada descargada con código (`pedir()` y `descargar()`); el índice y los dos mapas leídos con código (`leer_sitemap()`); y las 292 direcciones guardadas en la base de datos local `datos/scraping.db`, tabla `urls` (`abrir_base()`, `urls_desde_sitemap()` y `guardar_urls()`, probadas con `guardar_mapa.py`). |
| Resultado | Índice (`http://viviendoporelmundo.com/sitemap_index.xml`): generado por Yoast SEO, con **2 mapas hijos**, `post-sitemap.xml` (entradas) y `page-sitemap.xml` (páginas), ambos en `https://www.…`. `post-sitemap.xml`: **244 URLs** según su propio encabezado (el paso 6 lo confirmó con código), con fechas de modificación desde 2015-10-26 hasta 2026-06-20, ordenadas de la más antigua a la más reciente, y una columna con el número de imágenes por página (de 1 a 264). La fecha del índice (2026-06-20 04:46) coincide exactamente con la de la última entrada del mapa. `page-sitemap.xml`: 48 direcciones (contadas con código en el paso 6). No hay mapa de categorías ni de etiquetas. Paso 5 (portada, `http://viviendoporelmundo.com/`): código 200, tipo `text/html; charset=UTF-8`, 245.915 bytes de HTML, 1,86 s de respuesta; el sitio redirigió con un 301 a `https://www.viviendoporelmundo.com/`. El HTML crudo trae 136 etiquetas `<a href>` (conteo aproximado con expresión regular). Título: «Viviendo por el mundo - Fórmate como Nómada Digital y Viaja todo lo que quieras». Paso 6 (10 oct 2026, con código): el índice trae 2 mapas hijos y ninguna página suelta; `post-sitemap.xml` tiene **244** direcciones (coincide con el encabezado y con el paso 4) y `page-sitemap.xml` **48**; en total **292 direcciones, todas distintas**. Fechas de modificación de 2015-10-26 a 2026-06-20; por año, 2021 (78), 2025 (54) y 2026 (58) reúnen 190 de las 292. La fecha del índice para `page-sitemap.xml` (04:48:56) es exactamente la de su página más reciente. Paso 7 (10 oct 2026): las 292 direcciones guardadas en `datos/scraping.db` (unos 100 KB, fuera de git): 244 del mapa de entradas y 48 del de páginas, todas con `vale_la_pena` vacío. Volver a guardar no duplica ni borra marcas (probado en una copia). Carpetas: las 244 entradas cuelgan de la raíz; de las 48 páginas, 30 están en la raíz, 16 en `/paises/` (guías de costos por país) y 2 en `/quien-es-viviendo-por-el-mundo/`. Vistazo previo para Colombia, solo por palabras en la dirección: 9 direcciones, 8 entradas y la guía `/paises/guia-colombia-cuanto-cuesta-viajar/`. |
| Costo (tiempo, peticiones, tokens) | Paso 4: tres visitas con el navegador, sin programa. Paso 5: una página pedida con código; con la redirección fueron 2 peticiones al sitio, tras 10 s de espera, y la respuesta tardó 1,86 s. Paso 6: 3 peticiones (el índice y los dos mapas, más el robots.txt), 38 s en total con las esperas. Paso 7: otras 3 peticiones para leer los mapas otra vez y guardarlos (la base no hace peticiones). 0 tokens. |
| Qué falló o sorprendió | Tres cosas. 1) No hay mapa de categorías: el sitemap no es el plano completo. 2) En el mapa de entradas ninguna dirección tiene carpeta (`/blog/…`): todas cuelgan de la raíz; en el mapa de páginas, al menos las cinco últimas usan la carpeta `/paises/`. Las reglas de la guía (`PATRONES_UTILES`: `/blog/`, `/noticias/`, `/articulo/`) no coinciden con ninguna de las direcciones vistas. 3) `Last Mod.` no es la fecha de publicación: hay bloques de decenas de entradas con la misma fecha de edición (21 al 26 de julio de 2021) y otro de 9 entradas del 20 de junio de 2026. 4) Pedir la dirección con `http://` y sin `www` provocó una redirección 301: una sola página fueron dos peticiones, y el código sigue esa redirección sin esperar entre las dos, así que conviene pedir ya la dirección final (`https://www…`). 5) El inicio del HTML crudo es código (comentarios para navegadores antiguos, metadatos y scripts), no texto de artículo, y el título de la portada presenta el sitio como formación de nómada digital, lo que apunta a contenido comercial junto a los artículos de viaje. 6) El mapa de páginas tiene 48 direcciones, que no se habían visto en el navegador, y 18 de ellas usan carpeta: 16 en `/paises/` (guías de costos por país, que cuentan como material) y 2 en `/quien-es-viviendo-por-el-mundo/`. 7) En la primera ejecución del paso 7 falló la red (el nombre del sitio no se resolvió) y el programa se cayó con un error largo; el fallo fue momentáneo, pero mostró que leer el robots.txt no estaba protegido. Se corrigió: ahora `puede_visitar` avisa en una línea y no entra. 8) Buscar palabras de Colombia en las direcciones es solo un vistazo: puede dejar fuera artículos que hablan de Colombia sin nombrarla en la dirección. El filtro real es el paso 8. |
| Conclusión | El mapeo termina con 292 direcciones guardadas, sin repetidos y sin decidir. El sitemap sirvió de mapa, pero no basta: faltan categorías y mezcla contenido útil con podcasts, vídeos y venta. Siguiente: filtrar (etapa 3), empezando por Colombia. |


### Etapa 3. Filtrado

| Bloque | Registro |
|---|---|
| Qué se hizo | Etapa cerrada. Paso 8 hecho (10 oct 2026): las 292 direcciones marcadas con `vale_la_pena` y `motivo` usando reglas fijas sobre el nombre de la dirección y el mapa de origen (opciones A, B, C y D elegidas por el usuario), con `clasificar()` en `filtrar_colombia.py`. Cuentan todos los lugares de Colombia; no cuentan los vídeos; solo información tipo blog. |
| Resultado | **8 sí** y **284 no**. Las 8: la guía `/paises/guia-colombia-cuanto-cuesta-viajar/` y 7 entradas (Bogotá, Eje Cafetero, Cali y San Cipriano, Cartagena, Medellín y Guatapé, Taganga, Tayrona y Palomino). Descartes por motivo: 196 de otro tema, 32 páginas fijas, 15 vídeos o fotomontajes, 11 podcasts, 11 entrevistas, 10 de venta o afiliación y 9 posibles duplicados. El vídeo de Colombia quedó fuera, como se pidió. |
| Costo (tiempo, peticiones, tokens) | 0 peticiones al sitio y menos de un segundo. 0 tokens. Leer las 8 marcadas costará unos 80 segundos, en vez de casi 49 minutos para las 292. |
| Qué falló o sorprendió | 1) La regla de «posible duplicado» (termina en `-2`) se equivoca: atrapa partes de una serie, como `…-1-de-2`, `…-2-de-2` o `3-cosas-imprescindibles-mochila-2`, que no son copias. 2) La regla de venta descarta artículos que solo mencionan una palabra comercial, como `salud-vacunas-y-seguro-de-viaje-vuelta-al-mundo`, que posiblemente es información práctica. 3) La regla de tema no ve artículos que hablan de Colombia sin nombrarla en la dirección: esas omisiones no se pueden contar sin leer las páginas. 4) El script se cayó al final la primera vez, en la parte que muestra los dudosos, porque la portada no tiene nombre de página; las marcas ya estaban guardadas y se corrigió. |
| Conclusión | Las reglas fijas sirven para un primer corte barato y explicable, y sus errores no tocan a las 8 de Colombia, que son claras por su nombre. Pero fallan donde el nombre engaña y no ven lo que no está en la dirección: es el punto débil que se comparará con el agente. |


### Etapa 4. Scraping

| Bloque | Registro |
|---|---|
| Qué se hizo | En curso. Paso 9 (10 oct 2026): se abrió `/medellin-y-guatape/` en DevTools y se localizó el título; faltan la firma, la fecha y los párrafos. Pasos 10 y 12 pendientes: extraer el texto con código y hacerlo con una muestra de 3 y con las 8 marcadas, con 10 s de espera. |
| Resultado | Estructura localizada en `/medellin-y-guatape/`: `main.content` contiene un `article` (clase con `post-4906`, `category-america`, `category-colombia` y `tag-cronicas-de-viaje`), que lleva `header.entry-header` con `h1.entry-title` (texto: «Medellín y la gran sorpresa, Guatapé») y `p.entry-meta` (firma y fecha, sin abrir todavía), y después `div.entry-content`, el cuerpo del texto. En la página se ven la firma «BY … DE VIVIENDO POR EL MUNDO» y «9 comentarios». |
| Costo (tiempo, peticiones, tokens) | 0 peticiones del programa: una visita humana con el navegador. 0 tokens. |
| Qué falló o sorprendió | 1) El título («Medellín y la gran sorpresa, Guatapé») no coincide con el nombre de la dirección (`medellin-y-guatape`): otra razón por la que filtrar por el nombre no basta. 2) La etiqueta `article` declara sus categorías (`category-colombia`): es una señal de tema mucho más fiable que el nombre de la dirección y abre la opción de usar la página de la categoría «Colombia». 3) Dentro de `entry-content` hay elementos que no son texto del artículo, como los botones de compartir. 4) El buscador de DevTools dio «1 de 8» para «H1» porque cuenta toda aparición del texto, no solo etiquetas; la primera era la correcta. |
| Conclusión | Pendiente. |


### Etapa 5. Archivo y reescritura

| Bloque | Registro |
|---|---|
| Qué se hizo | Paso 11: ficha con cita. El artículo propio va aparte, no dentro del informe. |
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
| Muestra de la etapa 4 | 3 páginas y luego las 8 marcadas de Colombia. |
| Filtro elegido | Opciones A, B, C y D: mapa de origen, palabras de Colombia en la dirección, familia por el nombre y carpeta `/paises/`. Cuentan todos los lugares de Colombia; no cuentan los vídeos; solo información tipo blog. |
| Tema inicial | Colombia: el filtro del paso 8 busca el material que sirva para un artículo sobre ese tema. |
| Direcciones | Se guardan todas (292) y se marcan; no se borra nada. Las guías por país cuentan como material. |
| Contenido de terceros | El informe lleva cifras y citas cortas, nunca el texto completo de los artículos. |


## Versiones de este archivo

| Versión | Fecha | Archivo | Qué contiene |
|---|---|---|---|
| v1 | 9 de octubre de 2026 | `analisis-resultados-mapeo-scraping-manual_2026-10-09_v1.html` | Plan: modo de trabajo, checklist de pasos, esqueleto, métricas y resultados por etapa, todos pendientes. |
| v2 | 9 de octubre de 2026 | `analisis-resultados-mapeo-scraping-manual_2026-10-09_v2.html` | Cierra la etapa 0 (entorno) y la etapa 1 (permisos): robots.txt verificado y leído con código, términos de uso revisados, sección CONCEPTOS con los puntos 1 a 13. |
| v3 | 9 de octubre de 2026 | `analisis-resultados-mapeo-scraping-manual_2026-10-09_v3.html` | Agrega la tercera forma (DevTools) al contexto: tabla de las tres formas y métricas compartidas por tres informes. |
| v4 | 10 de octubre de 2026 | `analisis-resultados-mapeo-scraping-manual_2026-10-10_v4.html` | Cierra la etapa 2 (mapeo): sitemap leído con código (292 direcciones) y guardado en la base de datos `datos/scraping.db`; conceptos 14 a 18 y sección de códigos con 16 piezas. Tema inicial: Colombia. |
| v5 | 10 de octubre de 2026 | `analisis-resultados-mapeo-scraping-manual_2026-10-10_v5.html` | Cierra la etapa 3 (filtrado) con reglas fijas (opciones A, B, C y D): 8 direcciones de Colombia marcadas como útiles y 284 descartadas con su motivo; concepto 19 y piezas de código 17 y 18. |

Cada vez que se cierre un paso o una etapa se actualiza este informe y se guarda una versión nueva con la fecha en el nombre.


---

# CONCEPTOS DEL PROCESO IMPORTANTES PARA ENTENDER

Esta sección es para aprender, no para registrar resultados. Está escrita para alguien que empieza en este campo, con palabras simples y ejemplos. Crece con cada paso: cada vez que aparezca algo nuevo, se explica aquí. La etiqueta amarilla al frente de cada título indica a qué etapa y paso del proceso pertenece (haz clic en ella para ir a esa etapa), y el recuadro «Para qué» explica por qué se hizo eso y cuál es su objetivo.

> **Qué cubre ahora** Todo lo que sacamos del archivo robots.txt (etapa 1). Se agregarán después: entorno virtual y librerías (paso 1), términos de uso (paso 2), el sitemap, el HTML y la extracción del texto.


## [Etapa 1 · Permisos] 1. Qué es el robots.txt

> **Para qué:** Saber, antes de visitar nada, qué partes del sitio nos piden no tocar y a qué ritmo. Es el primer permiso que se revisa.

Es un archivo de texto que casi todos los sitios web tienen. Sirve para decirle a los programas automáticos (los **bots**) qué partes del sitio pueden visitar y cuáles no.

Piénsalo como los carteles en la puerta de un edificio: «Oficina del administrador: no pasar», «Sala de máquinas: no pasar», «Visitantes: toquen el timbre una vez cada 10 segundos». El edificio no tiene guardias que te frenen. Es una petición de cortesía, y un scraper responsable la respeta siempre.

> **Dos ideas clave** 1) No es un candado, es un pedido: nada te impide entrar, por eso la responsabilidad es nuestra. 2) No dice nada sobre derechos de autor ni sobre los términos de uso del sitio.


## [Etapa 1 · Permisos] 2. La dirección: dónde vive

> **Para qué:** Encontrar el robots.txt sin buscarlo: siempre está en el mismo lugar.

```
https://www.viviendoporelmundo.com/robots.txt
```

| Parte | Qué es | En este caso |
|---|---|---|
| Protocolo | Cómo se conecta tu navegador con el sitio. `https` es una conexión cifrada. | `https://` |
| Dominio | El nombre del sitio: dónde está. | `www.viviendoporelmundo.com` |
| Ruta | El archivo o página que pides dentro del sitio. | `/robots.txt` |

El robots.txt siempre vive en la raíz del dominio y se llama exactamente así. No hay que buscarlo: se escribe la dirección completa.


## [Etapa 1 · Permisos] 3. El archivo que extrajimos, completo

> **Para qué:** Ver el archivo entero y entender cómo se organiza antes de explicar cada línea.

```
User-agent: *
Disallow: /cgi-bin/
Disallow: /wp-admin/
Disallow: /wp-includes/
Crawl-delay: 10

Disallow: /xmlrpc.php
Disallow: /readme.html
Allow: /wp-content/uploads/
Disallow: /wp-content/plugins/

Sitemap: http://viviendoporelmundo.com/sitemap_index.xml

User-Agent: Googlebot
Allow: .js
Allow: .css
```

Tiene **dos bloques** y **una línea suelta**. Un bloque empieza con una línea `User-agent:` y sigue con sus reglas; cuando aparece otro `User-agent:`, cambia el destinatario.

| Parte | Para quién es |
|---|---|
| Bloque 1: `User-agent: *` y todo lo que sigue hasta la línea `Sitemap:` | Todos los bots. Incluye al nuestro. |
| Línea `Sitemap:` | Para cualquiera. No pertenece a ningún bloque: es un aviso general. |
| Bloque 2: `User-Agent: Googlebot` | Solo el bot de Google. |


## [Etapa 1 · Permisos] 4. Cada línea explicada (las «variables»)

> **Para qué:** Saber qué pide cada línea, y poder leer el robots.txt de cualquier otro sitio.

Cada línea tiene la forma `nombre: valor`. El nombre se llama **directiva** y funciona como una variable: lo que va después de los dos puntos es su valor. En este archivo solo importan cinco directivas.

**a) `User-agent` — a quién va dirigido**

El *user-agent* es el nombre con el que un programa se presenta ante un sitio. Cuando abres una página con Chrome, Chrome se presenta como navegador. Cuando Google recorre el sitio, se presenta como `Googlebot`. Nuestro scraper tendrá un nombre propio, por ejemplo `MiBotInvestigacion`.

El valor `*` es un comodín que significa «todos». Ejemplo: es como un cartel que dice «Para todos los invitados…», frente a otro que dice «Solo para el DJ…».

**b) `Disallow` — prohibido**

Su valor es una **ruta**: la parte de la dirección que va después del dominio. Prohíbe esa ruta y todo lo que cuelga de ella.

| Regla | Prohíbe | No prohíbe |
|---|---|---|
| `Disallow: /wp-admin/` | `/wp-admin/`, `/wp-admin/login.php`, `/wp-admin/usuarios/` | `/wp-contacto/` (empieza distinto) |

La comparación se hace por **prefijo**: si la dirección empieza igual que la ruta de la regla, la regla aplica.

**c) `Allow` — permitido**

Lo contrario de `Disallow`. Sirve para dejar abierta una carpeta, o como excepción dentro de algo prohibido. Aquí `Allow: /wp-content/uploads/` deja abierta la carpeta de fotos. Fíjate que `/wp-content/plugins/` está prohibida y `/wp-content/uploads/` permitida, y las dos están dentro de `/wp-content/`: cada regla se evalúa por separado.

**d) `Crawl-delay` — cuánto esperar**

Su valor es un número de segundos: el tiempo que debes esperar entre una petición y la siguiente. Con `Crawl-delay: 10` puedes pedir como máximo 6 páginas por minuto. Ejemplo: tocar el timbre una vez cada 10 segundos, no diez veces seguidas.

| Páginas | Tiempo mínimo (páginas × 10 s) |
|---|---|
| 50 | unos 8 minutos |
| 500 | cerca de 1 hora 23 minutos |
| 5.000 | unas 14 horas |

`Crawl-delay` no es parte oficial del estándar y Google lo ignora, pero la mayoría de bots y nosotros sí lo respetamos: un servidor pequeño se puede caer si recibe muchas peticiones seguidas.

**e) `Sitemap` — el plano del sitio**

Su valor es la dirección completa del **mapa del sitio**: un archivo con la lista de páginas que el sitio quiere que se conozcan. No pertenece a ningún bloque, es un aviso para todos. Analogía: el plano del edificio, colgado en la entrada.

Aquí es `http://viviendoporelmundo.com/sitemap_index.xml`, con dos detalles. Empieza con `http://` sin la «s» (el navegador normalmente te redirige solo). Y se llama `sitemap_index`, lo que indica que es un **índice**: no lista páginas directamente, sino otros mapas más pequeños.


## [Etapa 1 · Permisos] 5. Qué es cada ruta y para qué existe

> **Para qué:** Entender por qué se prohíbe cada ruta, para que no sea una lista de reglas sin sentido.

| Ruta | Qué es | Por qué importa |
|---|---|---|
| `/cgi-bin/` (prohibida) | Carpeta técnica del servidor, con programas internos. | No tiene artículos. |
| `/wp-admin/` (prohibida) | Panel de administración de WordPress, donde el dueño inicia sesión para publicar. | Es privada. |
| `/wp-includes/` (prohibida) | Archivos internos de WordPress. | Es código, no contenido. |
| `/xmlrpc.php` (prohibida) | Puerta técnica antigua para controlar WordPress a distancia. | Los sitios la cierran porque suele ser blanco de ataques. |
| `/readme.html` (prohibida) | Archivo de instalación de WordPress. | Sin contenido útil. |
| `/wp-content/plugins/` (prohibida) | Las extensiones instaladas en el sitio. | Es código, no contenido. |
| `/wp-content/uploads/` (permitida) | Donde WordPress guarda las fotos y archivos que se suben. | Que se pueda entrar no significa que se puedan reutilizar las fotos: tienen derechos de autor. |

> **Pista, no certeza** Que las rutas empiecen con `wp-` sugiere que el sitio está hecho con WordPress. Es una deducción, no un dato confirmado.


## [Etapa 1 · Permisos] 6. Los dos bloques: a quién le toca cada uno

> **Para qué:** Saber qué reglas nos tocan a nosotros y cuáles son solo de Google.

La regla: un bot busca el bloque que lleva **su propio nombre**. Si lo encuentra, sigue solo ese y deja de lado el resto. Si no lo encuentra, usa el bloque `*`.

| Bot | Bloque que lee | Qué le toca |
|---|---|---|
| Googlebot | El suyo (bloque 2) | Puede cargar archivos `.js` y `.css`. Ignora las reglas del bloque 1. |
| Nuestro scraper (`MiBotInvestigacion`) | `*` (bloque 1) | Las seis rutas prohibidas y la espera de 10 segundos. |
| Cualquier otro bot | `*` (bloque 1) | Lo mismo que el nuestro. |

¿Por qué existe el bloque de Googlebot? `.js` son los archivos de comportamiento de una página y `.css` los de diseño. Al permitírselos, Google ve la página como la vería una persona, con su aspecto completo.


## [Etapa 1 · Paso 3] 7. La lógica de decisión: ¿puedo entrar a esta página?

> **Para qué:** Que el programa pueda responder solo, página por página, si puede entrar o no.

1. Busco el bloque que lleva mi nombre. Si no hay, uso el bloque `*`.
2. Comparo la ruta de la página con las reglas `Disallow` y `Allow` de ese bloque.
3. Si ninguna regla coincide, está permitido.
4. Si coincide un `Disallow`, está prohibido, salvo que también coincida un `Allow` más específico (más largo).
5. Aun estando permitido, espero el `Crawl-delay` entre una página y la siguiente.

Ejemplos con el bloque `*` de este sitio:

| Dirección | ¿Puedo entrar? | Por qué |
|---|---|---|
| `/` (la portada) | Sí | Ninguna regla la prohíbe. |
| `/un-articulo/` | Sí | Ninguna regla la prohíbe. |
| `/wp-admin/` | No | Coincide con `Disallow: /wp-admin/`. |
| `/wp-admin/login.php` | No | Cuelga de `/wp-admin/`: el prefijo coincide. |
| `/wp-content/uploads/2025/foto.jpg` | Sí (la foto no se reutiliza) | `Allow: /wp-content/uploads/`. El permiso es de acceso, no de derechos de autor. |
| `/wp-content/plugins/algo/` | No | Coincide con `Disallow: /wp-content/plugins/`. |
| `/xmlrpc.php` | No | Coincide con `Disallow: /xmlrpc.php`. |

Esta tabla se comprobó con código en el paso 3 (punto 13), después de corregir una trampa del lector de Python.


## [Etapa 1 · Permisos] 8. Qué obtuvimos y para qué sirve

> **Para qué:** Ver qué nos dejó el paso de permisos y para qué se usa después cada dato.

El robots.txt no da contenido: da **permisos, límites y pistas**.

| Lo que descubrimos | Qué obtenemos | Para qué sirve |
|---|---|---|
| No hay `Disallow: /` para el bloque `*` | Permiso general: el contenido público no está prohibido. | Luz verde para seguir con el mapeo. |
| Seis rutas prohibidas | Una lista de exclusión. | El código las evita solo con la función `puede_visitar()`. |
| `Crawl-delay: 10` | Nuestro ritmo: una página cada 10 segundos. | Calcular cuánto tardará el trabajo y configurar la espera. |
| `Sitemap: …/sitemap_index.xml` | La dirección del mapa del dominio. | Es el siguiente archivo que abrimos. |
| Bloque aparte para Googlebot | Un sitio puede tratar distinto a cada bot. | Enseña a leer siempre el bloque que nos toca. |


## [Etapa 1 · Paso 2] 9. Lo que el robots.txt NO dice

> **Para qué:** No confundir «el robots.txt me deja pasar» con «puedo copiar todo».

- No dice nada sobre derechos de autor: poder entrar no es poder copiar. Por eso lo que se publique va reescrito y con la fuente citada.
- No dice nada sobre los términos de uso, que pueden ser más estrictos. Por eso el paso 2 es leerlos antes de extraer contenido.
- No dice nada sobre lo que está detrás de un inicio de sesión o un pago: eso no se extrae.


## [General · Todas las etapas] 10. Mini glosario

> **Para qué:** Tener a mano el significado de las palabras que más se repiten.

| Palabra | Significado simple |
|---|---|
| Bot | Programa que visita sitios web de forma automática. |
| Scraping | Sacar datos de una página web con un programa, en vez de copiarlos a mano. |
| Crawling | Recorrer un sitio siguiendo enlaces para descubrir qué páginas tiene. |
| Dominio | El nombre del sitio, por ejemplo `viviendoporelmundo.com`. |
| Ruta | La parte de la dirección después del dominio, por ejemplo `/wp-admin/`. |
| Directiva | Cada línea `nombre: valor` del robots.txt. |
| Comodín `*` | Símbolo que significa «todos» o «cualquiera». |
| Prefijo | El principio de algo. Una regla aplica a todas las rutas que empiezan igual. |
| HTTP / HTTPS | El lenguaje con el que tu navegador pide páginas. La «S» añade cifrado. |
| Error 404 | «No existe». Si el sitio no tiene robots.txt devuelve 404: no prohíbe nada, pero obliga a leer los términos de uso. |


## [Etapa 0 · Paso 1] 11. Entorno virtual y librerías (paso 1)

> **Para qué:** Tener las herramientas del proyecto instaladas y aisladas, sin mezclarlas con las de otros proyectos.

**Python** es el lenguaje en el que escribimos los programas. Por sí solo sabe hacer lo básico; para tareas específicas (descargar páginas, leer HTML) se le agregan **librerías**: paquetes de código ya escrito por otras personas.

**Entorno virtual (`.venv`)** es una carpeta dentro del proyecto con una copia limpia de Python y sus propias librerías. Es como una caja de herramientas exclusiva de este proyecto: lo que instalas aquí no afecta a otros proyectos ni al Python del computador, y otro proyecto puede usar versiones distintas sin pelearse.

| Comando | Qué hace | Ejemplo para entenderlo |
|---|---|---|
| `python --version` | Pregunta qué versión de Python hay instalada. | Mirar el modelo del carro antes de comprar repuestos. |
| `python -m venv .venv` | Crea la carpeta `.venv` con la copia limpia de Python. | Armar una caja de herramientas vacía. |
| `pip install ...` | Descarga e instala librerías dentro de `.venv`. `pip` es el instalador de Python. | Llenar la caja con las herramientas que vas a usar. |
| `python -c "import ..."` | Prueba que las librerías se pueden usar. | Comprobar que cada herramienta abre y funciona. |

| Librería | Para qué la usamos | Analogía |
|---|---|---|
| `requests` | Descarga páginas web por internet. | El mensajero que trae el paquete. |
| `beautifulsoup4` | Lee el HTML de una página y permite buscar etiquetas dentro de él. | Abrir el paquete y mirar lo que hay. |
| `lxml` | El motor que usa BeautifulSoup para leer el HTML rápido y bien. | La lupa de BeautifulSoup. |
| `trafilatura` | Deja solo el texto principal del artículo, sin menús ni publicidad. | Quedarte con la carne y tirar el empaque. |

¿Por qué `.venv` no se sube a git? Porque pesa mucho y se puede volver a crear en cualquier momento con los mismos comandos. Lo que sí se guarda es la lista de librerías necesarias (el `requirements.txt`, que crearemos con el primer script).


## [Etapa 1 · Paso 2] 12. Términos de uso, derechos de autor y derecho de cita (paso 2)

> **Para qué:** Saber qué permite el dueño más allá del robots.txt antes de extraer contenido. Es la condición para pasar a la extracción.

El **robots.txt** es un pedido dirigido a los bots. Los **términos de uso** (o aviso legal) son las reglas que el dueño del sitio pone a quien lo usa. Pueden ser más estrictos: un sitio puede prohibir copiar su contenido o usar programas automáticos aunque su robots.txt lo deje pasar. Por eso se leen antes de extraer nada.

Qué buscamos en ellos y qué encontramos en el aviso legal de este sitio (leído el 9 de octubre de 2026):

| Qué buscar | Por qué importa | Qué encontramos |
|---|---|---|
| ¿Prohíbe bots, scraping o uso automatizado? | Si lo prohíbe, nos detenemos. | No lo menciona. |
| ¿Prohíbe copiar o reproducir contenido? | Define qué podemos hacer con lo que leamos. | No aparece. |
| Propiedad intelectual | Dice quién es dueño del contenido. | No hay sección de propiedad intelectual: la página salta de la 1.3 a la 1.4.2. |
| Cláusula general de uso indebido | Es el aviso de que habrá consecuencias si se abusa. | Sección 1.7: el sitio perseguirá «cualquier utilización indebida» con acciones civiles y penales. Es genérica. |
| Quién es el titular y de qué vive el sitio | Ayuda a medir el impacto de lo que hacemos. | Es una persona natural; se financia con afiliación y publicidad. El contenido es su fuente de ingresos, y eso es una razón más para no copiarlo. |
| Ley que aplica | Define qué reglas rigen. | La española (LSSI y protección de datos europea). |

> **El hueco del aviso legal** La numeración salta de la sección 1.3 a la 1.4.2. Faltan la 1.4 y la 1.4.1, y eso es así en la propia página (verificado con captura el 9 de octubre). No sabemos qué decían. Que un texto no diga nada **no es un permiso**: por defecto, lo que alguien escribe está protegido por derechos de autor aunque no exista una cláusula que lo diga.

**Derechos de autor.** Protegen la *forma* en que algo está escrito, no los hechos ni las ideas. Ejemplo: «el museo abre a las 9 y la entrada cuesta 10 euros» es un hecho y se puede contar con palabras propias; la frase exacta tal como la escribió el autor está protegida. Por eso el proyecto reescribe con palabras propias y cita la fuente.

**Derecho de cita.** Permite usar un fragmento corto de un texto ajeno para comentarlo o analizarlo, siempre diciendo quién es el autor y de dónde sale. No equivale a copiar el artículo. Regla del proyecto: citas textuales de máximo 15 palabras, con enlace.

**Datos personales.** El aviso legal contiene datos de su titular (nombre, dirección, correo). Son públicos porque la ley obliga a publicarlos, pero no se guardan en la base de datos ni en estos informes: extraer datos de personas tiene reglas propias.

**Enlaces de afiliado.** El sitio gana comisiones cuando alguien compra a través de sus enlaces. No se copian esos enlaces: apuntan a su cuenta de afiliado.

> **Aviso** Esto es una guía de buenas prácticas para aprender, no asesoría legal. Si el proyecto llega a publicarse o a venderse, conviene consultarlo con quien lleve el tema legal.


## [Etapa 1 · Paso 3] 13. Leer el robots.txt con código (paso 3)

> **Para qué:** Que el programa respete las reglas solo, en vez de depender de que nosotros las recordemos.

En vez de leer el archivo a ojo cada vez, un programa se lo pregunta al robots.txt. Python trae para eso una herramienta llamada `RobotFileParser`. Se usan tres preguntas, que son las tres funciones de `scraper.py`:

| Función | Qué pregunta | Qué devuelve |
|---|---|---|
| `puede_visitar(url)` | ¿Puede nuestro bot visitar esta dirección? | `True` (sí) o `False` (no). |
| `espera_del_sitio(url)` | ¿Cuántos segundos hay que esperar entre una página y la siguiente? | El `Crawl-delay` del sitio, o 2 segundos si el sitio no indica nada. |
| `_robots(base)` | Descarga y lee el robots.txt de un sitio. Las otras dos funciones se apoyan en esta. | El archivo ya interpretado. `lru_cache` hace que se descargue una sola vez por sitio, no una vez por página. |

**Cómo se usa el nombre del bot.** `can_fetch(USER_AGENT, url)` busca el bloque que lleva nuestro nombre; como no hay ninguno, usa el bloque `*`. Es la regla de la sección 6 aplicada por el programa.

**Qué hace el código, paso a paso:**

1. `requests.get(...)` descarga el archivo presentándose con nuestro nombre.
2. Si la respuesta es 401 o 403, el sitio nos cierra la puerta: el programa asume que no podemos entrar a nada (`disallow_all`).
3. Si es otro error (por ejemplo 404, «no existe»), el sitio no tiene robots.txt y no prohíbe nada (`allow_all`); aun así quedan los términos de uso.
4. Si todo va bien, `_normalizar` arregla el texto y `rp.parse(...)` lo interpreta.

> **La trampa que encontramos** El robots.txt de este sitio tiene una **línea en blanco** justo después de `Crawl-delay: 10`. El lector de Python entiende que una línea en blanco cierra el bloque y **descarta todas las reglas que vienen después**. Resultado: `/xmlrpc.php`, `/readme.html` y `/wp-content/plugins/`, que están prohibidas, salían como permitidas. La función `_normalizar` quita esas líneas en blanco antes de leer el archivo. Lección: nunca se confía en un resultado sin comprobarlo con casos que sabemos que deben dar «no».

**Ejemplo de la prueba** (`probar_robots.py`, con el archivo ya corregido):

| Ruta | Resultado | Por qué |
|---|---|---|
| `/` y `/un-articulo/` | SÍ | Ninguna regla las prohíbe. |
| `/wp-admin/`, `/wp-admin/login.php`, `/wp-includes/js/jquery.js` | NO | Cuelgan de rutas prohibidas. |
| `/wp-content/uploads/2025/foto.jpg` | SÍ | Está permitida de forma explícita (la foto no se reutiliza). |
| `/wp-content/plugins/algo/`, `/xmlrpc.php`, `/readme.html` | NO | Prohibidas; son las tres que fallaban antes de la corrección. |

También devolvió una espera de **10 segundos** y la dirección del mapa: `http://viviendoporelmundo.com/sitemap_index.xml`.

> **Pendiente de tu parte** El nombre del bot lleva un correo de ejemplo (`tu-correo@dominio.com`). Antes de descargar páginas de verdad (paso 5) hay que poner un correo real, para que el dueño del sitio sepa a quién escribir si el bot le molesta.


## [Etapa 2 · Paso 4] 14. El sitemap: el plano del sitio (paso 4)

> **Para qué:** Saber **qué páginas existen en el sitio** antes de leer ninguna. Es el primer paso del mapeo. Analogía: antes de escribir sobre una biblioteca enorme pides el catálogo, la lista de todos los libros, sin abrir ninguno.

**Por qué importaba hacerlo antes de leer nada:**

1. **Ahorra trabajo.** Sin catálogo habría que ir de enlace en enlace buscando páginas, que es lento y puede dejar cosas fuera.
2. **Respeta el ritmo del sitio.** Con 10 segundos de espera entre páginas, leer 244 tarda cerca de 41 minutos. Saber el número *antes* permite calcular cuánto tiempo y cuánto trabajo es.
3. **Permite elegir.** No todas las páginas sirven para el artículo. Con solo ver los nombres ya aparecen guías de lugares (útiles), podcasts y vídeos (poco texto) y artículos comerciales (mejor descartarlos). Esa selección es el paso 8.
4. **Es la forma amable de mapear.** El sitio mismo publica ese catálogo para que los programas lo usen, así que pedirlo es lo esperado y cuesta muy poco al servidor.

**Cómo encaja en el camino.** El paso 4 fue *ver* el catálogo. Los siguientes lo vuelven útil:

| Paso | Qué hace con el catálogo |
|---|---|
| 5 | Aprende a descargar una página con código. |
| 6 | Lee el catálogo con código, en vez de a ojo, y cuenta las URLs de verdad. |
| 7 | Guarda la lista en la base de datos para trabajar con ella. |
| 8 | Elige cuáles de las 244 valen la pena. |

> **En resumen** El paso 4 no produjo datos para el artículo: produjo el **mapa para saber dónde buscarlos**.

Un **sitemap** es un archivo con la lista de páginas que un sitio quiere que se conozcan. El propio archivo lo dice en su encabezado: «meant for consumption by search engines», es decir, «hecho para que lo consuman los buscadores». Como nosotros también somos un programa que recorre el sitio, lo aprovechamos. Analogía: el índice de un libro, que te dice qué hay y dónde, sin que tengas que hojearlo entero.

**El formato.** El archivo termina en `.xml`. XML es un lenguaje de etiquetas, parecido al HTML pero pensado para guardar datos en vez de dibujar páginas. Tu navegador lo mostró como una tabla bonita; por dentro son etiquetas como `<loc>`.

**Dos tipos de archivo.** Un sitio puede tener un solo mapa, o un **índice** que apunta a varios mapas. Analogía: una enciclopedia en tomos. El índice es la lista de tomos, y cada tomo es la lista de las páginas que contiene.

| Tipo | Etiqueta que lo abre | Qué contiene | En este sitio |
|---|---|---|---|
| Índice de mapas | `<sitemapindex>`, con una `<sitemap>` por cada hijo | Direcciones de otros mapas | `sitemap_index.xml`: lista 2 mapas. |
| Mapa de páginas | `<urlset>`, con una `<url>` por cada página | Direcciones de páginas del sitio | Cada uno de los dos hijos. |

| Etiqueta | Qué significa | Ejemplo de lo que vimos |
|---|---|---|
| `<loc>` | La dirección (*location*) del mapa o de la página. | `https://www.viviendoporelmundo.com/post-sitemap.xml` |
| `<lastmod>` | Fecha y hora de la última modificación. | `2026-06-20 04:46 +00:00` |

`+00:00` indica la zona horaria: son las 04:46 en hora universal (UTC). Para saber la hora en Colombia se restan 5 horas. Lo importante es la fecha: dice cuándo cambió por última vez el contenido de ese mapa.

**Quién lo generó: Yoast SEO.** La página dice «Generated by Yoast SEO». Yoast SEO es un plugin (una extensión) de **WordPress** que crea y actualiza este archivo solo, cada vez que se publica algo. Eso confirma que el sitio es WordPress: hasta ahora era una deducción por las rutas con `wp-`.

**Qué vimos en el índice de este sitio** (9 de octubre de 2026): la frase «This XML Sitemap Index file contains 2 sitemaps» y esta tabla:

| Mapa hijo | Qué contiene | Última modificación |
|---|---|---|
| `post-sitemap.xml` | Las **entradas**: los artículos del blog, publicados con fecha. | 2026-06-20 04:46 UTC |
| `page-sitemap.xml` | Las **páginas**: contenido fijo como contacto, quiénes somos o el aviso legal. | 2026-06-20 04:48 UTC |

**Entradas y páginas en WordPress.** Una *entrada* (*post*) es un artículo del blog: tiene fecha y aparece en orden cronológico. Una *página* (*page*) es contenido que no cambia con el tiempo. Como nuestro objetivo son artículos de viaje, el mapa que más nos interesa es `post-sitemap.xml`.

**Lo que no vimos: categorías y etiquetas.** Un sitio WordPress suele agrupar sus artículos en categorías (por ejemplo, un país) y etiquetas, pero aquí no hay mapa para ellas. Yoast permite excluirlas, y eso lo decide el dueño. Consecuencia importante: **el sitemap no es el plano completo del sitio**, solo lo que el dueño quiso listar. Por eso conviene compararlo después con lo que se descubre siguiendo enlaces (DevTools o rastreo).

**Sobre las fechas.** Las dos fechas son del 20 de junio de 2026, hace unos tres meses y medio. Probablemente es la fecha del contenido modificado más recientemente (Yoast suele usar la del último artículo tocado), lo que sugeriría que el sitio no se actualiza desde entonces. Al abrir `post-sitemap.xml` se confirmó que la fecha del índice (04:46) es exactamente la de la última entrada de ese mapa; que se tocaran nueve entradas a la vez el 20 de junio de 2026 no prueba que se escribiera algo nuevo.

**Un detalle de direcciones.** El robots.txt anuncia el índice en `http://viviendoporelmundo.com/...` (sin la «s» ni `www`), pero los mapas hijos están en `https://www.viviendoporelmundo.com/...`. El navegador te llevó de una a otra automáticamente (una redirección). El código también tiene que seguirla; `requests` lo hace solo.

**El camino completo hasta una página, hasta ahora:**

1. `robots.txt` nos dice que podemos entrar, con 10 segundos de espera, y señala el sitemap.
2. `sitemap_index.xml` nos dice que hay dos mapas: entradas y páginas.
3. `post-sitemap.xml` (siguiente) lista las direcciones de los artículos.
4. Cada `<loc>` de ese mapa es una página que luego podremos filtrar y leer.


## [Etapa 2 · Paso 4] 15. Leer un mapa de páginas: `post-sitemap.xml` (paso 4)

> **Para qué:** Entender qué datos trae cada fila del mapa y qué se puede (y qué no) deducir de ellos, antes de decidir qué leer.

Este mapa es la lista de las **entradas** (los artículos) del blog. Según su propio encabezado contiene **244 URLs**. Cada fila trae tres datos:

| Columna | Qué significa | Ejemplo |
|---|---|---|
| URL | La dirección de la página. | `https://www.viviendoporelmundo.com/que-ver-en-budapest-2-dias-a-pie/` |
| Images | Cuántas imágenes tiene esa página (la cuenta Yoast). | 86 |
| Last Mod. | Fecha y hora de la última modificación, en hora universal (UTC). | 2026-06-20 04:46 |

**Anatomía de una dirección.** En `.../que-ver-en-budapest-2-dias-a-pie/`, la parte final se llama *slug*: es el nombre de la página dentro de la dirección, casi siempre un resumen del tema con palabras separadas por guiones. En este mapa de entradas todas las direcciones cuelgan directamente de la raíz: no hay carpetas como `/blog/` ni `/pais/`. (El mapa de páginas sí usa alguna, como se ve en el paso 6.)

**El orden de la lista.** Va de la fecha de modificación más antigua (2015-10-26) a la más reciente (2026-06-20). No es el orden de publicación.

> **Fecha de modificación no es fecha de publicación** `Last Mod.` dice cuándo se tocó la página por última vez, no cuándo se escribió. Cuando se editan muchas páginas a la vez (un cambio de diseño, una migración) todas quedan con casi la misma fecha. Aquí hay un bloque de más de 50 entradas con fechas entre el 21 y el 26 de julio de 2021, y otro de 9 entradas del 20 de junio de 2026 (seis guías de ruta y tres de lugares). Por eso esa columna no sirve para saber cuál artículo es el más nuevo.

**Comprobación de la fecha del mapa.** La fecha del índice para este mapa era `2026-06-20 04:46`, y es exactamente la de la última entrada de la lista. Así calcula Yoast la fecha de un mapa: toma la más reciente de sus páginas.

**Qué tipos de contenido se ven por el nombre.** Sin abrir ninguna página, solo leyendo las direcciones, ya se distinguen familias. Es una lectura a ojo; el filtrado de verdad es el paso 8.

| Familia | Pista en la dirección | Para el objetivo del proyecto |
|---|---|---|
| Guías de lugares | `que-ver-en-…`, `que-hacer-en-…`, `guia-…` | Las más útiles como fuente. |
| Vídeos, podcasts y entrevistas | `video-…`, `podcast-…`, `entrevista-…` | Suelen tener poco texto: son una página con un reproductor. |
| Contenido comercial o de afiliación | Seguros de viaje, hosting, cursos, afiliados | Mejor descartarlas: su fin es vender. |
| Posibles duplicados | Terminan en `-2` | Parecen una segunda versión de otra entrada. |

> **Aviso para el filtrado** Las reglas de la guía (`PATRONES_UTILES = ("/blog/", "/noticias/", "/articulo/")`) buscan carpetas dentro de la dirección. En el mapa de entradas ninguna dirección las tiene (y en el de páginas aparece `/paises/`, que tampoco coincide), así que esas reglas descartarían todo lo que hemos visto. Es un ejemplo claro de por qué las reglas fijas no sirven igual en todos los sitios, y de lo que un agente hará distinto: leer el nombre y decidir con criterio.

**La columna Images** va de 1 a 264. Sirve de pista del tamaño de una guía: una entrada con 264 imágenes es una guía muy larga. Recuerda que las fotos tienen derechos de autor: se cuentan, no se descargan.


## [Etapa 2 · Paso 5] 16. Descargar una página con código (paso 5)

> **Para qué:** Ver qué recibe un programa cuando pide una página, la respuesta del sitio y el HTML crudo, antes de limpiarlo. Es la base de todo lo que viene: leer los mapas y leer los artículos.

**Qué es una petición HTTP.** Cuando tu navegador abre una página, le *pide* esa página a un servidor y el servidor *responde*. El código hace exactamente lo mismo, con la librería `requests`. Analogía: un mensajero va a una dirección, pide un paquete y trae de vuelta el paquete y una nota con cómo salió todo. La respuesta tiene tres partes:

| Parte de la respuesta | Qué es | Lo que salió con la portada |
|---|---|---|
| Código de estado | Un número que dice cómo salió la petición. | `200`, que significa «todo bien». |
| Cabeceras | La nota del mensajero: datos sobre el paquete, como su tipo. | `Content-Type: text/html; charset=UTF-8`, es decir, una página HTML con codificación UTF-8, que guarda bien las tildes y las eñes. |
| Cuerpo | El paquete: el contenido de la página. | 245.915 bytes (unos 240 KB) de HTML, en 1,86 segundos. |

**Los códigos de estado que más se ven:**

| Código | Significa | Qué hacer |
|---|---|---|
| 200 | Todo bien. | Seguir. |
| 301 | La página se mudó a otra dirección y te dice cuál. | Seguir la redirección (`requests` lo hace solo). |
| 403 | Prohibido: el sitio te cierra la puerta. | Detenerse. No intentar esquivarlo. |
| 404 | Esa página no existe. | Saltarla y anotarla. |
| 429 | Demasiadas peticiones seguidas. | Esperar más. Es la señal de que vamos muy rápido. |
| 500 | El servidor falló. | Reintentar más tarde, sin insistir. |

**La redirección que vimos.** Pedimos `http://viviendoporelmundo.com/` y el sitio respondió `301` apuntando a `https://www.viviendoporelmundo.com/`: es como una dirección antigua con un cartel de «nos mudamos a…». El código siguió el cartel y terminó en la página correcta. Lo que hay que tener en cuenta: una sola página costó **dos peticiones**, y el código las hace seguidas, sin esperar entre ellas. Para respetar el ritmo al pie de la letra, lo mejor es pedir ya la dirección final (`https://www…`). Los mapas hijos del sitemap ya están en esa forma.

**Qué hace el código, paso a paso** (`pedir()` en `scraper.py`):

1. Pregunta a `puede_visitar()` si el robots.txt deja entrar a esa dirección. Si no, se detiene.
2. Espera lo que pide el sitio (`espera_del_sitio()`: 10 segundos).
3. Pide la página con `requests.get(...)`, presentándose con el nombre del bot y con un tope de 20 segundos (`timeout=20`) para no quedarse esperando para siempre si el servidor no responde.
4. Si la respuesta es un error (códigos 4xx o 5xx), `raise_for_status()` lo detecta y el código devuelve `None` en vez de seguir con una página rota.
5. Si todo va bien, devuelve la respuesta completa. `descargar()` la usa, descarta lo que no sea HTML (imágenes, PDF) y corrige la codificación si hiciera falta.

**El nombre del bot.** Cada petición lleva una cabecera `User-Agent` con el nombre del bot y un correo de contacto, para que el dueño del sitio sepa quién lo visita y a quién escribir si el bot le molesta. Es presentarse con honestidad en vez de hacerse pasar por un navegador. También se manda `Accept-Language`, que dice que preferimos contenido en español.

**Qué es el HTML crudo.** Es el texto tal como lo recibe el programa: etiquetas, comentarios y scripts, todo mezclado. Los primeros 500 caracteres de la portada son un buen ejemplo: `<!DOCTYPE html>`, comentarios para navegadores muy antiguos (Internet Explorer 7 y 8), `<meta charset>` y un `<script>`. Nada de eso es texto de artículo. Por eso existe el paso 10, que limpia el HTML y se queda solo con el texto principal.

> **Qué obtienes** Una función `pedir()` que descarga una página de forma educada (con permiso, espera y nombre) y devuelve todo lo que respondió el sitio, y una función `descargar()` que devuelve solo el texto HTML. Con ellas el paso 6 puede leer los mapas del sitemap.


## [Etapa 2 · Paso 6] 17. Leer los mapas con código: qué se buscaba y qué resultado salió (paso 6)

> **Para qué:** Pasar de ver el catálogo a mano a leerlo con código, para tener la lista completa de direcciones dentro del programa, comprobada y lista para guardar. Sin esa lista, el programa no sabe qué páginas existen.

**La analogía.** En el paso 4 mirabas el catálogo de la biblioteca y contabas las fichas con los ojos. Ahora un empleado copia el catálogo ficha por ficha a una hoja y la suma: es más rápido, no se cansa y se puede repetir cuando quieras.

**Qué resultados se buscaban:**

1. **La lista completa de direcciones dentro del programa**, no solo en la pantalla del navegador. Es la materia prima de los pasos 7 y 8.
2. **Comprobar que el código ve lo mismo que tú.** En el paso 4 viste 244 direcciones en el mapa de entradas; si el código daba otro número, algo estaba mal.
3. **Contar lo que nunca se había contado:** cuántas páginas fijas hay en `page-sitemap.xml`.

**La lógica, paso a paso:**

1. Se pide el índice (`sitemap_index.xml`). Responde con una lista de **2 mapas hijos**.
2. Se pide cada hijo, esperando 10 segundos entre petición y petición.
3. En cada hijo se lee cada ficha: su dirección y su fecha de modificación.
4. Todo se junta en una lista grande, anotando de qué mapa salió cada dirección.
5. Se cuenta, se comprueba que no haya repetidas y se compara con lo esperado.

**El resultado y por qué sale ese número** (10 de octubre de 2026):

| Qué se contó | Resultado | Por qué sale ese número |
|---|---|---|
| `post-sitemap.xml` (entradas) | 244 | Coincide con el encabezado del mapa y con lo que se vio en el paso 4: el código y el navegador ven lo mismo. |
| `page-sitemap.xml` (páginas) | 48 | No se había visto antes: son las páginas fijas del sitio. |
| Total | 292 | Es la suma: 244 + 48. |
| Direcciones distintas | 292 | Ninguna se repite: contar la lista y contar el conjunto sin repetidos da lo mismo. |

**Un ejemplo de la lógica.** Si un mapa tuviera 3 direcciones y otro 2, la lista grande tendría 5. Si el conjunto sin repetidos tuviera solo 4, sabrías que una dirección aparece en los dos mapas. Aquí el total y las distintas coinciden, así que no hay repetidas.

**Cómo leer las fechas.** Cada dirección trae la fecha de su última modificación. Contadas por año:

| Año | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Direcciones | 2 | 11 | 5 | 21 | 8 | 8 | **78** | 16 | 23 | 8 | **54** | **58** |

Los años 2021, 2025 y 2026 suman 190 de las 292 direcciones, casi dos de cada tres. No quiere decir que se publicara más en esos años, sino que se **editaron muchas páginas a la vez** (cambios en bloque), que es lo que ya se había visto con `Last Mod.`. Por eso esa fecha no sirve como fecha de publicación.

**Dos comprobaciones.** La modificación más antigua es del 26 de octubre de 2015 (una entrada) y la más reciente del 20 de junio de 2026 a las 04:48:56 (una página). Y esa última fecha es **exactamente** la que el índice daba para `page-sitemap.xml`: confirma que la fecha de un mapa es la de su página más reciente.

> **Algo nuevo: carpetas en las direcciones** Las cinco últimas direcciones, que son del mapa de páginas, tienen la forma `/paises/guia-china-cuanto-cuesta-viajar/`: usan la carpeta `/paises/`. Las entradas, en cambio, cuelgan todas de la raíz. Cuántas de las 48 páginas usan carpeta se verá al guardarlas en el paso 7. Lo que dije antes («ninguna dirección tiene carpeta») valía solo para el mapa de entradas.

**Lo que el resultado no significa.** 292 no es el tamaño del sitio: es lo que el sitemap lista (faltan, por ejemplo, las categorías). Y que una dirección exista no quiere decir que sirva para el artículo: elegir cuáles valen la pena es el paso 8.

**Cuánto costaría leerlas todas.** Con 10 segundos de espera, 292 páginas son casi 49 minutos (292 × 10 s). Saberlo antes es una de las razones del filtrado: leer solo las que sirven ahorra tiempo y respeta al sitio.

> **En resumen** El paso 6 convirtió el catálogo que veías en una lista de 292 direcciones comprobada con código. Es la lista que el paso 7 guarda en la base de datos.


## [Etapa 2 · Paso 7] 18. Guardar las direcciones en una base de datos (paso 7)

> **Para qué:** Que la lista de 292 direcciones deje de existir solo mientras corre el programa y quede guardada en un archivo, ordenada, sin repetidos y lista para filtrar. Sin guardarla, habría que volver a pedirle los mapas al sitio cada vez que se necesite.

**Qué es una base de datos.** Piensa en una hoja de cálculo (como Excel) con reglas: tiene columnas fijas, una fila por cada elemento y sabe responder preguntas como «dame las filas donde pase tal cosa». **SQLite** es una base de datos que vive en un solo archivo (aquí `datos/scraping.db`), no hay que instalar nada y viene con Python.

**La tabla `urls`.** Cada dirección es una fila, y estas son sus columnas:

| Columna | Qué guarda | Ejemplo |
|---|---|---|
| `url` | La dirección completa. Es la clave: no puede haber dos filas con la misma. | `https://www.viviendoporelmundo.com/medellin-y-guatape/` |
| `sitio` | A qué sitio pertenece. | `viviendoporelmundo.com` |
| `origen` | Cómo se encontró. | `sitemap` |
| `mapa` | De qué mapa salió. | `post-sitemap.xml` |
| `lastmod` | Fecha de su última modificación. | `2015-10-26T22:42:16+00:00` |
| `vale_la_pena` | Si sirve para el artículo: 1 sí, 0 no, vacío si aún no se decidió. | (vacío) |
| `motivo` | Por qué se decidió así. | (vacío) |
| `fecha_mapeo` | Cuándo se leyó. | `2026-10-10` |

**La clave (`PRIMARY KEY`).** Es como el número de cédula: no pueden existir dos personas con el mismo. Gracias a ella, guardar dos veces la misma dirección no crea una segunda fila.

**Guardar sin duplicar ni borrar decisiones.** La sentencia de guardado dice: «si la dirección no existe, agrégala; si ya existe, actualiza solo de qué mapa salió y la fecha». Nunca toca `vale_la_pena` ni `motivo`, porque ahí vivirán las decisiones del filtrado y no deben perderse al volver a mapear. Se comprobó en una copia de la base: se guardaron las 292 dos veces y siguieron siendo 292, y una marca puesta a mano se conservó.

**Por qué se guardan las 292 y se marca, en vez de guardar solo las que sirven:**

1. Las direcciones no son contenido del blog: son el mapa. Guardarlas todas pesa casi nada (la base ocupa unos 100 KB).
2. Marcar se puede deshacer; borrar no. Con `vale_la_pena` y `motivo` se ve por qué se descartó cada una.
3. Si una regla falla, se corrige sin volver a pedirle los mapas al sitio.
4. Lo que importa es qué se descarga después: solo se leerá el contenido de las páginas marcadas.

**El resultado** (10 de octubre de 2026):

| Qué se comprobó | Resultado |
|---|---|
| Filas guardadas | **292**: 244 del mapa de entradas y 48 del de páginas. |
| Marcadas con `vale_la_pena` | 0: todas sin decidir, a la espera del paso 8. |
| Repetidas al volver a guardar | Ninguna: sigue siendo 292. |
| Tamaño del archivo | Unos 100 KB, en `datos/scraping.db`, fuera de git. |

**Respuesta a la duda del paso 6: ¿cuántas direcciones usan carpeta?**

| Mapa | Carpeta | Direcciones |
|---|---|---|
| Entradas | (raíz, sin carpeta) | 244 |
| Páginas | (raíz, sin carpeta) | 30 |
| Páginas | `/paises/` (guías de costos por país) | 16 |
| Páginas | `/quien-es-viviendo-por-el-mundo/` | 2 |

Así, 18 de las 48 páginas usan carpeta. Las 16 de `/paises/` son las guías por país que decidiste conservar como material.

**Un vistazo a Colombia, solo mirando.** Con una consulta a la base se buscaron las direcciones que contienen palabras como `colombia`, `medellin`, `bogota`, `cartagena` o `tayrona`. Salieron 9, y no se marcó ninguna:

| Mapa | Dirección |
|---|---|
| Páginas | `/paises/guia-colombia-cuanto-cuesta-viajar/` |
| Entradas | `/bogota-y-el-fin-de-una-etapa-de-nuestro-viaje/` |
| Entradas | `/eje-cafetero-de-colombia-a-lo-juan-valdes/` |
| Entradas | `/llegamos-a-colombia-cali-y-san-cipriano/` |
| Entradas | `/llegamos-al-caribe-cartagena-de-indias/` |
| Entradas | `/medellin-y-guatape/` |
| Entradas | `/taganga-submarinismo-lowcost/` |
| Entradas | `/tayrona-y-palomino-lo-mejor-del-caribe-colombiano/` |
| Entradas | `/video-con-lo-mejor-de-colombia/` |

> **Ojo con este vistazo** Buscar palabras en la dirección es una pista y no un filtro: puede dejar fuera artículos que hablan de Colombia sin nombrarla en la dirección, y puede colar páginas poco útiles, como la del vídeo. El filtro de verdad es el paso 8.

> **Lo que falló en el camino** En la primera ejecución falló la red (el computador no pudo resolver el nombre del sitio) y el programa se cayó con un error larguísimo. El fallo era momentáneo, pero mostró que leer el robots.txt no estaba protegido. Se corrigió: ahora, si no se puede leer, el programa avisa en una línea y no entra. Un programa debe avisar y no romperse cuando falla algo que no depende de él.

> **En resumen** El paso 7 convirtió la lista de 292 direcciones en datos guardados, sin repetidos y sin decidir. Con esto termina el mapeo y empieza el filtrado.


## [Etapa 3 · Paso 8] 19. Filtrar con reglas fijas: elegir qué leer (paso 8)

> **Para qué:** Separar, entre las 292 direcciones, las pocas que sirven para un artículo sobre Colombia, y dejar escrito por qué se descartó cada una de las demás. Así solo se lee lo útil: se ahorra tiempo y se respeta al sitio.

**La analogía.** Tienes el catálogo de la biblioteca completo (292 fichas) y vas a escribir sobre Colombia. Antes de sacar libros de los estantes, pasas por el catálogo con un lápiz y pones al lado de cada ficha un «sí» o un «no», con una nota corta del porqué. No abres ningún libro: decides solo por el nombre y por la sección donde está.

**Qué elegiste filtrar** (opciones A, B, C y D):

| Opción | Regla | Ejemplo |
|---|---|---|
| A. Mapa de origen | Las páginas fijas (contacto, aviso legal…) no son artículos. | `/aviso-legal-…/` → no. |
| D. Carpeta `/paises/` | Excepción a la regla A: las guías por país sí cuentan como material. | `/paises/guia-colombia-cuanto-cuesta-viajar/` → sigue. |
| C. Familia por el nombre | Fuera lo que no es información tipo blog: vídeos y fotomontajes, podcasts, entrevistas, venta o afiliación y posibles duplicados (terminan en `-2`). | `/video-con-lo-mejor-de-colombia/` → no. |
| B. Palabras de Colombia | Sí, si el nombre contiene el país o uno de sus lugares: Colombia, Medellín, Bogotá, Cartagena, Cali, Tayrona, Palomino, Taganga, Guatapé, Eje Cafetero o San Cipriano. | `/medellin-y-guatape/` → sí. |

**La lógica: las reglas se aplican en orden, y la primera que decide, decide.** Por eso el orden importa:

1. ¿Es una página fija (del mapa de páginas y fuera de `/paises/`)? → **no**, «página fija».
2. ¿El nombre tiene una pista de familia (vídeo, podcast, entrevista, venta)? → **no**, con esa familia.
3. ¿El nombre termina en `-2`? → **no**, «posible duplicado».
4. ¿El nombre contiene un lugar de Colombia? → **sí**, con los lugares encontrados.
5. Si nada de lo anterior → **no**, «otro tema».

**Tres direcciones, paso a paso:**

| Dirección | Qué regla decide | Resultado |
|---|---|---|
| `/medellin-y-guatape/` | Pasa las reglas 1 a 3; en la 4 encuentra `medellin` y `guatape`. | Sí · Colombia |
| `/video-con-lo-mejor-de-colombia/` | La regla 2 encuentra `video` antes de llegar a la de Colombia. | No · vídeo |
| `/workaway-en-puerto-escondido-mexico-1-de-2/` | La regla 3 ve que termina en `-2`. | No · posible duplicado (y aquí la regla se equivoca: es la parte 1 de una serie) |

**El resultado** (10 de octubre de 2026, sin ninguna petición al sitio):

| Decisión y motivo | Direcciones |
|---|---|
| **Sí: Colombia** | **8** |
| No: otro tema (no nombra Colombia en la dirección) | 196 |
| No: página fija | 32 |
| No: vídeo o fotomontaje | 15 |
| No: podcast | 11 |
| No: entrevista | 11 |
| No: venta o afiliación | 10 |
| No: posible duplicado | 9 |
| Total | 292 |

**Las 8 que valen la pena:**

| Dirección | Lugares encontrados | Tipo |
|---|---|---|
| `/paises/guia-colombia-cuanto-cuesta-viajar/` | colombia | Guía por país |
| `/bogota-y-el-fin-de-una-etapa-de-nuestro-viaje/` | bogota | Entrada |
| `/eje-cafetero-de-colombia-a-lo-juan-valdes/` | cafetero, colombia | Entrada |
| `/llegamos-a-colombia-cali-y-san-cipriano/` | cali, cipriano, colombia | Entrada |
| `/llegamos-al-caribe-cartagena-de-indias/` | cartagena | Entrada |
| `/medellin-y-guatape/` | guatape, medellin | Entrada |
| `/taganga-submarinismo-lowcost/` | taganga | Entrada |
| `/tayrona-y-palomino-lo-mejor-del-caribe-colombiano/` | colombiano, palomino, tayrona | Entrada |

**Por qué importa:** leer las 292 costaba casi 49 minutos con las esperas; leer estas 8 costará unos 80 segundos.

**Dónde se equivocan las reglas.** Es lo que la guía 1 llama el punto débil del modo manual: las reglas solo ven el nombre, no el contenido.

| Regla | Error que comete | Ejemplo |
|---|---|---|
| Posible duplicado (`-2`) | Confunde partes de una serie con copias. | `…-1-de-2`, `…-2-de-2`, `3-cosas-imprescindibles-mochila-2` (que parece la segunda parte de otra entrada). |
| Venta o afiliación | Descarta artículos que solo mencionan una palabra comercial. | `salud-vacunas-y-seguro-de-viaje-vuelta-al-mundo` posiblemente es información práctica de viaje. |
| Palabras de Colombia | No ve artículos que hablan de Colombia sin nombrarla en la dirección. | No se puede saber cuántos son sin leer las páginas. |

Ninguno de esos errores toca a las 8 de Colombia, que son claras por su nombre. El riesgo real está en las **omisiones** de la última fila, y es lo que el agente (o el buscador del sitio) podrá mostrar en la comparación.

> **Las marcas son revisables** Cada dirección guarda su decisión y su motivo, que empieza por «regla:». Si vuelves a ejecutar el filtro, solo se recalculan esas marcas; si algún día marcas una dirección a mano, el filtro la respeta.

> **En resumen** El paso 8 redujo 292 direcciones a 8 candidatas de Colombia, sin pedir nada al sitio, y dejó escrito el motivo de cada descarte. Con esto termina el filtrado; lo siguiente es abrir uno de esos artículos y ver cómo está hecho por dentro.


## [Etapa 4 · Paso 9] 20. Leer la estructura de un artículo: el árbol de etiquetas (paso 9)

> **Para qué:** Descubrir dónde vive cada dato de un artículo (título, firma, fecha, texto) dentro del HTML, antes de escribir código que lo saque. Sin esa lectura, el programa no sabe qué parte de la página es el artículo y cuál es menú, publicidad o botones.

**La analogía.** Una página web es como un árbol genealógico. Cada etiqueta es una persona: tiene un **padre** (la etiqueta que la envuelve), **hijos** (las que lleva dentro) y **hermanos** (las que están a su lado, dentro del mismo padre). Para encontrar el título, se sigue el parentesco: «el título es hijo del encabezado, que es hijo del artículo, que es hijo del contenido principal».

**Lo que se vio en `/medellin-y-guatape/`** (10 de octubre de 2026, con DevTools, pestaña Elements). Así queda el árbol, de afuera hacia adentro:

```
main.content
├── div.breadcrumb              → «Inicio / América / Colombia / Medellín…» (el camino de migas)
└── article.post-4906 … entry   → el artículo completo
    ├── header.entry-header
    │   ├── h1.entry-title      → «Medellín y la gran sorpresa, Guatapé»
    │   └── p.entry-meta        → firma y fecha (por abrir)
    └── div.entry-content       → el cuerpo del texto
        └── div.addtoany_share… → botones de compartir (no es texto del artículo)
```

| Etiqueta | Qué es | Para qué sirve aquí |
|---|---|---|
| `main.content` | La zona principal de la página. | Deja fuera el menú, el pie de página y la barra lateral. |
| `article` | Un artículo completo e independiente. | Marca dónde empieza y dónde termina lo que nos interesa. |
| `header.entry-header` | El encabezado del artículo. | Agrupa el título y la firma. |
| `h1.entry-title` | El título principal. | Aquí está el título que se citará. |
| `p.entry-meta` | Los datos del artículo. | Ahí se esperan la firma y la fecha. |
| `div.entry-content` | El cuerpo. | Aquí están los párrafos del texto. |

**Etiqueta y clase.** `h1` es el *tipo* de etiqueta (título principal). `entry-title` es su *clase*: un apellido que le puso quien hizo la página, y que sirve para reconocerla entre muchas. Se escribe `h1.entry-title`, con un punto entre el tipo y la clase.

**Cómo se le pediría al código.** Con la librería que lee HTML se le dice «dame la etiqueta `h1` con clase `entry-title`, dentro del `article`». Es la lógica del paso 3 de la guía 1: `article h1.entry-title`. Aquí la estructura coincide con el ejemplo de la guía (`<article><h1>…`), por lo que ese tipo de reglas probablemente funcionaría en este sitio, y solo en este: otro sitio tendría otros nombres.

**Tres hallazgos de la captura:**

1. **El título no es el nombre de la dirección.** La dirección es `medellin-y-guatape`, y el título es «Medellín y la gran sorpresa, Guatapé». Es otra razón por la que filtrar por el nombre no basta.
2. **La etiqueta `<article>` declara a qué categorías pertenece.** Su clase incluye `category-america`, `category-colombia` y `tag-cronicas-de-viaje`. Es decir, la propia página dice «yo soy de Colombia», una señal de tema mucho más fiable que adivinarlo por el nombre. Esto abre una vía nueva para el filtro: leer esas clases, o pedir la página de la categoría «Colombia», que agrupa sus artículos.
3. **Dentro del cuerpo hay cosas que no son texto del artículo**, como el bloque «¡Comparte este artículo!» con los botones de WhatsApp, Facebook y Twitter. Un extractor tiene que saltárselos.

> **Sobre el buscador de DevTools** Al buscar «H1» salió «1 de 8». Eso no significa que haya 8 títulos: DevTools cuenta toda aparición de ese texto (etiquetas, clases, estilos). La primera, que es la que se vio, era la etiqueta correcta. Para contar solo las etiquetas hay que buscar `<h1`.

> **Lo que falta de este paso** Abrir `p.entry-meta` para ver la firma y la fecha, y localizar el primer párrafo dentro de `div.entry-content`. El paso 9 sigue en curso hasta tenerlos.


---

# CÓDIGOS DE PROGRAMACIÓN UTILIZADOS

Esta sección reúne cada pieza de código que se ha usado en el ejercicio, explicada para alguien que empieza. Todo está escrito en **Python**. Cada pieza trae: la etapa y el paso donde se usa (etiqueta amarilla), su «Para qué», el código, la lógica paso a paso, un ejemplo y la comparación con otras formas de hacerlo. Los códigos se muestran sin los comentarios largos; el archivo completo es `scraper.py`. Antes de las piezas hay un repaso de los conceptos básicos de programación y de las librerías; y cada pieza trae «Si lo hiciera una persona», los conceptos que aparecen y lo que hace cada librería, todo con ejemplos mínimos.

> **Cómo leerla** Las funciones (`puede_visitar`, `pedir`…) no se ejecutan solas: las llaman otros códigos. Lo que sí se ejecuta desde la terminal son los dos scripts de prueba, `probar_robots.py` y `probar_descarga.py`. Se ejecutan en la terminal, desde la carpeta del proyecto: `.venv\Scripts\python.exe probar_robots.py`.


## [General · Todas las etapas] 0. Antes de empezar: los conceptos básicos de programación

> **Para qué:** Tener a mano las ideas básicas que aparecen en todos los códigos, para poder seguir la lógica aunque nunca hayas programado. Cada una trae un ejemplo mínimo.

Programar es darle al computador instrucciones muy precisas, paso a paso, como una receta de cocina. Estas son las piezas con las que se escriben:

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Variable | Un nombre que guarda un valor, como una etiqueta en una caja. | `edad = 30` guarda el 30; desde ahí, `edad` vale 30. |
| Constante | Una variable que no se piensa cambiar. Por costumbre se escribe en MAYÚSCULAS. | `USER_AGENT = "MiBot/1.0"`. |
| Texto (`str`) | Letras entre comillas. | `"hola"`. |
| Número (`int` y `float`) | Entero, o con decimales. | `10` y `10.0`. |
| Verdadero o falso (`bool`) | Solo dos valores: `True` y `False`. | `5 > 3` da `True`. |
| Nada (`None`) | La ausencia de valor. | Un buscador que no halla nada devuelve `None`. |
| Lista | Varios valores en orden, entre corchetes. | `rutas = ["/", "/wp-admin/"]`; `rutas[0]` es `"/"`. |
| Diccionario | Pares nombre-valor, entre llaves. | `{"nombre": "Ana", "edad": 30}`; `persona["nombre"]` da `"Ana"`. |
| Función (`def`) | Una receta con nombre: recibe datos, hace algo y devuelve un resultado con `return`. | `def doble(n): return n * 2`; `doble(4)` da `8`. |
| Parámetro y valor por defecto | Los datos que recibe la receta; el valor por defecto se usa si no se da otro. | `def saludar(nombre="amigo")`; `saludar()` usa `"amigo"`. |
| Condicional (`if`, `elif`, `else`) | Decidir según una condición. | `if edad >= 18: print("mayor")`. |
| Bucle `for` | Repetir algo para cada elemento. | `for r in rutas: print(r)` imprime cada ruta. |
| Cadena con valores (f-string) | Un texto que mete el valor de variables entre llaves. | Con `nombre = "Ana"`, `f"Hola {nombre}"` da `Hola Ana`. |
| `try` y `except` | Intentar algo y, si falla, hacer otra cosa en vez de romperse. | `try: 10 / 0` y `except ZeroDivisionError: print("no se puede")`. |
| `import` | Traer funciones de una librería o de otro archivo. | `import time`; `from scraper import pedir`. |


## [General · Todas las etapas] Las librerías del proyecto, en simple

> **Para qué:** Saber qué hace cada librería con una imagen sencilla, antes de ver el código que la usa. Una librería es código que otras personas ya escribieron y que se puede usar sin volver a programarlo.

| Librería | Qué es, en simple | Ejemplo mínimo | Dónde se usa |
|---|---|---|---|
| `requests` | El mensajero: hace desde el programa lo que hace tu navegador al abrir una dirección. | `r = requests.get("https://x.com")`; `r.status_code` da `200` y `r.text` trae la página. | Etapa 1 · Paso 3 y Etapa 2 · Paso 5 |
| `urllib.robotparser` | Un lector de carteles: le das el robots.txt y responde si puedes entrar a una ruta. | `rp.can_fetch("MiBot", "https://x.com/wp-admin/")` da `False`. | Etapa 1 · Paso 3 |
| `urllib.parse` | Una navaja para partir direcciones en sus partes. | `urlparse("https://x.com/a/b")` da protocolo `https`, dominio `x.com` y ruta `/a/b`. | Etapa 1 · Paso 3 |
| `functools` | Herramientas para funciones. Aquí se usa `lru_cache`, que le da memoria a una función. | Pedir un archivo una sola vez, aunque se pregunte mil veces. | Etapa 1 · Paso 3 |
| `time` | Relojes y esperas. | `time.sleep(10)` pausa diez segundos. | Etapa 2 · Paso 5 |
| `re` | Búsqueda de patrones en textos. | `re.findall(r"<a ", texto)` encuentra cada etiqueta de enlace. | Etapa 2 · Paso 5, en el script de prueba |
| `beautifulsoup4` y `lxml` | Leen el HTML y permiten buscar etiquetas dentro. Todavía no se usan. | Pedir «todos los párrafos dentro del artículo». | Paso 9 y 10 (pendiente) |
| `trafilatura` | Deja solo el texto principal de un artículo. Todavía no se usa. | Quedarse con la carne y tirar el empaque. | Paso 10 (pendiente) |
| `sqlite3` | Una base de datos que vive en un archivo. Viene con Python. | Guardar las URLs sin repetirlas. | Etapa 2 · Paso 7 |
| `pathlib` | Maneja rutas de archivos y carpetas. | `Path("a") / "b"` une las partes de una ruta. | Etapa 2 · Paso 7 |
| `datetime` | Fechas y horas. | `date.today().isoformat()` da la fecha de hoy como `2026-10-10`. | Etapa 2 · Paso 7 |


## [Etapa 0 · Paso 1] 1. Comandos del entorno

> **Para qué:** Preparar las herramientas del proyecto en una caja propia, para que lo que se instale no se mezcle con otros proyectos ni con el Python del computador. Va en la etapa 0 porque nada de lo demás funciona sin esto.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Comprar una caja de herramientas vacía para este proyecto. | `python -m venv .venv` crea la carpeta `.venv`. |
| Abrir esa caja y ponerla sobre la mesa de trabajo. | `.venv\Scripts\activate` entra al entorno; la terminal muestra `(.venv)`. |
| Meter dentro las herramientas que se van a usar. | `pip install ...` descarga e instala las cuatro librerías. |
| Probar que cada herramienta abre y funciona. | El último comando intenta usar las cuatro y escribe `Todo instalado`. |

```
python --version
python -m venv .venv
.venv\Scripts\activate
pip install requests beautifulsoup4 lxml trafilatura
python -c "import requests, bs4, lxml, trafilatura; print('Todo instalado')"
```

**Cómo funciona, paso a paso:**

1. `python --version` confirma que Python responde y qué versión es (aquí, 3.12.10).
2. `python -m venv .venv` crea la carpeta `.venv`: una copia limpia de Python.
3. `.venv\Scripts\activate` entra a esa caja. Se nota porque la línea de la terminal empieza con `(.venv)`.
4. `pip install ...` descarga las cuatro librerías dentro de la caja.
5. La última línea intenta usar las cuatro; si imprime `Todo instalado`, funcionan.

**Ejemplo:** después de activar el entorno, `pip install requests` instala `requests` solo en este proyecto. Otro proyecto con su propio `.venv` puede usar otra versión sin que se pisen.

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Terminal | Una ventana donde se escriben órdenes en texto y el computador las ejecuta. | Escribir `python --version` y pulsar Enter muestra la versión. |
| Comando | Una orden de una línea. | `pip install requests` ordena instalar `requests`. |
| Librería | Código ya escrito por otras personas que se instala para no empezar de cero. | `requests` ya sabe pedir páginas; no hay que programarlo. |
| `pip` | El instalador de librerías de Python. | `pip list` muestra las que hay instaladas. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| Instalar las librerías en el Python general del computador | Se mezclan las versiones de todos los proyectos y es difícil saber qué usa cada uno. |
| Usar Conda, Poetry o uv | Son más herramientas que aprender. Para un proyecto pequeño, `venv` y `pip` vienen con Python y alcanzan; otro proyecto puede elegir distinto. |
| Copiar el código de las librerías dentro del proyecto | Pesa mucho y no se actualiza. |


## [Etapa 1 · Paso 3] 2. El nombre del bot: `USER_AGENT`

> **Para qué:** Presentarnos con honestidad ante el sitio: quiénes somos y cómo contactarnos. Se usa primero para leer el robots.txt con nuestro nombre, y después en cada descarga.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Al llegar a una oficina, decir tu nombre y dejar una tarjeta con tu teléfono. | El programa se presenta con `USER_AGENT`: nombre, versión y correo de contacto. |
| El recepcionista anota quién visitó y, si hay un problema, puede llamarte. | El sitio guarda el nombre en sus registros y puede escribir al correo. |

```
USER_AGENT = "MiBotInvestigacion/1.0 (contacto: CORREO)"
```

En el código real, `CORREO` es el correo de contacto elegido para el proyecto.

**Cómo funciona:** es un texto guardado con un nombre para reutilizarlo. Tiene la forma `nombre/versión (contacto)`. Dos partes del código lo leen: la que descarga el robots.txt y la que pide páginas. Además, `can_fetch` lo usa para buscar el bloque del robots.txt que lleve ese nombre (como no hay ninguno, cae en el bloque `*`).

| Qué ve el sitio | Con nuestro nombre | Con el nombre por defecto |
|---|---|---|
| Cabecera `User-Agent` | `MiBotInvestigacion/1.0 (contacto: …)` | `python-requests/2.34.2` |
| ¿Sabe quién lo visita? | Sí, y puede escribir si hay un problema. | No. |

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Constante | Un nombre que guarda un valor que no se piensa cambiar. Por costumbre va en MAYÚSCULAS. | `USER_AGENT = "MiBot/1.0"` guarda el nombre una vez y el resto del código lo reutiliza. |
| Texto (`str`) | Letras entre comillas. | `"hola"` es un texto; `hola` sin comillas sería un nombre. |
| Escribir un valor en un solo sitio | Si cambia, se cambia una vez y no en veinte lugares. | Cambiar el correo en `USER_AGENT` actualiza todas las peticiones. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| Dejar el nombre por defecto | No dice quién eres, y algunos sitios lo bloquean por sospechoso. |
| Fingir ser un navegador (Chrome) | Es engañar al sitio. El robots.txt existe justamente para que los bots se identifiquen y se les pida un trato. |
| Un nombre sin correo | El dueño no tendría cómo avisarte antes de bloquearte. |


## [Etapa 1 · Paso 3] 3. Arreglar el texto del robots.txt: `_normalizar`

> **Para qué:** Evitar que el lector de Python pierda reglas por una línea en blanco. Sin esta función, tres rutas prohibidas salían como permitidas.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Leer el texto línea por línea. | `for i, linea in enumerate(lineas)` recorre cada línea con su número. |
| Si la línea tiene letras, copiarla tal cual. | `if linea: resultado.append(linea)`. |
| Si la línea está vacía, mirar cuál es la siguiente que tenga letras. | `siguiente = next(...)` busca la próxima línea con texto. |
| Si esa siguiente empieza un grupo nuevo (`User-agent`), dejar el espacio; si no, taparlo. | `if siguiente.lower().startswith(...)` decide si conserva la línea vacía. |

```
def _normalizar(texto: str) -> list[str]:
    lineas = [linea.strip() for linea in texto.splitlines()]
    resultado = []
    for i, linea in enumerate(lineas):
        if linea:
            resultado.append(linea)
        else:
            siguiente = next((x for x in lineas[i + 1:] if x), "")
            if siguiente.lower().startswith("user-agent"):
                resultado.append("")
    return resultado
```

**Cómo funciona, paso a paso:**

1. `texto.splitlines()` parte el texto en líneas, y `.strip()` quita los espacios de los bordes.
2. Se recorre cada línea. Si no está vacía, se conserva.
3. Si está vacía, se mira cuál es **la siguiente línea con texto** (`next(...)`).
4. Si esa siguiente línea empieza por `user-agent`, la línea en blanco separaba dos bloques y se conserva.
5. Si no, la línea en blanco estaba partiendo un bloque por la mitad y se descarta.

**Ejemplo.** A la izquierda lo que llega; a la derecha lo que devuelve la función:

| Entrada | Salida |
|---|---|
| `Disallow: /a/` | `Disallow: /a/` |
| (línea en blanco)  ← parte el bloque | *(se descarta)* |
| `Disallow: /b/` | `Disallow: /b/` |
| (línea en blanco)  ← antes viene `User-agent` | (línea en blanco, se conserva) |
| `User-agent: Googlebot` | `User-agent: Googlebot` |

Con la entrada original, el lector de Python habría ignorado `Disallow: /b/`. Con la salida, la ve.

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Función (`def`) | Una receta con nombre: recibe datos, hace algo y devuelve un resultado con `return`. | `def doble(n): return n * 2`; `doble(4)` devuelve `8`. |
| Lista | Varios valores en orden, entre corchetes. | `resultado = []` es una lista vacía; `resultado.append("a")` le agrega `"a"`. |
| Bucle `for` | Repetir algo para cada elemento de una lista. | `for x in [1, 2, 3]: print(x)` imprime 1, 2 y 3. |
| Condicional `if` | Hacer algo solo si se cumple una condición. | `if edad >= 18: print("mayor")`. |
| Texto vacío cuenta como «no» | En una condición, un texto vacío vale como falso y uno con letras como verdadero. | `if linea:` solo entra si la línea tiene texto. |
| Métodos de texto | Acciones que se piden a un texto con un punto. | `"  hola ".strip()` da `"hola"`; `"ABC".lower()` da `"abc"`; `"user-agent: *".startswith("user")` da `True`. |
| Lista por comprensión | Una línea que hace algo con cada elemento y junta los resultados. | `[x.strip() for x in [" a ", " b "]]` da `["a", "b"]`. |
| `enumerate` | Recorre una lista dando también el número de cada elemento. | `for i, x in enumerate(["a", "b"])` da `0 a` y luego `1 b`. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| Usar el lector de Python sin arreglar el texto | Es lo que hace la guía y no funciona con este sitio: comprobado, tres rutas prohibidas salían como permitidas. |
| Escribir a mano la lista de rutas prohibidas | Se desactualiza cuando el sitio cambie su robots.txt y no sirve para otros sitios. |
| Instalar otra librería de robots.txt | Existen otras y podrían leer el archivo de otra manera, pero no se probaron. Se eligió corregir el texto porque el lector de Python ya viene con el lenguaje (nada que instalar) y el arreglo cabe en doce líneas. |


## [Etapa 1 · Paso 3] 4. Descargar y leer el robots.txt: `_robots`

> **Para qué:** Traer el robots.txt de un sitio, con nuestro nombre, y dejarlo interpretado para poder consultarlo. Las demás funciones de permisos se apoyan en esta.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Ir a la recepción del sitio y pedir el cartel de reglas, presentándose con tu nombre. | `requests.get(...robots.txt, headers=...)`. |
| Si no te lo quieren dar (403), asumir que no puedes pasar a nada. | `rp.disallow_all = True`. |
| Si no existe el cartel (404), asumir que no hay reglas. | `rp.allow_all = True`. |
| Si te lo dan, arreglarlo y leerlo. | `rp.parse(_normalizar(r.text))`. |
| Guardarlo en el cuaderno para no pedirlo otra vez. | `@lru_cache` recuerda el resultado. |

```
@lru_cache(maxsize=None)
def _robots(base: str) -> RobotFileParser:
    rp = RobotFileParser()
    r = requests.get(f"{base}/robots.txt",
                     headers={"User-Agent": USER_AGENT}, timeout=20)
    if r.status_code in (401, 403):
        rp.disallow_all = True
    elif r.status_code >= 400:
        rp.allow_all = True
    else:
        rp.parse(_normalizar(r.text))
    return rp
```

**Cómo funciona, paso a paso:**

1. `@lru_cache` recuerda el resultado: la segunda vez que se pregunta por el mismo sitio, no vuelve a descargar nada.
2. `requests.get(...)` descarga el robots.txt presentándose con nuestro nombre. `timeout=20` es el tiempo máximo de espera sin respuesta, para no quedar colgados.
3. Según el código de estado se decide: 401 o 403 significa que nos cierran la puerta y se asume que no se puede entrar a nada; cualquier otro error (como 404) significa que no hay robots.txt y no se prohíbe nada.
4. Si todo va bien, se arregla el texto con `_normalizar` y se interpreta con `rp.parse(...)`.

**Ejemplo:** `_robots("https://www.viviendoporelmundo.com")` descarga el archivo una vez. Si lo vuelves a llamar con el mismo sitio, responde al instante sin pedir nada.

| Código de estado | Qué decide el código |
|---|---|
| 200 | Leer las reglas del archivo. |
| 404 | No hay robots.txt: nada está prohibido (pero quedan los términos de uso). |
| 401 o 403 | Nos cierran la puerta: no se entra a nada. |

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Decorador `@` | Una etiqueta puesta encima de una función para darle un superpoder. | `@lru_cache` hace que la función recuerde sus respuestas. |
| Memoria de una función | Si se llama dos veces con el mismo dato, la segunda responde sin repetir el trabajo. | `cuadrado(3)` calcula; la segunda vez, `cuadrado(3)` responde de memoria. |
| Objeto y método | Un objeto es algo que sabe hacer cosas; sus acciones se llaman con un punto. | `rp = RobotFileParser()` crea el lector; `rp.parse(...)` le da el texto para que lo lea. |
| `if`, `elif`, `else` | Varias decisiones en cadena: gana la primera que se cumple. | Un 403 entra al primer caso, un 404 al segundo y un 200 al `else`. |
| Operador `in` | Pregunta si algo está dentro de un grupo. | `403 in (401, 403)` da `True`. |
| Cadena con valores (f-string) | Un texto que mete el valor de variables entre llaves. | Con `base = "https://x.com"`, `f"{base}/robots.txt"` da `https://x.com/robots.txt`. |
| Argumentos con nombre | Dar un dato diciendo para qué es. | `timeout=20` se entiende mejor que un `20` suelto. |

**La librería, en simple:**

| Herramienta | Qué hace | Ejemplo mínimo |
|---|---|---|
| `requests` | El mensajero: hace desde el programa lo que hace tu navegador al abrir una dirección. | `r = requests.get("https://x.com/robots.txt")`; `r.status_code` da `200` y `r.text` trae el texto. |
| `urllib.robotparser` | Un lector de carteles: le das el robots.txt y responde preguntas. | `rp.can_fetch("MiBot", "https://x.com/wp-admin/")` da `False`. |
| `functools.lru_cache` | Le da memoria a una función. | Pide el robots.txt de un sitio una sola vez, aunque se pregunte mil veces. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| `rp.read()`, que es lo que usa la guía | Descarga con el nombre por defecto de Python, no con el nuestro, y no deja arreglar el texto antes de leerlo. |
| Descargar el robots.txt cada vez que se visita una página | Le pediría el mismo archivo al sitio cientos de veces, sin necesidad. |


## [Etapa 1 · Paso 3] 5. Preguntar si se puede entrar: `puede_visitar`

> **Para qué:** Que el programa responda solo, página por página, si puede entrar o no. Es el guardia de la puerta: toda descarga pasa primero por aquí.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Mirar la dirección que el programa quiere visitar y apartar el nombre del sitio. | `urlparse(url)`. |
| Buscar el cartel de ese sitio en el cuaderno. | `_robots(...)`. |
| Comparar la dirección con las reglas del cartel y decir sí o no. | `can_fetch(USER_AGENT, url)`. |
| Si no se puede consultar el cartel (por ejemplo, se cayó internet), no entrar. | `except requests.RequestException: return False`. |

```
def puede_visitar(url: str) -> bool:
    p = urlparse(url)
    try:
        robots = _robots(f"{p.scheme}://{p.netloc}")
    except requests.RequestException as e:
        print(f"No se pudo leer el robots.txt de {p.netloc}: {e}")
        return False
    return robots.can_fetch(USER_AGENT, url)
```

**Cómo funciona, paso a paso:**

1. `urlparse(url)` parte la dirección en sus partes.
2. Con el protocolo y el dominio arma la dirección base del sitio.
3. Intenta pedir a `_robots` el robots.txt de ese sitio (ya interpretado).
4. Si falla la red y no se puede leer, imprime el motivo y devuelve `False`: sin poder comprobar el permiso, no se entra.
5. `can_fetch(USER_AGENT, url)` aplica la lógica de decisión de CONCEPTOS 7 y devuelve `True` o `False`.

| Dirección | `urlparse` la parte en | Resultado |
|---|---|---|
| `https://www.viviendoporelmundo.com/wp-admin/` | protocolo `https`, dominio `www.viviendoporelmundo.com`, ruta `/wp-admin/` | `False` |
| `https://www.viviendoporelmundo.com/` | ruta `/` | `True` |
| `https://www.viviendoporelmundo.com/xmlrpc.php` | ruta `/xmlrpc.php` | `False` |

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Parámetro con tipo | Después de los dos puntos va el tipo de dato esperado, y la flecha dice qué devuelve. Es una pista para quien lee. | `def puede_visitar(url: str) -> bool` recibe un texto y devuelve verdadero o falso. |
| Verdadero o falso (`bool`) | Solo dos valores posibles: `True` y `False`. | `5 > 3` da `True`; `"a" == "b"` da `False`. |
| Atributos | Los datos que guarda un objeto, que se leen con un punto. | `p.scheme` es el protocolo y `p.netloc` el dominio. |
| Funciones que usan funciones | Una receta puede apoyarse en otras. | `puede_visitar` pide a `_robots` el robots.txt en vez de descargarlo ella misma. |

**La librería, en simple:**

| Herramienta | Qué hace | Ejemplo mínimo |
|---|---|---|
| `urllib.parse.urlparse` | Una navaja que parte una dirección en sus partes. | `urlparse("https://x.com/a/b")` da protocolo `https`, dominio `x.com` y ruta `/a/b`. |
| `can_fetch` | La pregunta al lector de carteles. | `can_fetch(nombre, direccion)` da `True` o `False` aplicando la lógica de decisión. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| Comparar con una lista de rutas prohibidas escrita a mano | No sirve para otro sitio y se queda vieja. |
| Dejar que el programa se caiga si falla la red | Pasó de verdad en la primera ejecución del paso 7: un error de decenas de líneas, difícil de entender. Con el aviso de una línea se sabe qué pasó y se puede repetir. |
| No preguntar y confiar en no tocar nada prohibido | Un error de una sola línea haría que el programa entre a una zona prohibida sin que nadie lo note. |
| Revisar el robots.txt a ojo antes de cada ejecución | Se olvida. Con la función, el permiso queda dentro del código. |


## [Etapa 1 · Paso 3] 6. Cuánto esperar: `espera_del_sitio`

> **Para qué:** Respetar el ritmo que pide el sitio sin tener que acordarse del número. Cada sitio pide algo distinto.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Preguntar en recepción cuánto hay que esperar entre una visita y otra. | `crawl_delay(USER_AGENT)`. |
| Si dan un número, esperar eso; si no dicen nada, esperar al menos 2 segundos. | `float(retraso) if retraso else por_defecto`. |

```
def espera_del_sitio(url: str, por_defecto: float = 2.0) -> float:
    p = urlparse(url)
    retraso = _robots(f"{p.scheme}://{p.netloc}").crawl_delay(USER_AGENT)
    return float(retraso) if retraso else por_defecto
```

**Cómo funciona, paso a paso:** busca el robots.txt del sitio, le pregunta por el `Crawl-delay` que corresponde a nuestro bot, y si existe lo devuelve como número; si el sitio no indica nada, devuelve 2 segundos como mínimo de cortesía.

| Situación | Qué devuelve |
|---|---|
| El sitio dice `Crawl-delay: 10` (este sitio) | `10.0` |
| El sitio no dice nada | `2.0` |

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Valor por defecto | Lo que vale un dato si quien llama no lo da. | `def saludar(nombre="amigo")`; `saludar()` usa `"amigo"`. |
| `None` | La ausencia de valor: «aquí no hay nada». | Si el sitio no indica espera, `crawl_delay` devuelve `None`. |
| Entero y decimal | `int` no tiene decimales y `float` sí. | `10` es entero; `float(10)` da `10.0`. |
| Condicional en una línea | `A if condicion else B` elige entre dos valores. | `"mayor" if edad >= 18 else "menor"`. |

**La librería, en simple:**

| Herramienta | Qué hace | Ejemplo mínimo |
|---|---|---|
| `crawl_delay` | Le pregunta al lector de carteles cuánto hay que esperar. | Con este sitio da `10`; con uno que no pide nada da `None`. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| Esperar siempre 2 segundos, como en la guía | Es demasiado rápido para este sitio, que pide 10. |
| Esperar siempre 10 segundos | Es lento en sitios que no piden tanto, y no se adapta a los que piden más. |
| No esperar y ganar velocidad | Un servidor pequeño puede caerse o bloquearnos. Es el motivo de ser educados. |


## [Etapa 1 · Paso 3] 7. Comprobar el robots.txt: `probar_robots.py`

> **Para qué:** Comprobar con rutas que sabemos que deben dar «no» que los permisos funcionan de verdad. Gracias a esta prueba apareció el fallo de la línea en blanco.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Hacer una lista de nueve direcciones, unas que deben dejar pasar y otras que no. | La lista `rutas`. |
| Ir una por una preguntando al guardia y anotar SÍ o NO. | El bucle `for ruta in rutas`. |
| Al final, preguntar cuánto esperar y dónde está el plano del sitio. | `espera_del_sitio` y `site_maps()`. |

```
from scraper import USER_AGENT, _robots, espera_del_sitio, puede_visitar

SITIO = "https://www.viviendoporelmundo.com"
rutas = ["/", "/un-articulo/", "/wp-admin/", "/wp-admin/login.php",
         "/wp-includes/js/jquery.js", "/wp-content/uploads/2025/foto.jpg",
         "/wp-content/plugins/algo/", "/xmlrpc.php", "/readme.html"]

for ruta in rutas:
    resultado = puede_visitar(SITIO + ruta)
    print(f"  {'SÍ' if resultado else 'NO':<3} {ruta}")

print(espera_del_sitio(SITIO))
print(_robots(SITIO).site_maps())
```

Esta es una versión resumida del script. Se ejecuta en la terminal: `.venv\Scripts\python.exe probar_robots.py`.

**Cómo funciona:** toma nueve rutas, pregunta a `puede_visitar` por cada una e imprime `SÍ` o `NO`; al final imprime la espera y la dirección del sitemap. Mezcla rutas que deben dar sí (`/`, los artículos, las fotos) con rutas que deben dar no (las prohibidas).

| Ruta | Antes de arreglar | Después de arreglar |
|---|---|---|
| `/wp-admin/`, `/wp-admin/login.php`, `/wp-includes/js/jquery.js` | NO | NO |
| `/wp-content/plugins/algo/` | **SÍ (error)** | NO |
| `/xmlrpc.php` | **SÍ (error)** | NO |
| `/readme.html` | **SÍ (error)** | NO |
| `/`, `/un-articulo/`, `/wp-content/uploads/2025/foto.jpg` | SÍ | SÍ |

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Script y función | Una función espera a que la llamen; un script es un archivo que se ejecuta de arriba abajo. | `probar_robots.py` se ejecuta; `puede_visitar` solo trabaja cuando alguien la llama. |
| `import` | Traer funciones de otro archivo o de una librería. | `from scraper import puede_visitar` trae esa función de `scraper.py`. |
| Sumar textos | El signo `+` pega textos uno tras otro. | `"https://x.com" + "/wp-admin/"` da `https://x.com/wp-admin/`. |
| Formato de columnas | En un f-string, `:<3` reserva 3 espacios para alinear. | Con `:<3`, `NO` y `SÍ` ocupan el mismo ancho y las rutas quedan alineadas. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| Confiar en que el código funciona sin probarlo | No se habría visto que tres rutas prohibidas salían permitidas. Una prueba con casos que *deben* fallar es la que descubre este tipo de errores. |
| Probar a mano en el navegador | El navegador no ejecuta nuestras reglas: no comprueba lo que va a hacer el programa. |


## [Etapa 2 · Paso 5] 8. Pedir una página con educación: `HEADERS` y `pedir`

> **Para qué:** Descargar una página respetando todas las reglas de los pasos anteriores (permiso, espera y nombre) y devolver todo lo que respondió el sitio. Es la función que usará el resto del proyecto.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Preguntar al guardia si se puede entrar. | `puede_visitar(url)`. |
| Esperar los segundos que pide el sitio. | `time.sleep(...)`. |
| Tocar la puerta con tu tarjeta de presentación y pedir la página. | `requests.get(url, headers=HEADERS, timeout=20)`. |
| Si dicen que hubo un problema, anotarlo y seguir con otra cosa. | El bloque `try` y `except`, que imprime el motivo y devuelve `None`. |
| Traer la respuesta completa. | `return r`. |

```
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.5",
}

def pedir(url: str, espera: float | None = None) -> requests.Response | None:
    if not puede_visitar(url):
        print(f"El robots.txt no permite visitar {url}")
        return None
    time.sleep(espera_del_sitio(url) if espera is None else espera)
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"No se pudo descargar {url}: {e}")
        return None
    return r
```

**Cómo funciona, paso a paso:**

1. `HEADERS` son los datos con los que nos presentamos en cada petición: nuestro nombre y que preferimos contenido en español.
2. Primero se pregunta a `puede_visitar`. Si el robots.txt no lo permite, se imprime un aviso, se devuelve `None` y **no se hace ninguna petición**.
3. Luego se espera: lo que pida el sitio, salvo que se indique otro valor.
4. `requests.get(...)` pide la página. `raise_for_status()` convierte un error del sitio (404, 500…) en una excepción.
5. El bloque `try`/`except` atrapa cualquier fallo de red o de código de estado, imprime el motivo y devuelve `None`, en vez de romper el programa.
6. Si todo va bien, devuelve la respuesta completa (`r`), que incluye el código de estado, las cabeceras y el contenido.

| Caso | Qué pasa |
|---|---|
| `pedir("https://www.viviendoporelmundo.com/wp-admin/")` | Imprime «El robots.txt no permite visitar…», devuelve `None` y no toca el sitio. |
| `pedir` de una página que no existe (404) | Imprime el error, devuelve `None`; el programa sigue con la siguiente página. |
| `pedir("http://viviendoporelmundo.com/")` | Espera 10 s, pide la página, sigue la redirección y devuelve la respuesta con código 200. |

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Diccionario | Pares nombre-valor entre llaves. | `{"nombre": "Ana", "edad": 30}`; `persona["nombre"]` da `"Ana"`. |
| `try` y `except` | Intentar algo y, si falla, hacer otra cosa en vez de romperse. | `try: 10 / 0` y `except ZeroDivisionError: print("no se puede")` avisa en vez de detener el programa. |
| Salida temprana | Terminar una función apenas se sabe que no se puede seguir. | `if not puede_visitar(url): return None` corta antes de pedir nada. |
| Devolver `None` en vez de romper | Un fallo no detiene todo: se avisa y se sigue. | Si una página da 404, `pedir` devuelve `None` y el recorrido continúa con la siguiente. |
| `not` | Invierte una condición. | `not True` da `False`. |

**La librería, en simple:**

| Herramienta | Qué hace | Ejemplo mínimo |
|---|---|---|
| `time.sleep` | Pone el programa a dormir unos segundos. | `time.sleep(10)` hace una pausa de diez segundos. |
| `requests.get` | Pide la dirección, presentándose con la tarjeta (`headers`) y con un tiempo máximo de espera (`timeout`). | Pedir la portada devuelve una respuesta con el código 200. |
| `raise_for_status` | Si la respuesta es un error, avisa con una excepción. | Una página que no existe da el error 404 y salta al bloque `except`. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| Llamar directamente a `requests.get(url)` | No pregunta el permiso, no espera y se presenta con el nombre por defecto. Habría que repetir esas tres cosas en cada sitio donde se descargue algo. |
| Usar `urllib.request`, que viene con Python | Hace lo mismo, pero con más líneas y más difícil de leer. `requests` es la librería habitual para esto. |
| Descargar varias páginas a la vez para ir más rápido | Rompería la espera de 10 segundos: es justo lo que el sitio pidió que no se haga. |
| Que falle y se detenga el programa ante un error | Una sola página rota detendría el recorrido de las 244. Por convención del proyecto, un fallo imprime el motivo y devuelve `None`. |
| Sin `timeout` | Si el servidor no responde, el programa se quedaría esperando para siempre. |


## [Etapa 2 · Paso 5] 9. Obtener solo el texto HTML: `descargar`

> **Para qué:** Quedarse únicamente con el HTML legible de una página y descartar lo que no lo es. Es la versión simple de `pedir`: devuelve texto en vez de la respuesta completa.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Revisar el paquete: ¿es una página web o es una foto? | La condición sobre `Content-Type`. |
| Si es una foto o un PDF, dejarlo. | `return None`. |
| Comprobar que las letras se leen bien; si no, usar el diccionario adecuado. | `r.encoding = r.apparent_encoding`. |
| Entregar el texto de la página. | `return r.text`. |

```
def descargar(url: str, espera: float | None = None,
              solo_html: bool = True) -> str | None:
    r = pedir(url, espera)
    if r is None:
        return None
    if solo_html and "text/html" not in r.headers.get("Content-Type", ""):
        return None
    if r.encoding in (None, "ISO-8859-1"):
        r.encoding = r.apparent_encoding
    return r.text
```

**Cómo funciona, paso a paso:**

1. Llama a `pedir`. Si devolvió `None` (no se pudo o no se debe), devuelve `None`.
2. Si `solo_html` está activo, mira el tipo de contenido: si no es HTML (una imagen, un PDF), devuelve `None`.
3. Si la respuesta no declara su codificación, o declara una antigua (`ISO-8859-1`), deja que `requests` la adivine con `apparent_encoding`.
4. Devuelve el texto de la página.

| Caso | Qué devuelve |
|---|---|
| La portada de la web (HTML) | Un texto largo con todo el HTML. |
| Un archivo `.jpg` o `.pdf` | `None`. |
| Una dirección prohibida o que falla | `None`. |

**Sobre la codificación.** Es la tabla que dice cómo se guardan las letras. Si se lee con la tabla equivocada, «Acción» aparece como «AcciÃ³n». Por eso, cuando la respuesta no la declara bien, se deja que `requests` la deduzca del propio texto.

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Combinar condiciones | `and` pide que se cumplan las dos; `or`, que se cumpla una; `not`, que no se cumpla. | `solo_html and "text/html" not in tipo` solo descarta si el interruptor está activo y el tipo no es HTML. |
| Interruptor (`bool`) | Un parámetro verdadero o falso que activa o apaga algo. | `solo_html=True` activa el filtro; `False` lo apaga. |
| Pedir con respaldo | `.get(clave, respaldo)` devuelve el respaldo si la clave no existe. | `headers.get("Content-Type", "")` da texto vacío si falta, sin romperse. |
| Cambiar un atributo | Asignar un valor nuevo a una propiedad del objeto. | `r.encoding = r.apparent_encoding` corrige la codificación antes de leer el texto. |

**La librería, en simple:**

| Herramienta | Qué hace | Ejemplo mínimo |
|---|---|---|
| `r.text` | El contenido de la respuesta ya convertido a texto. | La página completa como un texto largo. |
| `r.headers` | La nota del mensajero, como un diccionario. | `r.headers["Content-Type"]` da `text/html; charset=UTF-8`. |
| `r.apparent_encoding` | La librería mira el contenido y adivina con qué tabla de letras estaba escrito. | La palabra «Acción» leída con la tabla equivocada sale como «AcciÃ³n». |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| Devolver siempre `r.text` sin revisar | Las tildes y las eñes podrían salir rotas en páginas que no declaren su codificación. |
| Usar `r.content` (los bytes sin decodificar) | Habría que decodificar a mano. Para texto es más cómodo recibirlo ya como texto. |
| Aceptar cualquier tipo de archivo | Al intentar leer una imagen o un PDF como HTML saldría basura, y el paso de extracción fallaría más adelante. |


## [Etapa 2 · Paso 5] 10. Ver la respuesta del sitio: `probar_descarga.py`

> **Para qué:** Pedir una sola página y mirar la respuesta completa: código de estado, tipo de contenido, redirecciones y HTML crudo. Sirve para entender qué recibe un programa antes de procesarlo.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Pedir la página y anotar lo que dicen en la puerta. | `pedir(URL)`. |
| Anotar el código de respuesta, la clase de paquete y cuánto pesa. | `r.status_code`, el tipo de contenido y `len(r.content)`. |
| Anotar a dónde lo mandaron si cambió de dirección. | `r.url` y `r.history`. |
| Leer los primeros renglones del paquete. | `r.text[:500]`. |

```
from scraper import espera_del_sitio, pedir

URL = "http://viviendoporelmundo.com/"
r = pedir(URL)

print(r.status_code)
print(r.headers.get("Content-Type"))
print(len(r.content))
print(r.url)
for salto in r.history:
    print(salto.status_code, salto.url, "->", salto.headers.get("Location"))
print(r.text[:500])
```

Es una versión resumida. Se ejecuta en la terminal: `.venv\Scripts\python.exe probar_descarga.py`.

**Cómo funciona:** pide la portada con `pedir` y luego imprime partes de la respuesta: el código de estado, el tipo de contenido, el tamaño, la dirección final y las redirecciones por las que pasó (`r.history`), y los primeros 500 caracteres del HTML.

| Dato | Lo que salió (9 oct 2026) | Qué dice |
|---|---|---|
| `r.status_code` | 200 | La petición salió bien. |
| Tipo de contenido | `text/html; charset=UTF-8` | Una página HTML con tildes bien guardadas. |
| Tamaño | 245.915 bytes | Unos 240 KB en una sola página. |
| `r.url` y `r.history` | 301 de `http://viviendoporelmundo.com/` a `https://www.viviendoporelmundo.com/` | El sitio se mudó de dirección y el código siguió el cambio. |
| `r.text[:500]` | `<!DOCTYPE html>`, comentarios para Internet Explorer, `<meta>` y un `<script>` | El HTML crudo es código, no texto de artículo. |

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Atributos de una respuesta | La respuesta sabe cosas de sí misma, y se leen con un punto. | `r.status_code` da `200`; `r.url` da la dirección final. |
| Rebanar un texto | `[:500]` toma solo los primeros 500 caracteres. | `"abcdef"[:3]` da `"abc"`. |
| Recorrer una lista de saltos | Un `for` sirve para ver uno por uno los elementos de `r.history`. | Cada salto es una redirección con su código y su dirección. |

**La librería, en simple:**

| Herramienta | Qué hace | Ejemplo mínimo |
|---|---|---|
| `r.history` | La lista de redirecciones por las que pasó la petición. | Aquí tiene un solo salto: el 301 hacia `https://www…`. |
| `r.elapsed` | Cuánto tardó la respuesta. | Dio 1,86 segundos. |
| `re.findall` | Busca todos los lugares donde aparece un patrón en un texto. | En el script completo, `re.findall(r"<a ", texto)` encuentra cada etiqueta de enlace y sirve para contarlos. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| Abrir la página en el navegador y mirarla | El navegador te muestra la página ya montada y oculta la redirección y las cabeceras. El programa recibe otra cosa. |
| Imprimir solo el texto, sin los datos de la respuesta | No se vería el código de estado ni la redirección, que fue justo lo que se descubrió. |
| Descargar muchas páginas para probar | Una sola basta para entender la respuesta, y cada petición de más es una visita más al sitio. |


## [Etapa 2 · Paso 6] 11. Leer un sitemap: `leer_sitemap`

> **Para qué:** Convertir un archivo de sitemap en una lista de datos que el programa pueda usar: direcciones, fechas y de qué mapa salió cada una. Con la misma función se lee el índice y cada mapa hijo.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Pedir el archivo del catálogo. | `descargar(sitemap_url, solo_html=False)`. |
| Si no te lo dan, dejarlo y seguir. | `if not contenido: return [], []`. |
| Abrir el catálogo y reconocer sus fichas. | `ET.fromstring(...)` y `raiz.findall(...)`. |
| Copiar de cada ficha su dirección y su fecha a una tabla. | La función `leer(...)`, con `findtext` para la dirección y para la fecha. |
| Anotar de qué catálogo salió cada ficha. | El dato `"mapa": sitemap_url`. |
| Entregar dos montones: los catálogos hijos y las páginas. | `return leer("sitemap"), leer("url")`. |

```
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

def leer_sitemap(sitemap_url: str) -> tuple[list[dict], list[dict]]:
    contenido = descargar(sitemap_url, solo_html=False)
    if not contenido:
        return [], []
    raiz = ET.fromstring(contenido.encode("utf-8"))

    def leer(etiqueta: str) -> list[dict]:
        return [
            {
                "url": e.findtext("sm:loc", "", NS).strip(),
                "lastmod": e.findtext("sm:lastmod", "", NS).strip(),
                "mapa": sitemap_url,
            }
            for e in raiz.findall(f"sm:{etiqueta}", NS)
        ]

    return leer("sitemap"), leer("url")
```

**Cómo funciona, paso a paso:**

1. `descargar(..., solo_html=False)` pide el archivo (con permiso, espera y nombre) y devuelve su texto. Se apaga el filtro de HTML porque un sitemap es XML.
2. Si no se pudo descargar, devuelve dos listas vacías y no rompe nada.
3. `ET.fromstring(...)` convierte el texto XML en un árbol de etiquetas que se puede recorrer. `raiz` es la etiqueta de más afuera (`sitemapindex` o `urlset`).
4. La función interna `leer` busca todas las etiquetas de un tipo (`sitemap` o `url`) y, de cada una, saca la dirección (`loc`) y la fecha (`lastmod`).
5. Cada ficha se guarda como un diccionario con tres datos: `url`, `lastmod` y `mapa` (de qué archivo salió).
6. La función devuelve **dos listas**: la de mapas hijos y la de páginas. Un índice llena la primera; un mapa de páginas llena la segunda.

**Ejemplo.** Lo que devuelve según el archivo que se le pase:

| Se le pasa | `mapas` | `paginas` |
|---|---|---|
| `.../sitemap_index.xml` (el índice) | 2 elementos: el de entradas y el de páginas | vacía |
| `.../post-sitemap.xml` | vacía | 244 elementos |
| `.../page-sitemap.xml` | vacía | 48 elementos |

Y así se ve una de las fichas que devuelve (la primera del mapa de entradas):

```
{"url": "https://www.viviendoporelmundo.com/9-beneficios-de-viajar-como-medicina-contra-el-estres/",
 "lastmod": "2015-10-26T22:42:16+00:00",
 "mapa": "https://www.viviendoporelmundo.com/post-sitemap.xml"}
```

**Qué es `NS`.** Las etiquetas de un sitemap pertenecen a un «dialecto» identificado por una dirección (`http://www.sitemaps.org/schemas/sitemap/0.9`). Si el lector no lo sabe, busca `url` y no encuentra nada, porque la etiqueta se llama en realidad «`url` del dialecto de sitemaps». `NS` le dice cuál es, y `sm:` es solo el apodo corto que se usa para escribirlo.

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Lista de diccionarios | Una lista donde cada elemento es un diccionario: como una tabla con una fila por ficha. | `[{"url": "a"}, {"url": "b"}]` tiene dos filas. |
| Función dentro de otra función | Una receta pequeña que solo existe dentro de la grande y le ayuda. | `leer` vive dentro de `leer_sitemap` y se usa dos veces. |
| Devolver dos cosas a la vez | `return a, b` entrega las dos; quien llama las recibe con `x, y = ...`. | `mapas, paginas = leer_sitemap(url)`. |
| Espacio de nombres (`NS`) | La dirección que identifica el «dialecto» de las etiquetas. | Sin `NS`, buscar `sm:url` no encuentra nada. |
| `findall` y `findtext` | `findall` busca todas las etiquetas de un tipo; `findtext` saca el texto de una etiqueta hija. | `e.findtext("sm:loc")` da la dirección de esa ficha. |
| Docstring | El texto entre triples comillas al inicio de una función, que explica qué hace. | El de `leer_sitemap` dice que devuelve `(mapas, paginas)`. |
| Convertir texto a bytes (`encode`) | Pasa el texto a bytes en UTF-8 para que el lector respete la codificación que declara el archivo. | `"Acción".encode("utf-8")` da bytes. |

**La librería, en simple:**

| Herramienta | Qué hace | Ejemplo mínimo |
|---|---|---|
| `xml.etree.ElementTree` (`ET`) | Un lector de etiquetas: convierte un texto XML en un árbol que se puede recorrer. | `ET.fromstring("<a><b>hola</b></a>").findtext("b")` da `hola`. |
| `descargar` | La función del paso 5: pide el archivo con permiso, espera y nombre. | `descargar(url, solo_html=False)` devuelve el texto del archivo. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| Leer el sitemap con BeautifulSoup y `lxml` | También funcionaría y se usará para el HTML. Para un XML regular y sencillo como este, `ElementTree` viene con Python y evita depender de otra librería. |
| Buscar las direcciones con una expresión regular (`re`) | Es frágil: un comentario o un cambio de formato la rompe. Un lector de XML entiende la estructura del archivo. |
| Copiar las direcciones a mano desde el navegador | Se hizo en el paso 4 y sirve para entender, pero no escala y es fácil equivocarse. El código lo repite en segundos y se puede comprobar (244 contra 244). |
| Una función recursiva que devuelva solo las direcciones, como la guía | Pierde la fecha y de qué mapa salió cada dirección, y no deja ver el índice por separado. En el paso 7 se usará una versión que recorra todo. |
| Pedir con `requests.get` directamente | Se salta el permiso, la espera y el nombre del bot. `descargar` ya los trae. |


## [Etapa 2 · Paso 6] 12. Leer el índice y los dos mapas: `probar_sitemap.py`

> **Para qué:** Leer el índice y sus dos mapas, sumar las direcciones y comprobar el resultado contra lo que se vio a ojo en el paso 4 (244). Sirve para verificar que el código lee lo mismo que el navegador y para conocer el tamaño del trabajo.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Abrir el catálogo general y anotar cuántos catálogos hijos hay. | `leer_sitemap(INDICE)`. |
| Ir a cada catálogo hijo y copiar todas sus fichas a una lista grande. | El bucle `for m in mapas` y `todas += paginas`. |
| Contar cuántas fichas hay y si alguna se repite. | `len(urls)` y `len(set(urls))`. |
| Contar cuántas vienen de cada catálogo. | `Counter(p["mapa"] for p in todas)`. |
| Mirar la ficha más vieja y la más nueva, y cuántas hay por año. | `fechas[0]`, `fechas[-1]` y `Counter(f[:4] ...)`. |

```
from collections import Counter
from scraper import leer_sitemap

INDICE = "https://www.viviendoporelmundo.com/sitemap_index.xml"

mapas, sueltas = leer_sitemap(INDICE)
todas = []
for m in mapas:
    _, paginas = leer_sitemap(m["url"])
    todas += paginas

urls = [p["url"] for p in todas]
print(len(urls), len(set(urls)))
print(Counter(p["mapa"] for p in todas))

fechas = sorted(p["lastmod"] for p in todas if p["lastmod"])
print(fechas[0], fechas[-1])
print(Counter(f[:4] for f in fechas))
```

Es una versión resumida. Se ejecuta en la terminal: `.venv\Scripts\python.exe probar_sitemap.py`. Tarda unos 40 segundos por las esperas de 10 s.

**Cómo funciona, paso a paso:**

1. Lee el índice y obtiene la lista de mapas hijos.
2. Crea una lista vacía (`todas`) y, por cada mapa hijo, lo lee y agrega sus direcciones al final.
3. Saca solo las direcciones (`urls`) y las cuenta de dos formas: con repetidas (`len(urls)`) y sin repetidas (`len(set(urls))`).
4. Cuenta cuántas direcciones salieron de cada mapa.
5. Ordena las fechas para ver la más antigua y la más reciente, y cuenta cuántas hay por año (los cuatro primeros caracteres de la fecha).

**El resultado real** (10 de octubre de 2026):

| Dato | Lo que salió | Qué dice |
|---|---|---|
| Mapas hijos | 2 | Entradas y páginas. |
| Direcciones por mapa | 244 y 48 | El de entradas coincide con el encabezado y con el paso 4. |
| Total y distintas | 292 y 292 | No hay repetidas. |
| Fecha más antigua y más reciente | 2015-10-26 y 2026-06-20 | El sitio lista contenido de unos once años. |
| Peticiones y tiempo | 3 (más el robots.txt) y 38 s | Dos esperas de 10 s y una respuesta más lenta. |

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Agregar al final de una lista (`+=`) | Suma los elementos de otra lista al final de la primera. | `[1, 2]` más `[3]` con `+=` queda `[1, 2, 3]`. |
| Conjunto (`set`) | Un grupo que guarda cada valor una sola vez. Comparar su tamaño con el de la lista detecta repetidos. | `set(["a", "a", "b"])` tiene 2 elementos; la lista tenía 3. |
| `sorted` | Devuelve una lista ordenada. | `sorted([3, 1, 2])` da `[1, 2, 3]`. |
| Primer y último elemento | `[0]` es el primero y `[-1]` el último. | `["a", "b", "c"][-1]` da `"c"`. |
| Rebanar un texto | `[:4]` toma los cuatro primeros caracteres. | `"2026-06-20"[:4]` da `"2026"`: el año. |
| Guion bajo `_` | Un nombre para un valor que se recibe pero no se va a usar. | `_, paginas = leer_sitemap(url)` ignora la primera lista. |
| Recorrido corto con corchetes | Una forma breve de recorrer una lista y sacar un dato de cada elemento. | `[p["url"] for p in todas]` saca solo las direcciones. |

**La librería, en simple:**

| Herramienta | Qué hace | Ejemplo mínimo |
|---|---|---|
| `collections.Counter` | Un contador: cuenta cuántas veces aparece cada cosa. | `Counter(["a", "b", "a"])` da `a: 2` y `b: 1`. |
| `time.time()` | Un reloj: dice la hora en segundos, y restando dos lecturas se mide cuánto tardó algo. | En el script completo, `time.time() - inicio` dio unos 38 segundos. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| Contar a mano en el navegador | Se hizo en el paso 4 y no se puede repetir ni comprobar. El código lo hace en 40 segundos y deja el número comprobado. |
| Guardar todo en la base de datos y contar después | Es el paso 7. Antes conviene ver los números en pantalla para saber que la lectura es correcta. |
| Pedir los dos mapas a la vez para ir más rápido | Rompería la espera de 10 segundos que pide el sitio. |
| Leer también las 292 páginas para comprobar que existen | Serían casi 49 minutos y no hace falta: ahora solo interesa la lista, no el contenido. |


## [Etapa 2 · Paso 7] 13. Abrir la base de datos: `abrir_base`

> **Para qué:** Tener un solo lugar desde el que se abre la base de datos y que, si no existe, la cree con su tabla. Así todos los scripts la abren igual.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Buscar el cuaderno del proyecto en su estante fijo, junto a los demás papeles. | `RUTA_BASE = Path(__file__).parent / "datos" / "scraping.db"`. |
| Si no existe el estante, construirlo. | `RUTA_BASE.parent.mkdir(exist_ok=True)`. |
| Abrir el cuaderno. | `sqlite3.connect(RUTA_BASE)`. |
| Si el cuaderno es nuevo, dibujarle las columnas. | `CREATE TABLE IF NOT EXISTS urls (...)`. |
| Entregar el cuaderno abierto. | `return con`. |

```
RUTA_BASE = Path(__file__).parent / "datos" / "scraping.db"

def abrir_base() -> sqlite3.Connection:
    RUTA_BASE.parent.mkdir(exist_ok=True)
    con = sqlite3.connect(RUTA_BASE)
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS urls (
            url          TEXT PRIMARY KEY,
            sitio        TEXT NOT NULL,
            origen       TEXT NOT NULL,
            mapa         TEXT,
            lastmod      TEXT,
            vale_la_pena INTEGER,
            motivo       TEXT,
            fecha_mapeo  TEXT NOT NULL
        )
        """
    )
    return con
```

**Cómo funciona, paso a paso:**

1. `RUTA_BASE` calcula dónde va el archivo: dentro de `datos/`, junto al código, sin importar en qué carpeta del computador esté el proyecto.
2. `mkdir(exist_ok=True)` crea la carpeta `datos/` si no existe y no se queja si ya existe.
3. `sqlite3.connect(...)` abre el archivo de la base; si no existe, lo crea.
4. `CREATE TABLE IF NOT EXISTS` dibuja la tabla `urls` con sus columnas solo si todavía no existe, así que abrir la base muchas veces no borra nada.
5. Devuelve la conexión (`con`), que es el canal por el que se hablará con la base.

| Situación | Qué pasa |
|---|---|
| Primera vez: no existe `datos/scraping.db` | Se crea la carpeta, el archivo y la tabla vacía. |
| Segunda vez en adelante | Se abre el mismo archivo con sus datos intactos. |

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Ruta (`Path`) | Una dirección de archivo tratada como objeto; sus partes se unen con `/`. | `Path("datos") / "scraping.db"` da `datos\scraping.db`. |
| `__file__` | El nombre del archivo de código que se está ejecutando. | `Path(__file__).parent` es la carpeta donde está `scraper.py`. |
| Conexión | El canal abierto hacia la base de datos, por el que se mandan órdenes. | `con = sqlite3.connect("cosas.db")`. |
| SQL | El idioma con el que se le dan órdenes y preguntas a una base de datos. | `CREATE TABLE`, `INSERT` y `SELECT` son órdenes de SQL. |
| Tipos de columna | Cada columna acepta un tipo de dato: `TEXT` para texto, `INTEGER` para enteros. | `vale_la_pena INTEGER` guarda 1, 0 o nada. |
| `PRIMARY KEY` y `NOT NULL` | La clave que no se repite, y una columna que no puede quedar vacía. | `url` es la clave; `sitio` es obligatorio. |
| `IF NOT EXISTS` | Hazlo solo si todavía no está hecho. | Evita borrar o duplicar la tabla al abrir la base otra vez. |
| Triples comillas | Permiten escribir un texto de varias líneas. | Así se escribe la orden SQL, que ocupa varias líneas. |

**La librería, en simple:**

| Herramienta | Qué hace | Ejemplo mínimo |
|---|---|---|
| `sqlite3` | El cuaderno en un archivo: guarda tablas y responde preguntas. Viene con Python. | `sqlite3.connect("cosas.db")` crea el archivo si no existe. |
| `pathlib.Path` | Maneja rutas de archivos sin pelearse con las barras. | `Path("a") / "b"` da `a\b` en Windows. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| Guardar en archivos JSON o CSV, como en la guía 1 | No evitan los repetidos ni responden preguntas como «dame las de este mapa». Una base de datos sí. |
| Usar Supabase, como propone la guía 2 | Pide cuenta, claves y conexión a internet, y aquí no hace falta. Es una decisión registrada (D2): el SQL de SQLite se pasa casi igual si algún día se necesita. |
| Una base distinta para cada ejercicio | El proyecto lo prohíbe: todo va a una sola base, separado por la columna `sitio`. |
| Escribir la ruta completa, como `C:\Users\...` | Se rompería en otro computador o en otra carpeta. Calcularla a partir del archivo funciona siempre. |


## [Etapa 2 · Paso 7] 14. Leer un sitemap completo: `urls_desde_sitemap`

> **Para qué:** Leer un sitemap entero de una vez, con sus mapas hijos, y devolver todas las páginas. Evita repetir a mano el recorrido que se hizo en el paso 6.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Abrir el catálogo general y anotar los catálogos hijos. | `leer_sitemap(sitemap_url)`. |
| Ir a cada catálogo hijo, uno por uno. | `for mapa in mapas`. |
| Si ya hay demasiadas fichas, parar. | `if len(paginas) >= limite: break`. |
| Pedir al hijo sus fichas y añadirlas a la lista. | `paginas += urls_desde_sitemap(mapa["url"], ...)`. |
| Entregar la lista sin pasar del tope. | `return paginas[:limite]`. |

```
def urls_desde_sitemap(sitemap_url: str, limite: int = 500) -> list[dict]:
    mapas, paginas = leer_sitemap(sitemap_url)
    for mapa in mapas:
        if len(paginas) >= limite:
            break
        paginas += urls_desde_sitemap(mapa["url"], limite - len(paginas))
    return paginas[:limite]
```

**Cómo funciona, paso a paso:**

1. Lee el archivo que se le da con `leer_sitemap`: obtiene mapas hijos y páginas sueltas.
2. Por cada mapa hijo, primero comprueba si ya se llegó al tope (`limite`); si es así, se detiene (`break`).
3. Si no, **se llama a sí misma** con la dirección de ese hijo, y suma lo que traiga a la lista.
4. Al final devuelve la lista, cortada para no pasar del tope.

**Qué es llamarse a sí misma (recursión).** Piensa en carpetas dentro de carpetas: para contar todos los archivos, abres una carpeta y, si encuentras otra, haces lo mismo con ella. La función hace igual: si un índice apunta a otro índice, lo resuelve sin saber de antemano cuántos niveles hay. Aquí solo hay dos niveles: el índice y sus dos hijos.

| Se le pide | Qué hace | Resultado |
|---|---|---|
| `urls_desde_sitemap(indice)` | Lee el índice, luego `post-sitemap.xml` y luego `page-sitemap.xml`. | 292 páginas, cada una con su `mapa` y su `lastmod`. |
| Con `limite=100` | Lee el índice, lee el primer hijo y, al llegar al tope, ya no pide el segundo. | Solo 100 páginas. |

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Recursión | Una función que se llama a sí misma para resolver un problema por capas. | Contar archivos en carpetas dentro de carpetas: abrir una y repetir con cada subcarpeta. |
| Tope (`limite`) | Un máximo que protege de recorridos interminables. | `limite=500` para en 500 páginas aunque el sitio tenga más. |
| `break` | Sale de un bucle antes de que termine. | `for x in lista: if x > 3: break` se detiene al ver un número mayor que 3. |
| Recortar una lista (`[:limite]`) | Se queda con los primeros elementos. | `[1, 2, 3, 4][:2]` da `[1, 2]`. |
| Valor por defecto | Si no se indica el tope, vale 500. | `urls_desde_sitemap(indice)` usa `limite=500`. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| Leer cada hijo a mano en el script, como en `probar_sitemap.py` | Sirve para ver paso a paso, pero repite código y no funciona si un índice apunta a otro índice. |
| Una función que devuelva solo texto con las direcciones, como la guía | Pierde la fecha y el mapa de origen, que la base necesita guardar. |
| No poner tope (`limite`) | Un sitio con miles de direcciones podría tardar horas. El proyecto exige un tope en todo recorrido. |


## [Etapa 2 · Paso 7] 15. Guardar sin duplicar: `guardar_urls`

> **Para qué:** Guardar las direcciones en la base sin repetirlas y sin borrar las decisiones que ya se hayan tomado sobre ellas.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Por cada ficha, mirar si ya está en el cuaderno. | `INSERT ... ON CONFLICT(url)`. |
| Si no está, anotarla completa. | El `INSERT`. |
| Si ya está, actualizar solo de qué catálogo salió y la fecha. | `DO UPDATE SET mapa, lastmod, fecha_mapeo`. |
| No tocar la columna donde se anota si sirve o no. | `vale_la_pena` y `motivo` no aparecen en el `UPDATE`. |
| Guardar los cambios de verdad. | `con.commit()`. |

```
def guardar_urls(con, paginas, sitio, origen="sitemap") -> int:
    hoy = date.today().isoformat()
    con.executemany(
        """
        INSERT INTO urls (url, sitio, origen, mapa, lastmod, fecha_mapeo)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET
            mapa = excluded.mapa,
            lastmod = excluded.lastmod,
            fecha_mapeo = excluded.fecha_mapeo
        """,
        [(p["url"], sitio, origen, p["mapa"], p["lastmod"], hoy) for p in paginas],
    )
    con.commit()
    return len(paginas)
```

**Cómo funciona, paso a paso:**

1. `date.today().isoformat()` obtiene la fecha de hoy en formato `2026-10-10`.
2. `INSERT INTO urls (...) VALUES (?, ?, ...)` es la orden de agregar una fila; cada `?` es un hueco que se llena con un dato.
3. `ON CONFLICT(url) DO UPDATE` dice qué hacer si la dirección ya existe: en vez de dar error, actualizar solo `mapa`, `lastmod` y `fecha_mapeo`.
4. `excluded` son los valores nuevos que se intentaron guardar.
5. La lista de abajo prepara una fila por cada página; `executemany` las manda todas de una vez.
6. `commit()` confirma los cambios: hasta entonces no quedan escritos de verdad.

| Situación | Qué pasa |
|---|---|
| La dirección no existe en la base | Se agrega la fila completa. |
| La dirección ya existe | Se actualizan el mapa, la fecha de modificación y la fecha de lectura. |
| La dirección ya existe y tiene `vale_la_pena = 1` | La marca se conserva, porque el `UPDATE` no la menciona. |
| Se guardan las 292 dos veces (probado) | Siguen siendo 292 filas y la marca de prueba sigue ahí. |

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Consulta con huecos (`?`) | Las órdenes SQL llevan `?` donde irán los datos, y los datos se pasan aparte. Evita errores y ataques. | `VALUES (?, ?)` con `("a", "b")` guarda a y b. |
| `executemany` | Ejecuta la misma orden con muchas filas de datos. | Guarda 292 filas con una sola llamada. |
| Tupla | Un grupo ordenado de valores entre paréntesis, como una fila. | `("url", "sitio")`. |
| `commit` | Confirmar los cambios: hasta entonces no quedan escritos. | Sin `commit`, lo guardado se perdería al cerrar. |
| `ON CONFLICT ... DO UPDATE` | Si hay choque con una clave que ya existe, en vez de fallar, actualiza. | Guardar dos veces la misma dirección no la duplica. |
| `excluded` | Dentro del `UPDATE`, son los valores nuevos que se intentaron guardar. | `mapa = excluded.mapa` pone el mapa nuevo. |

**La librería, en simple:**

| Herramienta | Qué hace | Ejemplo mínimo |
|---|---|---|
| `sqlite3`: `executemany` y `commit` | Mandar muchas filas a la vez y confirmar el guardado. | Se guardaron las 292 direcciones en una llamada. |
| `datetime.date` | Fechas. `date.today()` da la de hoy. | `date.today().isoformat()` da `2026-10-10`. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| `INSERT` simple, sin `ON CONFLICT` | Al guardar una dirección que ya existe, daría error o la duplicaría. |
| Borrar la tabla y volver a llenarla cada vez | Se perderían las marcas de `vale_la_pena` y `motivo`. |
| `INSERT OR REPLACE` | Reemplaza la fila entera y también borraría las marcas. |
| Comprobar en Python si existe antes de insertar | Es más largo y más lento: la base lo resuelve sola en una sentencia. |
| Guardar fila por fila con un `INSERT` por llamada | Funciona, pero `executemany` es más corto y más rápido. |


## [Etapa 2 · Paso 7] 16. Hacer el paso 7 completo: `guardar_mapa.py`

> **Para qué:** Hacer todo el paso 7 de una vez: leer el sitemap, guardar las direcciones y comprobar en la base lo que quedó.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Leer el catálogo completo. | `urls_desde_sitemap(INDICE)`. |
| Si no se pudo leer nada, parar y avisar. | `raise SystemExit(...)`. |
| Pasar las fichas al cuaderno. | `abrir_base()` y `guardar_urls(...)`. |
| Hacerle preguntas al cuaderno para comprobar lo guardado. | Las consultas con `con.execute(...)`. |

```
from scraper import abrir_base, guardar_urls, urls_desde_sitemap

SITIO = "viviendoporelmundo.com"
INDICE = "https://www.viviendoporelmundo.com/sitemap_index.xml"

paginas = urls_desde_sitemap(INDICE)
if not paginas:
    raise SystemExit("No se leyó ninguna dirección: no se guarda nada.")

con = abrir_base()
guardar_urls(con, paginas, SITIO)

total = con.execute("SELECT COUNT(*) FROM urls WHERE sitio = ?", (SITIO,)).fetchone()[0]
por_mapa = con.execute("SELECT mapa, COUNT(*) FROM urls GROUP BY mapa").fetchall()
colombia = con.execute("SELECT url FROM urls WHERE url LIKE ?", ("%colombia%",)).fetchall()
```

Es una versión resumida. Se ejecuta en la terminal: `.venv\Scripts\python.exe guardar_mapa.py`. Tarda unos 40 segundos por las esperas de 10 s.

**Cómo funciona, paso a paso:**

1. Lee el sitemap completo con `urls_desde_sitemap`.
2. Si no se leyó nada (por ejemplo, por un fallo de red), termina con un mensaje y no guarda nada.
3. Abre la base y guarda las direcciones.
4. Consulta la base con SQL para comprobar lo que quedó: cuántas filas hay, cuántas por mapa, cuántas usan carpeta y cuáles nombran Colombia.

**Las consultas SQL, explicadas** (el SQL es el idioma con que se le hacen preguntas a la base):

| Consulta | En palabras | Resultado |
|---|---|---|
| `SELECT COUNT(*) FROM urls` | Cuenta cuántas filas hay en la tabla. | 292 |
| `... GROUP BY mapa` | Agrupa las filas por mapa y cuenta cada grupo. | 244 y 48 |
| `... WHERE url LIKE '%colombia%'` | Solo las filas cuya dirección contiene «colombia» en cualquier parte. | Las direcciones que nombran Colombia |
| `... WHERE vale_la_pena IS NULL` | Solo las filas aún sin decidir. | 292 |

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| `SELECT ... FROM` | Pregunta a la base: «dame esto de esta tabla». | `SELECT url FROM urls`. |
| `COUNT(*)` | Cuenta filas. | `SELECT COUNT(*) FROM urls` da 292. |
| `WHERE` | Filtra: solo las filas que cumplen una condición. | `WHERE sitio = ?`. |
| `GROUP BY` | Agrupa filas iguales para contarlas. | `GROUP BY mapa` da 244 y 48. |
| `LIKE` y `%` | Busca texto parcial: `%` significa «cualquier cosa». | `LIKE '%colombia%'` encuentra todo lo que contenga «colombia». |
| `fetchone` y `fetchall` | Traer una fila, o todas, del resultado de una consulta. | `fetchone()[0]` toma el primer valor de la primera fila. |
| `raise SystemExit` | Termina el programa con un mensaje. | Se usa si no se leyó nada, para no guardar una lista vacía. |
| Función auxiliar | Una función pequeña para no repetir código. | `corto(mapa)` deja solo el nombre del archivo del mapa. |

**La librería, en simple:**

| Herramienta | Qué hace | Ejemplo mínimo |
|---|---|---|
| `sqlite3`: `execute` | Manda una orden o una consulta a la base y devuelve el resultado. | `con.execute("SELECT COUNT(*) FROM urls")`. |
| `collections.Counter` | Cuenta cuántas veces aparece cada cosa (ya vista). | En el script completo cuenta direcciones por carpeta. |
| `urllib.parse.urlparse` | Parte una dirección (ya vista). | `urlparse(url).path` da la ruta, de donde se saca la carpeta. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| Contar las filas en una hoja de Excel | Funciona para mirar, pero no se puede repetir ni comprobar con código. |
| Guardar las direcciones en una lista de Python sin base de datos | Se pierden al cerrar el programa y habría que volver a pedirle los mapas al sitio. |
| Leer los mapas en un script y guardar en otro | Sería leer dos veces: más peticiones al sitio y más espera, sin ninguna ganancia. |


## [Etapa 3 · Paso 8] 17. Decidir una dirección: `clasificar`

> **Para qué:** Tomar una dirección y su mapa, aplicar las reglas elegidas en orden y devolver la decisión (sí o no) con su motivo. Es el corazón del filtrado.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Leer el nombre de la ficha y ver en qué sección del catálogo está. | Partir la dirección en carpeta y nombre. |
| Si es una ficha de la sección de páginas fijas (y no es una guía por país), poner «no». | Regla A + D: `return 0, "regla: página fija..."`. |
| Si el nombre suena a vídeo, podcast, entrevista o venta, poner «no». | Regla C: el bucle sobre `FAMILIAS`. |
| Si termina en «-2», sospechar que es una copia y poner «no». | `if slug.endswith("-2")`. |
| Si el nombre trae un lugar de Colombia, poner «sí» y anotar cuál. | Regla B: `palabras & LUGARES_COLOMBIA`. |
| Si no pasa nada de eso, poner «no» porque es de otro tema. | El último `return 0, "regla: otro tema..."`. |

```
LUGARES_COLOMBIA = {"colombia", "colombiano", "colombiana", "medellin", "bogota",
                    "cartagena", "cali", "tayrona", "palomino", "taganga",
                    "guatape", "cafetero", "cipriano"}

FAMILIAS = [
    ("vídeo o fotomontaje", ("video", "fotomontaje")),
    ("podcast", ("podcast",)),
    ("entrevista", ("entrevista",)),
    ("venta o afiliación", ("seguro", "hosting", "siteground", "curso", "afiliado",
                            "afiliados", "monetiza", "descuento", "criptomonedas",
                            "ingresos", "regalos")),
]

def clasificar(url: str, mapa: str) -> tuple[int, str]:
    partes = [p for p in urlparse(url).path.split("/") if p]
    carpeta = partes[0] if len(partes) > 1 else ""
    slug = partes[-1] if partes else ""
    palabras = set(slug.split("-"))

    if mapa.endswith("page-sitemap.xml") and carpeta != "paises":
        return 0, "regla: página fija, no es un artículo"
    for familia, pistas in FAMILIAS:
        if palabras & set(pistas):
            return 0, f"regla: {familia}"
    if slug.endswith("-2"):
        return 0, "regla: posible duplicado (termina en -2)"

    encontradas = sorted(palabras & LUGARES_COLOMBIA)
    if encontradas:
        tipo = "guía por país" if carpeta == "paises" else "entrada"
        return 1, f"regla: Colombia ({', '.join(encontradas)}) · {tipo}"
    return 0, "regla: otro tema (no nombra Colombia en la dirección)"
```

**Cómo funciona, paso a paso:**

1. Parte la dirección en trozos por las barras: la carpeta (si la hay) y el nombre de la página (*slug*).
2. Parte el nombre por los guiones y lo convierte en un **conjunto de palabras**: `medellin-y-guatape` da `{medellin, y, guatape}`.
3. Aplica las reglas en orden. Cada una, si se cumple, **devuelve la decisión al instante** con `return`, y las de abajo ya no se miran.
4. La comparación de palabras usa `&` (la intersección de conjuntos): «las palabras que están en los dos grupos». Comparar palabras enteras evita falsos aciertos, como encontrar `cali` dentro de `calidad`.
5. Si encuentra lugares de Colombia, los escribe en el motivo para que se vea por qué entró.

| Se le da | Devuelve |
|---|---|
| `/medellin-y-guatape/` del mapa de entradas | `(1, "regla: Colombia (guatape, medellin) · entrada")` |
| `/video-con-lo-mejor-de-colombia/` | `(0, "regla: vídeo o fotomontaje")` |
| La portada, del mapa de páginas | `(0, "regla: página fija, no es un artículo")` |
| `/paises/guia-colombia-cuanto-cuesta-viajar/` | `(1, "regla: Colombia (colombia) · guía por país")` |

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| Conjunto (`set`) | Un grupo sin repetidos, ideal para preguntar «¿está esto aquí?». | `set("medellin-y-guatape".split("-"))` da `{medellin, y, guatape}`. |
| Intersección (`&`) | Lo que está en los dos conjuntos a la vez. | `{medellin, y, guatape} & {medellin, bogota}` da `{medellin}`. |
| Salir con `return` dentro de un `if` | En cuanto una regla decide, la función termina y no mira las demás. Por eso importa el orden. | Un vídeo de Colombia sale en la regla de vídeos y no llega a la de Colombia. |
| Lista de pares | Una lista cuyos elementos son pares (familia, pistas). | `for familia, pistas in FAMILIAS` recorre cada par. |
| `endswith` | Pregunta si un texto termina de cierta forma. | `"mochila-2".endswith("-2")` da `True`. |
| `join` | Une una lista de textos con un separador. | `", ".join(["cali", "colombia"])` da `cali, colombia`. |
| Devolver una tupla | La función devuelve dos datos juntos: la decisión y el motivo. | `return 1, "regla: Colombia..."`. |

**La librería, en simple:**

| Herramienta | Qué hace | Ejemplo mínimo |
|---|---|---|
| `urllib.parse.urlparse` | Parte la dirección para sacar la ruta (ya vista). | `urlparse(url).path` da `/medellin-y-guatape/`. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| Las reglas de la guía 1 (`PATRONES_UTILES`: `/blog/`, `/noticias/`, `/articulo/`) | En este sitio ninguna dirección tiene esas carpetas: lo descartarían todo. |
| Buscar con `"cali" in slug` (texto dentro de texto) | Daría falsos aciertos: `cali` está dentro de `calidad` o `california`. Por eso se comparan palabras enteras. |
| Expresiones regulares | Podrían hacer lo mismo, pero son más difíciles de leer para quien empieza; los conjuntos de palabras bastan. |
| El buscador del sitio (opción H) o un agente (opción K) | Verían el contenido y no solo el nombre, pero no fueron las opciones elegidas. Sirven para medir lo que estas reglas se pierden. |


## [Etapa 3 · Paso 8] 18. Marcar toda la base: `filtrar_colombia.py`

> **Para qué:** Aplicar `clasificar` a las 292 direcciones guardadas, escribir cada decisión en la base y mostrar el resumen y los casos dudosos. No pide nada al sitio.

**Si lo hiciera una persona:**

| Una persona haría | El código hace |
|---|---|
| Sacar del cuaderno las fichas que no tengan una nota escrita a mano. | `SELECT ... WHERE motivo IS NULL OR motivo LIKE 'regla:%'`. |
| Decidir cada ficha con las reglas. | `clasificar(url, mapa)` para cada una. |
| Escribir al lado de cada ficha el «sí» o el «no» y el porqué. | `UPDATE urls SET vale_la_pena = ?, motivo = ?`. |
| Contar cuántos «sí» y cuántos «no» quedaron. | `SELECT vale_la_pena, COUNT(*) ... GROUP BY 1`. |

```
con = abrir_base()
filas = con.execute(
    "SELECT url, mapa FROM urls WHERE sitio = ? "
    "AND (motivo IS NULL OR motivo LIKE 'regla:%')", (SITIO,)
).fetchall()

marcas = [(*clasificar(url, mapa), url) for url, mapa in filas]
con.executemany("UPDATE urls SET vale_la_pena = ?, motivo = ? WHERE url = ?", marcas)
con.commit()

for vale, cuantas in con.execute(
        "SELECT vale_la_pena, COUNT(*) FROM urls GROUP BY 1"):
    print(vale, cuantas)
```

Es una versión resumida; el script completo también imprime el resumen por motivo, la lista de las que valen la pena y los casos dudosos. Se ejecuta en la terminal: `.venv\Scripts\python.exe filtrar_colombia.py`. Tarda menos de un segundo.

**Cómo funciona, paso a paso:**

1. Abre la base y trae las direcciones del sitio que **no tienen marca manual**: o no tienen motivo, o su motivo empieza por `regla:`.
2. Por cada una llama a `clasificar` y arma una fila `(vale_la_pena, motivo, url)`.
3. Con `UPDATE` escribe la decisión en cada dirección, y `commit` la confirma.
4. Cuenta y muestra los resultados agrupados por decisión y por motivo.

| Dato | Lo que salió (10 de octubre de 2026) |
|---|---|
| Direcciones marcadas | 292 |
| Sí | 8 |
| No | 284 |
| Peticiones al sitio | 0 |

> **Un fallo de programación en el camino** La primera vez, el script se cayó al final, en la parte que muestra los casos dudosos: la portada (`/`) no tiene nombre de página y el código intentó leerlo igual. Las marcas ya estaban guardadas. Se corrigió con una comprobación: si no hay nombre, se usa un conjunto vacío.

**Conceptos de programación que aparecen aquí:**

| Concepto | Qué es, en simple | Ejemplo mínimo |
|---|---|---|
| `UPDATE ... SET ... WHERE` | La orden SQL para cambiar datos de filas que ya existen. | `UPDATE urls SET vale_la_pena = 1 WHERE url = ?`. |
| `LIKE 'regla:%'` | Solo las filas cuyo motivo empieza por «regla:». | Protege las marcas hechas a mano. |
| `IS NULL` | Pregunta si una celda está vacía (en SQL no se escribe `= NULL`). | `motivo IS NULL` son las direcciones nunca marcadas. |
| Desempaquetar con `*` | Mete los elementos de una tupla dentro de otra. | `(*clasificar(url, mapa), url)` da `(1, "regla: ...", url)`. |
| `GROUP BY 1` | Agrupa por la primera columna de la consulta. | Agrupa por `vale_la_pena` para contar los sí y los no. |

**La librería, en simple:**

| Herramienta | Qué hace | Ejemplo mínimo |
|---|---|---|
| `sqlite3`: `executemany` con `UPDATE` | Cambia muchas filas con una sola orden (ya vista con `INSERT`). | Escribió las 292 decisiones de una vez. |
| `collections.Counter.most_common` | Ordena lo contado de más a menos. | En el script completo muestra primero los 196 de otro tema. |

**Por qué este código y no otro:**

| Alternativa | Por qué no |
|---|---|
| Marcar a mano en DB Browser for SQLite (opción J) | Sirve para corregir casos sueltos, pero no se puede repetir ni medir. Las reglas dejan el criterio escrito y repetible. |
| Borrar las direcciones que no sirven | Se decidió marcar, no borrar (D12): así cada descarte queda revisable. |
| Recalcular todas las marcas, incluidas las manuales | Pisaría las correcciones hechas a mano. Por eso solo se tocan las que empiezan por `regla:`. |

> **En resumen** Estas dieciocho piezas son todo el código del ejercicio hasta el paso 8. Cada vez que se añada código nuevo, se explicará aquí con su etapa, su «Para qué», un ejemplo y la comparación con otras opciones.

