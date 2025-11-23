# modelos.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Institucion(Base):
    __tablename__ = 'instituciones'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    ciudad = Column(String(50), nullable=False)
    pais = Column(String(50), nullable=False)
    
    
    departamentos = relationship("Departamento", back_populates="institucion")
    
    def __repr__(self):
        return f"<Institucion(id={self.id}, nombre='{self.nombre}', ciudad='{self.ciudad}', pais='{self.pais}')>"

class Departamento(Base):
    __tablename__ = 'departamentos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(10), nullable=False)
    institucion_id = Column(Integer, ForeignKey('instituciones.id'), nullable=False)
    
    institucion = relationship("Institucion", back_populates="departamentos")
    investigadores = relationship("Investigador", back_populates="departamento")
    
    def __repr__(self):
        return f"<Departamento(id={self.id}, nombre='{self.nombre}', codigo='{self.codigo}')>"

class Investigador(Base):
    __tablename__ = 'investigadores'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    area_investigacion = Column(String(100), nullable=False)
    departamento_id = Column(Integer, ForeignKey('departamentos.id'), nullable=False)
    
    departamento = relationship("Departamento", back_populates="investigadores")
    publicaciones = relationship("Publicacion", back_populates="investigador")
    
    def __repr__(self):
        return f"<Investigador(id={self.id}, nombre='{self.nombre}', apellido='{self.apellido}', email='{self.email}')>"
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

class Publicacion(Base):
    __tablename__ = 'publicaciones'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    fecha_publicacion = Column(String(10), nullable=False)
    doi = Column(String(100), unique=True)
    tipo_publicacion = Column(String(50), nullable=False)
    investigador_id = Column(Integer, ForeignKey('investigadores.id'), nullable=False)
    
    investigador = relationship("Investigador", back_populates="publicaciones")
    
    def __repr__(self):
        return f"<Publicacion(id={self.id}, titulo='{self.titulo}', fecha='{self.fecha_publicacion}')>"