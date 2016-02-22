Característica: Crear Muestra
  Como coordinador
  Quiero poder crear muestras para la carga de lecturas de precios
  basadas en planillas de relevamiento habilitadas

  Antecedentes: Existe un conjunto básico de información
    Dado que existe al menos una Planilla de Relevamiento
    Y que existen varios Productos con marca
    Y que la Planilla de Relevamiento está habilitada
    
  Escenario: Crear Muestra
    Dado que me logueo en el sistema y mi Rol es de coordinador
    Y accedo a la funcionalidad para cargar lecturas de precios
    Cuando completo el formulario para crear una Muestra nueva y lo envío
    Entonces he creado una nueva Muestra

