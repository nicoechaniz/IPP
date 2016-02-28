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


from time import sleep
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from behave import *

from utils import seleccionar_primera_opcion

from ipp.relevamiento.constants import RELEVADOR
from ipp.relevamiento.factories import JerarquizacionMarcaFactory
from ipp.relevamiento.models import Muestra, PlanillaDeRelevamiento, Perfil, ProductoConMarca

@given(u'los productos en la planilla tienen marcas establecidas')
def impl(context):
    planilla = PlanillaDeRelevamiento.objects.last()
    producto_ids = [p.id for p in planilla.planilla_modelo.productos.all()]
    for p_id in producto_ids:
        producto_con_marca = ProductoConMarca.objects.get(producto_generico__id=p_id,
                                                          marca=context.MARCA_POR_DEFECTO)
        JerarquizacionMarcaFactory(tipo_marca="economica",
                                   planilla_de_relevamiento=planilla,
                                   producto_con_marca=producto_con_marca)
        
@when(u'selecciono la Muestra')
def impl(context):
    muestra = Muestra.objects.last()
    url = reverse("relevamiento:editar_muestra",
                  kwargs={"muestra_id": muestra.id})
    context.browser.click_link_by_href(url)

@when(u'establezco el precio para un producto')
def impl(context):
    context.browser.find_by_css('span.glyphicon').first.click()
    # cuando el behave_browser es un browser real, demora la animación para mostrar el modal
    sleep(1)
    context.browser.fill('precio', 112)
    context.browser.find_by_name('guardar_precio').first.click()
    
@then(u'la planilla refleja el precio cargado')
def impl(context):
    ocurrencia = context.browser.find_by_css('td.success')[1].html.find(u"112")
    assert ocurrencia >= 0

@then(u'si edito el precio cargado')
def impl(context):
    context.browser.find_by_css('span.glyphicon').first.click()
    # cuando el behave_browser es un browser real, demora la animación para mostrar el modal
    sleep(1)
    context.browser.fill('precio', 116)
    context.browser.find_by_name('guardar_precio').first.click()

@then(u'la planilla refleja el nuevo precio')
def impl(context):
    ocurrencia = context.browser.find_by_css('td.success')[1].html.find(u"116")
    assert ocurrencia >= 0
