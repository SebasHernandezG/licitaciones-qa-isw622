"""Casos de frontera para el defecto controlado del cierre.

La versión de laboratorio está en una rama separada; main no se altera.
"""
import os
import tempfile
from datetime import datetime, timedelta, timezone

os.environ.setdefault('DB_PATH', tempfile.mktemp(suffix='.db'))

from app import HTTPException, validar_oferta
import pytest


def licitacion(estado='Publicada'):
    cierre = datetime(2026, 12, 1, tzinfo=timezone.utc)
    return {'estado': estado, 'cierre': cierre.isoformat(), 'presupuesto': 100000000}, cierre


def test_cp004_retest_cierre_exacto():
    oferta, cierre = licitacion()
    with pytest.raises(HTTPException) as error:
        validar_oferta(oferta, 100000000, cierre)
    assert error.value.status_code == 409


def test_cp005_regresion_antes_cierre_monto_igual():
    oferta, cierre = licitacion()
    validar_oferta(oferta, 100000000, cierre - timedelta(microseconds=1))


def test_cp020_regresion_borrador():
    oferta, cierre = licitacion('Borrador')
    with pytest.raises(HTTPException) as error:
        validar_oferta(oferta, 100000000, cierre - timedelta(seconds=1))
    assert error.value.status_code == 409
