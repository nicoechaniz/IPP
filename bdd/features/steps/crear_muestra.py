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


from django.core.urlresolvers import reverse
from behave import *

from utils import seleccionar_primera_opcion

from ipp.relevamiento.constants import COORD_ZONAL
from ipp.relevamiento.models import PlanillaDeRelevamiento, Muestra


import sys
python_3 = sys.version.startswith('3')


@given(u'que la Planilla de Relevamiento está habilitada')
def impl(context):
    planilla_de_relevamiento = PlanillaDeRelevamiento.objects.first()
    planilla_de_relevamiento.habilitada = True
    planilla_de_relevamiento.save()
    context.planilla_de_relevamiento_id = planilla_de_relevamiento.id

@given(u'accedo a la funcionalidad para cargar lecturas de precios')
def impl(context):
    context.browser.click_link_by_text("Acciones")
    url = reverse("relevamiento:seleccionar_muestra")
    context.browser.click_link_by_href(url)

@when(u'completo el formulario para crear una Muestra nueva y lo envío')
def impl(context):
    seleccionar_primera_opcion(context.browser, "planilla_de_relevamiento")
    context.browser.fill('anio', "2016")
    seleccionar_primera_opcion(context.browser, "mes")
    seleccionar_primera_opcion(context.browser, "quincena")
    seleccionar_primera_opcion(context.browser, "relevadores")
    context.browser.find_by_css('form button[type=submit]').first.click()

@then(u'he creado una nueva Muestra')
def impl(context):
    muestra = Muestra.objects.get(planilla_de_relevamiento__pk=context.planilla_de_relevamiento_id)
    if not python_3:
        muestra = unicode(muestra)
    ocurrencias = context.browser.find_by_text(muestra)
    assert(len(ocurrencias)>0)
