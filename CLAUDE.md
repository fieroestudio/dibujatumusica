# Dibuja tu música: instrucciones para Claude

Antes de cambiar nada, lee `CONTEXTO.md`. Explica cómo funciona la app, qué se ha decidido, qué se ha descartado y por qué, y qué queda pendiente. No propongas de nuevo lo descartado sin explicar qué ha cambiado.

## Proyecto

- Toda la app está en `index.html`: HTML, CSS y JS en un solo archivo, sin npm y sin compilación. Mantenerlo así salvo que Adrian pida lo contrario.
- Única excepción aprobada por Adrian: `lib/lame.min.js` (codificador MP3, LGPL, sin modificar), que se carga solo al pulsar Sonido en Compartir y descargar.
- Además: `manifest.webmanifest` e `icons/` (icono de la app). Si cambia el icono, regenerar todos los PNG desde `icons/icon.svg`.
- **Publicación:** GitHub Pages desde la rama `main`, carpeta raíz. Un push a `main` publica, así que no se sube nada sin probar.
- `titulo/vectorizar.py` genera `titulo/titulo.svg` a partir de la foto original. La foto **no se sube al repositorio** (`.gitignore`): está solo en la carpeta local de Adrian. El SVG va incrustado en `index.html` (`TITLE_SVG`).

## Reglas que no se pueden romper

- **No cambiar el orden de `SLOTS` (los 10 colores).** El código guardado de cada dibujo usa el número del color. 0-4 van a pulsos y 5-9 son continuos. Caben 10 como máximo en el formato actual.
- **Cada color se comporta igual en todos los juegos de sonidos** (`KITS` y `SOUNDS`): solo cambia el sonido. Todos los juegos tienen los mismos 10 colores.
- **No cambiar el formato del código de dibujo (`v2…`)** sin crear una versión nueva que siga leyendo la anterior. `v2` sigue abriendo los `v1` del prototipo.
- **Claves de `localStorage`:** `dibuja-musica-lib` y `dibuja-musica-cur`. No renombrarlas.
- **Volumen:** después de cualquier cambio de sonido, medir con `window.__renderLoop()` usando un dibujo cargado con los 10 colores, en cada juego de sonidos. El pico debe quedar por debajo de 0,9 y sin recortes.

## Cómo trabajar con Adrian

- Ediciones quirúrgicas, nada de reescrituras completas.
- Primero los problemas, sin halagos. Si algo no se ha podido comprobar (por ejemplo, cómo suena), decirlo.
- Preguntar antes de crear archivos fuera de lo habitual.
- Probar en vertical (412×860), en horizontal (915×412) y en tablet (1280×800).
- Al terminar un cambio, actualizar `CONTEXTO.md`: versión, qué cambió y decisiones.
