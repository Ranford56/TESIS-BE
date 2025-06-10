from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from database import Base

class Contratante(Base):
    __tablename__ = "contratantes"

    id = Column(Integer, primary_key=True, index=True)
    tipo_identificacion = Column(String(255))
    numero_identificacion = Column(String(255))
    nombre_contratante = Column(String(255))
    residencia = Column(String(255))

    casos = relationship("Caso", secondary="caso_contratante", back_populates="contratantes")

class Asegurado(Base):
    __tablename__ = "asegurados"

    id = Column(Integer, primary_key=True, index=True)
    tipo_identificacion = Column(String(255))
    numero_identificacion = Column(String(255))
    nombre_asegurado = Column(String(255))
    residencia = Column(String(255))

    casos = relationship("Caso", secondary="caso_asegurado", back_populates="asegurados")

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String(255), unique=True)
    marca = Column(String(255))
    modelo = Column(String(255))
    anio = Column(String(255))

    casos = relationship("Caso", secondary="caso_vehiculo", back_populates="vehiculos")

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    tipo_documento = Column(String(255))
    ruta_archivo = Column(String(255))
    id_caso = Column(Integer, ForeignKey("casos.id"))

    caso = relationship("Caso", back_populates="documentos")

class Caso(Base):
    __tablename__ = "casos"

    id = Column(Integer, primary_key=True, index=True)
    fecha_incidente = Column(Date)
    detalles_incidente = Column(Text)
    danos_visibles = Column(Text)
    ya_reportado = Column(Boolean)
    numero_poliza = Column(String(255))
    aseguradora = Column(String(255))

    contratantes = relationship("Contratante", secondary="caso_contratante", back_populates="casos")
    asegurados = relationship("Asegurado", secondary="caso_asegurado", back_populates="casos")
    vehiculos = relationship("Vehiculo", secondary="caso_vehiculo", back_populates="casos")
    documentos = relationship("Documento", back_populates="caso")

class CasoContratante(Base):
    __tablename__ = "caso_contratante"

    id_caso = Column(Integer, ForeignKey("casos.id"), primary_key=True)
    id_contratante = Column(Integer, ForeignKey("contratantes.id"), primary_key=True)

class CasoAsegurado(Base):
    __tablename__ = "caso_asegurado"

    id_caso = Column(Integer, ForeignKey("casos.id"), primary_key=True)
    id_asegurado = Column(Integer, ForeignKey("asegurados.id"), primary_key=True)

class CasoVehiculo(Base):
    __tablename__ = "caso_vehiculo"

    id_caso = Column(Integer, ForeignKey("casos.id"), primary_key=True)
    id_vehiculo = Column(Integer, ForeignKey("vehiculos.id"), primary_key=True)
