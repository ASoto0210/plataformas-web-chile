# Chatbot multicanal — nota de producto

> Escrito el 2026-08-28, a partir de lo construido en el marketplace de STOM. Es una nota de
> decisión, no un plan de trabajo: sirve para retomar la idea sin volver a razonarla desde cero.

## De dónde sale

El bot de STOM (`repuestos-marketplace`) atiende consultas en **WhatsApp Cloud API** e
**Instagram DM** sobre el mismo catálogo, con memoria de conversación y captura de leads. No se
diseñó como producto: se construyó para un cliente. Pero resolvió los problemas que hacen difícil
un chatbot comercial de verdad, y esos no se resuelven leyendo documentación.

## Lo que ya está resuelto, y vale

La parte difícil de un bot multicanal **no es responder**: es convivir con las personas que
atienden el mismo canal.

| Pieza | Por qué cuesta |
|---|---|
| **Silencio por conversación** | Cuando una persona responde a mano, el bot se calla 4 h **con ese cliente**, no globalmente. Funciona en WhatsApp y en Instagram |
| **Detección de intervención humana** | Vía echoes (`smb_message_echoes` en WhatsApp, `is_echo` en Instagram). Cada canal los entrega distinto, y en Instagram el cliente es `recipient.id`, no `sender.id` |
| **Mensajes largos partidos** | Instagram parte las respuestas y cada trozo vuelve como su propio echo. Registrar solo el último hace que el bot se silencie a sí mismo |
| **Memoria por canal** | La clave es `ig:<IGSID>` o el teléfono, así el mismo cliente en dos canales no mezcla contextos |
| **Interruptor de pausa** | En base de datos, no en memoria: un bot pausado no puede volver a hablar solo con el próximo deploy |
| **Captura de leads** | Si el bot no puede resolver, deja el contacto registrado en vez de perder la consulta |

Cada una de esas líneas salió de un problema real en producción. Es el tipo de detalle que no
aparece en una demo y hunde una implementación a las dos semanas.

## Lo que falta para que sea un servicio

**Hoy es de un solo inquilino.** En `backend/whatsapp_api.py` las credenciales salen del entorno:

```
WHATSAPP_TOKEN · WHATSAPP_PHONE_NUMBER_ID · INSTAGRAM_TOKEN · INSTAGRAM_ACCOUNT_ID
```

Un despliegue = un negocio.

Convertirlo en servicio **no es rearquitectura, es refactor**: la lógica de negocio no cambia,
cambia de dónde salen las credenciales.

1. Mover esas cuatro variables a una tabla de inquilinos.
2. Enrutar el webhook entrante por `phone_number_id` — que ya viene en el payload — en vez de
   asumir que todo mensaje es del único negocio configurado.
3. Separar el catálogo y las respuestas por inquilino. Esto es lo que más trabajo tiene, porque
   hoy el bot sabe de repuestos diésel: hay vocabulario, matching por patente y categorías
   propias del rubro.

El punto 3 es el que decide si el producto es *"un bot para cualquier negocio"* o *"un bot para
tiendas de repuestos"*. Lo segundo es más chico, más defendible y más fácil de vender.

## La implicancia en Meta, que conviene no equivocar

Para operar el WhatsApp de **otros negocios** hay que ser **proveedor de tecnología**, y ese
modelo exige que **la app y la verificación del negocio vivan en el portfolio del proveedor**,
con los clientes colgando debajo.

De ahí se sigue algo práctico: la app de STOM (`2158235518085787`) está hoy en el portfolio
**STOM Repuestos** (`26545453645127525`), que es nuestro y no del cliente. Para el encargo de STOM
solo eso es indiferente. **Para el producto es lo correcto**, y moverla al portfolio del cliente
sería un camino que después habría que deshacer.

⚠️ Dos deudas de ese portfolio, si va a sostener un producto:

- **Un solo administrador.** Si se pierde esa cuenta, se pierde la app y con ella los dos bots.
  Meta lo advierte en el Centro de seguridad.
- **Autenticación en dos pasos sin activar.** Para un portfolio verificado que opera mensajería
  de negocios reales, no es opcional.

## Dos negocios distintos que conviene no confundir

**A. El bot como producto que se vende.** Necesita multi-tenancy, onboarding, facturación,
soporte y ser proveedor de tecnología ante Meta. Es un producto de software con todo lo que eso
arrastra.

**B. El bot como herramienta propia de prospección.** Ponerlo en la página de Plataformas Web para
capturar y calificar consultas de quienes buscan un sitio. **Esto se puede hacer con lo que ya
existe**, sin multi-tenancy: es un segundo despliegue con otro catálogo de respuestas.

B rinde antes, no compromete nada y además **es su propia demostración**: el prospecto que escribe
por WhatsApp y recibe una respuesta útil ya vio el producto funcionando.

## Orden propuesto

1. **Entregar STOM.** Corte del 31-08 y entrega comprometida para septiembre. Un producto a medio
   hacer con una entrega abierta es la forma clásica de que ninguna de las dos salga bien.
2. **Segundo inquilino gratis:** el marketplace de comida y congelados, que es propio. Es la prueba
   real de multi-tenancy sin SLA y sin que un error cueste un cliente. Si anda con dos negocios
   distintos, anda con diez.
3. **Opción B en la página de Plataformas Web**, como captación propia y demo viva.
4. **Recién ahí, ofrecerlo.** Con STOM como caso demostrable —"este negocio pasó de WordPress a
   esto y el bot atiende sus consultas"— que vende mucho más que una demo.

## Lo que no hay que subestimar

- **El soporte.** Un bot que atiende clientes de otro negocio es un servicio 24/7. El día que
  responde algo fuera de lugar, el que recibe el reclamo es el proveedor.
- **La verificación de cada cliente.** Cada negocio necesita su propia verificación ante Meta,
  con sus documentos y sus días de espera. Eso es fricción de onboarding, no un detalle técnico.
- **El costo por conversación** de la Cloud API, que hay que trasladar al precio o comerse.
