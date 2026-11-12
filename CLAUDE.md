# Dibuja tu música: instrucciones para Claude

Antes de cambiar nada, lee `CONTEXTO.md`. Explica cómo funciona la app, qué se ha decidido, qué se ha descartado y por qué, y qué queda pendiente. No propongas de nuevo lo descartado sin explicar qué ha cambiado.

## Proyecto

- Toda la app está en `index.html`: HTML, CSS y JS en un solo archivo, sin librerías, sin npm y sin compilación. Mantenerlo así salvo que Adrian pida lo contrario.
- **Publicación:** GitHub Pages desde la rama `main`, carpeta raíz. Un push a `main` publica, así que no se sube nada sin probar.
- `titulo/vectorizar.py` genera `titulo/titulo.svg` a partir de la foto original. La foto **no se sube al repositorio** (`.gitignore`): está solo en la carpeta local de Adrian. El SVG va incrustado en `index.html` (`TITLE_SVG`).

## Reglas que no se pueden romper

- **No cambiar el orden de `INSTRUMENTS`.** El código guardado de cada dibujo usa el índice del instrumento. Los instrumentos nuevos se añaden al final.
- **No cambiar el formato del código de dibujo (`v1…`)** sin crear una versión `v2` que siga leyendo `v1`. La gente tiene dibujos guardados.
- **Claves de `localStorage`:** `dibuja-musica-lib` y `dibuja-musica-cur`. No renombrarlas.
- **Volumen:** después de cualquier cambio de sonido, medir con `window.__renderLoop()` usando un dibujo cargado con los 8 instrumentos. El pico debe quedar por debajo de 0,9 y sin recortes.

## Cómo trabajar con Adrian

- Ediciones quirúrgicas, nada de reescrituras completas.
- Primero los problemas, sin halagos. Si algo no se ha podido comprobar (por ejemplo, cómo suena), decirlo.
- Preguntar antes de crear archivos fuera de lo habitual.
- Probar en vertical (412×860), en horizontal (915×412) y en tablet (1280×800).
- Al terminar un cambio, actualizar `CONTEXTO.md`: versión, qué cambió y decisiones.
