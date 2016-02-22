# -*- coding: utf-8 -*-

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


from django.conf.urls import url, patterns
from django.contrib import admin

from ipp.relevamiento.views import *

urlpatterns = (
#    url(r"^$", portada, name='portada'),
    url(r"^crear_planilla_de_relevamiento/$", crear_planilla_de_relevamiento, name='crear_planilla_de_relevamiento'),
    url(r"^seleccionar_planilla_de_relevamiento/$", seleccionar_planilla_de_relevamiento, name='seleccionar_planilla_de_relevamiento'),
    url(r"^completar_planilla_de_relevamiento/(?P<planilla_id>[0-9]+)$", completar_planilla_de_relevamiento, name='completar_planilla_de_relevamiento'),
    url(r"^habilitar_planilla_de_relevamiento/(?P<planilla_id>[0-9]+)$", habilitar_planilla_de_relevamiento, name='habilitar_planilla_de_relevamiento'),
    url(r"^deshabilitar_planilla_de_relevamiento/(?P<planilla_id>[0-9]+)$", deshabilitar_planilla_de_relevamiento, name='deshabilitar_planilla_de_relevamiento'),    
    url(r"^establecer_marca/(?P<planilla_id>[0-9]+)/(?P<tipo_marca>economica{1}|media{1}|premium{1})/(?P<producto_id>[0-9]+)$", establecer_marca, name='establecer_marca'),
    url(r"^remover_marca/(?P<planilla_id>[0-9]+)/(?P<tipo_marca>economica{1}|media{1}|premium{1})/(?P<producto_id>[0-9]+)$", remover_marca, name='remover_marca'),
    url(r"^nueva_marca/(?P<producto_id>[0-9]+)$", nueva_marca, name='nueva_marca'),
    url(r"^seleccionar_muestra/$", seleccionar_muestra, name='seleccionar_muestra'),
    url(r"^editar_muestra/(?P<muestra_id>[0-9]+)$", editar_muestra, name='editar_muestra'),
    url(r"^crear_lectura/(?P<muestra_id>[0-9]+)/(?P<producto_id>[0-9]+)$", crear_lectura, name='crear_lectura'),
    url(r"^editar_lectura/(?P<lectura_id>[0-9]+)$", editar_lectura, name='editar_lectura'),
    url(r"^seleccionar_comercio/$", SeleccionarComercio.as_view(), name='seleccionar_comercio'),
    url(r"^crear_comercio/$", CrearComercio.as_view(), name='crear_comercio'),
    url(r"^editar_comercio/(?P<pk>[0-9]+)$", EditarComercio.as_view(), name='editar_comercio'),
#    url(r"^crear_perfil/", CrearPerfil.as_view(), name='crear_perfil'),
    url(r"^seleccionar_zona/$", SeleccionarZona.as_view(), name='seleccionar_zona'),
    url(r"^crear_zona/$", CrearZona.as_view(), name='crear_zona'),
    url(r"^editar_zona/(?P<pk>[0-9]+)$", EditarZona.as_view(), name='editar_zona'),
    url(r"^seleccionar_jurisdiccion/$", SeleccionarJurisdiccion.as_view(), name='seleccionar_jurisdiccion'),
    url(r"^crear_jurisdiccion/$", CrearJurisdiccion.as_view(), name='crear_jurisdiccion'),
    url(r"^editar_jurisdiccion/(?P<pk>[0-9]+)$", EditarJurisdiccion.as_view(), name='editar_jurisdiccion'),
    url('^crear_usuario/', CrearUser.as_view(), name='crear_usuario'),
    url('^seleccionar_usuario/', SeleccionarUser.as_view(), name='seleccionar_usuario'),
    url('^editar_usuario/(?P<pk>[0-9]+)$', EditarUser.as_view(), name='editar_usuario'),
    url('^promedios_por_comercio/(?P<anio>[0-9]{4})/(?P<mes>[0-9]{1,2})/(?P<quincena>[1-2]{1})/(?P<region_id>[0-9]*)?$', promedios_por_comercio, name="promedios_por_comercio"),
    url('^maximos_por_comercio/(?P<anio>[0-9]{4})/(?P<mes>[0-9]{1,2})/(?P<quincena>[1-2]{1})/(?P<region_id>[0-9]*)?$', maximos_por_comercio, name="maximos_por_comercio"),
    url('^minimos_por_comercio/(?P<anio>[0-9]{4})/(?P<mes>[0-9]{1,2})/(?P<quincena>[1-2]{1})/(?P<region_id>[0-9]*)?$', minimos_por_comercio, name="minimos_por_comercio"),
    url('^descargar_datos$', descargar_datos, name="descargar_datos")
)
