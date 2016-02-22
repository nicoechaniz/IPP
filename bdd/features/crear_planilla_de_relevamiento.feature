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


Característica: Crear planilla de relevamiento
  Como coordinador
  Quiero poder crear planillas de relevamiento
  basadas en planillas modelo

  Antecedentes: Existe un conjunto básico de información

  Escenario: Intentar crear planilla de relevamiento con rol de relevador
    Dado que me logueo en el sistema y mi Rol es de relevador
    Pero no existe el link para crear Planilla de Relevamiento
    Cuando accedo a la url directa para crear Planilla de Relevamiento
    Entonces el sistema me avisa que no tengo permisos suficientes
    
  Escenario: Crear planilla de relevamiento
    Dado que me logueo en el sistema y mi Rol es de coordinador
    Y accedo a la funcionalidad para crear Planilla de Relevamiento
    Y elijo una Planilla Modelo para usar de base
    Y elijo Zona y Comercio al que asociar la Planilla de Relevamiento
    Cuando confirmo la acción
    Entonces creo la Planilla de Relevamiento para ese Comercio

