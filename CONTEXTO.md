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
- **Versión actual:** v11 (12-11-2026), primera subida a GitHub.

## Cómo funciona

- **El lienzo es cuadrado** en cualquier orientación. Coordenadas guardadas en relativo (0..1).
- **Tiempo en horizontal:** 32 pasos por bucle, cada paso una corchea.
- **Altura en vertical:** 15 filas en pentatónica de Do (Do Re Mi Sol La), 3 octavas. Arriba agudo, abajo grave.
- **Cada cruce del cabezal con un trazo es una nota.** Un óvalo da dos notas, arriba y abajo. Se marca con un punto negro y un aro.
- **Velocidades (BPM):** tortuga 80, normal 120, conejo 160.
- **Audio:** Web Audio sintetizado, sin librerías ni muestras. La cadena de salida es master 0.42, compresor suave, ganancia y saturación tanh. Una nota repetida del mismo instrumento corta la anterior para que no se acumulen colas.
- **Nivel medido:** con un dibujo cargado con los 8 instrumentos, el pico es 0,77 y no hay recorte. `window.__renderLoop()` genera el audio sin altavoces y devuelve pico, recortes y número de notas; con `__renderLoop(true)` devuelve las muestras.

### Instrumentos (el orden importa: el código guardado usa el índice)

| # | Instrumento | Color | Tipo |
|---|---|---|---|
| 0 | Campanita (kalimba) | #efa52f | Repite en cada cruce |
| 1 | Piano suave | #4a6fd6 | Repite en cada cruce |
| 2 | Trompeta (tipo fliscorno) | #de5b3c | Sostenido, desliza |
| 3 | Guitarra/bajo (una octava baja) | #e07bb5 | Sostenido, desliza |
| 4 | Tambor (abajo bombo, medio caja, arriba platillo) | #2f9a72 | Repite en cada cruce |
| 5 | Flauta (antes violín) | #7d63d1 | Sostenido, desliza |
| 6 | Gotas | #4fb3d9 | Repite en cada cruce |
| 7 | Palmas | #a77b54 | Repite en cada cruce |

**Sostenido y desliza:** un trazo es una sola nota que se desliza de nota en nota de la escala (setTargetAtTime 0,035). Si la línea salta más de 3 notas, empieza una frase nueva.

## Interfaz

- **Estilo plano, blanco y sobrio, a petición de Adrian.** Se descartó el "juguete de plástico" petróleo y amarillo.
- **Iconos de línea SVG en todo,** sin emojis: instrumentos, tortuga y conejo, goma, deshacer, papelera y galería.
- **Grupo sonido:** los 8 instrumentos en rejilla más la pastilla de velocidad. **Grupo herramientas:** play, goma, deshacer, papelera y Mis dibujos.
- **Vertical:** título, lienzo, sonido y herramientas. **Horizontal:** sonido, lienzo y herramientas. En el móvil en horizontal, el título va dentro del lienzo vacío.
- **Título:** "DIBUJA TU MÚSICA" escrito a mano por un niño (foto del 11-11-2026), vectorizado letra a letra con OpenCV en `TITLE_SVG`. Cada letra va en un color de instrumento. Se mantuvieron las "I" en forma de bandera; solo se ajustó el espacio entre letras.
- **Cuadrícula:** líneas por cada nota y columnas cada 2 pasos. No hacerla más fina que las notas reales, porque engañaría.
- **Goma:** borra con el dedo y parte los trazos. Deshacer funciona por instantáneas (máximo 40) y cubre trazo, borrado y papelera.
- **Papelera y "×" de la galería:** piden un segundo toque en 2 s.

## Guardado

- **Mis dibujos** se guarda en el `localStorage` del navegador: `dibuja-musica-lib` (lista `{id, code, t}`) y `dibuja-musica-cur`. Cada dibujo se guarda solo, los vacíos no se guardan y las miniaturas se generan desde el código.
- **Código de dibujo:** `v1` + velocidad (a/b/c) + trazos separados por `.` (dígito de instrumento + coordenadas en base36, 2 caracteres por eje). Abrir un código lo añade como dibujo nuevo.
- **Limitación:** los dibujos no pasan de un dispositivo a otro ni sobreviven a borrar los datos del navegador. Al mudarse a otro dominio no se trasladan.
- **Compartir por enlace con `#d=<código>`:** el código ya lo lee al abrir. En GitHub Pages funciona; falta un botón que genere ese enlace (en el artefacto no se podía).

## Pendiente e ideas (por prioridad aproximada)

1. **Mudanza a GitHub Pages:** en marcha (12-11-2026). Después, botón de compartir por enlace `#d=`.
2. **Exportar**, con opción de elegir foto, música, vídeo o todo. Adrian prefiere el vídeo, más adelante. Fuera del artefacto las descargas funcionan con normalidad; el WAV pesa unos 10 MB cada 30 s, así que mejor MP3 o vídeo.
3. **Páginas de una misma canción que suenan seguidas** (como los botones 1-2-3 del original). Esperar a ver si alguien lo pide.
4. **Ajustar sonidos según escuche Adrian.** La trompeta está en revisión; la alternativa es bajarla una octava, tipo trombón.

## Decisiones descartadas y por qué

- **taste-skill (Leonxlnx):** está pensada para webs de empresa y no encaja con un juguete.
- **Forzar horizontal 16:9:** en el móvil obligaba a girarlo. Se pasó a lienzo cuadrado.
- **Violín sintetizado:** sonaba mal y no gustó. Se cambió por la flauta.
- **Deslizar el piano:** un piano real no desliza.
- **Tono continuo libre** (tipo theremín): desafina. El deslizamiento va siempre por notas de la escala.

## Cómo trabajar

- **Ediciones quirúrgicas,** no reescrituras completas.
- **Problemas primero, sin halagos.**
- **Antes de entregar un archivo, preguntar dónde guardarlo.**
- **Probar con Playwright y Chrome headless** en vertical 412×860, horizontal 915×412 y tablet 1280×800, y medir el audio con `__renderLoop`. No se puede escuchar: avisar de ello.
