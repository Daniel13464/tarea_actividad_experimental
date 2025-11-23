# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelos import Base

def inicializar_base_datos():
   
    engine = create_engine('sqlite:///investigacion.db', echo=True)
    
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    return Session()

def cerrar_sesion(session):
    """Cierra la sesión de la base de datos"""
    session.close()
