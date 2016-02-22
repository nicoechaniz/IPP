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

from ipp.relevamiento.constants import RELEVADOR, COORD_ZONAL
from ipp.relevamiento.models import Perfil

@given(u'que me logueo en el sistema y mi Rol es de relevador')
def impl(context):
    perfil = Perfil.objects.get(rol=RELEVADOR)
    login_url = context.config.server_url + '/accounts/login/'
    context.browser.visit(login_url)
    context.browser.fill('username', perfil.user.username)
    context.browser.fill('password', 'pass')
    context.browser.find_by_css('form button[type=submit]').first.click()

@given(u'no existe el link para crear Planilla de Relevamiento')
def impl(context):
    url = reverse("relevamiento:crear_planilla_de_relevamiento")
    assert len(context.browser.find_link_by_href(url)) == 0
    
@when(u'accedo a la url directa para crear Planilla de Relevamiento')
def impl(context):
    url = reverse("relevamiento:crear_planilla_de_relevamiento")
    context.browser.visit(context.config.server_url + url)

@then(u'el sistema me avisa que no tengo permisos suficientes')
def impl(context):
    ocurrencia = context.browser.find_by_css(
        'div.alert-danger').first.html.find(u"Permisos insuficientes.")
    assert ocurrencia >= 0

@given(u'que me logueo en el sistema y mi Rol es de coordinador')
def impl(context):
    perfil = Perfil.objects.get(rol=COORD_ZONAL)
    login_url = context.config.server_url + '/accounts/login/'
    context.browser.visit(login_url)
    context.browser.fill('username', perfil.user.username)
    context.browser.fill('password', 'pass')
    context.browser.find_by_css('form button[type=submit]').first.click()

@given(u'accedo a la funcionalidad para crear Planilla de Relevamiento')
def impl(context):
    context.browser.click_link_by_text("Acciones")
    url = reverse("relevamiento:crear_planilla_de_relevamiento")
    assert len(context.browser.find_link_by_href(url)) >= 1
    context.browser.click_link_by_href(url)

@given(u'elijo una Planilla Modelo para usar de base')
def impl(context):
    seleccionar_primera_opcion(context.browser, "planilla_modelo")
    
@given(u'elijo Zona y Comercio al que asociar la Planilla de Relevamiento')
def impl(context):
    seleccionar_primera_opcion(context.browser, "zona")
    seleccionar_primera_opcion(context.browser, "comercio")

@when(u'confirmo la acción') 
def impl(context):
    context.browser.find_by_css('form button[type=submit]').first.click()

@then(u'creo la Planilla de Relevamiento para ese Comercio')
def impl(context):  
    ocurrencia = context.browser.find_by_css(
        'div.alert-success').first.html.find(u"La planilla de relevamiento fue creada con éxito")
    assert ocurrencia >= 0
