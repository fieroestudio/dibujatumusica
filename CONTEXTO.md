# Dibuja tu música: contexto del proyecto

Lee este documento al empezar una conversación nueva en el proyecto. Resume lo decidido y el estado actual.

**Dónde está cada cosa:**
- **Repositorio (referencia):** https://github.com/fieroestudio/dibujatumusica, rama `main`. Un push a `main` publica en GitHub Pages.
- **Carpeta local (PC "msi"):** `C:\Users\UNPARDEDOS\Desktop\CLAUDE\APP DIBUJA TU MUSICA`. Tiene además la foto original del título, que no se sube al repositorio.
- **Proyecto de claude.ai:** `claude/CONTEXTO.md` y `claude/codigo/index.html`. Es una copia para leer desde el móvil.
- **Artefacto antiguo en claude.ai** (slug `a65713c1-…`): fue el prototipo, se deja de usar y se le quitará el acceso público.

## Qué es

Web app de una sola página donde se dibuja con colores y el dibujo suena como música. La idea sale de *play_music_theory* (Tala Schlossberg). Es una versión propia, pensada para niños de 6 años en adelante y que también puedan usar adultos.

- **Web:** GitHub Pages del repositorio `fieroestudio/dibujatumusica` (ver arriba). Quien tiene el enlace ve cada versión nueva al recargar, así que no se publican versiones rotas.
- **Dispositivos de Adrian:** Android y PC, no hay iOS.
- **Versión actual:** v13 (12-11-2026): icono y manifiesto para guardarla como app. v12 trajo 10 colores, tres juegos de sonidos, compartir, descargas y pantalla completa. Nadie más tiene el enlace todavía.

## Cómo funciona

- **El lienzo es cuadrado** en cualquier orientación. Coordenadas guardadas en relativo (0..1).
- **Tiempo en horizontal:** 32 pasos por bucle, cada paso una corchea.
- **Altura en vertical:** 15 filas. Arriba agudo, abajo grave. La escala depende del juego de sonidos (ver abajo). La línea continua de la cuadrícula marca la nota base de cada octava.
- **Cada cruce del cabezal con un trazo es una nota.** Un óvalo da dos notas, arriba y abajo. Se marca con un punto negro y un aro.
- **Un cruce es cada pasada del trazo por una columna,** en el orden en que se dibujó. Corregido en v12: antes, dos líneas paralelas en notas vecinas dibujadas sin levantar el dedo se juntaban en una nota a media altura. El temblor dentro de una pasada sigue contando como una nota.
- **Velocidades (BPM):** tortuga 80, normal 120, conejo 160.
- **Audio:** Web Audio sintetizado, sin muestras grabadas. La cadena de salida es master 0.42, compresor suave, ganancia y saturación tanh. Una nota repetida del mismo color corta la anterior para que no se acumulen colas. Cada sonido decide cuánta reverb lleva (Videojuego seco, Espacio con mucha).
- **Nivel medido (v12):** con un dibujo con los 10 colores, el pico es 0,81 en Clásico, 0,78 en Videojuego y 0,74 en Espacio, sin recortes. El volumen de cada sonido nuevo se igualó midiendo, no escuchando. `window.__renderLoop()` genera un bucle sin altavoces y devuelve pico, recortes y número de notas; con `__renderLoop(true)` devuelve las muestras.

### Colores y juegos de sonidos

El número de cada color es el que se guarda en el código: no reordenar. 0-4 van a pulsos (una nota en cada cruce); 5-9 son continuos. **Cada color se comporta igual en todos los juegos**, a petición de Adrian, para que el niño no tenga que reaprender; solo cambia el sonido. Todos los juegos tienen los 10 colores. En la interfaz los de pulsos van juntos (fila de arriba en vertical, columna izquierda en horizontal) y los continuos juntos, sin marca que los separe.

| # | Color | Tipo | Clásico | Videojuego | Espacio |
|---|---|---|---|---|---|
| 0 | #efa52f ámbar | Pulsos | Campanita (kalimba) | Moneda | Estrella que titila |
| 1 | #4a6fd6 azul | Pulsos | Piano suave | Bip | Púlsar (campana de cristal FM) |
| 2 | #2f9a72 verde | Percusión | Tambor | Batería 8 bits | Meteoritos |
| 3 | #4fb3d9 celeste | Pulsos | Gotas | Salto | Burbujas |
| 4 | #a77b54 marrón | Pulsos | Palmas | Chasquido | Radar (pip con eco) |
| 5 | #de5b3c rojo | Continuo | Trompeta (fliscorno) | Láser | Cometa |
| 6 | #e07bb5 rosa | Continuo, grave | Guitarra/bajo | Bajo 8 bits | Planeta (zumbido grave) |
| 7 | #7d63d1 morado | Continuo, agudo | Flauta | Silbato | Ovni (sirena) |
| 8 | #93c13e lima | Continuo | Órgano | Nave | Nebulosa (colchón) |
| 9 | #5f7186 gris azulado | Continuo | Acordeón | Power-up (arpegio) | Viento solar (la altura cambia el brillo) |

- **Percusión (color 2):** en los tres juegos, abajo grave, en medio seca y arriba brillante.
- **Escalas:** Clásico, pentatónica de Do; Videojuego, pentatónica menor de Do; Espacio, tonos enteros. Con cualquiera de ellas, toques donde toques suena bien.
- **Iconos:** Clásico y Espacio llevan iconos de línea. Videojuego usa botones cuadrados sin icono, a propósito, por abstracto. Órgano se dibuja como tubos y acordeón como fuelle, para no confundirlos con el piano y la flauta.
- **Botón de juego:** junto a la velocidad; cada toque pasa al siguiente (nota, mando, cohete). El juego se guarda con el dibujo.
- **Colores nuevos:** lima y gris azulado, elegidos por Adrian. Si el gris azulado confunde, la alternativa es subir la trompeta a un rojo puro y añadir un naranja (con la campanita algo más amarilla).

**Sostenido y desliza:** un trazo es una sola nota que se desliza de nota en nota de la escala (setTargetAtTime 0,035). Si la línea salta más de 3 notas, empieza una frase nueva.

## Interfaz

- **Estilo plano, blanco y sobrio, a petición de Adrian.** Se descartó el "juguete de plástico" petróleo y amarillo.
- **Iconos de línea SVG en todo,** sin emojis.
- **Grupo sonido:** los 10 colores (5×2 en vertical, 2×5 en horizontal), la pastilla de velocidad y el botón de juego de sonidos. **Grupo herramientas:** play, goma, deshacer, papelera, Compartir y descargar, y Mis dibujos.
- **Vertical:** título, lienzo, sonido y herramientas. **Horizontal:** sonido, lienzo y herramientas. En el móvil en horizontal, el título va dentro del lienzo vacío.
- **Pantalla completa:** botón pequeño arriba a la izquierda. No aparece donde el navegador no lo permite (iPhone) ni cuando se abre como app instalada.
- **Icono y app instalable (v13):** icono = un trazo ámbar con el cabezal, el punto negro y el aro de una nota que suena (opción elegida por Adrian para probar; se puede cambiar). Archivos: `icons/icon.svg` (pestaña), `icon-180.png` (iPhone/iPad), `icon-192.png` y `icon-512.png` (Android) e `icon-maskable-512.png` (Android recorta la forma), y `manifest.webmanifest` con nombre corto "Dibuja música" y apertura a pantalla completa. Los PNG se generaron desde el SVG con Chrome headless.
- **Título:** "DIBUJA TU MÚSICA" escrito a mano por un niño (foto del 11-11-2026), vectorizado letra a letra con OpenCV en `TITLE_SVG`. Cada letra va en un color de instrumento. Se mantuvieron las "I" en forma de bandera; solo se ajustó el espacio entre letras.
- **Cuadrícula:** líneas por cada nota y columnas cada 2 pasos. No hacerla más fina que las notas reales, porque engañaría.
- **Goma:** borra con el dedo y parte los trazos. Deshacer funciona por instantáneas (máximo 40) y cubre trazo, borrado y papelera.
- **Papelera y "×" de la galería:** piden un segundo toque en 2 s.

## Guardado

- **Mis dibujos** se guarda en el `localStorage` del navegador: `dibuja-musica-lib` (lista `{id, code, t}`) y `dibuja-musica-cur`. Cada dibujo se guarda solo, los vacíos no se guardan y las miniaturas se generan desde el código.
- **Código de dibujo `v2`:** `v2` + velocidad (a/b/c) + juego de sonidos (a/b/c) + trazos separados por `.` (dígito del color 0-9 + coordenadas en base36, 2 caracteres por eje). Abrir un código lo añade como dibujo nuevo. Los `v1` del prototipo se siguen abriendo (con su color traducido al orden nuevo y sonido Clásico).
- **Limitación:** los dibujos no pasan de un dispositivo a otro ni sobreviven a borrar los datos del navegador. Al mudarse a otro dominio no se trasladan.
- **Se quitó la migración del prototipo** (`dibuja-musica`): en otro dominio no había nada que migrar.

## Compartir y descargar (v12)

Un botón abre un panel con cuatro opciones. Los archivos se generan primero y luego hay botones de Guardar y, si el móvil lo permite, Compartir (el menú de Android, sin tener que buscar el archivo).

- **Enlace:** `…#d=<código>`. En Android abre el menú de compartir; en el PC lo copia. Al abrir un enlace se quita el `#d=` de la barra para que al recargar no se duplique el dibujo.
- **Imagen:** PNG 1080×1200, con el dibujo arriba y el título pequeño abajo.
- **Vídeo:** MP4 1080×1200, misma lámina, dos vueltas grabadas en tiempo real (unos 16 s a velocidad normal) con brillos, puntos y cabezal. Mientras graba, la app queda bloqueada con un aviso rojo arriba. Formato preferido H.264 + AAC; si el navegador no lo tiene, cae a H.264 + Opus, otro MP4 o WebM (y lo avisa). **No comprobado en el Android de Adrian:** en el Chrome de Linux de las pruebas sale VP9 + Opus dentro de MP4, que puede no abrirse en WhatsApp o en iPhone.
- **Sonido:** MP3 160 kbps de dos vueltas, generado sin altavoces con `lib/lame.min.js` (lamejs 1.2.1, LGPL, sin modificar). Es la única librería, aprobada por Adrian, y se carga solo al pulsar Sonido.

## Pendiente e ideas (por prioridad aproximada)

1. **Que Adrian escuche los 30 sonidos** y diga cuáles cambiar. Los de Videojuego y Espacio, el órgano y el acordeón son nuevos y nadie los ha escuchado. La trompeta sigue en revisión (alternativa: una octava más baja, tipo trombón).
2. **Probar el vídeo en el Android:** comprobar que el MP4 se abre en la galería y en WhatsApp.
3. **Probar en un iPad o iPhone** antes de mandárselo a alguien que use Apple. Ni Adrian ni Claude pueden probarlo ahora.
4. **Páginas de una misma canción que suenan seguidas** (como los botones 1-2-3 del original). Esperar a ver si alguien lo pide.
5. **Icono definitivo:** Adrian pasará un dibujo hecho por un niño para sustituir el icono provisional (vectorizarlo como el título y regenerar todos los PNG).
6. **Que funcione sin conexión** (service worker): Adrian quiere añadirlo cuando terminen los cambios actuales. Hasta entonces no, porque haría que cada versión nueva tardara una recarga más en verse.
7. **Para profesores, solo si alguien lo pide:** nombres de notas en la cuadrícula, elegir escala, pregunta y respuesta, juegos con reglas. Adrian prefiere que siga siendo un juego, no una app didáctica.

## Decisiones descartadas y por qué

- **taste-skill (Leonxlnx):** está pensada para webs de empresa y no encaja con un juguete.
- **Forzar horizontal 16:9:** en el móvil obligaba a girarlo. Se pasó a lienzo cuadrado.
- **Violín sintetizado:** sonaba mal y no gustó. Se cambió por la flauta.
- **Deslizar el piano:** un piano real no desliza.
- **Tono continuo libre** (tipo theremín): desafina. El deslizamiento va siempre por notas de la escala.
- **Sonidos realistas con grabaciones:** obligaban a usar muestras en archivos aparte y licencias. Se eligieron sonidos abstractos sintetizados.
- **Mezclar juegos de sonidos en un mismo dibujo:** exigiría 20 o 30 colores; para un niño, cada color tiene que significar siempre lo mismo.
- **Que un color cambie de comportamiento según el juego:** se valoró y Adrian prefirió que se comporte igual en todos.
- **JPG:** basta con PNG.
- **Nombres de notas en la cuadrícula:** de momento no.

## Cómo trabajar

- **Ediciones quirúrgicas,** no reescrituras completas.
- **Problemas primero, sin halagos.**
- **Antes de entregar un archivo, preguntar dónde guardarlo.**
- **Carpeta local:** se conecta a cada conversación, no al proyecto. Pedir acceso al empezar si hay que actualizarla.
- **Probar con Playwright y Chrome headless** en vertical 412×860, horizontal 915×412 y tablet 1280×800, y medir el audio con `__renderLoop` en los tres juegos. No se puede escuchar: avisar de ello. Las descargas se prueban sirviendo la carpeta por http (con `file://` el enlace no se limpia).
