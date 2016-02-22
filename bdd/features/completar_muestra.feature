#    IPP, Plataforma web del Índice de Precios Popular
#    Copyright (c) 2016 Nicolás Echániz and contributors.
#
#    This file is part of IPP
#
#    IPP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
