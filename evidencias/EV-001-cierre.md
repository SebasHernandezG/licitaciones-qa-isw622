# EV-001 · Límite de cierre de ofertas

**CP-004 / RUN-004** · REQ-004 · 26 de noviembre de 2026 (Costa Rica).

- Base Git probada: `e83a91e5692a574cc1b2faad46ab342d03907912`. La interfaz se probó desde el árbol de trabajo de este aporte; la regla del servidor coincide con la base.
- Preparación: base SQLite sintética temporal, un proveedor y una licitación publicada con cierre futuro T. Fijar el reloj del servidor en T con `unittest.mock.patch` y enviar una oferta válida por monto.
- Esperado: HTTP 409 y listado de ofertas vacío. Obtenido: HTTP 409, `{"detail":"Licitación no disponible"}`, y listado vacío.
- Resultado: aprobado. BUG-001, aceptación al instante exacto, no se reprodujo. La comparación existente es `instante >= cierre`.

Verificación adicional con TestClient: edición de proveedor HTTP 200, registro antes del cierre HTTP 201, cierre manual HTTP 200. El presupuesto fue 1 000 000 000 céntimos CRC y la oferta 900 000 000 céntimos CRC. La evaluación devolvió USD 18 000 con tasa 500. La suite existente produjo `12 passed, 1 warning`; la prueba aislada de cierre produjo `1 passed, 1 warning`. El aviso corresponde a una API obsoleta de Starlette TestClient.
