# Cuentitis
Web estática de lectura comprensiva (5-12 años). Sin servidor ni API: las lecturas están en `lecturas.json`. El catálogo actual contiene 50 lecturas, 16 temas y cuatro tramos de edad.

## Probar en local
`python3 -m http.server 8000` y abre http://localhost:8000 (hace falta servidor; no vale abrir el archivo directamente).

## Publicar gratis
1. Sube esta carpeta a un repositorio de GitHub.
2. GitHub Pages: Settings → Pages → Deploy from branch → `main` / root. (También vale Netlify, Vercel o Cloudflare Pages conectando el repo.)
3. Cada `git push` actualiza la web.

## Añadir lecturas
Pide a Claude lecturas nuevas con este prompt y pega el resultado dentro del array de `lecturas.json`:

> Genera N lecturas en español de España para niños, en JSON con esta forma: {"id","band" (5-6|7-8|9-10|11-12),"topics" (1-2 de: Animales, Dinosaurios, Espacio, Fútbol, Princesas y reyes, Superhéroes, Piratas, Coches, Cocina, Ciencia, Dragones, Robots, Naturaleza y medioambiente, Música, Misterios y detectives, ¿Sabías que...?),"hero" (niño|niña|neutro),"title","paragraphs","questions" (5: {"q","options","answer" (índice desde 0),"why"}),"english","sources" (referencias cuando el tema sea ¿Sabías que...?)}. Longitud: 5-6 años, 350-550 palabras; 7-8, 380-600; 9-10 y 11-12, 450-650. Opciones: 3 por pregunta en 5-6 y 7-8 años, 4 en 9-10 y 11-12. 2 preguntas de detalle, 2 de inferencia, 1 de vocabulario o idea principal. Posición de la correcta variada. Cada lectura debe incluir 3-4 palabras en inglés marcadas con [en:english|español] y listadas en english. Lenguaje adaptado a la edad. Contenido positivo y apto para niños. En ¿Sabías que...? utiliza datos reales y contrastados con fuentes fiables; incluye `sources` como una lista de objetos `{"name":"Fuente","url":"https://..."}`. El validador exige al menos una referencia con URL HTTPS para cada lectura de esta categoría. Las referencias son editoriales y no se muestran en la vista infantil.

Después ejecuta `python3 validate.py` para comprobar el formato.

## Identidad visual y mascota (DEV)
La interfaz utiliza la identidad visual de Cuentitis: libro morado aventurero, marcapáginas y detalles naranjas, estrella dorada, fondos crema y lavanda.
- Paleta de referencia: morado `#6926B9`, lavanda `#F0E5FF`, naranja `#FF901F`, dorado `#FFD044`, crema `#FFF9F1` y tinta `#351653`.
- Tipografías: Fredoka para títulos y elementos expresivos; Nunito para lectura y textos de interfaz.
- El favicon vive en `favicon.svg`.
- La cabecera principal utiliza la imagen raster de referencia `assets/hero/cuentitis-home.webp` (1133 × 650), sin reconstruir la ilustración con SVG ni CSS. Los controles de Información, Premios y edad se superponen como HTML para mantener su funcionalidad y sus valores dinámicos. El selector de los 16 temas y el footer continúan siendo elementos interactivos independientes.
- Las ilustraciones SVG de `assets/mascots/` se conservan para los estados secundarios de carga, lectura, test y diálogos. La versión 3D aprobada como recurso independiente todavía queda pendiente de exportación e integración.

## Cómo elige la lectura
El niño elige un solo tema favorito. Cuentitis intenta ofrecer primero una lectura inédita de ese tema dentro de su tramo de edad. Cuando ya se han leído todas las lecturas de ese tema, continúa con otras lecturas inéditas de la misma edad. No repite ninguna lectura hasta que una persona adulta reinicie el historial desde Información para familias. La selección y el historial se guardan en el navegador.

## Aviso de «lecturas nuevas»
Al abrir la web, esta compara los `id` de `lecturas.json` con los que ese navegador ya conocía. Si hay `id` nuevos, aparece una etiqueta 🆕 en la cabecera; al pulsarla se listan los títulos nuevos. La primera vez que alguien entra no se avisa de nada (todo es nuevo para él).
- Cada lectura nueva debe tener un `id` **único y nunca reutilizado**.
- Si cambias el texto de una lectura ya existente sin cambiar su `id`, no se avisa.

## Criterios de redacción (los comprueba `validate.py`)
- Diálogos con raya (—), cada intervención en su propio párrafo; las comillas « » solo para títulos o frases citadas.
- Español de España y frases adaptadas a la edad: 5-6 años, frases cortas (media 7-13 palabras); 7-8, 8-15; 9-10, 11-18; 11-12, 14-22.
- Longitud: 5-6 años desde 350 palabras; 7-8 desde 380; 9-10 y 11-12 desde 450.
- Evitar series de frases muy cortas seguidas en 9-10 y 11-12 años.
- 5 preguntas por lectura: 3 opciones hasta los 8 años y 4 desde los 9. Todas deben ser textos completos, sin valores `null`; el índice `answer` debe señalar la opción correcta y `why` explicar la respuesta.

## Comentarios de usuarios beta
El pie de página tiene un botón «Enviar comentarios» que abre un formulario y lo reenvía por correo con FormSubmit (sin cuenta ni servidor propio).
1. Publica la web y envía **un comentario de prueba** desde la dirección real (no funciona abriendo el archivo desde el disco).
2. FormSubmit te enviará un correo de activación: pulsa el enlace (mira también en spam). Ese primer mensaje queda retenido hasta activar.
3. Tras activar, FormSubmit te da un código aleatorio. sustituye `FORM_ENDPOINT` en `index.html` por `https://formsubmit.co/ajax/<código>`, para que el correo no quede visible en la página.
4. Si hay spam, el formulario ya lleva un campo trampa. Puedes mirar las opciones extra en la documentación de FormSubmit.

## Palabras en inglés
Cada lectura lleva 3-4 palabras básicas que aparecen **en inglés en lugar de la palabra española**. En el texto se escriben como `[en:palabra inglesa|palabra española]`, por ejemplo `un cuenco de [en:milk|leche]`, y el campo `english` debe contener exactamente las mismas parejas `en`/`es` que aparecen en las etiquetas. Si la palabra está en plural o tiene género, utiliza la forma que corresponda dentro de los corchetes y repítela igual en `english`.
La web las muestra resaltadas. Al pulsarlas aparece un aviso con la traducción («milk = leche») y se pronuncian con la voz del dispositivo (inglés británico). Al final del texto se repasan todas en una cajita «Palabras en inglés».
- Escribe cada forma completa dentro de la etiqueta: por ejemplo, `[en:birds|pájaros]`, nunca `[en:bird|pájaro]s` ni `[en:team|cuadrilla]es`.
- El glosario debe coincidir carácter por carácter con las parejas de las etiquetas; incluye las formas plurales o de género usadas en el relato.
- Evita verbos conjugados: utiliza infinitivos o formas adecuadas (`[en:asleep|dormido]`).
- Nivel: 5-6 años, colores, animales y objetos; 7-8, casa, comida y naturaleza; 9-10 y 11-12, palabras cotidianas algo más largas.
- `validate.py` comprueba que cada pareja de las etiquetas coincida exactamente con `english`, detecta sufijos fuera de los corchetes y exige opciones completas, respuestas válidas y explicaciones `why`.
