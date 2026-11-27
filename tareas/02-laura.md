# Aporte 2 de 4 — Laura

**Responsable:** @Paty-FN. **Base:** después del aporte 1 de Sebas. **Rama:** `laura`. **Paquete inicial:** `02-Laura.zip`.

## Trabajo

- Revisar y adaptar `index.html` para registrar, listar y editar proveedores; registrar y listar licitaciones y ofertas; publicar, cerrar, evaluar y alternar la vista CRC/USD.
- Comprobar que los importes almacenados siguen en CRC y que la interfaz muestra errores controlados.
- Ejecutar el caso límite REQ-004 contra la versión 2. El defecto temporal está documentado en `LAB_DEFECTO.md`: acepta una oferta exactamente al cierre.
- Registrar CP, RUN fallida, BUG-001 y EV real; guardar el hash de este commit para el retest del aporte 3.

## Criterios de aceptación

- La interfaz permite las acciones anteriores sin editar código ni llamar manualmente a la API.
- El caso de cierre falla de forma reproducible y queda registrado con versión, pasos, esperado y obtenido. Si no se reproduce, registrar el resultado real.
- Laura revisa el diff, ejecuta las pruebas, explica sus cambios y abre un PR de un commit suyo hacia `main`.

Referencia: REQ-001 a REQ-010 del PDF; `PLAN_APORTES.md`.
