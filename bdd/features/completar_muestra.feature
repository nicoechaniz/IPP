Característica: Completar Muestra
  Como relevador
  Quiero poder completar precios en planillas de Muestra

Antecedentes: Existe un conjunto básico de información
  Dado que existe al menos una Planilla de Relevamiento
  Y que existen varios Productos con marca
  Y que la Planilla de Relevamiento está habilitada
  Y los productos en la planilla tienen marcas establecidas

Escenario: Cargar precios de productos
  Dado que me logueo en el sistema y mi Rol es de relevador
  Y accedo a la funcionalidad para cargar lecturas de precios
  Cuando completo el formulario para crear una Muestra nueva y lo envío
  Y selecciono la muestra creada
  Cuando establezco el precio para un producto
  Entonces la planilla refleja el precio cargado
  Y si edito el precio cargado
  Entonces la planilla refleja el nuevo precio
