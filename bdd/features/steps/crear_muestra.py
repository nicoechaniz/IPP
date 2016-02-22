# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from behave import *

from utils import seleccionar_primera_opcion

from ipp.relevamiento.constants import COORD_ZONAL
from ipp.relevamiento.models import PlanillaDeRelevamiento, Muestra

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
    ocurrencias = context.browser.find_by_text(unicode(muestra))
    assert(ocurrencias>0)
