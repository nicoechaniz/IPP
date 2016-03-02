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
from behave import *

from ipp.relevamiento.constants import RELEVADOR, COORD_ZONAL
from ipp.relevamiento.factories import PlanillaDeRelevamientoFactory, ProductoConMarcaFactory
from ipp.relevamiento.models import PlanillaModelo, PlanillaDeRelevamiento, Zona, Comercio, ProductoGenerico, ProductoConMarca


import sys
python_3 = sys.version.startswith('3')


@given('que existe al menos una Planilla de Relevamiento')
def impl(context):
    planilla_modelo = PlanillaModelo.objects.first()
    zona = Zona.objects.first()
    comercio = Comercio.objects.first()
    planilla_de_relevamiento = PlanillaDeRelevamientoFactory(planilla_modelo=planilla_modelo,
                                                             zona=zona, comercio=comercio)

@given('que existen varios Productos con marca')
def impl(context):
    for prod_generico in ProductoGenerico.objects.all():
        ProductoConMarcaFactory(producto_generico=prod_generico, marca=context.MARCA_POR_DEFECTO)

@given('accedo a la funcionalidad para completar Planilla de Relevamiento')
def impl(context):
    url = reverse("relevamiento:seleccionar_planilla_de_relevamiento")
    context.browser.visit(context.config.server_url + url)

@given('elijo una Planilla de Relevamiento para trabajar')
def impl(context):
    planilla = PlanillaDeRelevamiento.objects.last()
    url = reverse("relevamiento:completar_planilla_de_relevamiento",
                  kwargs={"planilla_id": planilla.pk})
    context.browser.click_link_by_partial_href(url)

@when('establezco marcas para algunos productos')
def impl(context):
    planilla = PlanillaDeRelevamiento.objects.last()
    producto_ids = [p.id for p in planilla.planilla_modelo.productos.all()]
    for p_id in producto_ids:
        producto_con_marca = ProductoConMarca.objects.get(producto_generico__id=p_id,
                                                          marca=context.MARCA_POR_DEFECTO)
        url = reverse("relevamiento:establecer_marca",
                      kwargs={"planilla_id": planilla.id,
                              "tipo_marca": "economica", "producto_id": p_id})
        context.browser.click_link_by_href(url)
        for key in context.browser.type('producto_con_marca-autocomplete',
                                        context.MARCA_POR_DEFECTO):
            # el auto-complete trae la opción; la buscamos por su texto
            if not python_3:
                producto_con_marca = str(producto_con_marca)
            if context.browser.is_element_present_by_text(producto_con_marca):
                opcion = context.browser.find_by_text(producto_con_marca)
                opcion.first.click()
                context.browser.find_by_css('form button[type=submit]').first.click()
                break
        
@when('habilito la planilla')
def impl(context):
    planilla = PlanillaDeRelevamiento.objects.last()
    url = reverse("relevamiento:habilitar_planilla_de_relevamiento",
                  kwargs={"planilla_id": planilla.id})
    context.browser.click_link_by_href(url)

@then('la planilla queda habilitada')
def impl(context):
    # el test corriendo en firefox falla si no esperamos aquí
    sleep(1)
    planilla = PlanillaDeRelevamiento.objects.last()
    assert(planilla.habilitada==True)
