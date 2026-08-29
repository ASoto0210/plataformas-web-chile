# Plataformas Web Chile

Sitio propio de la agencia y el kit de marca. Publicado con **GitHub Pages** desde la rama
`main`.

- En vivo hoy: <https://asoto0210.github.io/plataformas-web-chile/>
- Dominio propio: **plataformasweb.cl** — inscrito el 28-08-2026, **todavía sin delegación**
  (faltan los nameservers en NIC). Ver *Cambio de dominio* más abajo.

## El sitio

`index.html` es todo el sitio: una sola página, sin build ni dependencias. Se abre
directamente o con `python -m http.server` desde la raíz.

| Sección | id |
|---|---|
| Portada | — |
| Servicios | `#servicios` |
| Trabajos (caso STOM) | `#trabajos` |
| Cómo trabajamos | `#proceso` |
| Contacto | `#contacto` |

**Contacto:** WhatsApp +56 9 9991 8241 (acción principal), correo
`plataformasweb.chile@gmail.com`, Instagram [@plataformasweb.chile](https://instagram.com/plataformasweb.chile).

### Decisiones que conviene no deshacer sin querer

- **Las fuentes se sirven desde este mismo sitio** (`fuentes/`, Archivo). Con Google Fonts,
  basta una extensión de privacidad o una red que bloquee el dominio para que la página
  pierda su tipografía. Las dos variantes del titular van precargadas.
- **Los rótulos de sección son `<h2>` con clase `.rotulo`**, no párrafos. La clase fija peso
  400 e interlineado 1.55 justamente para neutralizar la regla `h2` y que se vean igual. Si
  se vuelven `<p>`, el índice de encabezados salta de `h1` a `h3` y las secciones dejan de
  existir para un lector de pantalla.
- **`v5-oscuro.html`, `v6-bento.html` y `v7-suizo.html`** son las tres direcciones que se
  compararon; ganó la v5 y está fusionada en `index.html`. Llevan `noindex`, así que no
  compiten en Google. Se conservan como referencia.

## Paleta

**Una sola, la del sitio.** El 29-08-2026 se llevó todo el kit de marca al tabaco: hasta ese
día el logo y el favicon eran azul-teal mientras el sitio era tabaco, así que la pestaña del
navegador mostraba un ícono azul sobre una página cálida.

| Nombre | HEX | Uso |
|---|---|---|
| Fondo | `#100E0B` | Negro cálido, nunca `#000` |
| Superficie | `#181510` / `#211C15` | Tarjetas y bloques |
| Tinta | `#EFEBE3` | Texto principal |
| Gris | `#9A9489` | Texto secundario |
| Hueso | `#E4DCCB` | Acento, botón principal, marca |
| Bronce | `#C9AF82` | Cifras del caso y capa base del símbolo |
| Intermedio | `#D6C5A6` | Capa media del símbolo |

En el sitio están como variables CSS en `:root`.

**Las capas del símbolo ascienden del bronce al hueso** — la que apoya es la más terrosa, la
que llega arriba es la más luminosa. Es el mismo gesto que cuenta la marca (*una plataforma
que te eleva*), ahora en la familia cálida.

**Sobre fondo claro** el hueso desaparece, así que `logo-horizontal-claro.svg` usa tonos
cálidos oscuros: `#6B5330`, `#8C7147` y `#B08F5B`.

⚠️ **Al tamaño de favicon (16px) las tres capas casi se funden**, porque ahora son tonos
vecinos de la misma familia; antes el azul→teal separaba más. Se distingue la silueta y es
consistente con la marca del header, que también es monocroma. Si alguna vez molesta, la
salida es abrir el espacio entre capas, no volver a meter un color frío.

## Kit de marca

Dirección elegida: **Capas** — tres planos que ascienden, una plataforma que te eleva.

| Archivo | Uso |
|---|---|
| `icono-color.svg` | Símbolo a color. Uso general. |
| `icono-blanco.svg` | Símbolo blanco, fondos oscuros. |
| `icono-negro.svg` | Símbolo tinta, fondos claros. |
| `logo-horizontal-oscuro.svg` | Ícono + texto, fondo oscuro. |
| `logo-horizontal-claro.svg` | Ícono + texto, fondo claro. |
| `logo-vertical-oscuro.svg` | Ícono arriba, texto abajo. |
| `avatar-instagram.svg` | Avatar 320×320. IG / FB / Google. |
| `favicon.svg` | Ícono de la pestaña. |

**Pendiente del kit:** el texto de los `logo-horizontal-*` y `logo-vertical-*` usa fuentes del
sistema (Segoe UI / Consolas). Para imprenta conviene convertirlo a trazos, si no se ve
distinto en cada equipo. El símbolo ya es geométrico y no depende de fuentes.

## ⏸ Pendiente con fecha: el lunes 31-08-2026 a las 15:00

El caso de STOM tiene **el enlace a `stom.cl` en pausa**: hasta esa hora el dominio sigue
mostrando el WordPress viejo, que es justo lo que el titular de esta página promete
reemplazar. En `index.html`, en el `caso-pie`, hay un comentario con la línea exacta que hay
que restaurar apenas se haga el corte.

No se puso una clave de acceso porque **en GitHub Pages no existe**: es hosting estático y el
HTML se entrega completo a quien lo pida, así que cualquier clave en JavaScript es decorativa.
Y apagar Pages tampoco servía: **el pie de `stom.cl` enlaza a este sitio** (`Footer.jsx`), así
que dejarlo caído rompería el crédito en el sitio del cliente.

## Cambio de dominio

Cuando `plataformasweb.cl` tenga delegación:

```bash
python cambiar-dominio.py            # solo revisa
python cambiar-dominio.py --aplicar  # cambia las 8 referencias y crea el CNAME
```

Después, en GitHub: **Settings → Pages → Custom domain**, esperar el certificado y marcar
*Enforce HTTPS*.

**El script comprueba el DNS antes de tocar nada, y no es opcional.** El archivo `CNAME` no se
puede crear antes de que el dominio resuelva: apenas existe, GitHub redirige la URL de
github.io al dominio nuevo, y si ese no apunta a ninguna parte el sitio queda inalcanzable —
incluido el enlace del crédito en el pie de stom.cl. El script también detecta el caso de que
el dominio resuelva pero con el proxy naranja de Cloudflare encendido, que impide a GitHub
emitir el certificado.

## Archivos de trabajo

`_shots/` son capturas de direcciones descartadas (v1 a v4) y `png/` quedó de una exportación
que falló. No los usa nada del sitio.
