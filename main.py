# main.py
from database import inicializar_base_datos, cerrar_sesion
from gestor_investigacion import GestionInvestigacion

def mostrar_menu():
    print("\n=== SISTEMA DE GESTIÓN DE INVESTIGACIÓN ===")
    print("1. Crear Institución")
    print("2. Crear Departamento")
    print("3. Crear Investigador")
    print("4. Crear Publicación")
    print("5. Consultar Instituciones")
    print("6. Consultar Investigadores por Área")
    print("7. Consultar Publicaciones por Investigador")
    print("8. Ver Estadísticas")
    print("9. Salir")
    return input("Seleccione una opción: ")

def main():
    session = inicializar_base_datos()
    gestor = GestionInvestigacion(session)

    crear_datos_ejemplo(gestor)
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == '1':
            crear_institucion(gestor)
        elif opcion == '2':
            crear_departamento(gestor)
        elif opcion == '3':
            crear_investigador(gestor)
        elif opcion == '4':
            crear_publicacion(gestor)
        elif opcion == '5':
            consultar_instituciones(gestor)
        elif opcion == '6':
            consultar_investigadores_por_area(gestor)
        elif opcion == '7':
            consultar_publicaciones_por_investigador(gestor)
        elif opcion == '8':
            ver_estadisticas(gestor)
        elif opcion == '9':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
    
    cerrar_sesion(session)

def crear_datos_ejemplo(gestor):
    """Crear datos de ejemplo para probar el sistema"""
    try:

        instituciones = gestor.obtener_instituciones()
        if not instituciones:
            print("Creando datos de ejemplo...")
            
            uni1 = gestor.crear_institucion("Universidad UTPL", "Cuenca", "Ecuador")
            uni2 = gestor.crear_institucion("Instituto Tecnológico", "Medellín", "Colombia")
            
            depto1 = gestor.crear_departamento("Ingenieria de Requisitos", "IR001", uni1.id)
            depto2 = gestor.crear_departamento("Gestion de la Calidad", "GC001", uni1.id)
            depto3 = gestor.crear_departamento("Redes de Dispositivos", "RD001", uni2.id)
            
            inv1 = gestor.crear_investigador("Ana", "Gómez", "ana.gomez@email.com", "Inteligencia Artificial", depto1.id)
            inv2 = gestor.crear_investigador("Carlos", "López", "carlos.lopez@email.com", "Bioinformática", depto2.id)
            inv3 = gestor.crear_investigador("María", "Rodríguez", "maria.rodriguez@email.com", "Genética", depto3.id)
            
            gestor.crear_publicacion("Avances en Machine Learning", "2023-05-15", "10.1234/ml.2023", "Artículo", inv1.id)
            gestor.crear_publicacion("Análisis Genómico", "2023-08-20", "10.1234/bio.2023", "Artículo", inv2.id)
            gestor.crear_publicacion("Sistemas Autónomos", "2023-11-10", "10.1234/rob.2023", "Conferencia", inv1.id)
            
            print("Datos de ejemplo creados exitosamente!")
    except Exception as e:
        print(f"Error creando datos de ejemplo: {e}")

def crear_institucion(gestor):
    print("\n--- CREAR INSTITUCIÓN ---")
    nombre = input("Nombre: ")
    ciudad = input("Ciudad: ")
    pais = input("País: ")
    
    institucion = gestor.crear_institucion(nombre, ciudad, pais)
    print(f"Institución creada: {institucion}")

def crear_departamento(gestor):
    print("\n--- CREAR DEPARTAMENTO ---")
    instituciones = gestor.obtener_instituciones()
    if not instituciones:
        print("Primero debe crear una institución")
        return
    
    print("Instituciones disponibles:")
    for inst in instituciones:
        print(f"{inst.id}. {inst.nombre}")
    
    try:
        institucion_id = int(input("ID de la institución: "))
        nombre = input("Nombre del departamento: ")
        codigo = input("Código del departamento: ")
        
        departamento = gestor.crear_departamento(nombre, codigo, institucion_id)
        print(f"Departamento creado: {departamento}")
    except ValueError:
        print("ID debe ser un número")

def crear_investigador(gestor):
    print("\n--- CREAR INVESTIGADOR ---")
    departamentos = gestor.obtener_departamentos()
    if not departamentos:
        print("Primero debe crear un departamento")
        return
    
    print("Departamentos disponibles:")
    for depto in departamentos:
        print(f"{depto.id}. {depto.nombre} - {depto.institucion.nombre}")
    
    try:
        departamento_id = int(input("ID del departamento: "))
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        email = input("Email: ")
        area = input("Área de investigación: ")
        
        investigador = gestor.crear_investigador(nombre, apellido, email, area, departamento_id)
        print(f"Investigador creado: {investigador.nombre_completo()}")
    except ValueError:
        print("ID debe ser un número")

def crear_publicacion(gestor):
    print("\n--- CREAR PUBLICACIÓN ---")
    investigadores = gestor.obtener_investigadores()
    if not investigadores:
        print("Primero debe crear un investigador")
        return
    
    print("Investigadores disponibles:")
    for inv in investigadores:
        print(f"{inv.id}. {inv.nombre_completo()}")
    
    try:
        investigador_id = int(input("ID del investigador: "))
        titulo = input("Título: ")
        fecha = input("Fecha (YYYY-MM-DD): ")
        doi = input("DOI: ")
        tipo = input("Tipo (Artículo/Tesis/Conferencia): ")
        
        publicacion = gestor.crear_publicacion(titulo, fecha, doi, tipo, investigador_id)
        print(f"Publicación creada: {publicacion.titulo}")
    except ValueError:
        print("ID debe ser un número")

def consultar_instituciones(gestor):
    print("\n--- INSTITUCIONES ---")
    instituciones = gestor.obtener_instituciones()
    for inst in instituciones:
        print(f"{inst.id}. {inst.nombre} - {inst.ciudad}, {inst.pais}")
        for depto in inst.departamentos:
            print(f"   - {depto.nombre} ({depto.codigo})")

def consultar_investigadores_por_area(gestor):
    print("\n--- INVESTIGADORES POR ÁREA ---")
    area = input("Área de investigación a buscar: ")
    investigadores = gestor.obtener_investigadores_por_area(area)
    
    if investigadores:
        for inv in investigadores:
            print(f"{inv.nombre_completo()} - {inv.email} - {inv.departamento.nombre}")
    else:
        print(f"No se encontraron investigadores en el área: {area}")

def consultar_publicaciones_por_investigador(gestor):
    print("\n--- PUBLICACIONES POR INVESTIGADOR ---")
    investigadores = gestor.obtener_investigadores()
    
    if not investigadores:
        print("No hay investigadores registrados")
        return
    
    print("Investigadores disponibles:")
    for inv in investigadores:
        print(f"{inv.id}. {inv.nombre_completo()}")
    
    try:
        investigador_id = int(input("ID del investigador: "))
        publicaciones = gestor.obtener_publicaciones_por_investigador(investigador_id)
        
        if publicaciones:
            investigador = next((inv for inv in investigadores if inv.id == investigador_id), None)
            print(f"\nPublicaciones de {investigador.nombre_completo()}:")
            for pub in publicaciones:
                print(f"- {pub.titulo} ({pub.tipo_publicacion}, {pub.fecha_publicacion})")
        else:
            print("El investigador no tiene publicaciones registradas")
    except ValueError:
        print("ID debe ser un número")

def ver_estadisticas(gestor):
    print("\n--- ESTADÍSTICAS DEL SISTEMA ---")
    stats = gestor.obtener_estadisticas()
    print(f"Total Instituciones: {stats['instituciones']}")
    print(f"Total Departamentos: {stats['departamentos']}")
    print(f"Total Investigadores: {stats['investigadores']}")
    print(f"Total Publicaciones: {stats['publicaciones']}")

if __name__ == "__main__":
    main()