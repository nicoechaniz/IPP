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


Característica: Completar planilla de relevamiento
    Como coordinador
    Quiero poder completar y habilitar planillas de relevamiento
    para que los relevadores puedan tomar sus lecturas

  Antecedentes: Existe un conjunto básico de información
    Dado que existe al menos una Planilla de Relevamiento
    Y que existen varios Productos con marca

  Escenario: Editar planilla de relevamiento y habilitarla
    Dado que me logueo en el sistema y mi Rol es de coordinador
    Y accedo a la funcionalidad para completar Planilla de Relevamiento
    Y elijo una Planilla de Relevamiento para trabajar
    Cuando establezco marcas para algunos productos
    Y habilito la planilla
    Entonces la planilla queda habilitada

