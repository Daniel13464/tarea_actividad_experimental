# gestor_investigacion.py
from modelos import Institucion, Departamento, Investigador, Publicacion

class GestionInvestigacion:
    def __init__(self, session):
        self.session = session
    
    def crear_institucion(self, nombre, ciudad, pais):
        institucion = Institucion(nombre=nombre, ciudad=ciudad, pais=pais)
        self.session.add(institucion)
        self.session.commit()
        return institucion
    
    def obtener_instituciones(self):
        return self.session.query(Institucion).all()
    
    def obtener_institucion_por_id(self, institucion_id):
        return self.session.query(Institucion).filter_by(id=institucion_id).first()
    

    def crear_departamento(self, nombre, codigo, institucion_id):
        departamento = Departamento(nombre=nombre, codigo=codigo, institucion_id=institucion_id)
        self.session.add(departamento)
        self.session.commit()
        return departamento
    
    def obtener_departamentos(self):
        return self.session.query(Departamento).all()
    
    def obtener_departamentos_por_institucion(self, institucion_id):
        return self.session.query(Departamento).filter_by(institucion_id=institucion_id).all()
    
    def crear_investigador(self, nombre, apellido, email, area_investigacion, departamento_id):
        investigador = Investigador(
            nombre=nombre, 
            apellido=apellido, 
            email=email, 
            area_investigacion=area_investigacion,
            departamento_id=departamento_id
        )
        self.session.add(investigador)
        self.session.commit()
        return investigador
    
    def obtener_investigadores(self):
        return self.session.query(Investigador).all()
    
    def obtener_investigadores_por_departamento(self, departamento_id):
        return self.session.query(Investigador).filter_by(departamento_id=departamento_id).all()
    
    def obtener_investigadores_por_area(self, area):
        return self.session.query(Investigador).filter_by(area_investigacion=area).all()
    
    def crear_publicacion(self, titulo, fecha_publicacion, doi, tipo_publicacion, investigador_id):
        publicacion = Publicacion(
            titulo=titulo,
            fecha_publicacion=fecha_publicacion,
            doi=doi,
            tipo_publicacion=tipo_publicacion,
            investigador_id=investigador_id
        )
        self.session.add(publicacion)
        self.session.commit()
        return publicacion
    
    def obtener_publicaciones(self):
        return self.session.query(Publicacion).all()
    
    def obtener_publicaciones_por_investigador(self, investigador_id):
        return self.session.query(Publicacion).filter_by(investigador_id=investigador_id).all()
    
    def obtener_publicaciones_por_tipo(self, tipo):
        return self.session.query(Publicacion).filter_by(tipo_publicacion=tipo).all()
    
    def obtener_informacion_completa_investigador(self, investigador_id):
        investigador = self.session.query(Investigador).filter_by(id=investigador_id).first()
        if investigador:
            return {
                'investigador': investigador,
                'departamento': investigador.departamento,
                'institucion': investigador.departamento.institucion,
                'publicaciones': investigador.publicaciones
            }
        return None
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas generales del sistema"""
        total_instituciones = self.session.query(Institucion).count()
        total_departamentos = self.session.query(Departamento).count()
        total_investigadores = self.session.query(Investigador).count()
        total_publicaciones = self.session.query(Publicacion).count()
        
        return {
            'instituciones': total_instituciones,
            'departamentos': total_departamentos,
            'investigadores': total_investigadores,
            'publicaciones': total_publicaciones
        }