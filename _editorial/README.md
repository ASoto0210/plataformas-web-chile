# Operación editorial

Fuentes de los artículos, no archivos para servir directamente. `catalog.json` gobierna fechas y estado; `scripts/build_editorial.py` genera la versión pública.

## Qué queda listo

- Doce guías: PHP existente, dos guías listas para las fechas del 2 y 9 de noviembre, ocho borradores editoriales y una pieza pendiente de revisión jurídica.
- Doce apoyos con fecha propia. No se incorporan antes del día programado.
- Índice, diseño compartido, fuentes, llamadas a contacto, impresión, calculadora de costos y mapa del sitio.
- Una revisión diaria del calendario en GitHub Actions. No programa redes ni declara revisiones de fuentes que no se hayan hecho.

## Publicar localmente

```powershell
python -B -m unittest discover -s tests -v
python -B scripts/build_editorial.py --output _site
python -B scripts/check_public_site.py _site
python -m http.server 8766 --bind 127.0.0.1 --directory _site
```

El destino debe estar vacío: el generador nunca borra carpetas. Para repetir una prueba usa otro destino, por ejemplo `_site-prueba2`. Para simular una fecha utiliza `--date 2026-11-12`; esa opción no debe ponerse en producción.

## Revisión y estado

- `draft`: contenido preparado que aún necesita revisión editorial.
- `legal-review`: requiere revisión jurídica antes de habilitarse.
- `ready`: contenido revisado; puede publicarse cuando llegue `publish_on` y la comprobación no haya caducado.
- `reviewed_on`: fecha real de comprobación de las fuentes, no la fecha de ejecutar el script.
- `review_days`: plazo interno para revisar el contenido. No ampliar para saltarse una comprobación.
- `published_on`: reservado para contenido que ya fue publicado. No usarlo para forzar una primera publicación.

Antes de pasar a `ready`, comprueba enlaces, afirmaciones, procedimiento, ortografía y contacto. Registra revisión en el commit. Actualiza `reviewed_on` solo después de hacerla. Para la guía de datos, documenta también la revisión especializada.

No se debe publicar una guía nueva con fuentes cuya revisión haya vencido. Una guía previamente publicada conserva su URL y muestra un aviso de revisión pendiente; se conserva el registro del último despliegue en `/guias/publicadas.json`. Para reconstruir localmente ese mismo conjunto, descarga ese registro y pásalo con `--previous ruta-al-registro.json`.

## GitHub Pages

El workflow `.github/workflows/editorial.yml` genera y despliega únicamente `_site`. En el repositorio, **Settings → Pages → Build and deployment → Source** debe ser **GitHub Actions**. El dominio sigue siendo `plataformasweb.cl`; no cambies DNS, CNAME ni desactives HTTPS.

El workflow corre con cada push a main, manualmente y a diario a las 13:15 UTC. En verano de Chile equivale a 10:15; al cambiar el horario puede variar una hora. La elegibilidad usa fecha de America/Santiago. GitHub puede retrasar una ejecución programada: no se ofrece puntualidad contractual.

La consulta del registro previo falla de forma segura si el sitio no responde: no se despliega un índice incompleto que retire URLs anteriores. Un 404 permite la primera puesta en marcha. Un 200 inválido detiene el proceso. La interfaz de Actions muestra la lista de artículos retenidos.

Mientras Pages use la rama, el índice y la guía PHP incluidos en raíz sirven como respaldo estático. El calendario automático y las guías futuras requieren el workflow. `_config.yml` excluye fuentes editoriales, scripts y pruebas de Jekyll. El despliegue por Actions usa además una lista explícita de carpetas públicas.

## Medición y distribución

No hay una cuenta de analítica del sitio configurada en esta implementación y no se envían valores de la calculadora. La línea base debe levantarse con acceso real a Search Console, analítica y registro comercial.

Anota semanalmente: páginas indexadas, consultas relevantes, clics de contacto, conversaciones efectivas, consultas calificadas, propuestas y horas editoriales. No confundas un clic en correo con una consulta recibida. Consulta `medicion.csv` para el registro vacío.

Facebook/Instagram, YouTube y TikTok se programan solo tras comprobar la URL publicada y la identidad de la cuenta. Los textos de apoyo son la base; la automatización actual publica en el sitio, no en las redes.

La estrategia y el calendario CSV entregados al usuario permanecen como documentos locales; no se incluyen en el despliegue público.
