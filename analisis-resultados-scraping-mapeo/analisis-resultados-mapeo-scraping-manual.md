# Análisis de los resultados: mapeo y scraping manual

Registro de lo que sale en cada etapa del ejercicio sobre viviendoporelmundo.com, hecho a mano con Python y guiado paso a paso.

**Versión** v3 · **Fecha** 9 de octubre de 2026 · **Estado** Etapas 0 y 1 hechas

> Fuente original: `analisis-resultados-mapeo-scraping-manual_2026-10-09_v3.html` (respaldo, no leer). Este `.md` es la copia para leer y actualizar.

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
- [ ] **Paso 5. Descargar una página con código** *(en curso)* — Terminal · Etapa 2 · Qué es una petición HTTP y el HTML crudo.
- [ ] **Paso 6. Leer el índice y los mapas hijos** — Terminal · Etapa 2 · Cómo se pasa de un índice a la lista de URLs.
- [ ] **Paso 7. Guardar las URLs en SQLite** — Terminal · Etapa 2 · Qué es una base de datos y cómo se evita duplicar.
- [ ] **Paso 8. Filtrar las URLs** — Terminal · Etapa 3 · Dónde fallan las reglas fijas.
- [ ] **Paso 9. Inspeccionar el HTML de un artículo** — Navegador (F12) · Etapa 4 · La estructura de una página.
- [ ] **Paso 10. Extraer el texto de una página** — Terminal · Etapa 4 · Qué hacen BeautifulSoup y trafilatura.
- [ ] **Paso 11. Guardar la ficha y la cita** — Terminal · Etapa 5 · Cómo queda un dato citable.
- [ ] **Paso 12. Muestra de 3 y luego 10 páginas** — Terminal · Etapas 4 y 5 · Qué pasa al repetir a escala.


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
| Qué se hizo | Paso 4 hecho (9 oct 2026): el índice del sitemap y `post-sitemap.xml` abiertos en el navegador. Pasos 5 a 7 pendientes: descarga con código, lectura de los mapas hijos y tabla `urls`. |
| Resultado | Índice (`http://viviendoporelmundo.com/sitemap_index.xml`): generado por Yoast SEO, con **2 mapas hijos**, `post-sitemap.xml` (entradas) y `page-sitemap.xml` (páginas), ambos en `https://www.…`. `post-sitemap.xml`: **244 URLs** según su propio encabezado (el paso 6 las recontará con código), con fechas de modificación desde 2015-10-26 hasta 2026-06-20, ordenadas de la más antigua a la más reciente, y una columna con el número de imágenes por página (de 1 a 264). La fecha del índice (2026-06-20 04:46) coincide exactamente con la de la última entrada del mapa. `page-sitemap.xml`: todavía sin contar (lo hará el paso 6). No hay mapa de categorías ni de etiquetas. |
| Costo (tiempo, peticiones, tokens) | Paso 4: tres visitas con el navegador (índice y mapas), sin programa. 0 tokens. |
| Qué falló o sorprendió | Tres cosas. 1) No hay mapa de categorías: el sitemap no es el plano completo. 2) Ninguna dirección tiene carpeta (`/blog/…`): todas cuelgan de la raíz, así que las reglas de la guía (`PATRONES_UTILES`) descartarían todas las páginas. 3) `Last Mod.` no es la fecha de publicación: hay bloques de decenas de entradas con la misma fecha de edición (21 al 26 de julio de 2021) y otro de 9 entradas del 20 de junio de 2026. |
| Conclusión | Pendiente. |


### Etapa 3. Filtrado

| Bloque | Registro |
|---|---|
| Qué se hizo | Paso 8: reglas fijas de URL. |
| Resultado | Pendiente. |
| Costo (tiempo, peticiones, tokens) | Pendiente. |
| Qué falló o sorprendió | Pendiente. |
| Conclusión | Pendiente. |


### Etapa 4. Scraping

| Bloque | Registro |
|---|---|
| Qué se hizo | Pasos 9, 10 y 12: muestra de 3 y luego 10 páginas, con 10 s de espera. |
| Resultado | Pendiente. |
| Costo (tiempo, peticiones, tokens) | Pendiente. |
| Qué falló o sorprendió | Pendiente. |
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
| Muestra de la etapa 4 | 3 páginas y luego 10. |
| Contenido de terceros | El informe lleva cifras y citas cortas, nunca el texto completo de los artículos. |


## Versiones de este archivo

| Versión | Fecha | Archivo | Qué contiene |
|---|---|---|---|
| v1 | 9 de octubre de 2026 | `analisis-resultados-mapeo-scraping-manual_2026-10-09_v1.html` | Plan: modo de trabajo, checklist de pasos, esqueleto, métricas y resultados por etapa, todos pendientes. |
| v2 | 9 de octubre de 2026 | `analisis-resultados-mapeo-scraping-manual_2026-10-09_v2.html` | Cierra la etapa 0 (entorno) y la etapa 1 (permisos): robots.txt verificado y leído con código, términos de uso revisados, sección CONCEPTOS con los puntos 1 a 13. |
| v3 | 9 de octubre de 2026 | `analisis-resultados-mapeo-scraping-manual_2026-10-09_v3.html` | Agrega la tercera forma (DevTools) al contexto: tabla de las tres formas y métricas compartidas por tres informes. |

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

**Anatomía de una dirección.** En `.../que-ver-en-budapest-2-dias-a-pie/`, la parte final se llama *slug*: es el nombre de la página dentro de la dirección, casi siempre un resumen del tema con palabras separadas por guiones. Aquí todas las direcciones cuelgan directamente de la raíz: no hay carpetas como `/blog/` ni `/pais/`.

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

> **Aviso para el filtrado** Las reglas de la guía (`PATRONES_UTILES = ("/blog/", "/noticias/", "/articulo/")`) buscan carpetas dentro de la dirección. En este sitio ninguna dirección las tiene, así que esas reglas descartarían todo. Es un ejemplo claro de por qué las reglas fijas no sirven igual en todos los sitios, y de lo que un agente hará distinto: leer el nombre y decidir con criterio.

**La columna Images** va de 1 a 264. Sirve de pista del tamaño de una guía: una entrada con 264 imágenes es una guía muy larga. Recuerda que las fotos tienen derechos de autor: se cuentan, no se descargan.

