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

## ⚠️ La marca y el sitio no usan la misma paleta

Hoy conviven dos identidades de color, y conviene resolverlo antes de imprimir nada:

| Pieza | Paleta |
|---|---|
| Kit de logo (`icono-*.svg`, `avatar-instagram.svg`) y **el favicon** | azul `#2F6BFF` + teal `#2CE4C4` sobre tinta azulada `#0B1220` |
| **El sitio** (v5) y la marca del header | tabaco cálido `#100E0B`, hueso `#E4DCCB`, bronce `#C9AF82` |

No es un descuido del sitio: la v5 se alejó del azul-teal a propósito, porque el gris
azulado es el tono más visto en la categoría. Pero el resultado es que **la pestaña del
navegador muestra un ícono azul-teal sobre una página tabaco**, y este README documentaba
solo la paleta azul.

La marca del header no usa los SVG: son tres barras dibujadas con CSS en color hueso.

**Queda por decidir:** llevar el kit de logo al tabaco, o mantener el azul-teal como marca y
aceptar el contraste. Mientras no se decida, el favicon es la pieza más visible del desajuste.

### Paletas, para referencia

**Sitio (v5 tabaco)** — están como variables CSS en `:root`:

| Nombre | HEX | Uso |
|---|---|---|
| Fondo | `#100E0B` | Negro cálido, nunca `#000` |
| Superficie | `#181510` / `#211C15` | Tarjetas y bloques |
| Tinta | `#EFEBE3` | Texto principal |
| Gris | `#9A9489` | Texto secundario |
| Hueso | `#E4DCCB` | Acento, botón principal, marca |
| Bronce | `#C9AF82` | Solo las cifras del caso |

**Kit de logo (azul-teal)**

| Nombre | HEX |
|---|---|
| Tinta | `#0B1220` |
| Azul (acento) | `#2F6BFF` |
| Azul suave | `#5B8CFF` |
| Teal | `#2CE4C4` |
| Neutro claro | `#EAF0FA` |
| Apagado | `#8A97AD` |

Variantes para fondo claro: azul `#245BE0`, teal `#12B79B`.

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
