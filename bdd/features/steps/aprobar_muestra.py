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

from ipp.relevamiento.models import PlanillaDeRelevamiento, Muestra
from ipp.relevamiento.factories import MuestraFactory, LecturaFactory


import sys
python_3 = sys.version.startswith('3')

@given('que existe una Muestra con lecturas de precios')
def impl(context):
    planilla = PlanillaDeRelevamiento.objects.last()
    muestra = MuestraFactory(planilla_de_relevamiento=planilla, anio=2016, mes=1, quincena=1)
    for producto in planilla.productos.all():
        LecturaFactory(producto_con_marca=producto, precio=10, muestra=muestra)

@when('apruebo la Muestra')
def impl(context):
    muestra = Muestra.objects.last()
    url = reverse("relevamiento:aprobar_muestra",
                  kwargs={"muestra_id": muestra.id})
    context.browser.click_link_by_href(url)

@then('la Muestra queda aprobada')
def impl(context):
    muestra = Muestra.objects.last()
    assert muestra.aprobada == True

@then('ya no aparece en el listado para cargar lecturas')
def impl(context):
    muestra = Muestra.objects.last()
    if not python_3:
        muestra = str(muestra)
    assert context.browser.is_element_present_by_text(muestra) == False

