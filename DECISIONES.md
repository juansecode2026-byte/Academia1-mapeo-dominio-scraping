# Decisiones

Registro de lo que se decidió y por qué, para no volver a discutirlo. Antes de proponer un cambio de stack, de estructura o de alcance, revisar si ya está aquí. Para cambiar una decisión, se agrega una entrada nueva que la reemplace; la anterior no se borra.

Estados: **Aceptada** · **Rechazada** · **Aplazada** (con condición de activación).

---

## D1 · Sacar el pipeline de blog con agentes de este proyecto

- **Fecha:** 8 oct 2026 · **Estado:** Aceptada
- **Contexto:** se trajo `pipeline-blog-agentes_v1.1_2026-10-08.html` a la documentación.
- **Opciones:** dejarlo aquí · sacarlo a otro proyecto.
- **Decisión:** sacarlo. El original y su `.md` quedaron en Descargas.
- **Motivo:** solo encaja en un 30–35 % (la parte de investigar y curar fuentes). El resto (redacción, imágenes, QA, publicación en WordPress, costos) es un sistema de producción de contenido, no aprender a mapear y extraer de un dominio.

## D2 · SQLite como almacenamiento, no Supabase

- **Fecha:** 8 oct 2026 · **Estado:** Aceptada
- **Contexto:** la guía 2 propone Supabase para guardar las fichas.
- **Opciones:** archivos JSON/CSV · SQLite local · Supabase.
- **Decisión:** una sola base SQLite en `datos/scraping.db` para todos los ejercicios de este proyecto, separada por la columna `sitio`. La guía 1 usa JSON/CSV hasta el paso 7; desde el mapeo del sitemap se guarda en SQLite.
- **Motivo:** cubre lo que hace falta (no duplicar, acumular entre corridas, estados de revisión, consultas) sin instalar nada, sin claves y sin costo. El SQL se pasa casi tal cual a Supabase si algún día hace falta.
- **Revisar si:** algo tiene que correr solo en un servidor, varias personas usan los datos o una aplicación web los consulta.

## D3 · Los datos extraídos no se suben a git

- **Fecha:** 8 oct 2026 · **Estado:** Aceptada
- **Decisión:** `datos/`, `*.db`, `resultados.json`, `resultados.csv` y `fichas_agente.json` están en `.gitignore`.
- **Motivo:** son contenido de terceros; el repositorio guarda el código y la documentación, no lo extraído.

## D4 · Nombres en español

- **Fecha:** 8 oct 2026 · **Estado:** Aceptada
- **Decisión:** funciones, variables, columnas y archivos de documentación en español.
- **Motivo:** las dos guías ya están escritas así; mezclar idiomas dificulta seguirlas.

## D5 · `ruff` para formato y lint

- **Fecha:** 8 oct 2026 · **Estado:** Aceptada (se activa con el primer script)
- **Decisión:** `ruff format .` y `ruff check .` antes de cada commit con código, configurado en `pyproject.toml`.
- **Motivo:** una regla verificable ("pasa ruff") en lugar de una vaga ("código limpio"); una sola herramienta para formato y lint.

## D6 · Guía 2: empezar por la opción A

- **Fecha:** 8 oct 2026 · **Estado:** Aceptada
- **Opciones:** A, pipeline con IA en dos puntos (selector y analista) · B, agente autónomo con herramientas.
- **Decisión:** construir primero la A (`pipeline.py`).
- **Motivo:** costo bajo y predecible, fácil de depurar; es lo que recomienda la guía. La B se prueba después con el mismo tema para comparar resultado y costo.

## D7 · Firecrawl o Tavily

- **Fecha:** 8 oct 2026 · **Estado:** Aplazada
- **Decisión:** por ahora se usa el código propio de la guía 1 para mapear y leer.
- **Revisar si:** el sitio carga contenido con JavaScript que `trafilatura` no lee, o se trabaja con muchos dominios a la vez.

## D8 · Archivos de documentación del proyecto

- **Fecha:** 8 oct 2026 · **Estado:** Aceptada
- **Decisión:** se crean `DECISIONES.md` y `FUENTES.md` en la raíz. Lo propio de cada sitio sale del CLAUDE.md y va a `FUENTES.md`. Se referencian sin `@` desde el CLAUDE.md para que no se carguen en cada sesión.
- **Rechazados:** `ARCHITECTURE.md` (no hay código; basta el mapa del CLAUDE.md), `ROADMAP.md`/`TODO.md` (duplicaría el estado), `CHANGELOG.md` (no hay entregas; basta git), `AGENTS.md` (solo se usa Claude), `.claude/skills/` (no hay procedimientos largos).
- **Aplazados:**
  - `PROMPTS.md`: cuando se escriba el primer prompt de la guía 2.
  - `TESTING.md`: cuando exista `scraper.py`.
  - `README.md`: cuando otra persona vaya a usar el proyecto.

## D9 · Comando `/traer-documentacion`

- **Fecha:** 8 oct 2026 · **Estado:** Aplazada
- **Contexto:** dos veces se repitió el mismo proceso: buscar el archivo en Descargas, compararlo con la documentación, reemplazar el `.html` y generar o actualizar el `.md`.
- **Revisar si:** el proceso se repite una tercera vez; entonces se evalúa convertirlo en `.claude/commands/traer-documentacion.md`.
