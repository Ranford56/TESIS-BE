from sqlalchemy.orm import Session

import models
import schemas

# Operaciones para Contratantes
def get_contratantes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contratante).order_by(models.Contratante.id).offset(skip).limit(limit).all()

def get_contratante(db: Session, contratante_id: int):
    return db.query(models.Contratante).filter(models.Contratante.id == contratante_id).first()

def create_contratante(db: Session, contratante: schemas.ContratanteCreate):
    db_contratante = models.Contratante(**contratante.dict())
    db.add(db_contratante)
    db.commit()
    db.refresh(db_contratante)
    return db_contratante

# Operaciones para Asegurados
def get_asegurados(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Asegurado).order_by(models.Asegurado.id).offset(skip).limit(limit).all()

def get_asegurado(db: Session, asegurado_id: int):
    return db.query(models.Asegurado).filter(models.Asegurado.id == asegurado_id).first()

def create_asegurado(db: Session, asegurado: schemas.AseguradoCreate):
    db_asegurado = models.Asegurado(**asegurado.dict())
    db.add(db_asegurado)
    db.commit()
    db.refresh(db_asegurado)
    return db_asegurado

# Operaciones para Vehículos
def get_vehiculos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehiculo).order_by(models.Vehiculo.id).offset(skip).limit(limit).all()

def get_vehiculo(db: Session, vehiculo_id: int):
    return db.query(models.Vehiculo).filter(models.Vehiculo.id == vehiculo_id).first()

def create_vehiculo(db: Session, vehiculo: schemas.VehiculoCreate):
    db_vehiculo = models.Vehiculo(**vehiculo.dict())
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

# Operaciones para Documentos
def get_documentos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Documento).order_by(models.Documento.id).offset(skip).limit(limit).all()

def get_documento(db: Session, documento_id: int):
    return db.query(models.Documento).filter(models.Documento.id == documento_id).first()

def create_documento(db: Session, documento: schemas.DocumentoCreate):
    db_documento = models.Documento(**documento.dict())
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento

# Operaciones para Casos
def get_casos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Caso).order_by(models.Caso.id).offset(skip).limit(limit).all()


def get_caso(db: Session, caso_id: int):
    return db.query(models.Caso).filter(models.Caso.id == caso_id).first()

def create_caso(db: Session, caso: schemas.CasoCreate):
    # Crear el caso principal
    db_caso = models.Caso(**caso.dict(exclude={"contratantes", "asegurados", "vehiculos", "documentos"}))
    db.add(db_caso)
    db.commit()
    db.refresh(db_caso)
    
    # Manejar contratantes
    for contratante in caso.contratantes:
        db_contratante = create_contratante(db, contratante)
        db.add(models.CasoContratante(id_caso=db_caso.id, id_contratante=db_contratante.id))
    
    # Manejar asegurados
    for asegurado in caso.asegurados:
        db_asegurado = create_asegurado(db, asegurado)
        db.add(models.CasoAsegurado(id_caso=db_caso.id, id_asegurado=db_asegurado.id))
    
    # Manejar vehículos
    for vehiculo in caso.vehiculos:
        db_vehiculo = create_vehiculo(db, vehiculo)
        db.add(models.CasoVehiculo(id_caso=db_caso.id, id_vehiculo=db_vehiculo.id))
    
    # Manejar documentos
    for documento in caso.documentos:
        documento.id_caso = db_caso.id
        create_documento(db, documento)
    
    db.commit()
    return db_caso
