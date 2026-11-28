import os, sqlite3, re, secrets
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
app=FastAPI(title='Gestión de licitaciones')
security=HTTPBasic()
def auth(c:HTTPBasicCredentials=Depends(security)):
    usuario=os.getenv('APP_USER'); clave=os.getenv('APP_PASSWORD')
    if not usuario or not clave: raise HTTPException(503,'Configurar credenciales locales')
    if not (secrets.compare_digest(c.username,usuario) and secrets.compare_digest(c.password,clave)): raise HTTPException(401,'Credenciales incorrectas')
def db():
    c=sqlite3.connect(os.getenv('DB_PATH','licitaciones.db')); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON'); return c
def init():
    with db() as c: c.executescript('''CREATE TABLE IF NOT EXISTS proveedores(id INTEGER PRIMARY KEY,nombre TEXT NOT NULL,clave TEXT UNIQUE NOT NULL); CREATE TABLE IF NOT EXISTS licitaciones(id INTEGER PRIMARY KEY,codigo TEXT UNIQUE NOT NULL,titulo TEXT NOT NULL,presupuesto INTEGER NOT NULL,cierre TEXT NOT NULL,estado TEXT NOT NULL DEFAULT 'Borrador'); CREATE TABLE IF NOT EXISTS ofertas(id INTEGER PRIMARY KEY,licitacion INTEGER REFERENCES licitaciones(id),proveedor INTEGER REFERENCES proveedores(id),monto INTEGER NOT NULL,UNIQUE(licitacion,proveedor)); CREATE TABLE IF NOT EXISTS tasa(id INTEGER PRIMARY KEY CHECK(id=1),valor TEXT,fecha TEXT); INSERT OR IGNORE INTO tasa VALUES(1,'500','inicial');''')
init()
def now(): return datetime.now(timezone.utc)
def fecha(s):
    try:
        d=datetime.fromisoformat(s); return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError: raise HTTPException(422,'Fecha inválida')
def dinero(v):
    if not v.is_finite() or v<=0 or v!=v.quantize(Decimal('.01')) or v>Decimal('1000000000000'): raise HTTPException(422,'Monto inválido')
    return int(v*100)
def nombre(s):
    s=' '.join(s.split());
    if not s or not all(x.isalnum() or x in ' .,()' for x in s): raise HTTPException(422,'Nombre inválido')
    return s,s.casefold()
def ejecutar(sql,args=()):
    try:
        with db() as c:
            cur=c.execute(sql,args); return {'id':cur.lastrowid,'filas':cur.rowcount}
    except sqlite3.IntegrityError: raise HTTPException(409,'Registro duplicado o relacionado')
def consulta(sql,args=()):
    with db() as c: return [dict(r) for r in c.execute(sql,args)]
def uno(tabla,id):
    r=consulta(f'SELECT * FROM {tabla} WHERE id=?',(id,))
    if not r: raise HTTPException(404,'Registro inexistente')
    return r[0]
class Proveedor(BaseModel): nombre:str
class Licitacion(BaseModel): codigo:str; titulo:str; presupuesto:Decimal; cierre:str
class Oferta(BaseModel): licitacion:int; proveedor:int; monto:Decimal
class Estado(BaseModel): estado:str
class Tasa(BaseModel): valor:Decimal
@app.get('/api/{tabla}',dependencies=[Depends(auth)])
def listar(tabla:str):
    if tabla not in ('proveedores','licitaciones','ofertas','tasa'): raise HTTPException(404)
    return consulta(f'SELECT * FROM {tabla}')
@app.post('/api/proveedores',dependencies=[Depends(auth)],status_code=201)
def crear_p(p:Proveedor): return ejecutar('INSERT INTO proveedores(nombre,clave) VALUES(?,?)',nombre(p.nombre))
@app.put('/api/proveedores/{id}',dependencies=[Depends(auth)])
def editar_p(id:int,p:Proveedor):
    uno('proveedores',id); return ejecutar('UPDATE proveedores SET nombre=?,clave=? WHERE id=?',(*nombre(p.nombre),id))
def datos_l(p):
    if not p.codigo.strip() or not p.titulo.strip() or fecha(p.cierre)<=now(): raise HTTPException(422,'Datos o cierre inválidos')
    return p.codigo.strip().upper(),p.titulo.strip(),dinero(p.presupuesto),fecha(p.cierre).isoformat()
@app.post('/api/licitaciones',dependencies=[Depends(auth)],status_code=201)
def crear_l(p:Licitacion): return ejecutar('INSERT INTO licitaciones(codigo,titulo,presupuesto,cierre) VALUES(?,?,?,?)',datos_l(p))
@app.put('/api/licitaciones/{id}',dependencies=[Depends(auth)])
def editar_l(id:int,p:Licitacion):
    if uno('licitaciones',id)['estado']!='Borrador': raise HTTPException(409,'Solo borradores')
    return ejecutar('UPDATE licitaciones SET codigo=?,titulo=?,presupuesto=?,cierre=? WHERE id=?',(*datos_l(p),id))
def transicion(a,b): return (a,b) in [('Borrador','Publicada'),('Borrador','Cerrada'),('Publicada','Cerrada')]
@app.patch('/api/licitaciones/{id}/estado',dependencies=[Depends(auth)])
def estado(id:int,p:Estado):
    l=uno('licitaciones',id)
    if not transicion(l['estado'],p.estado) or (p.estado=='Publicada' and fecha(l['cierre'])<=now()): raise HTTPException(409,'Transición inválida')
    return ejecutar('UPDATE licitaciones SET estado=? WHERE id=?',(p.estado,id))
def validar_oferta(l,m,instante):
    if l['estado']!='Publicada' or instante>fecha(l['cierre']): raise HTTPException(409,'Licitación no disponible')
    if m>l['presupuesto']: raise HTTPException(422,'Supera presupuesto')
@app.post('/api/ofertas',dependencies=[Depends(auth)],status_code=201)
def ofertar(p:Oferta):
    l=uno('licitaciones',p.licitacion); uno('proveedores',p.proveedor); m=dinero(p.monto); validar_oferta(l,m,now()); return ejecutar('INSERT INTO ofertas(licitacion,proveedor,monto) VALUES(?,?,?)',(p.licitacion,p.proveedor,m))
@app.delete('/api/{tabla}/{id}',dependencies=[Depends(auth)])
def eliminar(tabla:str,id:int):
    if tabla not in ('proveedores','licitaciones','ofertas'): raise HTTPException(404)
    uno(tabla,id); return ejecutar(f'DELETE FROM {tabla} WHERE id=?',(id,))
def clasificar(p,m):
    a=Decimal(p-m)*100/Decimal(p); return float(a),'conveniente' if a>=10 else 'aceptable' if a>0 else 'válida sin ahorro'
def aprobador(m): return 'Encargado de área' if m<100000000 else 'Gerencia' if m<1000000000 else 'Junta Directiva'
@app.get('/api/evaluacion/{id}',dependencies=[Depends(auth)])
def evaluar(id:int):
    l=uno('licitaciones',id); r=consulta('SELECT * FROM ofertas WHERE licitacion=? ORDER BY monto,id LIMIT 1',(id,))
    if not r:return {'mensaje':'Sin ofertas válidas'}
    o=r[0]; a,k=clasificar(l['presupuesto'],o['monto']); t=uno('tasa',1); return {'oferta':o,'ahorro':a,'clasificacion':k,'aprobador':aprobador(o['monto']),'USD':float(Decimal(o['monto'])/100/Decimal(t['valor'])),'tasa':t}
@app.put('/api/tasa/1',dependencies=[Depends(auth)])
def tasa(p:Tasa):
    if not p.valor.is_finite() or p.valor<=0: raise HTTPException(422,'Tasa inválida')
    return ejecutar('UPDATE tasa SET valor=?,fecha=? WHERE id=1',(str(p.valor),now().isoformat()))
@app.get('/',response_class=HTMLResponse,dependencies=[Depends(auth)])
def home(): return open(os.path.join(os.path.dirname(__file__),'index.html'),encoding='utf8').read()
