from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Tabla intermedia para relación muchos a muchos entre registros y emociones
registro_emocion = Table(
    'registro_emocion',
    Base.metadata,
    Column('registro_id', Integer, ForeignKey('registros.id'), primary_key=True),
    Column('emocion_id', Integer, ForeignKey('emociones.id'), primary_key=True)
)

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    registros = relationship("Registro", back_populates="usuario")

class Registro(Base):
    __tablename__ = "registros"
    id = Column(Integer, primary_key=True, index=True)
    texto = Column(Text, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    emociones = relationship("Emocion", secondary=registro_emocion, back_populates="registros")
    usuario = relationship("Usuario", back_populates="registros")

class Emocion(Base):
    __tablename__ = "emociones"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    registros = relationship("Registro", secondary=registro_emocion, back_populates="emociones")
