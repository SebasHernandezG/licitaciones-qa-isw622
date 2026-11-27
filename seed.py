"""Carga datos sintéticos de referencia en una base local de SQLite."""

import argparse
import os
from datetime import timedelta
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Cargar datos de ejemplo")
    parser.add_argument("--db", default="licitaciones.db", help="Ruta de la base SQLite")
    parser.add_argument("--reset", action="store_true", help="Borrar primero esa base")
    args = parser.parse_args()

    path = Path(args.db).resolve()
    if args.reset and path.exists():
        path.unlink()
    os.environ["DB_PATH"] = str(path)

    from app import db, dinero, nombre, now
    from decimal import Decimal

    cierre = (now() + timedelta(hours=48)).isoformat()
    with db() as conn:
        p1 = conn.execute(
            "INSERT INTO proveedores(nombre, clave) VALUES(?, ?)",
            nombre("Tecnología Norte S.A."),
        ).lastrowid
        p2 = conn.execute(
            "INSERT INTO proveedores(nombre, clave) VALUES(?, ?)",
            nombre("Servicios del Valle"),
        ).lastrowid
        licitacion = conn.execute(
            "INSERT INTO licitaciones(codigo, titulo, presupuesto, cierre, estado) "
            "VALUES(?, ?, ?, ?, ?)",
            ("LIC-2026-001", "Equipo informático", dinero(Decimal("10000000.00")), cierre, "Publicada"),
        ).lastrowid
        conn.execute(
            "INSERT INTO ofertas(licitacion, proveedor, monto) VALUES(?, ?, ?)",
            (licitacion, p1, dinero(Decimal("9000000.00"))),
        )
        conn.execute(
            "INSERT INTO ofertas(licitacion, proveedor, monto) VALUES(?, ?, ?)",
            (licitacion, p2, dinero(Decimal("9500000.00"))),
        )
        conn.execute(
            "UPDATE tasa SET valor=?, fecha=? WHERE id=1",
            ("500.00", now().isoformat()),
        )
    print(f"Datos sintéticos cargados en {path}")


if __name__ == "__main__":
    main()
