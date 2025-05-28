from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import crud
from database import SessionLocal
import schemas

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contratantes/", response_model=schemas.Contratante)
def crear_contratante(contratante: schemas.ContratanteCreate, db: Session = Depends(get_db)):
    return crud.create_contratante(db=db, contratante=contratante)

@app.get("/contratantes/", response_model=List[schemas.Contratante])
def listar_contratantes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contratantes = crud.get_contratantes(db, skip=skip, limit=limit)
    return contratantes

@app.post("/asegurados/", response_model=schemas.Asegurado)
def crear_asegurado(asegurado: schemas.AseguradoCreate, db: Session = Depends(get_db)):
    return crud.create_asegurado(db=db, asegurado=asegurado)

@app.get("/asegurados/", response_model=List[schemas.Asegurado])
def listar_asegurados(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    asegurados = crud.get_asegurados(db, skip=skip, limit=limit)
    return asegurados

@app.post("/vehiculos/", response_model=schemas.Vehiculo)
def crear_vehiculo(vehiculo: schemas.VehiculoCreate, db: Session = Depends(get_db)):
    return crud.create_vehiculo(db=db, vehiculo=vehiculo)

@app.get("/vehiculos/", response_model=List[schemas.Vehiculo])
def listar_vehiculos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vehiculos = crud.get_vehiculos(db, skip=skip, limit=limit)
    return vehiculos

@app.post("/casos/", response_model=schemas.Caso)
def crear_caso(caso: schemas.CasoCreate, db: Session = Depends(get_db)):
    return crud.create_caso(db=db, caso=caso)

@app.get("/casos/", response_model=List[schemas.Caso])
def listar_casos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    casos = crud.get_casos(db, skip=skip, limit=limit)
    return casos

@app.get("/casos/{caso_id}", response_model=schemas.Caso)
def leer_caso(caso_id: int, db: Session = Depends(get_db)):
    db_caso = crud.get_caso(db, caso_id=caso_id)
    if db_caso is None:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
    return db_caso