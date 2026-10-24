# Implementación editorial

Objetivo: ejecutar la estrategia aprobada con un centro de guías, contenido inicial completo y publicación por calendario en GitHub Pages.
Especificación: `docs/estrategia-editorial-2026-10-23.md`.
Tecnología: HTML/CSS estáticos, Python estándar y GitHub Actions. Sin CMS ni dependencias de producción.

- [x] Preparar un catálogo editorial con las doce guías, sus fechas, fuentes y estado. PHP conserva su URL publicada; las demás solo se generan cuando estén listas y llegue su fecha.
- [x] Crear el formato común, índice, breadcrumbs, relacionadas, CTA, impresión y sitemap/robots. Integrarlo desde la portada.
- [x] Redactar las guías iniciales de elección y costo total; preparar las restantes con fuentes y listas operativas. El contenido legal necesita revisión especializada antes de publicarse.
- [x] Añadir una publicación programada desde GitHub Actions y un comando local equivalente. Ningún artículo se publica por mera existencia de una fecha: exige contenido listo y fuentes revisadas cerca de su salida.
- [x] Probar selección por fecha, bloqueo de revisión caducada, privacidad del borrador, enlaces, metadatos y render móvil/escritorio.
- [ ] Documentar el uso, revisar el diff, guardar solo archivos de esta tarea y publicar si la conexión lo permite.

Decisiones: la estrategia y calendario son documentos internos locales, no se incluyen en los archivos desplegados. No se instala analítica sin una configuración real. La distribución en redes depende de verificar primero la URL pública. El índice muestra solo contenido disponible y no enlaces vacíos a futuras guías.

Riesgos: escribir al mismo `index.html` desde tareas concurrentes; publicar precios desactualizados; convertir una fecha en aprobación jurídica; desplegar borradores por el alojamiento desde raíz; compartir datos de clientes en ejemplos. Las pruebas cubren fecha, revisión, rutas publicadas y referencias internas. Se conserva `gf.css` ajeno al cambio.

Verificación: ocho pruebas unitarias pasan; simulación actual y del 12-11 pasan enlaces internos y metadatos. Navegador a 320, 390, 768, 1024 y 1366 px sin desbordamiento; calculadora validada a 12/36 meses, cero y negativo. Revisión independiente detectó y se corrigió pérdida de historial y publicación de apoyos sin revisión vigente; revisión posterior aprobó ambas correcciones.

Limitación externa: git/gh no pueden conectar con GitHub desde este entorno. El despliegue y cambio de origen de Pages requieren ejecución desde una conexión con acceso. No se declara publicación remota ni se inventa una línea base de medición.
