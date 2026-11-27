import os,tempfile,secrets
os.environ['DB_PATH']=tempfile.mktemp(suffix='.db')
credentials=('qa',secrets.token_urlsafe(24))
os.environ['APP_USER'],os.environ['APP_PASSWORD']=credentials
from app import *
from fastapi.testclient import TestClient
import pytest
from datetime import timedelta
client=TestClient(app)
@pytest.mark.parametrize('v',[Decimal('0'),Decimal('-1')])
def test_monto(v):
    with pytest.raises(HTTPException): dinero(v)
def test_nombre(): assert nombre('  Norte   SA ') == ('Norte SA','norte sa')
def test_seguridad():
    with pytest.raises(HTTPException): nombre('<script>')
@pytest.mark.parametrize('m,k',[(900,'conveniente'),(950,'aceptable'),(1000,'válida sin ahorro')])
def test_ahorro(m,k): assert clasificar(1000,m)[1]==k
def test_estado(): assert not transicion('Cerrada','Publicada')
def test_cierre():
    t=now(); l={'estado':'Publicada','cierre':t.isoformat(),'presupuesto':100}
    with pytest.raises(HTTPException): validar_oferta(l,100,t)
def test_api():
    assert client.post('/api/proveedores',json={'nombre':'Norte SA'},auth=credentials).status_code==201
    assert client.post('/api/proveedores',json={'nombre':' norte  sa '},auth=credentials).status_code==409
    assert client.get('/api/proveedores',auth=credentials).status_code==200
def test_sin_auth(): assert client.get('/api/proveedores').status_code==401
def test_flujo():
    p=client.post('/api/proveedores',json={'nombre':'Valle'},auth=credentials).json()['id']; l=client.post('/api/licitaciones',json={'codigo':'LIC-2026-001','titulo':'Equipo','presupuesto':10000000,'cierre':(now()+timedelta(days=2)).isoformat()},auth=credentials).json()['id']; assert client.patch(f'/api/licitaciones/{l}/estado',json={'estado':'Publicada'},auth=credentials).status_code==200
    assert client.post('/api/ofertas',json={'licitacion':l,'proveedor':p,'monto':9000000},auth=credentials).status_code==201
    assert client.get(f'/api/evaluacion/{l}',auth=credentials).json()['ahorro']==10
