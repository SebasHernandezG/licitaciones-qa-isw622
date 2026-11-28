# Sistema de Gestión de Licitaciones — ISW-622

Aplicación web local para registrar proveedores, licitaciones y ofertas; calcular la mejor oferta y evaluar el ahorro. Usa FastAPI y SQLite. El repositorio está preparado para **cuatro aportes alternados** de Sebas y Laura. Cada persona debe revisar y adaptar su paquete, ejecutar las pruebas y registrar sus propios resultados antes de crear el commit.

## Instalación y ejecución

En PowerShell, desde esta carpeta:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe seed.py --reset
$env:APP_USER = "demo"
$env:APP_PASSWORD = [guid]::NewGuid().ToString("N")
Write-Host "Contraseña local temporal: $env:APP_PASSWORD"
.\.venv\Scripts\python.exe -m uvicorn app:app --reload
```

Abrir <http://127.0.0.1:8000>. API interactiva: <http://127.0.0.1:8000/docs>. La aplicación exige `APP_USER` y `APP_PASSWORD`; el ejemplo genera una clave temporal local y la muestra solo en la consola. No incluirla en Git ni en capturas. Los importes se guardan en céntimos CRC en `licitaciones.db`. Para restablecer la base, detener el servidor y volver a ejecutar `seed.py --reset`.

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

La versión original de `app.py`, `index.html` y `test_app.py` provino del ZIP `Licitaciones_avance.zip` aportado por Laura. Este repositorio conserva esa procedencia; los siguientes paquetes proponen cambios asistidos por IA que requieren validación humana. El resultado técnico de una ejecución automatizada no equivale a aceptación del equipo.

Ver [plan de aportes](PLAN_APORTES.md) para el orden de ramas, commits y Pull Requests. Las plantillas institucionales Word y Excel aún deben incorporarse y completarse con ejecuciones reales.


