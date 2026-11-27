# Plan de cuatro aportes verificables

El PDF de la práctica pide al menos dos commits **no consecutivos por integrante**, ramas y entrada a `main` mediante Pull Request. Para lograr exactamente cuatro commits de código en `main`, usar el orden Sebas → Laura → Sebas → Laura. Cada paquete es un punto de partida generado con IA; el autor del commit debe revisarlo, modificarlo cuando corresponda, ejecutar y explicar sus pruebas. No cambiar la autoría de Git para simular trabajo.

| Orden | Responsable | Aporte concreto | Verificación humana mínima |
| --- | --- | --- | --- |
| 1 | Sebas | Importación acreditada del prototipo de Laura, entorno reproducible, seed sintético y documentación de alcance. | Arrancar, restablecer BD, comprobar seed y registrar salida real de pytest. |
| 2 | Laura | Interfaz navegable para edición de proveedores, listados y cambio de vista CRC/USD. Caso de límite de cierre. | Probar la interfaz, diseñar el CP de cierre y registrar el resultado en versión 2. |
| 3 | Sebas | Corrección del defecto de cierre, rangos configurables de aprobación y pruebas API. | Registrar BUG, hash previo/posterior, retest y regresión. |
| 4 | Laura | Automatización adicional, colección Postman y documentación de ejecución final. | Ejecutar suites, Postman, seguridad, UX con 2 personas ajenas y carga 5 VU/30 s. |

## Flujo Git

1. Sebas aplica `01-Sebas.zip` en la rama `sebas`, revisa y crea su primer commit. Abre PR hacia `main` y fusiona sin commit de merge adicional (rebase o fast-forward).
2. Laura crea/actualiza su rama `laura` desde el `main` actualizado, aplica `02-Laura.zip`, revisa y crea su primer commit. PR y fusión igual.
3. Sebas actualiza su rama `sebas` desde el nuevo `main`, aplica `03-Sebas.zip` y crea su segundo commit. Abre PR.
4. Laura actualiza `laura` desde el nuevo `main`, aplica `04-Laura.zip` y crea su segundo commit. Abre PR.

Los paquetes son **instantáneas completas** del proyecto en cada etapa. Copiar únicamente los archivos fuente que cambian respecto de la etapa anterior; no copiar `.git`, bases de datos, entornos virtuales ni evidencia no ejecutada por la persona. Cada etapa debe ser revisada con `git diff` antes del commit. Si un PR requiere un commit extra para resolver un conflicto o corregir un hallazgo, priorizar la trazabilidad real sobre el número exacto de cuatro.

La versión 2 puede contener un defecto de laboratorio señalado en su paquete. Registrar una falla solo si se reproduce realmente. La versión 3 debe corregirlo y la 4 demostrar regresión. Completar 14 REQ, ≥20 CP, ≥23 RUN, ≥8 pruebas automatizadas, IA, riesgos, usabilidad, carga y seguridad en las plantillas originales; no inventar resultados.
