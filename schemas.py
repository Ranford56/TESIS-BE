from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# Esquemas base
class ContratanteBase(BaseModel):
    tipo_identificacion: str
    numero_identificacion: str
    nombre_contratante: str

class AseguradoBase(BaseModel):
    tipo_identificacion: str
    numero_identificacion: str
    nombre_asegurado: str

class VehiculoBase(BaseModel):
    placa: str
    marca: str
    modelo: str
    anio: str

class DocumentoBase(BaseModel):
    tipo_documento: str
    ruta_archivo: str
    id_caso: int

class AseguradorBase(BaseModel):
    nombre: str


# Esquemas para creación
class ContratanteCreate(ContratanteBase):
    pass

class AseguradoCreate(AseguradoBase):
    pass

class VehiculoCreate(VehiculoBase):
    pass

class DocumentoCreate(DocumentoBase):
    pass

class AseguradorCreate(AseguradorBase):
    pass

class CasoBase(BaseModel):
    fecha_incidente: date
    detalles_incidente: str
    danos_visibles: str
    ya_reportado: bool
    numero_poliza: Optional[str]
    aseguradora: str

class CasoCreate(CasoBase):
    contratantes: List[ContratanteCreate] = []
    asegurados: List[AseguradoCreate] = []
    vehiculos: List[VehiculoCreate] = []
    documentos: List[DocumentoCreate] = []

# Esquemas para respuesta
class Contratante(ContratanteBase):
    id: int
    class Config:
        orm_mode = True

class Asegurado(AseguradoBase):
    id: int
    class Config:
        orm_mode = True

class Vehiculo(VehiculoBase):
    id: int
    class Config:
        orm_mode = True

class Documento(DocumentoBase):
    id: int
    class Config:
        orm_mode = True

class Asegurador(AseguradorBase):
    id: int
    class Config:
        orm_mode = True

class Caso(CasoBase):
    id: int
    contratantes: List[Contratante] = []
    asegurados: List[Asegurado] = []
    vehiculos: List[Vehiculo] = []
    documentos: List[Documento] = []
    class Config:
        orm_mode = True
