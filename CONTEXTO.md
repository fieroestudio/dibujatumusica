# Dibuja tu música: contexto del proyecto

Lee este documento al empezar una conversación nueva en el proyecto. Resume lo decidido y el estado actual.

**Dónde está cada cosa:**
- **Repositorio (referencia):** https://github.com/fieroestudio/dibujatumusica, rama `main`. Un push a `main` publica en GitHub Pages.
- **Carpeta local (PC "msi"):** `C:\Users\UNPARDEDOS\Desktop\CLAUDE\DIBUJA TU MUSICA`. Tiene además la foto original del título, que no se sube al repositorio.
- **Proyecto de claude.ai:** `claude/CONTEXTO.md` y `claude/codigo/index.html`. Es una copia para leer desde el móvil.
- **Artefacto antiguo en claude.ai** (slug `a65713c1-…`): fue el prototipo, se deja de usar y se le quitará el acceso público.

## Qué es

Web app de una sola página donde se dibuja con colores y el dibujo suena como música. La idea sale de *play_music_theory* (Tala Schlossberg). Es una versión propia, pensada para niños de 6 años en adelante y que también puedan usar adultos.

- **Web:** GitHub Pages del repositorio `fieroestudio/dibujatumusica` (ver arriba). Quien tiene el enlace ve cada versión nueva al recargar, así que no se publican versiones rotas.
- **Dispositivos de Adrian:** Android y PC, no hay iOS.
- **Versión actual:** v18.2 (20-11-2026): puntos animados por tiempo y medición por vuelta en `?prueba`. v18.1: arreglada una fuga que cargaba el audio vuelta a vuelta. v18: modo ligero para aparatos lentos. v17.1: medición de rendimiento con `?prueba`. v17 (12-11-2026): arreglos de sonido en iPhone. v16: lo que se dibuja mientras suena se oye en la misma vuelta. v15: líneas de pulsos menos densas, graves audibles en el móvil, tortuga a 90. v14: icono dibujado por un niño. v13: icono y manifiesto para guardarla como app. v12 trajo 10 colores, tres juegos de sonidos, compartir, descargas y pantalla completa. Nadie más tiene el enlace todavía.

## Cómo funciona

- **El lienzo es cuadrado** en cualquier orientación. Coordenadas guardadas en relativo (0..1).
- **Tiempo en horizontal:** 32 pasos por bucle, cada paso una corchea.
- **Altura en vertical:** 15 filas. Arriba agudo, abajo grave. La escala depende del juego de sonidos (ver abajo). La línea continua de la cuadrícula marca la nota base de cada octava.
- **Cada cruce del cabezal con un trazo es una nota.** Un óvalo da dos notas, arriba y abajo. Se marca con un punto negro y un aro.
- **iPhone (v17):** un iPhone no sonaba y otro sí. Causas posibles y arreglos:
  - **iOS anterior a 14.5:** desde v13.1 el código usaba `AudioContext` sin prefijo y Safari antiguo solo tiene `webkitAudioContext`: la reproducción daba error y quedaba muda (la nota de prueba sí sonaba). Corregido y comprobado simulando ese Safari.
  - **Interruptor de silencio** (era la causa: el iPhone que no sonaba lo tenía puesto): en iPhone apaga el sonido de las webs. Se pide `navigator.audioSession.type = 'playback'` para sonar igualmente; según WebKit funciona desde iOS 17 (la API existe desde 16.4). En versiones anteriores hay que quitar el modo silencio. Efecto secundario aceptado por Adrian: al sonar la app se pausa la música de otras apps (Spotify, etc.); para volver a respetar el modo silencio, quitar esa línea.
  - **Desbloqueo del audio:** iPhone solo lo permite al terminar un toque (`touchend`/`click`); en el primero se reproduce un silencio de una muestra.
  - Nada de esto se ha podido probar en un iPhone real.
- **Dibujar mientras suena (v16):** la partitura se recalcula mientras el dedo está en la pantalla (unas 10 veces por segundo), así que lo que se dibuja delante del cabezal suena en esa misma vuelta. Una línea continua que el cabezal encuentra sin estar sonando (recién dibujada, o alargada) arranca desde ese punto, no espera a su inicio en la vuelta siguiente; puede notarse un pequeño ataque en el empalme. Lo que se dibuja por detrás del cabezal suena en la vuelta siguiente (inevitable: el tiempo va de izquierda a derecha). Comprobado: antes una línea de trompeta dibujada a mitad de vuelta no sonaba (0,0001), ahora suena (0,094); un garabato no acumula voces de una vuelta a otra.
- **Modo ligero (v18):** para aparatos que no dan para generar el sonido a tiempo y se entrecorta. Se activa solo si el navegador dice que hay 2 GB de memoria o menos (`navigator.deviceMemory`; Safari no lo da, así que en iPhone nunca), o a mano con `?ligero` en la dirección (`?ligero=N` cambia el límite de voces, para probar). Cambia tres cosas: el audio va a 22 050 Hz en vez de 44 100 (y `latencyHint: 'playback'`), la reverb dura 0,7 s en vez de 1,8 (con algo más de envío para que se oiga parecida) y suenan como mucho 10 voces a la vez (al pasar, la más antigua se apaga en 0,1 s y sus osciladores se paran, que es lo que ahorra trabajo). Además programa las notas con 0,35 s de margen en vez de 0,12, así que lo que se dibuja justo delante del cabezal puede no sonar hasta la vuelta siguiente (lo de v16 se nota menos). En aparatos normales no cambia nada. El MP3 sale a 44 100 Hz en los dos modos.
  - **Medido en el PC:** con 20 trazos, generar el sonido cuesta entre 2,8 y 3,6 veces menos (Clásico 1561 → 436 ms por vuelta; Videojuego 1114 → 397; Espacio 1705 → 505). Con 30 trazos, del 21 % al 5-6 % del tiempo real. Con la CPU frenada 12 veces, 0 pasos tarde (antes 4-7 de 29). Picos de 0,64 a 0,76, sin recortes. Si la tablet medía 234 %, debería quedar en torno al 65-80 %: justo. Si sigue entrecortándose, bajar el límite de voces (7 ahorra poco más) o quitar la reverb.
  - **No se ha escuchado.** Lo que puede notarse: menos brillo en los agudos (platillos, chasquidos), colas de campanita y púlsar cortadas cuando suena mucho a la vez, y la reverb más corta (sobre todo en Espacio).
- **Fuga de voces (arreglada en v18.1):** la lista de voces de cada trazo (`sounding`, para apagarlas al borrar) solo se limpiaba al editar el dibujo. Reproduciendo sin tocar nada crecía cada vuelta y retenía las voces viejas, así que el audio iba cada vez más cargado: en la tablet se entrecortaba tras unas vueltas (Adrian, 20-11-2026). Ahora se limpian las acabadas al añadir cada voz. Medido con 20 trazos a 160 BPM: antes 275 → 1052 nodos de ganancia vivos en 6 vueltas; ahora estable (~220 en modo ligero, ~285 en normal). Borrar mientras suena sigue apagando la nota (comprobado). Afectaba a todos los aparatos; en los rápidos no se notaba.
- **Puntos animados por tiempo (v18.2):** los aros que salen al sonar una nota se apagaban un poco en cada imagen pintada. En un aparato lento (pocas imágenes por segundo) duraban mucho más y se acumulaban: en el PC frenado 12 veces había 200-420 a la vez, lo que frena aún más el pintado. Ahora se apagan en ~0,55 s pase lo que pase (a 60 imágenes por segundo se ven igual que antes): quedan ~60.
- **Pausa:** apaga en el acto todo lo que suena (v13.3); antes, las notas largas ya programadas seguían hasta el final de la línea.
- **Si un trazo desaparece mientras suena** (papelera, goma, deshacer o abrir otro dibujo), sus notas se apagan en el acto (v13.1). Antes, las notas largas ya programadas seguían sonando hasta el final de la línea. Dibujar o cambiar de juego no corta nada.
- **Colores de pulsos: una línea larga suena cada 2 pasos** (v15). Antes una línea horizontal daba 32 notas seguidas y varias juntas sonaban a jaleo (comprobado por Adrian en el móvil). Se aplica dentro de cada trazo: puntos y trazos distintos siguen sonando en cualquier paso, así que los ritmos de corcheas siguen siendo posibles con trazos sueltos. Los puntos negros solo marcan lo que suena. Alternativa descartada por ahora: bajar a 16 pasos por vuelta.
- **Un cruce es cada pasada del trazo por una columna,** en el orden en que se dibujó. Corregido en v12: antes, dos líneas paralelas en notas vecinas dibujadas sin levantar el dedo se juntaban en una nota a media altura. El temblor dentro de una pasada sigue contando como una nota.
- **Velocidades (BPM):** tortuga 90 (antes 80: 12 s por vuelta se hacía largo; ahora 10,7 s), normal 120 (8 s), conejo 160 (6 s). El código guarda la letra, así que los dibujos con tortuga pasan solos a 90.
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

- **Cómo responde a la altura cada continuo (v13.2, en prueba: si no gusta, se deshace):** por defecto, de nota en nota de la escala. Excepciones solo en los juegos abstractos (`mode` en `SOUNDS`):
  - **Altura libre, sin escalones** (`free`): Láser (Videojuego) y Ovni (Espacio). Sigue la línea como una sirena. Es una vuelta parcial a lo descartado como "tono continuo libre"; lo que cambió es que son sonidos de efecto, donde desafinar no suena a error. Puede chocar con colores melódicos del mismo dibujo.
  - **La altura no cambia la nota sino otra cosa** (`bend`): Nave (abre y cierra el filtro) y Power-up (rapidez del arpegio). La nota es la del inicio del trazo. El Viento solar ya funcionaba así (brillo).
  - Clásico no cambia; el bajo y el planeta siguen en la escala para que haya base.
- **Graves en el altavoz del móvil (v15):** el bajo de las filas de abajo no se oía en el Android de Adrian (baja hasta ~65 Hz y el altavoz no da nada por debajo de ~200). Se añadió a los graves una capa de armónicos, más fuerte cuanto más grave la nota, para que el oído reconozca la nota aunque el altavoz no la dé (guitarra/bajo, bajo 8 bits, planeta, bombo y meteorito grave). Medido con un filtro que imita el altavoz (corta por debajo de 250 Hz): el bajo de abajo pasa de 0,008 a 0,032 en Clásico, de 0,014 a 0,031 en Videojuego y de 0,038 a 0,049 en Espacio, al nivel de una línea en medio (~0,05). Falta que Adrian lo escuche.
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
- **Actualizar la app instalada (hoy, sin service worker):** carga la web cada vez que se abre. Los cambios se ven al cerrarla del todo y volver a abrirla (GitHub Pages puede tardar unos 10 min). El icono y el nombre los actualiza Chrome por su cuenta, en un día o así, o desinstalando y volviendo a instalar. Los dibujos se guardan en Chrome para esa web, no en la app; antes de desinstalar, copiar el código de los que importen.
- **Icono y app instalable (v13, icono cambiado en v14):** el icono es una nota dibujada por un niño (12-11-2026): corchetes negros y tres notas rosas. Adrian eligió esta entre varias del mismo papel. Vectorizada con `icons/vectorizar_icono.py` (separa tinta negra y rosa; se pintan con #1d1d1b y el rosa de la app #e07bb5) sobre fondo blanco. La foto original no se sube (`.gitignore`). Archivos: `icons/icon.svg` (pestaña), `icon-180.png` (iPhone/iPad), `icon-192.png` y `icon-512.png` (Android) e `icon-maskable-512.png` (más margen, Android lo recorta en círculo), y `manifest.webmanifest` con nombre corto "Dibuja música" y apertura a pantalla completa. A 32 px los trazos rosas finos se ven flojos. Alternativa guardada en la misma hoja: la onda azul con la línea negra y el punto (es justo la idea del icono provisional).
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
- **Vídeo:** MP4 1080×1200, misma lámina, dos vueltas grabadas en tiempo real (unos 16 s a velocidad normal) con brillos, puntos y cabezal. Mientras graba, la app queda bloqueada con un aviso rojo arriba. Formato preferido H.264 + AAC; si el navegador no lo tiene, cae a H.264 + Opus, otro MP4 o WebM (y lo avisa). **Comprobado por Adrian (12-11-2026):** el vídeo grabado en su Android se manda por WhatsApp y se ve bien. Queda por ver en iPhone.
- **Sonido:** MP3 160 kbps de dos vueltas, generado sin altavoces con `lib/lame.min.js` (lamejs 1.2.1, LGPL, sin modificar). Es la única librería, aprobada por Adrian, y se carga solo al pulsar Sonido.

## Pendiente e ideas (por prioridad aproximada)

0. **Sigue entrecortándose en la tablet a las 5-6 vueltas** (Adrian, 20-11-2026, con v18.1 en la app instalada; no consta que ya tuviera v18.1 cargada). Al pausar y volver a darle, se oye bien otra vez. En el PC no se reproduce (10 vueltas frenado 12 veces: sin cortes ni pasos tarde). Desde v18.2, `?prueba` muestra la versión y una línea por vuelta: cortes del audio (cuando el reloj del audio se queda atrás respecto al del navegador, medido con `getOutputTimestamp`), pasos tarde, imágenes por segundo y puntos animados. Falta esa foto tras 8 vueltas para ver qué crece. En el modo ligero no se notó peor sonido. Antes: **comprobar el modo ligero en la tablet** (abrir con `?prueba`: la primera línea debe decir "modo ligero" y bajar del 100 %). Historia del problema: **sonido entrecortado en la tablet Samsung SM-T550 (Android 7.1.1, Chrome 119) con bastantes trazos** (20-11-2026). Se instala y abre a pantalla completa bien (sin service worker: Chrome lo permite desde la 108). Chrome 119 es la última para Android 7.
   - Medido en el PC (Chrome headless, dibujo de 30 trazos con los 10 colores): generar el sonido cuesta el 15-22 % del tiempo real de un núcleo rápido; la reverb es unos 2/5 del coste fijo y el resto son las voces (todos los colores cuestan parecido). En un procesador como el de la tablet (2015) eso puede pasar del 100 %, y entonces el sonido se corta.
   - Además, con la CPU frenada 12 veces, los parones del hilo principal llegan a 270-380 ms y casi un 30 % de las notas salen tarde (el programador mira solo 0,12 s por delante). Con 6 veces, ninguna.
   - **Medición en el aparato real:** abrir la web en Chrome (no en la app instalada) con `?prueba` en la dirección (`…/dibujatumusica/?prueba`). Sale un recuadro arriba a la izquierda (abajo tapaba el play en vertical): "Medir" calcula una vuelta del dibujo actual sin altavoces y da el % del tiempo real (más de 100 % = no le da tiempo); al reproducir muestra pasos que salen tarde y el mayor parón. Sin `?prueba` no cambia nada.
   - Posibles arreglos según lo que salga: si el % pasa de 100, modo ligero (reverb más corta o sin ella, límite de voces a la vez); si salen pasos tarde, mirar más lejos (0,25-0,3 s; empeora un poco lo de v16, lo dibujado justo delante del cabezal) y aligerar el pintado de los brillos. `latencyHint: 'playback'` ayuda a los cortes sueltos, pero retrasa el sonido al tocar un color.
   - **Primera medición en la tablet (20-11-2026):** 0 de 132 pasos tarde, mayor parón 108 ms (cerca del margen de 0,12 s, pero sin pasarlo). 4 núcleos, 1 GB, latencia de salida 80 ms, 48 kHz. Falta el % de "Medir" (no se pulsó o no terminó) y saber si en esa prueba se oyó entrecortado. Si se oyó, la causa no es el hilo principal sino el procesador al generar el sonido.
   - **Segunda medición (20-11-2026, 20 trazos, Clásico):** 234 % del tiempo real; 54 de 78 pasos tarde, parón de 317 ms. Causa: el procesador no da para generar el sonido. De ahí el modo ligero (v18).
   - **Medición con v18 (20-11-2026, mismo dibujo):** 65 % del tiempo real (antes 234 %), 0 de 42 pasos tarde, parón de 61 ms. Latencia de salida 175 ms (antes 80): es el precio de `latencyHint: 'playback'` y se nota como retraso al tocar un color o dibujar. Si molesta, quitar esa opción (vuelve a 80 ms, con menos margen contra cortes). Falta que Adrian diga si se oye bien.
   - Visto de paso: ese dibujo de 30 trazos da un pico de 0,90-0,92 (límite 0,9), sin recortes.

1. **Que Adrian escuche los 30 sonidos** y diga cuáles cambiar. Los de Videojuego y Espacio, el órgano y el acordeón son nuevos y nadie los ha escuchado. La trompeta sigue en revisión (alternativa: una octava más baja, tipo trombón).
2. **Probar en un iPad o iPhone** antes de mandárselo a alguien que use Apple. Ni Adrian ni Claude pueden probarlo ahora.
3. **Páginas de una misma canción que suenan seguidas** (como los botones 1-2-3 del original). Esperar a ver si alguien lo pide.
4. **Que funcione sin conexión** (service worker): Adrian quiere añadirlo cuando terminen los cambios actuales. Hasta entonces no, porque haría que cada versión nueva tardara una recarga más en verse. **Al hacerlo, es obligatorio añadir un aviso de versión nueva** ("Hay una versión nueva, toca para actualizar"): con el service worker la app instalada guarda su propia copia y, sin ese aviso, se quedaría con la versión vieja sin que nadie se dé cuenta.
5. **Para profesores, solo si alguien lo pide:** nombres de notas en la cuadrícula, elegir escala, pregunta y respuesta, juegos con reglas. Adrian prefiere que siga siendo un juego, no una app didáctica.

## Decisiones descartadas y por qué

- **taste-skill (Leonxlnx):** está pensada para webs de empresa y no encaja con un juguete.
- **Forzar horizontal 16:9:** en el móvil obligaba a girarlo. Se pasó a lienzo cuadrado.
- **Violín sintetizado:** sonaba mal y no gustó. Se cambió por la flauta.
- **Deslizar el piano:** un piano real no desliza.
- **Tono continuo libre** (tipo theremín): desafina. El deslizamiento va por notas de la escala, salvo en Láser y Ovni (v13.2, a prueba; ver arriba).
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
