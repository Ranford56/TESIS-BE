import base64
import os
from fastapi import FastAPI, Depends, HTTPException, UploadFile
from typing import List
from fastapi.params import File
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import crud
from database import SessionLocal
import schemas
from azure.storage.blob import BlobServiceClient

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

service = BlobServiceClient.from_connection_string(os.getenv('BLOB_STORAGE_CONN_STRING'))

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

@app.get("/blob/")
def get_blob(blob_name: str):
    try:
        blob_client = service.get_blob_client(container="insurance", blob=blob_name)
        blob_data = blob_client.download_blob().readall()
        return {"blob_name": blob_name, "data": base64.b64encode(blob_data).decode('utf-8')}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Blob no encontrado: {str(e)}")

@app.post("/blob/upload")
async def upload_blob(blob_name: str, file: UploadFile = File(...)):
    try:
        blob_client = service.get_blob_client(container="insurance", blob=blob_name)
        file_content = await file.read()
        
        # Upload the file content directly (as bytes) to Azure Blob Storage
        blob_client.upload_blob(file_content, overwrite=True)
        return {"message": "Archivo subido exitosamente", "blob_name": blob_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir el archivo: {str(e)}")