# Dibuja tu música

Juego web para dibujar con colores y escuchar el dibujo como música. Pensado para niños de 6 años en adelante, y también para adultos.

- Una sola página (`index.html`), sin compilación: HTML, CSS y JavaScript con Web Audio.
- La única dependencia es `lib/lame.min.js` ([LAME](https://lame.sourceforge.io) vía lamejs 1.2.1, licencia LGPL, sin modificar), que solo se carga al descargar el sonido en MP3. Ver `lib/lame.LICENSE`.
- Funciona en móvil, tablet y ordenador, en vertical y en horizontal.
- Los dibujos se guardan en el navegador de cada persona ("Mis dibujos").

Para probarlo en local, sirve la carpeta con `python -m http.server` (abriendo `index.html` directamente, el MP3 y el enlace pueden no funcionar).
