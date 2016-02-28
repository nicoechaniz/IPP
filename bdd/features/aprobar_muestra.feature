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


Característica: Aprobar Muestra
  Como coordinador
  Quiero poder aprobar muestras de lecturas de precios
  Para que ya no sean editables los precios de las muestras aprobadas

  Antecedentes: Existe un conjunto básico de información
    Dado que existe al menos una Planilla de Relevamiento
    Y que existen varios Productos con marca
    Y que la Planilla de Relevamiento está habilitada
    Y los productos en la planilla tienen marcas establecidas
    Y que existe una Muestra con lecturas de precios

  Escenario: Aprobar Muestra
    Dado que me logueo en el sistema y mi Rol es de coordinador
    Y accedo a la funcionalidad para cargar lecturas de precios
    Cuando selecciono la Muestra
    Y apruebo la Muestra
    Entonces la Muestra queda aprobada
    Y ya no aparece en el listado para cargar lecturas

