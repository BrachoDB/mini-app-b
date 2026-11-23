## Rol
Actúa como desarrollador backend con experiencia en FastAPI, Jinja2 y pruebas con pytest.

## Objetivo
Modificar la aplicación web de trivia de cultura general para que el endpoint `GET /api/preguntas` acepte el parámetro opcional `cantidad` (entero entre `1` y `5`) y devuelva solo esa cantidad de preguntas; si no se envía `cantidad`, devuelve `5` preguntas, y si `cantidad` está fuera del rango `1` a `5`, responde con el código `422`. Además, permite elegir cuántas preguntas jugar desde la página principal (`GET /`) y agrega una prueba nueva en `tests/test_mejora.py` que verifique el contenido de la respuesta de la mejora.

## Contexto
Lee `AGENTS.md` y revisa la implementación actual en `app/main.py`, `app/servicios.py` y `app/templates/index.html`. El contrato base está en `tests/test_aceptacion.py` y no debe alterarse.

## Restricciones
Usa solo las dependencias de `requirements.txt`.
Mantén las rutas en `app/main.py` y la lógica en `app/servicios.py`, sin importar FastAPI en `app/servicios.py`.
Guarda los datos en memoria, sin base de datos ni archivos.
No modifiques ni borres `tests/test_aceptacion.py`.
Crea una prueba nueva en `tests/test_mejora.py` que compruebe la mejora (incluyendo el contenido de la respuesta y no solo el código de estado).
La página principal (`app/templates/index.html`) debe permitir elegir cuántas preguntas se juegan usando HTML, CSS y JavaScript sin librerías externas
No hagas commit ni push

## Formato de salida
Antes de escribir o modificar código, muestra el plan con las rutas completas de los archivos que vas a crear o modificar y espera mi aprobación. Al terminar, resume en una línea qué hace cada archivo creado o modificado.

## Ejemplo
Petición:
`GET /api/preguntas?cantidad=2`
Respuesta esperada (ejemplo):
Devuelve una lista con 2 preguntas (cada una con `id`, `texto` y `opciones` de 4 elementos, sin revelar la respuesta correcta).
Si `GET /api/preguntas` se llama sin `cantidad`, devuelve 5 preguntas.
Si `GET /api/preguntas?cantidad=10` o `cantidad=0`, responde con código `422`.

## Criterio de éxito
Ejecuta `python -m pytest -v` y `ruff check`: todas las pruebas (en `tests/test_aceptacion.py` y `tests/test_mejora.py`) pasan y `ruff check` no reporta errores. Si después de 3 intentos las pruebas o Ruff no pasan, detente y explica el problema.